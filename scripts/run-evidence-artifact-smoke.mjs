#!/usr/bin/env node
import { mkdir, readFile, rm } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';

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

await assertArtifactSet();
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

async function assertArtifactSet() {
  const required = [
    snapshotPath,
    aggregationLogPath,
    runLogPath,
    summaryJsonPath,
    summaryMarkdownPath,
    briefingPath,
    hnDraftPath
  ];

  for (const file of required) {
    if (!existsSync(file)) {
      throw new Error(`Missing artifact: ${file}`);
    }
  }

  const snapshot = JSON.parse(await readFile(snapshotPath, 'utf8'));
  assertEqual(snapshot.schema_version, 'snapshot-v1.2', 'snapshot schema');
  assertEqual(snapshot.metrics.candidate_count, 4, 'snapshot candidate count');
  assertEqual(snapshot.no_change_baseline_candidate.votes, 20, 'snapshot baseline votes');
  assertNoForbiddenIdentityFields(snapshot, snapshotPath);

  const summary = JSON.parse(await readFile(summaryJsonPath, 'utf8'));
  assertEqual(summary.schema_version, 'snapshot-summary-v1.0', 'summary schema');
  assertEqual(summary.week_count, 1, 'summary week count');
  assertNoForbiddenIdentityFields(summary, summaryJsonPath);

  const runLog = await readFile(runLogPath, 'utf8');
  assertIncludes(runLog, 'Participation Metrics', 'run log metrics');
  assertIncludes(runLog, 'Ranked Candidates With Baseline', 'run log baseline table');

  const summaryMarkdown = await readFile(summaryMarkdownPath, 'utf8');
  assertIncludes(summaryMarkdown, 'Weekly Metrics Summary', 'summary markdown title');

  const briefing = await readFile(briefingPath, 'utf8');
  assertIncludes(briefing, 'Prompt Vote Lab Briefing', 'briefing title');
  assertIncludes(briefing, '## Observe', 'briefing observe');
  assertIncludes(briefing, '## Orient', 'briefing orient');
  assertIncludes(briefing, '## Decide', 'briefing decide');
  assertIncludes(briefing, '## Act', 'briefing act');
  assertIncludes(briefing, 'Submit prompt:', 'briefing submit link');
  assertIncludes(briefing, 'Vote:', 'briefing vote link');

  const hnDraft = await readFile(hnDraftPath, 'utf8');
  assertIncludes(hnDraft, 'Do-not-post checklist', 'HN draft safety checklist');
  assertIncludes(hnDraft, 'Run log still contains unrecorded fields.', 'HN draft evidence blocker');
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

function assertNoForbiddenIdentityFields(value, location) {
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
