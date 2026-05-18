import { readFileSync, existsSync } from 'node:fs'
import { join } from 'node:path'

const root = process.cwd()

const requiredFiles = [
  'SKILL.md',
  'README.md',
  'agents/openai.yaml',
  'assets/starter-pack/root/agents.md',
  'assets/starter-pack/root/progress.md',
  'assets/starter-pack/planning/vision.md',
  'assets/starter-pack/planning/bookkeeping.md',
  'assets/starter-pack/planning/story-management.md',
  'assets/starter-pack/planning/testing-strategy.md',
  'assets/starter-pack/planning/design-direction.md',
  'assets/starter-pack/stories/index.md',
  'assets/starter-pack/stories/story-template.md',
  'assets/starter-pack/optional/compliance/planning/regulations.md',
  'assets/starter-pack/optional/bootstrap/planning/bootstrap-plan.md',
  'assets/starter-pack/optional/bootstrap/steps/step-01.md',
  'assets/starter-pack/optional/owner-run-demo/planning/owner-run-demo-workflows.md',
  'assets/starter-pack/optional/owner-run-demo/demos/owner-run-demo-plan.md',
  'assets/starter-pack/optional/owner-run-demo/prompts/implement-owner-run-demo.md',
]

const requiredSkillTerms = [
  'Owner-run demo module',
  'window.__ownerRunDemo',
  'data-demo-*',
  'OS-level input',
  'app-orchestrated',
  'harness-orchestrated',
  'hybrid',
  'a step is not complete when narration text changes',
  'assets/starter-pack/optional/owner-run-demo/planning/owner-run-demo-workflows.md',
  'assets/starter-pack/optional/owner-run-demo/demos/owner-run-demo-plan.md',
  'assets/starter-pack/optional/owner-run-demo/prompts/implement-owner-run-demo.md',
]

const requiredDemoGuideTerms = [
  'OwnerRunDemoState',
  'OwnerRunDemoStep',
  'CGEventCreateMouseEvent',
  'CGEventCreateScrollWheelEvent',
  'CGEventPost',
  'Accessibility permission',
  'Do not use browser JavaScript clicks',
  'Orchestration Model Contract',
  'Step Synchronization Contract',
  'narrationStatus',
  'actionStatus',
  'canAdvance',
  'timingFallback',
  'Verification proves visible actions happened',
]

function read(relativePath) {
  return readFileSync(join(root, relativePath), 'utf8')
}

function normalizeStart(content) {
  return content.replace(/^\uFEFF/, '')
}

function assert(condition, message) {
  if (!condition) {
    throw new Error(message)
  }
}

for (const file of requiredFiles) {
  assert(existsSync(join(root, file)), `Missing required file: ${file}`)
}

const skill = normalizeStart(read('SKILL.md'))
assert(/^---\r?\nname: speclite/m.test(skill), 'SKILL.md frontmatter is missing or malformed')
for (const term of requiredSkillTerms) {
  assert(skill.includes(term), `SKILL.md is missing reference: ${term}`)
}

const readme = read('README.md')
assert(readme.includes('Owner-run AI demos'), 'README.md is missing owner-run demo discovery section')
assert(readme.includes('assets/starter-pack/optional/owner-run-demo/'), 'README.md is missing owner-run demo path')

const manifest = read('agents/openai.yaml')
assert(manifest.includes('display_name: "Speclite"'), 'agents/openai.yaml is missing display name')
assert(manifest.includes('workflow modules'), 'agents/openai.yaml is missing workflow module discovery text')

const demoGuide = read('assets/starter-pack/optional/owner-run-demo/planning/owner-run-demo-workflows.md')
for (const term of requiredDemoGuideTerms) {
  assert(demoGuide.includes(term), `Owner-run demo guide is missing: ${term}`)
}

const demoPlan = read('assets/starter-pack/optional/owner-run-demo/demos/owner-run-demo-plan.md')
for (const heading of [
  '## Demo Summary',
  '## Required Owner Permissions',
  '## Orchestration Model',
  '## App State Contract',
  '## Stable DOM Target List',
  '## Narration Steps',
  '## Step Synchronization Contract',
  '## Visible Cursor Actions',
  '## Fake Typing Segments',
  '## Wait Conditions',
  '## Failure And Abort Behavior',
  '## Acceptance Criteria',
  '## Test Plan',
]) {
  assert(demoPlan.includes(heading), `Owner-run demo plan is missing heading: ${heading}`)
}

const prompt = read('assets/starter-pack/optional/owner-run-demo/prompts/implement-owner-run-demo.md')
for (const term of [
  'Inspect the target app',
  'Add hidden owner-demo mode',
  'Choose and document the primary orchestration model',
  'Step synchronization contract',
  'Only one narration may be active at a time',
  'Use OS-level input',
  'Use CDP, Playwright, browser APIs, or equivalent only for state and bounds',
  'Verification proves visible actions happened',
  'Document how to rerun it',
]) {
  assert(prompt.includes(term), `Implementation prompt is missing: ${term}`)
}

console.log('Speclite validation passed.')
