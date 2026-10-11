// Deterministic scroll capture: jump to N evenly spaced scroll positions, let the frame settle, screenshot.
// Usage: node stepcap.cjs <url> <outdir> <name> [N=48] [waitMs=2500] [W=960] [H=540] [preClickSelector]
const { chromium } = require(process.env.PW_PATH);
const fs = require('fs');
const path = require('path');

(async () => {
  const [url, outdir, name, N = '48', wait = '2500', W = '960', H = '540', click = ''] = process.argv.slice(2);
  const dir = path.join(outdir, name + '_steps');
  fs.mkdirSync(dir, { recursive: true });
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required'] });
  const page = await (await browser.newContext({ viewport: { width: +W, height: +H } })).newPage();
  const logs = [];
  page.on('pageerror', (e) => logs.push('pageerror: ' + e.message));
  await page.goto(url, { waitUntil: 'load', timeout: 120000 });
  await page.waitForTimeout(7000);
  if (click) { try { await page.click(click, { timeout: 5000 }); await page.waitForTimeout(3000); } catch (e) { logs.push('click failed: ' + click); } }
  const max = await page.evaluate(() => document.documentElement.scrollHeight - window.innerHeight);
  const rows = [];
  for (let i = 0; i < +N; i++) {
    const y = Math.round((max * i) / (+N - 1));
    await page.evaluate((y) => {
      // drive both native scroll and Lenis if the page exposes one
      window.scrollTo(0, y);
      if (window.lenis && window.lenis.scrollTo) window.lenis.scrollTo(y, { immediate: true, force: true });
    }, y);
    await page.waitForTimeout(+wait);
    const f = path.join(dir, String(i).padStart(3, '0') + '.png');
    await page.screenshot({ path: f });
    rows.push({ i, y, progress: +(y / max).toFixed(4), vh: +(y / +H).toFixed(3), actualY: await page.evaluate(() => window.scrollY) });
  }
  await browser.close();
  fs.writeFileSync(path.join(outdir, name + '_steps.json'), JSON.stringify({ url, max, viewports: +(max / +H).toFixed(2), N: +N, rows, logs }, null, 1));
  console.log(JSON.stringify({ name, max, viewports: +(max / +H).toFixed(2), N: +N, errors: logs }));
})().catch((e) => { console.error(e); process.exit(1); });
