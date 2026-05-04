#!/usr/bin/env node
import { mkdir, writeFile, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';

const owner = process.env.GITHUB_REPOSITORY_OWNER || 'Unjuno';
const repo = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'prompt-vote-lab';
const repository = `${owner}/${repo}`;
const token = process.env.GITHUB_TOKEN;
const promptLabel = process.env.PROMPT_LABEL || 'prompt-proposal';
const week = process.env.WEEK_ID || inferWeekId();
const cutoffTimezone = process.env.CUTOFF_TIMEZONE || 'Asia/Tokyo';
const snapshotAt = process.env.SNAPSHOT_AT || new Date().toISOString();
const allowSnapshotOverwrite = process.env.ALLOW_SNAPSHOT_OVERWRITE === 'true';
const snapshotFixture = process.env.SNAPSHOT_FIXTURE || '';

const noChangeBaseline = Number(process.env.NO_CHANGE_BASELINE || 20);
const requiredMargin = Number(process.env.REQUIRED_MARGIN || 1);
const minimumTotalVotes = Number(process.env.MINIMUM_TOTAL_VOTES || 20);

const snapshotPath = process.env.SNAPSHOT_OUTPUT || `data/snapshots/week-${week}.json`;
const aggregationLogPath = process.env.AGGREGATION_LOG_OUTPUT || `logs/aggregation/week-${week}.jsonl`;
const runLogPath = process.env.RUN_LOG_OUTPUT || `runs/week-${week}.md`;

if (!token && !snapshotFixture) {
  throw new Error('GITHUB_TOKEN is required unless SNAPSHOT_FIXTURE is provided.');
}

if (existsSync(snapshotPath) && !allowSnapshotOverwrite) {
  throw new Error(`${snapshotPath} already exists. Refusing to overwrite an existing weekly snapshot.`);
}

const headers = token ? {
  Accept: 'application/vnd.github+json',
  Authorization: `Bearer ${token}`,
  'X-GitHub-Api-Version': '2022-11-28',
  'User-Agent': 'prompt-vote-lab-weekly-snapshot'
} : null;

function inferWeekId() {
  const now = new Date();
  const start = Date.UTC(now.getUTCFullYear(), 0, 1);
  const elapsedDays = Math.floor((now.getTime() - start) / 86400000);
  const weekNumber = Math.floor(elapsedDays / 7) + 1;
  return String(weekNumber).padStart(3, '0');
}

async function github(path) {
  const response = await fetch(`https://api.github.com${path}`, { headers });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`GitHub API ${response.status} for ${path}: ${body}`);
  }
  return response.json();
}

async function paginate(path) {
  const results = [];
  for (let page = 1; page <= 10; page += 1) {
    const separator = path.includes('?') ? '&' : '?';
    const data = await github(`${path}${separator}per_page=100&page=${page}`);
    if (!Array.isArray(data) || data.length === 0) break;
    results.push(...data);
    if (data.length < 100) break;
  }
  return results;
}

async function plusOneVotes(issueNumber) {
  const reactions = await paginate(`/repos/${repository}/issues/${issueNumber}/reactions?content=%2B1`);
  return reactions.filter((reaction) => reaction.content === '+1').length;
}

function decisionFor(totalVotes, topPromptVotes) {
  const selected = topPromptVotes >= noChangeBaseline + requiredMargin && totalVotes >= minimumTotalVotes;
  return selected ? 'selected' : 'no_run';
}

function decisionReasonFor(decision, totalVotes, topPromptVotes) {
  if (decision === 'selected') {
    return 'top_prompt_beat_no_change_baseline';
  }
  if (totalVotes < minimumTotalVotes) {
    return 'minimum_total_votes_not_met';
  }
  if (topPromptVotes < noChangeBaseline + requiredMargin) {
    return 'no_change_baseline_won_or_tied';
  }
  return 'no_run';
}

function candidateRecord(issue, votes) {
  return {
    issue: issue.number,
    title: issue.title.replace(/^\[Prompt\]:\s*/i, '').trim(),
    author: issue.user?.login || 'unknown',
    votes,
    url: issue.html_url,
    created_at: issue.created_at,
    updated_at: issue.updated_at
  };
}

function fixtureCandidateRecord(candidate) {
  return {
    issue: Number(candidate.issue),
    title: String(candidate.title || '').replace(/^\[Prompt\]:\s*/i, '').trim(),
    author: candidate.author || 'unknown',
    votes: Number(candidate.votes || 0),
    url: candidate.url || `https://github.com/${repository}/issues/${candidate.issue}`,
    created_at: candidate.created_at || null,
    updated_at: candidate.updated_at || null
  };
}

