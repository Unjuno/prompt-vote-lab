#!/usr/bin/env node
import { readFile, rm } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';

const testRoot = 'tmp/smoke';
const week = 'smoke-001';
const snapshotPath = `${testRoot}/data/snapshots/week-${week}.json`;
const aggregationLogPath = `${testRoot}/logs/aggregation/week-${week}.jsonl`;
const runLogPath = `${testRoot}/runs/week-${week}.md`;
const hnDraftPath = `${testRoot}/reports/hn/week-${week}.md`;

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
assertEqual(snapshot.schema_version, 'snapshot-v1.1', 'snapshot schema version');
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
assertEqual(snapshot.no_change_baseline_candidate.virtual, true, 'baseline virtual flag');
assertEqual(snapshot.ranked_candidates_with_baseline.length, 5, 'ranked candidates with baseline count');
assertEqual(snapshot.ranked_candidates_with_baseline[0].issue, 3, 'ranked baseline table rank 1 issue');
assertEqual(snapshot.ranked_candidates_with_baseline[1].virtual, true, 'ranked baseline table rank 2 baseline');
assertEqual(snapshot.top_prompts.length, 3, 'top prompt count');
assertEqual(snapshot.top_prompts[0].issue, 3, 'rank 1 issue');
assertEqual(snapshot.top_prompts[1].issue, 2, 'rank 2 tie-break issue');
assertEqual(snapshot.top_prompts[2].issue, 4, 'rank 3 tie-break issue');

const runLog = await readFile(runLogPath, 'utf8');
assertIncludes(runLog, 'Ranked Candidates With Baseline', 'run log baseline table heading');
assertIncludes(runLog, '[Baseline]: No change this week', 'run log baseline row');
assertIncludes(runLog, 'Decision reason: `top_prompt_beat_no_change_baseline`', 'run log decision reason');

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
