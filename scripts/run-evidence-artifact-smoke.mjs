#!/usr/bin/env node
import { mkdir, rm } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';

const root = process.env.EVIDENCE_SMOKE_ROOT || 'tmp/evidence-smoke';
const week = process.env.WEEK_ID || 'artifact-smoke-001';
const snapshotPath = `${root}/data/snapshots/week-${week}.json`;
const aggregationLogPath = `${root}/logs/aggregation/week-${week}.jsonl`;
const runLogPath = `${root}/runs/week-${week}.md`;
const summaryJsonPath = `${root}/reports/summary/weekly-metrics.json`;
const summaryMarkdownPath = `${root}/reports/summary/weekly-metrics.md`;
const briefingPath = `${root}/reports/briefings/week-${week}.md`;
const hnDraftPath = `${root}/reports/hn/week-${week}.md`;

await rm(root, { recursive: true, force: true });
await mkdir(root, { recursive: true });

run('node', ['scripts/create-weekly-snapshot.mjs'], {
  SNAPSHOT_FIXTURE: 'tests/fixtures/prompt-candidates.json',
  WEEK_ID: week,
  SNAPSHOT_AT: '2026-05-11T00:00:00+09:00',
  SNAPSHOT_OUTPUT: snapshotPath,
  AGGREGATION_LOG_OUTPUT: aggregationLogPath,
  RUN_LOG_OUTPUT: runLogPath,
  ALLOW_SNAPSHOT_OVERWRITE: 'true'
});

run('node', ['scripts/create-snapshot-summary.mjs'], {
  SNAPSHOT_DIR: `${root}/data/snapshots`,
  SUMMARY_OUTPUT: summaryJsonPath,
  SUMMARY_MARKDOWN_OUTPUT: summaryMarkdownPath
});

run('node', ['scripts/create-public-briefing.mjs'], {
  WEEK_ID: week,
  SNAPSHOT_INPUT: snapshotPath,
  SUMMARY_INPUT: summaryJsonPath,
  RUN_LOG_INPUT: runLogPath,
  BRIEFING_OUTPUT: briefingPath,
  SITE_URL: 'https://unjuno.github.io/prompt-vote-lab/',
  REPO_URL: 'https://github.com/Unjuno/prompt-vote-lab'
});

run('node', ['scripts/create-hn-draft.mjs'], {
  WEEK_ID: week,
  SNAPSHOT_INPUT: snapshotPath,
  RUN_LOG_INPUT: runLogPath,
  HN_DRAFT_OUTPUT: hnDraftPath,
  SITE_URL: 'https://unjuno.github.io/prompt-vote-lab/',
  REPO_URL: 'https://github.com/Unjuno/prompt-vote-lab'
});

run('node', ['scripts/validate-evidence-artifact.mjs', root, week], {});
console.log(`Evidence artifact smoke passed: ${root}`);

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
