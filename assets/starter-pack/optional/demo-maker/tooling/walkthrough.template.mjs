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
const SPLASH_DUR = 4.0 // seconds for silent beats (splash cards with no narration)

await generate() // cached by text, voice and settings, so unchanged lines cost nothing
const clips = Object.fromEntries(
  beats.filter(b => b.text).map((b) => [b.id, { file: clipPath(b), dur: duration(clipPath(b)) }])
)

const APP_URL = process.env.TOUR_URL ?? '{{APP_URL}}'
const DEMO_EMAIL = '{{DEMO_EMAIL}}'
const DEMO_PASS = '{{DEMO_PASS}}'

// baseUrl: where the app is served (check it is the right app). storage: start state written to localStorage before the app loads (for example a theme key). scrollSelector: the element that scrolls.
const t = await start({ name: OUT, baseUrl: APP_URL, storage: {}, scrollSelector: 'main' })
const { page } = t
const t0 = Date.now()
const now = () => (Date.now() - t0) / 1000

// Hold times written for one narration can be stretched when a line runs longer, so the picture keeps pace.
let F = 1
const hover = async (loc, ms = 1400, opts) => { await t.moveTo(loc, opts); await sleep(ms * F) }

const starts = {} // wall-clock time each beat started
const cards = {} // wall-clock time the title and closing cards appeared (calibration anchors)
const chapters = {} // wall-clock time each chapter label appeared (extra anchors)
const chap = async (n, text) => { await t.chapter(n, text); chapters[n] = now() }

// One async function per beat id. Use REAL clicks (t.click) so the video shows the product being used.
// Prefer text-based Playwright locators (page.getByText(), page.getByRole()) over CSS class selectors.
// Many apps use CSS-in-JS or inline styles with no class names; text locators are resilient.
// Each action should finish a little before its narration does.
const actions = {
  async T0() {
    // Show splash immediately so the video opens on the branded card (frame 1)
    await t.showCard(`
      <div class="glow" style="top:-200px;left:50%;transform:translateX(-50%)"></div>
      <div class="badge" data-anim style="animation-delay:0ms"><span class="dot"></span>{{BADGE TEXT}}</div>
      <h1 data-anim style="animation-delay:200ms;margin-top:24px">{{Title}}<br><em>{{Subtitle}}</em></h1>
      <p data-anim style="animation-delay:400ms;margin-top:8px">{{One-line description}}</p>
    `)
    cards.T0 = now()
    starts.T0 = cards.T0
    // Log in behind the splash card — the viewer never sees the login screen
    await t.goto('/login')
    await sleep(400)
    await page.fill('input[type="email"]', DEMO_EMAIL)
    await sleep(200)
    await page.fill('input[type="password"]', DEMO_PASS)
    await sleep(200)
    await page.click('button[type="submit"]')
    await page.waitForURL('**/', { timeout: 15000 })
    await page.waitForLoadState('networkidle')
    await sleep(300)
  },
  async P1() {
    await chap('1', '{{Chapter name}}')
    await t.hideCard()
    await sleep(900)
    // await hover(page.getByText('{{visible text}}').first(), 800)
  },
  // async D1() { await t.click(page.getByRole('link', { name: /Start/ })); await page.waitForURL(/\/step-1/); ... },
  async E1() {
    await t.showCard(`
      <div class="glow" style="top:-200px;left:50%;transform:translateX(-50%)"></div>
      <h1 data-anim>{{Product}} <em>{{Name}}</em></h1>
      <p data-anim style="animation-delay:200ms">{{One-line value prop}}</p>
      <div class="cta-btn" data-anim style="animation-delay:400ms">Start a Free Trial →</div>
      <div data-anim style="animation-delay:600ms;margin-top:24px;font-size:15px;color:var(--muted,#a1a1aa)">{{domain.com}}</div>
    `)
    cards.E1 = now()
    await sleep(500)
  },
}

for (const b of beats) {
  if (b.id !== 'T0') starts[b.id] = now()
  const clip = clips[b.id]
  const beatDur = clip ? (clip.dur + PAD) : SPLASH_DUR
  if (clip) F = Math.min(1.8, Math.max(1, clip.dur / (b.nominal ?? clip.dur)))
  await Promise.all([actions[b.id](), sleep(beatDur * 1000)])
  console.log(`${b.id.padEnd(3)} start ${starts[b.id].toFixed(2)}s  dur ${beatDur.toFixed(2)}s${clip ? '' : ' (silent)'}`)
}
const raw = await t.finish(1400)
const timings = { starts, cards, chapters }
fs.writeFileSync(`tour/out/timings-${VERSION}.json`, JSON.stringify(timings, null, 2))
console.log('raw video:', raw)
mux(raw, timings, OUT)
