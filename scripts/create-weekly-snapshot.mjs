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

async function plusOneReactionSummary(issueNumber) {
  const reactions = await paginate(`/repos/${repository}/issues/${issueNumber}/reactions?content=%2B1`);
  const plusOnes = reactions.filter((reaction) => reaction.content === '+1');
  const voterLogins = plusOnes
    .map((reaction) => reaction.user?.login)
    .filter((login) => typeof login === 'string' && login.length > 0);

  return {
    votes: plusOnes.length,
    voter_count: new Set(voterLogins).size,
    voter_logins: voterLogins
  };
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

function candidateRecord(issue, reactionSummary) {
  return {
    issue: issue.number,
    title: issue.title.replace(/^\[Prompt\]:\s*/i, '').trim(),
    author: issue.user?.login || 'unknown',
    votes: reactionSummary.votes,
    voter_count: reactionSummary.voter_count,
    url: issue.html_url,
    created_at: issue.created_at,
    updated_at: issue.updated_at,
    _voter_logins: reactionSummary.voter_logins
  };
}

function fixtureCandidateRecord(candidate) {
  const votes = Number(candidate.votes || 0);
  return {
    issue: Number(candidate.issue),
    title: String(candidate.title || '').replace(/^\[Prompt\]:\s*/i, '').trim(),
    author: candidate.author || 'unknown',
    votes,
    voter_count: Number(candidate.voter_count ?? votes),
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
    voter_count: 0,
    url: null,
    virtual: true,
    created_at: null,
    updated_at: null
  };
}

function publicCandidate(candidate) {
  const { _voter_logins, ...rest } = candidate;
  return rest;
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

function buildMetrics(candidates) {
  const authors = new Set(candidates.map((candidate) => candidate.author).filter(Boolean));
  const voterLogins = candidates.flatMap((candidate) => candidate._voter_logins || []);
  const uniqueVoterCount = voterLogins.length > 0 ? new Set(voterLogins).size : null;
  const candidateCount = candidates.length;
  const totalVotes = candidates.reduce((sum, candidate) => sum + candidate.votes, 0);
  const topPromptVotes = sortCandidates(candidates)[0]?.votes || 0;

  return {
    candidate_count: candidateCount,
    unique_author_count: authors.size,
    total_votes: totalVotes,
    top_prompt_votes: topPromptVotes,
    unique_voter_count: uniqueVoterCount,
    unique_voter_count_available: uniqueVoterCount !== null,
    average_votes_per_candidate: candidateCount > 0 ? Number((totalVotes / candidateCount).toFixed(2)) : 0,
    top_prompt_vote_share: totalVotes > 0 ? Number((topPromptVotes / totalVotes).toFixed(4)) : 0
  };
}

async function appendJsonl(path, record) {
  await mkdir(path.split('/').slice(0, -1).join('/'), { recursive: true });
  const previous = existsSync(path) ? await readFile(path, 'utf8') : '';
  await writeFile(path, `${previous}${JSON.stringify(record)}\n`, 'utf8');
}

function runLogMarkdown(snapshot) {
  const selected = snapshot.decision === 'selected' ? snapshot.selected_issue : 'none';
  const topRows = snapshot.top_prompts.map((prompt) => (
    `| ${prompt.rank} | #${prompt.issue} | ${escapePipes(prompt.title)} | ${prompt.author} | ${prompt.votes} | ${prompt.voter_count} | ${prompt.url} |`
  )).join('\n') || '| - | - | - | - | - | - | - |';
  const rankedRows = snapshot.ranked_candidates_with_baseline.map((candidate) => (
    `| ${candidate.rank} | ${candidate.issue === null ? 'baseline' : `#${candidate.issue}`} | ${escapePipes(candidate.title)} | ${candidate.author} | ${candidate.votes} | ${candidate.voter_count} | ${candidate.virtual ? 'yes' : 'no'} | ${candidate.url || '-'} |`
  )).join('\n') || '| - | - | - | - | - | - | - | - |';

  return `# Week ${snapshot.week}: Prompt Vote Lab Run\n\n` +
`## Vote Snapshot\n\n` +
`Snapshot: \`${snapshot.snapshot_path}\`  \n` +
`Snapshot at: ${snapshot.snapshot_at}  \n` +
`Cutoff timezone: ${snapshot.cutoff_timezone}\n\n` +
`## Participation Metrics\n\n` +
`- Candidate count: ${snapshot.metrics.candidate_count}\n` +
`- Unique author count: ${snapshot.metrics.unique_author_count}\n` +
`- Total real prompt votes: ${snapshot.metrics.total_votes}\n` +
`- Top prompt votes: ${snapshot.metrics.top_prompt_votes}\n` +
`- Unique voter count: ${snapshot.metrics.unique_voter_count_available ? snapshot.metrics.unique_voter_count : 'unavailable'}\n` +
`- Average votes per candidate: ${snapshot.metrics.average_votes_per_candidate}\n` +
`- Top prompt vote share: ${snapshot.metrics.top_prompt_vote_share}\n\n` +
`## Ranked Candidates With Baseline\n\n` +
`| Rank | Issue | Prompt | Author | Votes | Voters | Virtual | URL |\n` +
`|---:|---|---|---|---:|---:|---|---|\n` +
`${rankedRows}\n\n` +
`## Top Prompts\n\n` +
`| Rank | Issue | Prompt | Author | Votes | Voters | URL |\n` +
`|---:|---:|---|---|---:|---:|---|\n` +
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
    const reactionSummary = await plusOneReactionSummary(issue.number);
    rawCandidates.push(candidateRecord(issue, reactionSummary));
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
const allCandidatesInternal = sortCandidates(rawCandidates);
const allCandidates = allCandidatesInternal.map(publicCandidate);
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
const metrics = buildMetrics(allCandidatesInternal);
const totalVotes = metrics.total_votes;
const topPromptVotes = metrics.top_prompt_votes;
const decision = decisionFor(totalVotes, topPromptVotes);
const selectedIssue = decision === 'selected' ? topPrompts[0]?.issue ?? null : null;
const decisionReason = decisionReasonFor(decision, totalVotes, topPromptVotes);

const snapshot = {
  schema_version: 'snapshot-v1.2',
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
  metrics,
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
  candidate_count: metrics.candidate_count,
  unique_author_count: metrics.unique_author_count,
  total_votes: totalVotes,
  top_prompt_votes: topPromptVotes,
  unique_voter_count: metrics.unique_voter_count,
  unique_voter_count_available: metrics.unique_voter_count_available,
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
