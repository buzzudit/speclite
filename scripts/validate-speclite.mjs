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
  'assets/starter-pack/optional/demo-maker/planning/demo-maker-workflows.md',
  'assets/starter-pack/optional/demo-maker/demos/demo-plan.md',
  'assets/starter-pack/optional/demo-maker/prompts/implement-demo-maker.md',
  'assets/starter-pack/optional/demo-maker/tooling/lib.mjs',
  'assets/starter-pack/optional/demo-maker/tooling/voice.mjs',
  'assets/starter-pack/optional/demo-maker/tooling/mux.mjs',
  'assets/starter-pack/optional/demo-maker/tooling/script.template.mjs',
  'assets/starter-pack/optional/demo-maker/tooling/walkthrough.template.mjs',
  'assets/starter-pack/optional/skill-builder/SKILL.md',
  'assets/starter-pack/optional/skill-builder/references/interview-guide.md',
  'assets/starter-pack/optional/skill-builder/references/generation-contract.md',
  'assets/starter-pack/optional/skill-builder/references/provenance-guide.md',
  'assets/starter-pack/optional/skill-builder/references/port-catalog.md',
  'assets/starter-pack/optional/skill-builder/scripts/validate_manifest.py',
  'assets/starter-pack/optional/skill-builder/scripts/validate_skill_package.py',
  'assets/starter-pack/optional/skill-builder/scripts/discover_compositions.py',
  'assets/skill-builder/schemas/skill-manifest.schema.json',
  'assets/skill-builder/schemas/port-types.json',
  'assets/skill-builder/schemas/deliverable-types.json',
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

const requiredDemoMakerSkillTerms = [
  'Demo Maker module',
  'eleven_v3',
  'calibrate picture time against the clock',
  'full ffmpeg and ffprobe',
  'never print it or commit it',
  'assets/starter-pack/optional/demo-maker/planning/demo-maker-workflows.md',
  'assets/starter-pack/optional/demo-maker/tooling/',
]

const requiredDemoMakerGuideTerms = [
  'Demo Maker versus the owner-run demo',
  'the product must carry the journey',
  'Calibrate.',
  'Playwright',
  'ELEVENLABS_API_KEY',
  '[short pause]',
  'does not support request stitching',
  'Verification checklist',
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

for (const term of requiredDemoMakerSkillTerms) {
  assert(skill.toLowerCase().includes(term.toLowerCase()), `SKILL.md is missing Demo Maker reference: ${term}`)
}
assert(readme.includes('Demo Maker'), 'README.md is missing Demo Maker discovery section')
const makerGuide = read('assets/starter-pack/optional/demo-maker/planning/demo-maker-workflows.md')
for (const term of requiredDemoMakerGuideTerms) {
  assert(makerGuide.toLowerCase().includes(term.toLowerCase()), `Demo Maker guide is missing: ${term}`)
}
const makerPlan = read('assets/starter-pack/optional/demo-maker/demos/demo-plan.md')
for (const heading of ['## Demo Summary', '## Journey', '## Voice', '## Beats', '## Start State And Data', '## Sync Plan', '## Acceptance Criteria', '## Test Plan']) {
  assert(makerPlan.includes(heading), `Demo Maker plan is missing heading: ${heading}`)
}
const makerPrompt = read('assets/starter-pack/optional/demo-maker/prompts/implement-demo-maker.md')
for (const term of ['Never print the key', 'full ffmpeg and ffprobe', 'Get the owner', 'Verify: video length']) {
  assert(makerPrompt.includes(term), `Demo Maker prompt is missing: ${term}`)
}

// Skill Builder module validation
const requiredSkillBuilderSkillTerms = [
  'Skill Builder module',
  'skill-manifest.json',
  'provenance',
  'academic',
  'industry',
  'session-flow',
  'reference',
  'one-shot',
  'recurring-check',
  'typed ports',
  'validate_manifest.py',
  'assets/starter-pack/optional/skill-builder/',
  'assets/skill-builder/schemas/',
]

for (const term of requiredSkillBuilderSkillTerms) {
  assert(skill.includes(term), `SKILL.md is missing Skill Builder reference: ${term}`)
}

const sbSkill = normalizeStart(read('assets/starter-pack/optional/skill-builder/SKILL.md'))
assert(/^---\r?\nname: skill-builder/m.test(sbSkill), 'Skill Builder SKILL.md frontmatter is missing or malformed')
for (const term of [
  'Deep methodology extraction',
  'Provenance gathering',
  'Port definition',
  'severity-findings',
  'skill-manifest.json',
  'verify_delivery.py',
  'session-flow',
  'recurring-check',
]) {
  assert(sbSkill.includes(term), `Skill Builder SKILL.md is missing: ${term}`)
}

const sbInterviewGuide = read('assets/starter-pack/optional/skill-builder/references/interview-guide.md')
for (const term of [
  'Extract, don\'t prescribe',
  'Challenge, don\'t accept',
  'Ground, don\'t assume',
  'Phase 3: Deep extraction',
  'Adaptive depth',
]) {
  assert(sbInterviewGuide.includes(term), `Skill Builder interview guide is missing: ${term}`)
}

const sbProvenanceGuide = read('assets/starter-pack/optional/skill-builder/references/provenance-guide.md')
for (const term of [
  'Academic (required, agent-gathered)',
  'Industry (required, agent-gathered)',
  'Organizational (optional, user-supplied)',
  'Conflict resolution',
  'Minimum requirements',
]) {
  assert(sbProvenanceGuide.includes(term), `Skill Builder provenance guide is missing: ${term}`)
}

const sbManifestSchema = read('assets/skill-builder/schemas/skill-manifest.schema.json')
try {
  JSON.parse(sbManifestSchema)
} catch (e) {
  assert(false, `skill-manifest.schema.json is not valid JSON: ${e.message}`)
}

const sbPortTypes = read('assets/skill-builder/schemas/port-types.json')
try {
  const portData = JSON.parse(sbPortTypes)
  assert(portData.types && typeof portData.types === 'object', 'port-types.json missing "types" object')
  assert('severity-findings' in portData.types, 'port-types.json missing severity-findings type')
} catch (e) {
  assert(false, `port-types.json validation failed: ${e.message}`)
}

console.log('Speclite validation passed.')
