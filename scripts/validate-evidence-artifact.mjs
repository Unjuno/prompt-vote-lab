#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';

const root = process.env.EVIDENCE_ROOT || process.argv[2] || 'tmp/evidence';
const week = process.env.WEEK_ID || process.argv[3] || inferWeek(root);

const paths = {
  snapshot: `${root}/data/snapshots/week-${week}.json`,
  aggregationLog: `${root}/logs/aggregation/week-${week}.jsonl`,
  runLog: `${root}/runs/week-${week}.md`,
  summaryJson: `${root}/reports/summary/weekly-metrics.json`,
  summaryMarkdown: `${root}/reports/summary/weekly-metrics.md`,
  briefing: `${root}/reports/briefings/week-${week}.md`,
  hnDraft: `${root}/reports/hn/week-${week}.md`
};

await validateArtifact();
console.log(`Evidence artifact validation passed: ${root} week=${week}`);

function inferWeek(base) {
  const prefix = `${base}/data/snapshots/week-`;
  const candidates = [];
  for (const maybe of [
    'dry-run-001',
    'artifact-smoke-001',
    'smoke-001'
  ]) {
    if (existsSync(`${prefix}${maybe}.json`)) return maybe;
  }
  throw new Error('WEEK_ID is required when the snapshot name is not one of the known smoke defaults');
}

async function validateArtifact() {
  for (const [label, file] of Object.entries(paths)) {
    if (!existsSync(file)) throw new Error(`missing ${label}: ${file}`);
  }

  const snapshot = JSON.parse(await readFile(paths.snapshot, 'utf8'));
  assertEqual(snapshot.schema_version, 'snapshot-v1.2', 'snapshot schema');
  assertEqual(snapshot.selection_rule?.no_change_baseline, 20, 'selection baseline');
  assertEqual(snapshot.no_change_baseline_candidate?.votes, 20, 'baseline candidate votes');
  assertArray(snapshot.top_prompts, 'top_prompts');
  if (snapshot.top_prompts.length > 3) throw new Error('top_prompts must contain at most 3 prompts');
  assertObject(snapshot.metrics, 'snapshot metrics');
  assertNoForbiddenIdentityFields(snapshot, paths.snapshot);

  const aggregationLog = await readFile(paths.aggregationLog, 'utf8');
  assertIncludes(aggregationLog, 'weekly_snapshot_started', 'aggregation start event');
  assertIncludes(aggregationLog, 'weekly_snapshot_finished', 'aggregation finish event');

  const runLog = await readFile(paths.runLog, 'utf8');
  assertIncludes(runLog, 'Participation Metrics', 'run log metrics');
  assertIncludes(runLog, 'Ranked Candidates With Baseline', 'run log baseline table');
  assertIncludes(runLog, 'Selection Rule', 'run log selection rule');

  const summary = JSON.parse(await readFile(paths.summaryJson, 'utf8'));
  assertEqual(summary.schema_version, 'snapshot-summary-v1.0', 'summary schema');
  if (!Number.isInteger(summary.week_count) || summary.week_count < 1) throw new Error('summary week_count must be >= 1');
  assertObject(summary.latest_week, 'summary latest_week');
  assertObject(summary.trend, 'summary trend');
  assertNoForbiddenIdentityFields(summary, paths.summaryJson);

  const summaryMarkdown = await readFile(paths.summaryMarkdown, 'utf8');
  assertIncludes(summaryMarkdown, 'Weekly Metrics Summary', 'summary markdown title');

  const briefing = await readFile(paths.briefing, 'utf8');
  assertIncludes(briefing, 'Prompt Vote Lab Briefing', 'briefing title');
  assertIncludes(briefing, '## Observe', 'briefing observe');
  assertIncludes(briefing, '## Orient', 'briefing orient');
  assertIncludes(briefing, '## Decide', 'briefing decide');
  assertIncludes(briefing, '## Act', 'briefing act');
  assertIncludes(briefing, 'Submit prompt:', 'briefing submit link');
  assertIncludes(briefing, 'Vote:', 'briefing vote link');
  assertNoForbiddenText(briefing, paths.briefing);

  const hnDraft = await readFile(paths.hnDraft, 'utf8');
  assertIncludes(hnDraft, 'Do-not-post checklist', 'HN draft checklist');
}

function assertEqual(actual, expected, label) {
  if (actual !== expected) throw new Error(`${label}: expected ${expected}, got ${actual}`);
}

function assertIncludes(text, expected, label) {
  if (!text.includes(expected)) throw new Error(`${label}: missing ${expected}`);
}

function assertArray(value, label) {
  if (!Array.isArray(value)) throw new Error(`${label} must be an array`);
}

function assertObject(value, label) {
  if (value === null || typeof value !== 'object' || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
}

function assertNoForbiddenText(text, location) {
  for (const needle of ['_voter_logins', 'voter_logins', 'reaction_users']) {
    if (text.includes(needle)) throw new Error(`${location}: forbidden text ${needle}`);
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
      if (forbidden.has(key)) throw new Error(`${location}: forbidden key ${current.path}.${key}`);
      stack.push({ value: child, path: `${current.path}.${key}` });
    }
  }
}