function baselineCandidateRecord() {
  return {
    issue: null,
    title: '[Baseline]: No change this week',
    author: 'system',
    votes: noChangeBaseline,
    url: null,
    virtual: true,
    created_at: null,
    updated_at: null
  };
}

function sortCandidates(candidates) {
  return [...candidates].sort((a, b) => {
    if (b.votes !== a.votes) return b.votes - a.votes;
    return a.issue - b.issue;
  });
}

function sortCandidatesWithBaseline(candidates) {
  return [...candidates].sort((a, b) => {
    if (b.votes !== a.votes) return b.votes - a.votes;
    if (a.virtual && !b.virtual) return -1;
    if (!a.virtual && b.virtual) return 1;
    if (a.issue === null && b.issue === null) return 0;
    if (a.issue === null) return 1;
    if (b.issue === null) return -1;
    return a.issue - b.issue;
  });
}

async function appendJsonl(path, record) {
  await mkdir(path.split('/').slice(0, -1).join('/'), { recursive: true });
  const previous = existsSync(path) ? await readFile(path, 'utf8') : '';
  await writeFile(path, `${previous}${JSON.stringify(record)}\n`, 'utf8');
}

function runLogMarkdown(snapshot) {
  const selected = snapshot.decision === 'selected' ? snapshot.selected_issue : 'none';
  const topRows = snapshot.top_prompts.map((prompt) => (
    `| ${prompt.rank} | #${prompt.issue} | ${escapePipes(prompt.title)} | ${prompt.author} | ${prompt.votes} | ${prompt.url} |`
  )).join('\n') || '| - | - | - | - | - | - |';
  const rankedRows = snapshot.ranked_candidates_with_baseline.map((candidate) => (
    `| ${candidate.rank} | ${candidate.issue === null ? 'baseline' : `#${candidate.issue}`} | ${escapePipes(candidate.title)} | ${candidate.author} | ${candidate.votes} | ${candidate.virtual ? 'yes' : 'no'} | ${candidate.url || '-'} |`
  )).join('\n') || '| - | - | - | - | - | - | - |';

  return `# Week ${snapshot.week}: Prompt Vote Lab Run\n\n` +
`## Vote Snapshot\n\n` +
`Snapshot: \`${snapshot.snapshot_path}\`  \n` +
`Snapshot at: ${snapshot.snapshot_at}  \n` +
`Cutoff timezone: ${snapshot.cutoff_timezone}\n\n` +
`## Ranked Candidates With Baseline\n\n` +
`| Rank | Issue | Prompt | Author | Votes | Virtual | URL |\n` +
`|---:|---|---|---|---:|---|---|\n` +
`${rankedRows}\n\n` +
`## Top Prompts\n\n` +
`| Rank | Issue | Prompt | Author | Votes | URL |\n` +
`|---:|---:|---|---|---:|---|\n` +
`${topRows}\n\n` +
`## Selection Rule\n\n` +
`- Rule: \`${snapshot.selection_rule.rule}\`\n` +
`- No-change baseline: ${snapshot.selection_rule.no_change_baseline}\n` +
`- Required margin: ${snapshot.selection_rule.required_margin}\n` +
`- Minimum total votes: ${snapshot.selection_rule.minimum_total_votes}\n` +
`- Total real prompt votes: ${snapshot.total_votes}\n` +
`- Top prompt votes: ${snapshot.top_prompt_votes}\n` +
`- Baseline candidate: \`${snapshot.no_change_baseline_candidate.title}\` with ${snapshot.no_change_baseline_candidate.votes} virtual votes\n\n` +
`Decision: \`${snapshot.decision}\`  \n` +
`Decision reason: \`${snapshot.decision_reason}\`  \n` +
`Selected issue: ${selected}\n\n` +
`## Agent Conditions\n\n` +
`- Agent: unrecorded\n` +
`- Rule: \`static-ui-v1.0\`\n` +
`- Target: \`lab/\`\n` +
`- Editable files:\n` +
`  - \`lab/index.html\`\n` +
`  - \`lab/style.css\`\n` +
`  - \`lab/app.js\`\n\n` +
`## Pull Request\n\n` +
`PR: unrecorded\n\n` +
`## Changed Files\n\n` +
`- unrecorded\n\n` +
`## Safety Check\n\n` +
`| Check | Result |\n` +
`|---|---|\n` +
`| Only \`lab/\` changed | unrecorded |\n` +
`| No external network calls | unrecorded |\n` +
`| No cookie access | unrecorded |\n` +
`| No eval/new Function misuse | unrecorded |\n` +
`| Browser display check | unrecorded |\n\n` +
`## Result\n\n` +
`Status: unrecorded\n\n` +
`## Expectation Gap\n\n` +
`Expected before implementation: unrecorded\n\n` +
`Actual result: unrecorded\n\n` +
`Gap classification: unrecorded\n\n` +
`Reviewer note: unrecorded\n\n` +
`Rule change for next run: unrecorded\n`;
}

