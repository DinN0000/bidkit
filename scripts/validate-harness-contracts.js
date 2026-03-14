#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const errors = [];

const fileCache = {};
function read(relPath) {
  if (!fileCache[relPath]) {
    fileCache[relPath] = fs.readFileSync(path.join(root, relPath), 'utf8');
  }
  return fileCache[relPath];
}

function walk(dirPath, out = []) {
  for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
    const full = path.join(dirPath, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (entry.isFile()) out.push(full);
  }
  return out;
}

const requiredFiles = [
  'AGENTS.md',
  'CLAUDE.md',
  'reference/proposal-guide-format.md',
  'skills/output/SKILL.md',
  'templates/init/outline.yaml',
  'templates/init/runtime-state.json',
  'skills/setup/SKILL.md',
];

for (const relPath of requiredFiles) {
  if (!fs.existsSync(path.join(root, relPath))) {
    errors.push(`Missing required file: ${relPath}`);
  }
}

for (const target of ['agents', 'skills', 'reference', 'templates']) {
  const abs = path.join(root, target);
  if (!fs.existsSync(abs)) continue;
  for (const file of walk(abs)) {
    const content = read(path.relative(root, file));
    if (content.includes('depends_on')) {
      errors.push(`Use "dependencies" instead of "depends_on": ${path.relative(root, file)}`);
    }
  }
}

const outputSkill = read('skills/output/SKILL.md');
if (!outputSkill.includes('required_for_output')) {
  errors.push('skills/output/SKILL.md must reference required_for_output');
}
if (!outputSkill.includes('defaults to `true`')) {
  errors.push('skills/output/SKILL.md must document that missing required_for_output defaults to true');
}
if (!outputSkill.includes('## Summary')) {
  errors.push('skills/output/SKILL.md must use the SSOT body Summary section');
}
if (/summary front-matter/i.test(outputSkill)) {
  errors.push('skills/output/SKILL.md must not require a summary front-matter field');
}

const outlineTemplate = read('templates/init/outline.yaml');
if (!outlineTemplate.includes('required_for_output')) {
  errors.push('templates/init/outline.yaml must include required_for_output');
}

for (const entryFile of ['AGENTS.md', 'CLAUDE.md']) {
  const content = read(entryFile);
  if (!content.includes('One question at a time')) {
    errors.push(`${entryFile} must include the one-question-at-a-time rule`);
  }
  if (!content.includes('Project control')) {
    errors.push(`${entryFile} must distinguish proposal content from project control data`);
  }
}

// Runtime state must be described as optional/fallback in key docs
const runtimeStateDocs = {
  'skills/status/SKILL.md': read('skills/status/SKILL.md'),
  'skills/write/SKILL.md': read('skills/write/SKILL.md'),
  'skills/design/SKILL.md': read('skills/design/SKILL.md'),
  'ARCHITECTURE.md': read('ARCHITECTURE.md'),
};
for (const [file, content] of Object.entries(runtimeStateDocs)) {
  const hasOptional = /runtime[^.]*optional|optional[^.]*runtime/i.test(content);
  const hasFallback = /runtime[^.]*fallback|fallback[^.]*runtime/i.test(content);
  const hasAdvisory = /runtime[^.]*advisory|advisory[^.]*runtime/i.test(content);
  if (!hasOptional && !hasFallback && !hasAdvisory) {
    errors.push(`${file} must describe runtime state as optional, fallback, or advisory`);
  }
}

const guide = read('reference/proposal-guide-format.md');
if (!guide.includes('Current: [user-facing situation label]')) {
  errors.push('Proposal Guide must include a Current line');
}
if (!guide.includes('User-Facing Status Labels')) {
  errors.push('Proposal Guide must define user-facing status labels');
}

if (errors.length > 0) {
  console.error('Harness contract validation failed:\n');
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log('Harness contract validation passed.');
