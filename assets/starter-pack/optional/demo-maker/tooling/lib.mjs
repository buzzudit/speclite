// Demo Maker helper: drives a web app in headless Chromium with a visible cursor, click ripples, chapter labels and title cards,
// and records the browser video. Part of the Speclite Demo Maker module.
import { chromium } from 'playwright'
import fs from 'node:fs'
import path from 'node:path'

export const BASE = process.env.TOUR_URL ?? 'http://localhost:5190'
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms))

const overlay = () => {
  const css = document.createElement('style')
  css.textContent = `
    #tour-cursor{position:fixed;z-index:2147483647;pointer-events:none;width:22px;height:22px;left:0;top:0;margin:-3px 0 0 -3px;transition:transform 40ms linear}
    #tour-ripple{position:fixed;z-index:2147483646;pointer-events:none;width:34px;height:34px;border-radius:50%;border:3px solid #0f766e;background:rgba(15,118,110,.18);opacity:0;transform:translate(-50%,-50%) scale(.4)}
    #tour-ripple.go{animation:tourRipple 520ms ease-out}
    @keyframes tourRipple{0%{opacity:.95;transform:translate(-50%,-50%) scale(.4)}100%{opacity:0;transform:translate(-50%,-50%) scale(1.9)}}
    #tour-caption{position:fixed;z-index:2147483645;left:50%;bottom:26px;transform:translateX(-50%);max-width:880px;padding:10px 18px;border-radius:10px;background:rgba(17,24,28,.92);color:#fff;font:500 16px/1.35 Inter,system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.25);opacity:0;transition:opacity 220ms;text-align:center}
    #tour-caption.on{opacity:1}
    #tour-chapter{position:fixed;z-index:2147483645;left:28px;bottom:26px;padding:8px 14px;border-radius:8px;background:rgba(17,24,28,.9);color:#fff;font:600 14px/1.2 Inter,system-ui,sans-serif;letter-spacing:.01em;opacity:0;transform:translateY(6px);transition:opacity 260ms,transform 260ms}
    #tour-chapter.on{opacity:1;transform:none}
    #tour-chapter b{color:#5eead4;margin-right:8px}
    #tour-card{position:fixed;inset:0;z-index:2147483640;background:#0f1418;color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:18px;font-family:Inter,system-ui,sans-serif;text-align:center;padding:60px}
    #tour-card.fade{transition:opacity 700ms;opacity:0}
    #tour-card h1{font-size:56px;font-weight:600;letter-spacing:-.02em;margin:0}
    #tour-card h1 em{font-style:normal;color:#5eead4}
    #tour-card p{font-size:22px;color:#a9b3bf;margin:0;max-width:820px;line-height:1.45}
    #tour-card ol{list-style:none;padding:0;margin:8px 0 0;display:flex;flex-direction:column;gap:14px;max-width:880px;text-align:left}
    #tour-card li{font-size:24px;line-height:1.35;display:flex;gap:16px;align-items:baseline}
    #tour-card li b{color:#5eead4;font-weight:600;font-size:22px}
    #tour-caption b{color:#5eead4;font-weight:600;margin-right:8px}`
  const add = () => {
    document.head.appendChild(css)
    const cur = document.createElement('div')
    cur.id = 'tour-cursor'
    cur.innerHTML = '<svg width="22" height="22" viewBox="0 0 22 22"><path d="M3 2 L3 17 L7.2 13.2 L10 19.5 L12.6 18.4 L9.8 12.2 L15.5 12 Z" fill="#fff" stroke="#111" stroke-width="1.4" stroke-linejoin="round"/></svg>'
    const rip = document.createElement('div')
    rip.id = 'tour-ripple'
    const cap = document.createElement('div')
    cap.id = 'tour-caption'
    document.body.append(cur, rip, cap)
    window.addEventListener('mousemove', (e) => { cur.style.left = e.clientX + 'px'; cur.style.top = e.clientY + 'px'; rip.style.left = e.clientX + 'px'; rip.style.top = e.clientY + 'px' }, true)
    window.addEventListener('mousedown', () => { rip.classList.remove('go'); void rip.offsetWidth; rip.classList.add('go') }, true)
  }
  if (document.body) add(); else document.addEventListener('DOMContentLoaded', add)
}

