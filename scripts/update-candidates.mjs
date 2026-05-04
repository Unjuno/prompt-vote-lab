#!/usr/bin/env node
import { writeFile, mkdir } from 'node:fs/promises';

const owner = process.env.GITHUB_REPOSITORY_OWNER || 'Unjuno';
const repo = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'prompt-vote-lab';
const token = process.env.GITHUB_TOKEN;
const label = process.env.PROMPT_LABEL || 'prompt-proposal';

const noChangeBaseline = Number(process.env.NO_CHANGE_BASELINE || 5);
const requiredMargin = Number(process.env.REQUIRED_MARGIN || 2);
const minimumTotalVotes = Number(process.env.MINIMUM_TOTAL_VOTES || 5);
const outputPath = process.env.CANDIDATE_OUTPUT || 'data/prompt-candidates.js';

if (!token) {
  throw new Error('GITHUB_TOKEN is required.');
}

const apiBase = 'https://api.github.com';
const headers = {
  Accept: 'application/vnd.github+json',
  Authorization: `Bearer ${token}`,
  'X-GitHub-Api-Version': '2022-11-28',
  'User-Agent': 'prompt-vote-lab-candidate-updater'
};

async function github(path) {
  const response = await fetch(`${apiBase}${path}`, { headers });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`GitHub API ${response.status} for ${path}: ${body}`);
  }
  return response.json();
}

async function paginate(path) {
  const results = [];
  let page = 1;
  while (page <= 10) {
    const separator = path.includes('?') ? '&' : '?';
    const data = await github(`${path}${separator}per_page=100&page=${page}`);
    if (!Array.isArray(data) || data.length === 0) break;
    results.push(...data);
    if (data.length < 100) break;
    page += 1;
  }
  return results;
}

function section(body, heading) {
  if (!body) return '';
  const escaped = heading.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`(?:^|\\n)##\\s+${escaped}\\s*\\n([\\s\\S]*?)(?=\\n##\\s+|$)`, 'i');
  const match = body.match(pattern);
  return match ? match[1].trim() : '';
}

function firstParagraph(markdown) {
  return markdown
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('- ') && !line.startsWith('* '))[0] || '';
}

function plainText(value) {
  return value
    .replace(/[`*_>#]/g, '')
    .replace(/\[(.*?)\]\(.*?\)/g, '$1')
    .replace(/\s+/g, ' ')
    .trim();
}

async function plusOneVotes(issueNumber) {
  const reactions = await paginate(`/repos/${owner}/${repo}/issues/${issueNumber}/reactions?content=%2B1`);
  return reactions.filter((reaction) => reaction.content === '+1').length;
}

const issues = await paginate(`/repos/${owner}/${repo}/issues?state=open&labels=${encodeURIComponent(label)}`);
const promptIssues = issues.filter((issue) => !issue.pull_request);

const candidates = [];
for (const issue of promptIssues) {
  const votes = await plusOneVotes(issue.number);
  const expectedResult = plainText(firstParagraph(section(issue.body || '', 'Expected result')));
  const votedPrompt = plainText(firstParagraph(section(issue.body || '', 'Voted prompt')));
  candidates.push({
    number: issue.number,
    title: issue.title.replace(/^\[Prompt\]:\s*/i, '').trim(),
    url: issue.html_url,
    votes,
    comments: issue.comments,
    createdAt: issue.created_at,
    updatedAt: issue.updated_at,
    expectedResult,
    summary: votedPrompt
  });
}

candidates.sort((a, b) => {
  if (b.votes !== a.votes) return b.votes - a.votes;
  const updatedDelta = Date.parse(b.updatedAt) - Date.parse(a.updatedAt);
  if (updatedDelta !== 0) return updatedDelta;
  return a.number - b.number;
});

const totalVotes = candidates.reduce((sum, candidate) => sum + candidate.votes, 0);
const topPromptVotes = candidates[0]?.votes || 0;
const selected = topPromptVotes >= noChangeBaseline + requiredMargin && totalVotes >= minimumTotalVotes;

const payload = {
  generatedAt: new Date().toISOString(),
  source: 'github-actions',
  repository: `${owner}/${repo}`,
  voteContent: '+1',
  selection: {
    noChangeBaseline,
    requiredMargin,
    minimumTotalVotes,
    totalVotes,
    topPromptVotes,
    selected,
    selectedIssueNumber: selected ? candidates[0]?.number ?? null : null
  },
  candidates
};

const outputDirectory = outputPath.split('/').slice(0, -1).join('/');
if (outputDirectory) {
  await mkdir(outputDirectory, { recursive: true });
}
await writeFile(
  outputPath,
  `window.PROMPT_VOTE_LAB_CANDIDATES = ${JSON.stringify(payload, null, 2)};\n`,
  'utf8'
);

console.log(`Wrote ${outputPath}`);
console.log(`Candidates: ${candidates.length}, total votes: ${totalVotes}, top votes: ${topPromptVotes}, selected: ${selected}`);
