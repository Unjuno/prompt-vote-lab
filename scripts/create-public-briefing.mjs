#!/usr/bin/env node
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';

const week = process.env.WEEK_ID || inferWeekId();
const snapshotPath = process.env.SNAPSHOT_INPUT || `data/snapshots/week-${week}.json`;
const summaryPath = process.env.SUMMARY_INPUT || 'reports/summary/weekly-metrics.json';
const runLogPath = process.env.RUN_LOG_INPUT || `runs/week-${week}.md`;
const outputPath = process.env.BRIEFING_OUTPUT || `reports/briefings/week-${week}.md`;
const siteUrl = process.env.SITE_URL || 'https://unjuno.github.io/prompt-vote-lab/';
const repoUrl = process.env.REPO_URL || 'https://github.com/Unjuno/prompt-vote-lab';

function inferWeekId() {
  const now = new Date();
  const start = Date.UTC(now.getUTCFullYear(), 0, 1);
  const elapsedDays = Math.floor((now.getTime() - start) / 86400000);
  const weekNumber = Math.floor(elapsedDays / 7) + 1;
  return String(weekNumber).padStart(3, '0');
}

function escapeMarkdown(value) {
  return String(value ?? '').replace(/\|/g, '\\|').trim();
}

function statusFromRunLog(markdown) {
  const match = markdown.match(/^Status:\s*(.+)$/im);
  return match ? match[1].trim() : 'unrecorded';
}

function gapFromRunLog(markdown) {
  const match = markdown.match(/^Gap classification:\s*(.+)$/im);
  return match ? match[1].trim() : 'unrecorded';
}

function includesUnrecorded(markdown) {
  return /\bunrecorded\b/i.test(markdown || '');
}

function assertNoForbiddenKeys(value, location) {
  const forbidden = new Set(['_voter_logins', 'voter_logins', 'voters', 'reaction_users']);
  const stack = [{ value, path: '$' }];
  while (stack.length > 0) {
    const current = stack.pop();
    if (!current || current.value === null || typeof current.value !== 'object') continue;
    if (Array.isArray(current.value)) {
      current.value.forEach((item, index) => stack.push({ value: item, path: `${current.path}[${index}]` }));
      continue;
    }
    for (const [key, child] of Object.entries(current.value)) {
      if (forbidden.has(key)) {
        throw new Error(`${location}: forbidden key ${current.path}.${key}`);
      }
      stack.push({ value: child, path: `${current.path}.${key}` });
    }
  }
}

function promptTable(snapshot) {
  const prompts = snapshot.top_prompts || [];
  if (prompts.length === 0) {
    return '| Rank | Issue | Prompt | Votes |\n|---:|---:|---|---:|\n| - | - | - | - |';
  }
  const rows = prompts.map((prompt) => (
    `| ${prompt.rank} | #${prompt.issue} | ${escapeMarkdown(prompt.title)} | ${prompt.votes} |`
  ));
  return ['| Rank | Issue | Prompt | Votes |', '|---:|---:|---|---:|', ...rows].join('\n');
}

function actionList(snapshot) {
  if (snapshot.decision === 'selected') {
    return [
      'Review the selected issue and check whether the prompt is specific enough to implement.',
      'Inspect the resulting PR before trusting the outcome.',
      'Submit a sharper competing prompt if the selected prompt looks vague or overfit.'
    ];
  }

  return [
    'Submit a clearer prompt proposal before the next cutoff.',
    'Vote with a 👍 / +1 reaction on prompts that should beat no-change.',
    'Comment to challenge vague proposals, but remember that comments are not votes.'
  ];
}

function orientationNote(snapshot, summary) {
  const metrics = snapshot.metrics || {};
  const topShare = Number(metrics.top_prompt_vote_share ?? 0);
  const candidateCount = Number(metrics.candidate_count ?? 0);
  const voteTrend = summary?.trend?.total_votes || 'unknown';

  if (candidateCount === 0) {
    return 'No prompt candidates were recorded. The next priority is proposal creation, not implementation.';
  }

  if (topShare >= 0.7) {
    return 'Votes are highly concentrated. That can mean strong consensus, but it can also mean the field lacks alternatives.';
  }

  if (voteTrend === 'down') {
    return 'Vote trend is down. The next public message should reduce friction and explain the shortest path to participate.';
  }

  if (snapshot.decision === 'no_run') {
    return 'The no-change baseline held. This is useful evidence: current prompts did not earn enough public trust.';
  }

  return 'The week produced a selected prompt. The next risk is implementation quality, not vote collection alone.';
}

