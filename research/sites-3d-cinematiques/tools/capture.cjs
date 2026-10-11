// Record a constant-speed wheel scroll through a page.
// Usage: node capture.cjs <url> <outdir> <name> [scrollSeconds=50] [settleMs=5000]
const { chromium } = require(process.env.PW_PATH);
const fs = require('fs');
const path = require('path');

(async () => {
  const [url, outdir, name, secs = '50', settle = '5000', W = '960', H = '540', every = '100'] = process.argv.slice(2);
  const browser = await chromium.launch({
    args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'],
  });
  const vdir = path.join(outdir, name + '_raw');
  fs.mkdirSync(vdir, { recursive: true });
  const ctx = await browser.newContext({ viewport: { width: +W, height: +H }, recordVideo: { dir: vdir, size: { width: +W, height: +H } } });
  const page = await ctx.newPage();
  const logs = [];
  page.on('console', (m) => { if (m.type() === 'error') logs.push('console.error: ' + m.text()); });
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  const t0 = Date.now();
  await page.goto(url, { waitUntil: 'load', timeout: 120000 });
  await page.waitForTimeout(+settle);
  // some sites gate the experience behind a click / enter button
  await page.mouse.move(+W / 2, +H / 2);
  const max = await page.evaluate(() => document.documentElement.scrollHeight - window.innerHeight);
  const vh = +H;
  const steps = Math.round((+secs * 1000) / +every);
  const delta = max / steps;
  const track = [];
  const tStart = Date.now();
  for (let i = 0; i < steps; i++) {
    await page.mouse.wheel(0, delta);
    await page.waitForTimeout(+every);
    if (i % 25 === 0) track.push({ t: (Date.now() - t0) / 1000, y: await page.evaluate(() => window.scrollY) });
  }
  const tEnd = Date.now();
  await page.waitForTimeout(+settle);
  track.push({ t: (Date.now() - t0) / 1000, y: await page.evaluate(() => window.scrollY) });
  const fpsProbe = await page.evaluate(() => new Promise((res) => { let n = 0; const s = performance.now(); const f = () => { n++; if (performance.now() - s < 2000) requestAnimationFrame(f); else res(n / 2); }; requestAnimationFrame(f); }));
  await ctx.close();
  await browser.close();
  const vid = fs.readdirSync(vdir).find((f) => f.endsWith('.webm'));
  fs.renameSync(path.join(vdir, vid), path.join(outdir, name + '.webm'));
  fs.rmSync(vdir, { recursive: true, force: true });
  const meta = { url, maxScroll: max, viewports: +(max / vh).toFixed(2), scrollStartS: (tStart - t0) / 1000, scrollEndS: (tEnd - t0) / 1000, rafFps: fpsProbe, track, logs: logs.slice(0, 20) };
  fs.writeFileSync(path.join(outdir, name + '.json'), JSON.stringify(meta, null, 1));
  console.log(JSON.stringify({ name, maxScroll: max, viewports: meta.viewports, scroll: [meta.scrollStartS, meta.scrollEndS], rafFps: fpsProbe, errors: logs.length }));
})().catch((e) => { console.error(e); process.exit(1); });
