#!/usr/bin/env node
import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';

const testRoot = 'tmp/smoke';
const week = 'smoke-001';
const snapshotDir = `${testRoot}/data/snapshots`;
const snapshotPath = `${snapshotDir}/week-${week}.json`;
const aggregationLogPath = `${testRoot}/logs/aggregation/week-${week}.jsonl`;
const runLogPath = `${testRoot}/runs/week-${week}.md`;
const hnDraftPath = `${testRoot}/reports/hn/week-${week}.md`;
const summaryPath = `${testRoot}/reports/summary/weekly-metrics.json`;
const summaryMarkdownPath = `${testRoot}/reports/summary/weekly-metrics.md`;
const briefingPath = `${testRoot}/reports/briefings/week-${week}.md`;

await rm(testRoot, { recursive: true, force: true });

function run(command, args, env) {
  const result = spawnSync(command, args, {
    env: { ...process.env, ...env },
    encoding: 'utf8',
    stdio: 'pipe'
  });

  if (result.status !== 0) {
    console.error(result.stdout);
    console.error(result.stderr);
    throw new Error(`${command} ${args.join(' ')} failed with status ${result.status}`);
  }

  if (result.stdout) process.stdout.write(result.stdout);
  if (result.stderr) process.stderr.write(result.stderr);
}

function runExpectFailure(command, args, env, expectedText) {
  const result = spawnSync(command, args, {
    env: { ...process.env, ...env },
    encoding: 'utf8',
    stdio: 'pipe'
  });

  if (result.status === 0) {
    console.error(result.stdout);
    console.error(result.stderr);
    throw new Error(`${command} ${args.join(' ')} should have failed`);
  }

  const combined = `${result.stdout}\n${result.stderr}`;
  if (!combined.includes(expectedText)) {
    console.error(result.stdout);
    console.error(result.stderr);
    throw new Error(`Expected failure text missing: ${expectedText}`);
  }
}

run('node', ['scripts/create-weekly-snapshot.mjs'], {
  SNAPSHOT_FIXTURE: 'tests/fixtures/prompt-candidates.json',
  WEEK_ID: week,
  SNAPSHOT_AT: '2026-05-11T00:00:00+09:00',
  SNAPSHOT_OUTPUT: snapshotPath,
  AGGREGATION_LOG_OUTPUT: aggregationLogPath,
  RUN_LOG_OUTPUT: runLogPath,
  ALLOW_SNAPSHOT_OVERWRITE: 'true'
});

assertExists(snapshotPath);
assertExists(aggregationLogPath);
assertExists(runLogPath);

const snapshot = JSON.parse(await readFile(snapshotPath, 'utf8'));
assertEqual(snapshot.schema_version, 'snapshot-v1.2', 'snapshot schema version');
assertEqual(snapshot.source, 'fixture', 'snapshot source');
assertEqual(snapshot.decision, 'selected', 'snapshot decision');
assertEqual(snapshot.decision_reason, 'top_prompt_beat_no_change_baseline', 'snapshot decision reason');
assertEqual(snapshot.selected_issue, 3, 'selected issue');
assertEqual(snapshot.total_votes, 52, 'total votes');
assertEqual(snapshot.top_prompt_votes, 24, 'top prompt votes');
assertEqual(snapshot.selection_rule.no_change_baseline, 20, 'no-change baseline');
assertEqual(snapshot.selection_rule.required_margin, 1, 'required margin');
assertEqual(snapshot.no_change_baseline_candidate.title, '[Baseline]: No change this week', 'baseline title');
assertEqual(snapshot.no_change_baseline_candidate.votes, 20, 'baseline votes');
assertEqual(snapshot.no_change_baseline_candidate.voter_count, 0, 'baseline voter count');
assertEqual(snapshot.no_change_baseline_candidate.virtual, true, 'baseline virtual flag');
assertEqual(snapshot.metrics.candidate_count, 4, 'metrics candidate count');
assertEqual(snapshot.metrics.unique_author_count, 4, 'metrics unique author count');
assertEqual(snapshot.metrics.total_votes, 52, 'metrics total votes');
assertEqual(snapshot.metrics.top_prompt_votes, 24, 'metrics top prompt votes');
assertEqual(snapshot.metrics.unique_voter_count, null, 'metrics unique voter count unavailable for fixture');
assertEqual(snapshot.metrics.unique_voter_count_available, false, 'metrics unique voter availability');
assertEqual(snapshot.metrics.average_votes_per_candidate, 13, 'metrics average votes per candidate');
assertEqual(snapshot.metrics.top_prompt_vote_share, 0.4615, 'metrics top prompt vote share');
assertEqual(snapshot.ranked_candidates_with_baseline.length, 5, 'ranked candidates with baseline count');
assertEqual(snapshot.ranked_candidates_with_baseline[0].issue, 3, 'ranked baseline table rank 1 issue');
assertEqual(snapshot.ranked_candidates_with_baseline[1].virtual, true, 'ranked baseline table rank 2 baseline');
assertEqual(snapshot.top_prompts.length, 3, 'top prompt count');
assertEqual(snapshot.top_prompts[0].issue, 3, 'rank 1 issue');
assertEqual(snapshot.top_prompts[0].voter_count, 24, 'rank 1 voter count');
assertEqual(snapshot.top_prompts[1].issue, 2, 'rank 2 tie-break issue');
assertEqual(snapshot.top_prompts[2].issue, 4, 'rank 3 tie-break issue');
assertEqual(snapshot.all_candidates.some((candidate) => Object.hasOwn(candidate, '_voter_logins')), false, 'snapshot must not expose voter logins');