async function readJson(path) {
  const text = await readFile(path, 'utf8');
  const json = JSON.parse(text);
  assertNoForbiddenKeys(json, path);
  return json;
}

const snapshot = existsSync(snapshotPath) ? await readJson(snapshotPath) : null;
const summary = existsSync(summaryPath) ? await readJson(summaryPath) : null;
const runLog = existsSync(runLogPath) ? await readFile(runLogPath, 'utf8') : '';

if (!snapshot) {
  throw new Error(`Snapshot not found: ${snapshotPath}`);
}

const runStatus = statusFromRunLog(runLog);
const gapClassification = gapFromRunLog(runLog);
const generatedAt = new Date().toISOString();
const metrics = snapshot.metrics || {};
const selected = snapshot.decision === 'selected' ? snapshot.top_prompts?.[0] : null;
const evidenceWarning = includesUnrecorded(runLog)
  ? 'Some run-log fields are still unrecorded. Treat this as a participation briefing, not a final result report.'
  : 'Run-log fields appear recorded. Still review manually before public reposting.';

const markdown = `# Prompt Vote Lab Briefing: Week ${week}\n\n` +
`Generated at: ${generatedAt}\n\n` +
`## Public status\n\n` +
`- Decision: \`${snapshot.decision}\`\n` +
`- Reason: \`${snapshot.decision_reason || 'unknown'}\`\n` +
`- Selected issue: ${selected ? `#${selected.issue} — ${selected.title}` : 'none'}\n` +
`- Run status: ${runStatus}\n` +
`- Gap classification: ${gapClassification}\n` +
`- Evidence note: ${evidenceWarning}\n\n` +
`## Observe\n\n` +
`- Candidates: ${metrics.candidate_count ?? 'unknown'}\n` +
`- Unique authors: ${metrics.unique_author_count ?? 'unknown'}\n` +
`- Total votes: ${metrics.total_votes ?? snapshot.total_votes ?? 'unknown'}\n` +
`- Unique voters: ${metrics.unique_voter_count_available ? metrics.unique_voter_count : 'unavailable'}\n` +
`- Top prompt vote share: ${metrics.top_prompt_vote_share ?? 'unknown'}\n` +
`- Summary trend: total votes ${summary?.trend?.total_votes || 'unknown'}, candidates ${summary?.trend?.candidate_count || 'unknown'}, authors ${summary?.trend?.unique_author_count || 'unknown'}\n\n` +
`## Orient\n\n` +
`${orientationNote(snapshot, summary)}\n\n` +
`## Decide\n\n` +
`${snapshot.decision === 'selected'
  ? 'The selected prompt deserves review, not blind trust. Popularity opened the gate; implementation quality still decides whether the round was useful.'
  : 'Do not spend an implementation attempt this week. The correct move is to improve prompt quality and attract more votes.'}\n\n` +
`## Act\n\n` +
`${actionList(snapshot).map((item) => `- ${item}`).join('\n')}\n\n` +
`## Top prompts\n\n` +
`${promptTable(snapshot)}\n\n` +
`## Links\n\n` +
`- Site: ${siteUrl}\n` +
`- Repository: ${repoUrl}\n` +
`- Submit prompt: ${repoUrl}/issues/new?template=prompt_proposal.yml\n` +
`- Vote: ${repoUrl}/issues?q=is%3Aissue+is%3Aopen+label%3Aprompt-proposal\n\n` +
`## Share note\n\n` +
`This briefing is safe to share as a status update only after checking that the linked snapshot and run log match the text above. Do not treat it as an automated external post.\n`;

await mkdir(outputPath.split('/').slice(0, -1).join('/'), { recursive: true });
await writeFile(outputPath, markdown, 'utf8');
console.log(`Wrote ${outputPath}`);