export async function start({ name, width = 1280, height = 720, storage = {}, scrollSelector = 'main' }) {
  const outDir = path.resolve('tour/out')
  fs.mkdirSync(outDir, { recursive: true })
  const tmp = path.join(outDir, `.${name}-raw`)
  fs.rmSync(tmp, { recursive: true, force: true })
  const browser = await chromium.launch({ headless: true })
  const context = await browser.newContext({
    viewport: { width, height },
    recordVideo: { dir: tmp, size: { width, height } },
    colorScheme: 'light',
  })
  await context.grantPermissions(['clipboard-read', 'clipboard-write'], { origin: BASE })
  await context.addInitScript(overlay)
  // Clean, repeatable start: clear storage once per run, then apply any start state the demo needs (for example a theme key).
  await context.addInitScript((st) => { try { if (!sessionStorage.getItem('tour-init')) { localStorage.clear(); for (const [k, v] of Object.entries(st)) localStorage.setItem(k, v); sessionStorage.setItem('tour-init', '1') } } catch { /* ignore */ } }, storage)
  const page = await context.newPage()
  let mouse = { x: 640, y: 360 }

  const tour = {
    page,
    async goto(p = '/') { await page.goto(BASE + p); await page.waitForLoadState('networkidle') },
    async caption(step, text) {
      await page.evaluate(([s, t]) => {
        const c = document.getElementById('tour-caption'); if (!c) return
        c.innerHTML = (s ? `<b>${s}</b>` : '') + t; c.classList.add('on')
      }, [step, text])
    },
    async hideCaption() { await page.evaluate(() => document.getElementById('tour-caption')?.classList.remove('on')) },
    async chapter(num, text, ms = 3200) {
      await page.evaluate(([n, t]) => {
        const c = document.getElementById('tour-chapter'); if (!c) return
        c.innerHTML = `<b>${n}</b>${t}`; c.classList.add('on')
      }, [num, text])
      setTimeout(() => page.evaluate(() => document.getElementById('tour-chapter')?.classList.remove('on')).catch(() => {}), ms)
    },
    async showCard(html) {
      await page.evaluate((h) => {
        document.getElementById('tour-card')?.remove()
        const d = document.createElement('div'); d.id = 'tour-card'; d.innerHTML = h; document.body.appendChild(d)
      }, html)
    },
    async hideCard() {
      await page.evaluate(() => { const d = document.getElementById('tour-card'); if (d) { d.classList.add('fade'); setTimeout(() => d.remove(), 800) } })
    },
    async moveTo(locator, { steps = 28, dx = 0, dy = 0 } = {}) {
      await locator.scrollIntoViewIfNeeded()
      const b = await locator.boundingBox()
      const x = b.x + b.width / 2 + dx, y = b.y + b.height / 2 + dy
      await page.mouse.move(x, y, { steps })
      mouse = { x, y }
    },
    async click(locator, opts) { await tour.moveTo(locator, opts); await sleep(350); await page.mouse.down(); await sleep(80); await page.mouse.up(); await sleep(300) },
    async scrollMain(top, wait = 900) { await page.evaluate(([t, sel]) => document.querySelector(sel)?.scrollTo({ top: t, behavior: 'smooth' }), [top, scrollSelector]); await sleep(wait) },
    async finish(hold = 800) {
      await sleep(hold)
      const video = page.video()
      await context.close()
      const raw = await video.path()
      const out = path.join(outDir, `${name}.webm`)
      fs.copyFileSync(raw, out)
      fs.rmSync(tmp, { recursive: true, force: true })
      await browser.close()
      return out
    },
  }
  return tour
}
