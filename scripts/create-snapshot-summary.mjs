#!/usr/bin/env node
import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';

const snapshotDir = process.env.SNAPSHOT_DIR || 'data/snapshots';
const summaryOutput = process.env.SUMMARY_OUTPUT || 'reports/summary/weekly-metrics.json';
const markdownOutput = process.env.SUMMARY_MARKDOWN_OUTPUT || 'reports/summary/weekly-metrics.md';

if (!existsSync(snapshotDir)) {
  throw new Error(`Snapshot directory not found: ${snapshotDir}`);
}

const files = (await readdir(snapshotDir))
  .filter((file) => /^week-.+\.json$/.test(file))
  .sort();

const snapshots = [];
for (const file of files) {
  const snapshotPath = path.join(snapshotDir, file);
  const snapshot = JSON.parse(await readFile(snapshotPath, 'utf8'));
  snapshots.push(normalizeSnapshot(snapshot, snapshotPath));
}

const weeks = snapshots.map((snapshot) => weekRecord(snapshot));
const summary = buildSummary(weeks);

await mkdir(path.dirname(summaryOutput), { recursive: true });
await writeFile(summaryOutput, `${JSON.stringify(summary, null, 2)}\n`, 'utf8');

await mkdir(path.dirname(markdownOutput), { recursive: true });
await writeFile(markdownOutput, summaryMarkdown(summary), 'utf8');

console.log(`Wrote ${summaryOutput}`);
console.log(`Wrote ${markdownOutput}`);
console.log(`Weeks summarized: ${summary.week_count}`);

function normalizeSnapshot(snapshot, snapshotPath) {
  const schema = String(snapshot.schema_version || '');
  if (!schema.startsWith('snapshot-v1.')) {
    throw new Error(`${snapshotPath}: unsupported schema_version ${schema || '(missing)'}`);
  }

  if (!snapshot.week) {
    throw new Error(`${snapshotPath}: missing week`);
  }

  if (!Array.isArray(snapshot.all_candidates)) {
    throw new Error(`${snapshotPath}: all_candidates must be an array`);
  }

  if (snapshot.all_candidates.some((candidate) => Object.hasOwn(candidate, '_voter_logins'))) {
    throw new Error(`${snapshotPath}: must not expose voter login lists`);
  }

  const metrics = snapshot.metrics || deriveMetrics(snapshot);
  assertFiniteNumber(metrics.candidate_count, `${snapshotPath}: metrics.candidate_count`);
  assertFiniteNumber(metrics.unique_author_count, `${snapshotPath}: metrics.unique_author_count`);
  assertFiniteNumber(metrics.total_votes, `${snapshotPath}: metrics.total_votes`);
  assertFiniteNumber(metrics.top_prompt_votes, `${snapshotPath}: metrics.top_prompt_votes`);
  assertFiniteNumber(metrics.average_votes_per_candidate, `${snapshotPath}: metrics.average_votes_per_candidate`);
  assertFiniteNumber(metrics.top_prompt_vote_share, `${snapshotPath}: metrics.top_prompt_vote_share`);

  if (metrics.unique_voter_count !== null && metrics.unique_voter_count !== undefined) {
    assertFiniteNumber(metrics.unique_voter_count, `${snapshotPath}: metrics.unique_voter_count`);
  }

  return {
    ...snapshot,
    metrics,
    snapshot_path: snapshot.snapshot_path || snapshotPath
  };
}

function deriveMetrics(snapshot) {
  const candidates = snapshot.all_candidates || [];
  const authors = new Set(candidates.map((candidate) => candidate.author).filter(Boolean));
  const totalVotes = Number(snapshot.total_votes ?? candidates.reduce((sum, candidate) => sum + Number(candidate.votes || 0), 0));
  const topPromptVotes = Number(snapshot.top_prompt_votes ?? snapshot.top_prompts?.[0]?.votes ?? 0);
  const candidateCount = candidates.length;

  return {
    candidate_count: candidateCount,
    unique_author_count: authors.size,
    total_votes: totalVotes,
    top_prompt_votes: topPromptVotes,
    unique_voter_count: null,
    unique_voter_count_available: false,
    average_votes_per_candidate: candidateCount > 0 ? Number((totalVotes / candidateCount).toFixed(2)) : 0,
    top_prompt_vote_share: totalVotes > 0 ? Number((topPromptVotes / totalVotes).toFixed(4)) : 0
  };
}

