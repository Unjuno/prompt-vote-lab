#!/usr/bin/env node
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';

const week = process.env.WEEK_ID || inferWeekId();
const snapshotPath = process.env.SNAPSHOT_INPUT || `data/snapshots/week-${week}.json`;
const runLogPath = process.env.RUN_LOG_INPUT || `runs/week-${week}.md`;
const outputPath = process.env.HN_DRAFT_OUTPUT || `reports/hn/week-${week}.md`;
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
  return String(value || '').replace(/\|/g, '\\|').trim();
}

function includesUnrecorded(markdown) {
  return /\bunrecorded\b/i.test(markdown || '');
}

function statusFromRunLog(markdown) {
  const match = markdown.match(/^Status:\s*(.+)$/im);
  return match ? match[1].trim() : 'unrecorded';
}

function gapFromRunLog(markdown) {
  const match = markdown.match(/^Gap classification:\s*(.+)$/im);
  return match ? match[1].trim() : 'unrecorded';
}

function selectedPrompt(snapshot) {
  if (!snapshot || snapshot.decision !== 'selected') return null;
  return snapshot.top_prompts?.[0] || null;
}

function titleCandidates(snapshot, runStatus, gapClassification) {
  const selected = selectedPrompt(snapshot);
  const base = 'Prompt Vote Lab';

  if (!selected) {
    return [
      `${base}: a weekly public prompt-voting experiment`,
      `${base}: recording no-run weeks in a public AI coding experiment`,
      `${base}: using vote snapshots before AI coding runs`
    ];
  }

  return [
    `${base}: voters selected “${selected.title}” for a constrained AI coding run`,
    `${base}: week ${snapshot.week} vote snapshot and AI coding result`,
    `${base}: ${selected.votes} votes selected a prompt, result classified as ${gapClassification || runStatus}`
  ];
}

function doNotPostReasons(snapshot, runLog, runStatus, gapClassification) {
  const reasons = [];
  if (!snapshot) reasons.push('Snapshot file is missing or unreadable.');
  if (!runLog) reasons.push('Run log is missing or unreadable.');
  if (runLog && includesUnrecorded(runLog)) reasons.push('Run log still contains unrecorded fields.');
  if (runStatus === 'unrecorded') reasons.push('Run status is unrecorded.');
  if (gapClassification === 'unrecorded') reasons.push('Expectation-gap classification is unrecorded.');
  return reasons;
}

function promptTable(snapshot) {
  const prompts = snapshot?.top_prompts || [];
  if (prompts.length === 0) return '| Rank | Issue | Prompt | Author | Votes |\n|---:|---:|---|---|---:|\n| - | - | - | - | - |';
  const rows = prompts.map((prompt) => (
    `| ${prompt.rank} | #${prompt.issue} | ${escapeMarkdown(prompt.title)} | ${escapeMarkdown(prompt.author)} | ${prompt.votes} |`
  ));
  return ['| Rank | Issue | Prompt | Author | Votes |', '|---:|---:|---|---|---:|', ...rows].join('\n');
}

function draftText(snapshot, runStatus, gapClassification) {
  const selected = selectedPrompt(snapshot);
  if (!snapshot) {
    return 'Internal draft only: snapshot evidence is missing, so this should not be posted.';
  }

  if (!selected) {
    return `This is a small public experiment around prompt voting and constrained AI coding. For week ${snapshot.week}, the vote snapshot did not pass the selection threshold, so no implementation run should be treated as selected. The snapshot is kept as evidence rather than silently skipping the week.`;
  }

  return `This is a small public experiment around prompt voting and constrained AI coding. For week ${snapshot.week}, the vote snapshot selected issue #${selected.issue}, “${selected.title}”, with ${selected.votes} votes. The implementation surface is constrained to the repository's lab/ directory, and the run log records the result, safety checks, and expectation-gap classification. Current recorded status: ${runStatus}. Gap classification: ${gapClassification}.`;
}

async function readJson(path) {
  const text = await readFile(path, 'utf8');
  return JSON.parse(text);
}

const snapshot = existsSync(snapshotPath) ? await readJson(snapshotPath) : null;
const runLog = existsSync(runLogPath) ? await readFile(runLogPath, 'utf8') : '';
const runStatus = statusFromRunLog(runLog);
const gapClassification = gapFromRunLog(runLog);
const titles = titleCandidates(snapshot, runStatus, gapClassification);
const reasons = doNotPostReasons(snapshot, runLog, runStatus, gapClassification);
const generatedAt = new Date().toISOString();

const markdown = `# HN Draft: Week ${week}\n\n` +
`Generated at: ${generatedAt}\n\n` +
`## Title candidates\n\n` +
`${titles.map((title, index) => `${index + 1}. ${title}`).join('\n')}\n\n` +
`## Recommended title\n\n` +
`${titles[0]}\n\n` +
`## Submission URL candidate\n\n` +
`${siteUrl}\n\n` +
`Alternative repository URL: ${repoUrl}\n\n` +
`## Text draft\n\n` +
`${draftText(snapshot, runStatus, gapClassification)}\n\n` +
`## Top prompts from snapshot\n\n` +
`${promptTable(snapshot)}\n\n` +
`## Evidence checklist\n\n` +
`- [${snapshot ? 'x' : ' '}] Weekly snapshot exists: \`${snapshotPath}\`\n` +
`- [${runLog ? 'x' : ' '}] Run log exists: \`${runLogPath}\`\n` +
`- [${runStatus !== 'unrecorded' ? 'x' : ' '}] Run status is recorded\n` +
`- [${gapClassification !== 'unrecorded' ? 'x' : ' '}] Expectation-gap classification is recorded\n\n` +
`## Do-not-post checklist\n\n` +
`${reasons.length === 0 ? '- [ ] No blocking issues detected by this generator.' : reasons.map((reason) => `- [x] ${reason}`).join('\n')}\n\n` +
`## Maintainer action\n\n` +
`This file is a draft only. Manually review, edit, and submit to Hacker News if appropriate. Do not automate posting.\n`;

await mkdir(outputPath.split('/').slice(0, -1).join('/'), { recursive: true });
await writeFile(outputPath, markdown, 'utf8');
console.log(`Wrote ${outputPath}`);