const runLog = await readFile(runLogPath, 'utf8');
assertIncludes(runLog, 'Participation Metrics', 'run log metrics section');
assertIncludes(runLog, 'Unique voter count: unavailable', 'run log unique voter unavailable note');
assertIncludes(runLog, 'Ranked Candidates With Baseline', 'run log baseline table heading');
assertIncludes(runLog, '[Baseline]: No change this week', 'run log baseline row');
assertIncludes(runLog, 'Decision reason: `top_prompt_beat_no_change_baseline`', 'run log decision reason');

await mkdir(snapshotDir, { recursive: true });
const secondSnapshot = structuredClone(snapshot);
secondSnapshot.week = 'smoke-002';
secondSnapshot.snapshot_at = '2026-05-18T00:00:00+09:00';
secondSnapshot.snapshot_path = `${snapshotDir}/week-smoke-002.json`;
secondSnapshot.metrics = {
  ...secondSnapshot.metrics,
  candidate_count: 5,
  unique_author_count: 5,
  total_votes: 60,
  top_prompt_votes: 30,
  unique_voter_count: 48,
  unique_voter_count_available: true,
  average_votes_per_candidate: 12,
  top_prompt_vote_share: 0.5
};
secondSnapshot.total_votes = 60;
secondSnapshot.top_prompt_votes = 30;
secondSnapshot.top_prompts[0].votes = 30;
secondSnapshot.top_prompts[0].voter_count = 30;
secondSnapshot.all_candidates.push({
  issue: 5,
  title: 'Add a public metrics summary',
  author: 'example-epsilon',
  votes: 8,
  voter_count: 8,
  url: 'https://github.com/Unjuno/prompt-vote-lab/issues/5',
  created_at: '2026-05-08T00:00:00Z',
  updated_at: '2026-05-08T00:00:00Z'
});
await writeFile(`${snapshotDir}/week-smoke-002.json`, `${JSON.stringify(secondSnapshot, null, 2)}\n`, 'utf8');

run('node', ['scripts/create-snapshot-summary.mjs'], {
  SNAPSHOT_DIR: snapshotDir,
  SUMMARY_OUTPUT: summaryPath,
  SUMMARY_MARKDOWN_OUTPUT: summaryMarkdownPath
});

assertExists(summaryPath);
assertExists(summaryMarkdownPath);
const summary = JSON.parse(await readFile(summaryPath, 'utf8'));
assertEqual(summary.schema_version, 'snapshot-summary-v1.0', 'summary schema version');
assertEqual(summary.week_count, 2, 'summary week count');
assertEqual(summary.selected_count, 2, 'summary selected count');
assertEqual(summary.no_run_count, 0, 'summary no-run count');
assertEqual(summary.latest_week.week, 'smoke-002', 'summary latest week');
assertEqual(summary.latest_delta.total_votes, 8, 'summary total votes delta');
assertEqual(summary.latest_delta.candidate_count, 1, 'summary candidate count delta');
assertEqual(summary.latest_delta.unique_voter_count, null, 'summary unique voter delta unavailable when previous is null');
assertEqual(summary.trend.total_votes, 'up', 'summary total votes trend');
assertEqual(summary.trend.candidate_count, 'up', 'summary candidate count trend');
assertEqual(summary.trend.unique_author_count, 'up', 'summary unique author trend');
assertEqual(summary.trend.unique_voter_count, 'insufficient_data', 'summary unique voter trend');
assertEqual(summary.weeks.some((record) => Object.hasOwn(record, '_voter_logins')), false, 'summary must not expose voter logins');
const summaryMarkdown = await readFile(summaryMarkdownPath, 'utf8');
assertIncludes(summaryMarkdown, 'Weekly Metrics Summary', 'summary markdown title');
assertIncludes(summaryMarkdown, '| smoke-002 | selected | 5 | 5 | 60 | 48 | 0.5 | 3 |', 'summary markdown latest row');

run('node', ['scripts/create-public-briefing.mjs'], {
  WEEK_ID: week,
  SNAPSHOT_INPUT: snapshotPath,
  SUMMARY_INPUT: summaryPath,
  RUN_LOG_INPUT: runLogPath,
  BRIEFING_OUTPUT: briefingPath,
  SITE_URL: 'https://unjuno.github.io/prompt-vote-lab/',
  REPO_URL: 'https://github.com/Unjuno/prompt-vote-lab'
});