function weekRecord(snapshot) {
  return {
    week: snapshot.week,
    snapshot_at: snapshot.snapshot_at || null,
    snapshot_path: snapshot.snapshot_path,
    decision: snapshot.decision || 'unknown',
    decision_reason: snapshot.decision_reason || 'unknown',
    selected_issue: snapshot.selected_issue ?? null,
    selected_title: snapshot.top_prompts?.[0]?.title || null,
    candidate_count: snapshot.metrics.candidate_count,
    unique_author_count: snapshot.metrics.unique_author_count,
    total_votes: snapshot.metrics.total_votes,
    top_prompt_votes: snapshot.metrics.top_prompt_votes,
    unique_voter_count: snapshot.metrics.unique_voter_count ?? null,
    unique_voter_count_available: Boolean(snapshot.metrics.unique_voter_count_available),
    average_votes_per_candidate: snapshot.metrics.average_votes_per_candidate,
    top_prompt_vote_share: snapshot.metrics.top_prompt_vote_share
  };
}

function buildSummary(weeks) {
  const selectedCount = weeks.filter((week) => week.decision === 'selected').length;
  const noRunCount = weeks.filter((week) => week.decision === 'no_run').length;
  const latest = weeks.at(-1) || null;
  const previous = weeks.length > 1 ? weeks.at(-2) : null;

  return {
    schema_version: 'snapshot-summary-v1.0',
    generated_at: new Date().toISOString(),
    source_snapshot_count: weeks.length,
    week_count: weeks.length,
    selected_count: selectedCount,
    no_run_count: noRunCount,
    latest_week: latest,
    latest_delta: latest && previous ? deltaRecord(previous, latest) : null,
    trend: {
      total_votes: slopeDirection(weeks.map((week) => week.total_votes)),
      candidate_count: slopeDirection(weeks.map((week) => week.candidate_count)),
      unique_author_count: slopeDirection(weeks.map((week) => week.unique_author_count)),
      unique_voter_count: slopeDirection(weeks.map((week) => week.unique_voter_count).filter((value) => value !== null)),
      top_prompt_vote_share: slopeDirection(weeks.map((week) => week.top_prompt_vote_share))
    },
    weeks
  };
}

function deltaRecord(previous, latest) {
  return {
    candidate_count: latest.candidate_count - previous.candidate_count,
    unique_author_count: latest.unique_author_count - previous.unique_author_count,
    total_votes: latest.total_votes - previous.total_votes,
    top_prompt_votes: latest.top_prompt_votes - previous.top_prompt_votes,
    unique_voter_count: latest.unique_voter_count !== null && previous.unique_voter_count !== null
      ? latest.unique_voter_count - previous.unique_voter_count
      : null,
    top_prompt_vote_share: Number((latest.top_prompt_vote_share - previous.top_prompt_vote_share).toFixed(4))
  };
}

function slopeDirection(values) {
  if (values.length < 2) return 'insufficient_data';
  const first = values[0];
  const last = values[values.length - 1];
  if (last > first) return 'up';
  if (last < first) return 'down';
  return 'flat';
}

function summaryMarkdown(summary) {
  const rows = summary.weeks.map((week) => (
    `| ${week.week} | ${week.decision} | ${week.candidate_count} | ${week.unique_author_count} | ${week.total_votes} | ${week.unique_voter_count ?? 'n/a'} | ${week.top_prompt_vote_share} | ${week.selected_issue ?? '-'} |`
  )).join('\n') || '| - | - | - | - | - | - | - | - |';

  return `# Weekly Metrics Summary\n\n` +
`Generated at: ${summary.generated_at}\n\n` +
`## Overview\n\n` +
`- Weeks: ${summary.week_count}\n` +
`- Selected weeks: ${summary.selected_count}\n` +
`- No-run weeks: ${summary.no_run_count}\n` +
`- Total-vote trend: ${summary.trend.total_votes}\n` +
`- Candidate-count trend: ${summary.trend.candidate_count}\n` +
`- Unique-author trend: ${summary.trend.unique_author_count}\n` +
`- Unique-voter trend: ${summary.trend.unique_voter_count}\n` +
`- Top-prompt vote-share trend: ${summary.trend.top_prompt_vote_share}\n\n` +
`## Weeks\n\n` +
`| Week | Decision | Candidates | Authors | Votes | Voters | Top share | Selected |\n` +
`|---|---|---:|---:|---:|---:|---:|---|\n` +
`${rows}\n`;
}

function assertFiniteNumber(value, label) {
  if (typeof value !== 'number' || !Number.isFinite(value)) {
    throw new Error(`${label} must be a finite number`);
  }
}
