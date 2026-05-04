#!/usr/bin/env node
import { readFile } from 'node:fs/promises';

const html = await readFile('lab/index.html', 'utf8');
const css = await readFile('lab/style.css', 'utf8');
const js = await readFile('lab/app.js', 'utf8');
const combined = `${html}\n${css}\n${js}`;
const visibleText = html
  .replace(/<script[\s\S]*?<\/script>/gi, ' ')
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<[^>]+>/g, ' ')
  .replace(/\s+/g, ' ')
  .trim();

const checks = [
  {
    label: 'lab title is present',
    pass: /Prompt Vote Lab/i.test(visibleText)
  },
  {
    label: 'lab identifies itself as constrained implementation target',
    pass: /constrained/i.test(visibleText) && /implementation target/i.test(visibleText)
  },
  {
    label: 'lab explains accepted experiment runs change it',
    pass: /accepted/i.test(visibleText) && /experiment runs/i.test(visibleText)
  },
  {
    label: 'lab keeps a no-network expectation visible',
    pass: /without network access/i.test(visibleText) || /no network/i.test(visibleText)
  },
  {
    label: 'lab links back to the landing page',
    pass: /href=["']\.\.\/["']/i.test(html) || /href=["']\/["']/i.test(html)
  },
  {
    label: 'lab links to prompt proposal submission',
    pass: /issues\/new\?template=prompt_proposal\.yml/i.test(html)
  },
  {
    label: 'lab links to prompt vote list',
    pass: /issues\?q=.*prompt-proposal/i.test(html)
  },
  {
    label: 'lab explains votes are +1 reactions',
    pass: /(\+1|👍)/u.test(visibleText) && /reaction/i.test(visibleText)
  },
  {
    label: 'lab mentions 20-vote no-change baseline',
    pass: /20/.test(visibleText) && /baseline/i.test(visibleText)
  },
  {
    label: 'lab links to official run or snapshot evidence',
    pass: /runs\//i.test(html) || /data\/snapshots/i.test(html) || /docs\/snapshot-spec\.md/i.test(html)
  },
  {
    label: 'lab has Content-Security-Policy with connect-src none',
    pass: /Content-Security-Policy/i.test(html) && /connect-src 'none'/i.test(html)
  },
  {
    label: 'lab does not reference external http resources',
    pass: !/https?:\/\//i.test(combined)
  },
  {
    label: 'lab does not contain network APIs',
    pass: !/fetch\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon/i.test(combined)
  }
];

const failures = checks.filter((check) => !check.pass);

for (const check of checks) {
  console.log(`${check.pass ? 'PASS' : 'FAIL'}: ${check.label}`);
}

if (failures.length > 0) {
  console.error('\nLab smoke test failed:');
  for (const failure of failures) {
    console.error(`- ${failure.label}`);
  }
  process.exit(1);
}

console.log('Lab smoke test passed.');