assertExists(briefingPath);
const briefing = await readFile(briefingPath, 'utf8');
assertIncludes(briefing, 'Prompt Vote Lab Briefing: Week smoke-001', 'briefing title');
assertIncludes(briefing, '## Observe', 'briefing observe section');
assertIncludes(briefing, '## Orient', 'briefing orient section');
assertIncludes(briefing, '## Decide', 'briefing decide section');
assertIncludes(briefing, '## Act', 'briefing act section');
assertIncludes(briefing, 'Vote:', 'briefing vote link');
assertIncludes(briefing, 'Submit prompt:', 'briefing submit link');
assertIncludes(briefing, 'This briefing is safe to share as a status update only after checking', 'briefing share warning');
assertEqual(briefing.includes('voter_logins'), false, 'briefing must not expose voter login lists');

const emptySnapshotDir = `${testRoot}/bad/empty`;
await mkdir(emptySnapshotDir, { recursive: true });
runExpectFailure('node', ['scripts/create-snapshot-summary.mjs'], {
  SNAPSHOT_DIR: emptySnapshotDir,
  SUMMARY_OUTPUT: `${testRoot}/bad/empty-summary.json`,
  SUMMARY_MARKDOWN_OUTPUT: `${testRoot}/bad/empty-summary.md`
}, 'No weekly snapshot files found');

const duplicateSnapshotDir = `${testRoot}/bad/duplicate`;
await mkdir(duplicateSnapshotDir, { recursive: true });
await writeFile(`${duplicateSnapshotDir}/week-a.json`, `${JSON.stringify(snapshot, null, 2)}\n`, 'utf8');
await writeFile(`${duplicateSnapshotDir}/week-b.json`, `${JSON.stringify(snapshot, null, 2)}\n`, 'utf8');
runExpectFailure('node', ['scripts/create-snapshot-summary.mjs'], {
  SNAPSHOT_DIR: duplicateSnapshotDir,
  SUMMARY_OUTPUT: `${testRoot}/bad/duplicate-summary.json`,
  SUMMARY_MARKDOWN_OUTPUT: `${testRoot}/bad/duplicate-summary.md`
}, 'duplicate week');

const identitySnapshotDir = `${testRoot}/bad/identity`;
await mkdir(identitySnapshotDir, { recursive: true });
const identitySnapshot = structuredClone(snapshot);
identitySnapshot.metrics.voter_logins = ['example-user'];
await writeFile(`${identitySnapshotDir}/week-identity.json`, `${JSON.stringify(identitySnapshot, null, 2)}\n`, 'utf8');
runExpectFailure('node', ['scripts/create-snapshot-summary.mjs'], {
  SNAPSHOT_DIR: identitySnapshotDir,
  SUMMARY_OUTPUT: `${testRoot}/bad/identity-summary.json`,
  SUMMARY_MARKDOWN_OUTPUT: `${testRoot}/bad/identity-summary.md`
}, 'forbidden key');

const mismatchSnapshotDir = `${testRoot}/bad/mismatch`;
await mkdir(mismatchSnapshotDir, { recursive: true });
const mismatchSnapshot = structuredClone(snapshot);
mismatchSnapshot.metrics.candidate_count = 999;
await writeFile(`${mismatchSnapshotDir}/week-mismatch.json`, `${JSON.stringify(mismatchSnapshot, null, 2)}\n`, 'utf8');
runExpectFailure('node', ['scripts/create-snapshot-summary.mjs'], {
  SNAPSHOT_DIR: mismatchSnapshotDir,
  SUMMARY_OUTPUT: `${testRoot}/bad/mismatch-summary.json`,
  SUMMARY_MARKDOWN_OUTPUT: `${testRoot}/bad/mismatch-summary.md`
}, 'metrics.candidate_count must match');

run('node', ['scripts/create-hn-draft.mjs'], {
  WEEK_ID: week,
  SNAPSHOT_INPUT: snapshotPath,
  RUN_LOG_INPUT: runLogPath,
  HN_DRAFT_OUTPUT: hnDraftPath,
  SITE_URL: 'https://unjuno.github.io/prompt-vote-lab/',
  REPO_URL: 'https://github.com/Unjuno/prompt-vote-lab'
});

assertExists(hnDraftPath);
const draft = await readFile(hnDraftPath, 'utf8');
assertIncludes(draft, 'HN Draft: Week smoke-001', 'HN draft title');
assertIncludes(draft, 'Do-not-post checklist', 'HN do-not-post section');
assertIncludes(draft, 'Run log still contains unrecorded fields.', 'HN blocker for incomplete run log');

console.log('Offline workflow smoke test passed.');

function assertExists(path) {
  if (!existsSync(path)) {
    throw new Error(`Expected file to exist: ${path}`);
  }
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) {
    throw new Error(`${label}: expected ${expected}, got ${actual}`);
  }
}

function assertIncludes(text, expected, label) {
  if (!text.includes(expected)) {
    throw new Error(`${label}: missing ${expected}`);
  }
}