function escapePipes(value) {
  return String(value).replace(/\|/g, '\\|');
}

async function loadCandidates() {
  if (snapshotFixture) {
    const fixture = JSON.parse(await readFile(snapshotFixture, 'utf8'));
    if (!Array.isArray(fixture.candidates)) {
      throw new Error('SNAPSHOT_FIXTURE must contain a candidates array.');
    }
    return fixture.candidates.map(fixtureCandidateRecord);
  }

  const issues = await paginate(`/repos/${repository}/issues?state=open&labels=${encodeURIComponent(promptLabel)}`);
  const promptIssues = issues.filter((issue) => !issue.pull_request);
  const rawCandidates = [];
  for (const issue of promptIssues) {
    const votes = await plusOneVotes(issue.number);
    rawCandidates.push(candidateRecord(issue, votes));
  }
  return rawCandidates;
}

const startedAt = new Date().toISOString();
await appendJsonl(aggregationLogPath, {
  event: 'weekly_snapshot_started',
  week,
  repository,
  prompt_label: promptLabel,
  fixture: Boolean(snapshotFixture),
  started_at: startedAt
});

const rawCandidates = await loadCandidates();
const allCandidates = sortCandidates(rawCandidates);
const noChangeBaselineCandidate = baselineCandidateRecord();
const rankedCandidatesWithBaseline = sortCandidatesWithBaseline([
  noChangeBaselineCandidate,
  ...allCandidates.map((candidate) => ({ ...candidate, virtual: false }))
]).map((candidate, index) => ({
  rank: index + 1,
  ...candidate
}));
const topPrompts = allCandidates.slice(0, 3).map((candidate, index) => ({
  rank: index + 1,
  ...candidate
}));
const totalVotes = allCandidates.reduce((sum, candidate) => sum + candidate.votes, 0);
const topPromptVotes = topPrompts[0]?.votes || 0;
const decision = decisionFor(totalVotes, topPromptVotes);
const selectedIssue = decision === 'selected' ? topPrompts[0]?.issue ?? null : null;
const decisionReason = decisionReasonFor(decision, totalVotes, topPromptVotes);

const snapshot = {
  schema_version: 'snapshot-v1.1',
  week,
  snapshot_at: snapshotAt,
  cutoff_timezone: cutoffTimezone,
  source: snapshotFixture ? 'fixture' : 'github-issues-reactions',
  repository,
  snapshot_path: snapshotPath,
  selection_rule: {
    rule: 'selection-v1.1',
    no_change_baseline: noChangeBaseline,
    required_margin: requiredMargin,
    minimum_total_votes: minimumTotalVotes
  },
  no_change_baseline_candidate: noChangeBaselineCandidate,
  total_votes: totalVotes,
  top_prompt_votes: topPromptVotes,
  decision,
  decision_reason: decisionReason,
  selected_issue: selectedIssue,
  ranked_candidates_with_baseline: rankedCandidatesWithBaseline,
  top_prompts: topPrompts,
  all_candidates: allCandidates
};

await mkdir(snapshotPath.split('/').slice(0, -1).join('/'), { recursive: true });
await writeFile(snapshotPath, `${JSON.stringify(snapshot, null, 2)}\n`, 'utf8');

await mkdir(runLogPath.split('/').slice(0, -1).join('/'), { recursive: true });
if (!existsSync(runLogPath)) {
  await writeFile(runLogPath, runLogMarkdown(snapshot), 'utf8');
}

await appendJsonl(aggregationLogPath, {
  event: 'weekly_snapshot_finished',
  week,
  repository,
  snapshot_path: snapshotPath,
  run_log_path: runLogPath,
  candidate_count: allCandidates.length,
  total_votes: totalVotes,
  top_prompt_votes: topPromptVotes,
  decision,
  decision_reason: decisionReason,
  selected_issue: selectedIssue,
  fixture: Boolean(snapshotFixture),
  started_at: startedAt,
  finished_at: new Date().toISOString()
});

console.log(`Wrote ${snapshotPath}`);
console.log(`Ensured ${runLogPath}`);
console.log(`Decision: ${decision}, reason: ${decisionReason}, selected issue: ${selectedIssue ?? 'none'}`);
