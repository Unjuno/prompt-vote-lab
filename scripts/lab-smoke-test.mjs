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

const externalResourcePatterns = [
  /<script[^>]+src=["']https?:\/\//i,
  /<link[^>]+href=["']https?:\/\//i,
  /<img[^>]+src=["']https?:\/\//i,
  /<iframe[^>]+src=["']https?:\/\//i,
  /<object[^>]+data=["']https?:\/\//i,
  /@import\s+url\(["']?https?:\/\//i,
  /url\(["']?https?:\/\//i
];

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
    label: 'lab keeps a small experiment status card visible',
    pass: /Experiment status/i.test(visibleText)
  },
  {
    label: 'lab has Content-Security-Policy with connect-src none',
    pass: /Content-Security-Policy/i.test(html) && /connect-src 'none'/i.test(html)
  },
  {
    label: 'lab does not load external http resources',
    pass: !externalResourcePatterns.some((pattern) => pattern.test(combined))
  },
  {
    label: 'lab does not contain network APIs',
    pass: !/fetch\(|XMLHttpRequest|WebSocket|EventSource|sendBeacon/i.test(combined)
  },
  {
    label: 'lab root is not a large participant docs index',
    pass: !/Primary participant navigation|Latest comparison|Public results|Weekly runs/i.test(visibleText)
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