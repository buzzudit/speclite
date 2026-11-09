// Demo Maker recorder (Speclite). Copy to tour/walkthrough.mjs, replace the example actions, then run: node tour/walkthrough.mjs
// Flow: generate any missing voice clips, drive the real app beat by beat (each beat lasts as long as its clip),
// record the video, calibrate picture time against the clock, and mux voice and picture into an mp4.
import fs from 'node:fs'
import { beats, NAME, VERSION } from './script.mjs'
import { clipPath, duration, generate } from './voice.mjs'
import { sleep, start } from './lib.mjs'
import { mux } from './mux.mjs'

const OUT = `${NAME}-${VERSION}`
const PAD = 0.55 // seconds of breathing room after each line

await generate() // cached by text, voice and settings, so unchanged lines cost nothing
const clips = Object.fromEntries(beats.map((b) => [b.id, { file: clipPath(b), dur: duration(clipPath(b)) }]))

// storage: start state written to localStorage before the app loads (for example a theme key). scrollSelector: the element that scrolls.
const t = await start({ name: OUT, storage: {}, scrollSelector: 'main' })
const { page } = t
const t0 = Date.now()
const now = () => (Date.now() - t0) / 1000

// Hold times written for one narration can be stretched when a line runs longer, so the picture keeps pace.
let F = 1
const hover = async (loc, ms = 1400, opts) => { await t.moveTo(loc, opts); await sleep(ms * F) }

await t.goto('/')
await sleep(1200)

const starts = {} // wall-clock time each beat started
const cards = {} // wall-clock time the title and closing cards appeared (calibration anchors)
const chapters = {} // wall-clock time each chapter label appeared (extra anchors)
const chap = async (n, text) => { await t.chapter(n, text); chapters[n] = now() }

// One async function per beat id. Use REAL clicks (t.click) so the video shows the product being used. Prefer stable selectors
// (data-demo-* attributes, roles, labels) over text. Each action should finish a little before its narration does.
const actions = {
  async T0() {
    await t.showCard('<h1>{{Product}} <em>{{walkthrough}}</em></h1><p>{{one-line subtitle}}</p>')
    cards.T0 = now() // the dark card is the first calibration anchor
    starts.T0 = cards.T0
    await sleep(300)
  },
  async P1() {
    await chap('1', '{{Chapter name}}')
    await t.hideCard()
    await sleep(900)
    // await hover(page.locator('main h1').first(), 800)
  },
  // async D1() { await t.click(page.getByRole('link', { name: /Start/ })); await page.waitForURL(/\/step-1/); ... },
  async E1() {
    await t.showCard('<h1>{{Closing title}}</h1><ol><li><b>1</b><span>{{What we still need to learn}}</span></li></ol>')
    cards.E1 = now() // the closing card is the second calibration anchor
    await sleep(500)
  },
}

for (const b of beats) {
  if (b.id !== 'T0') starts[b.id] = now()
  const clip = clips[b.id]
  F = Math.min(1.8, Math.max(1, clip.dur / (b.nominal ?? clip.dur)))
  await Promise.all([actions[b.id](), sleep((clip.dur + PAD) * 1000)])
  console.log(`${b.id.padEnd(3)} start ${starts[b.id].toFixed(2)}s  clip ${clip.dur.toFixed(2)}s`)
}
const raw = await t.finish(1400)
const timings = { starts, cards, chapters }
fs.writeFileSync(`tour/out/timings-${VERSION}.json`, JSON.stringify(timings, null, 2))
console.log('raw video:', raw)
mux(raw, timings, OUT)
