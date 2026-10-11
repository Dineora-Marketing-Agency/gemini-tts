const { chromium } = require(process.env.PW_PATH);
(async () => {
  const [url, w, h] = process.argv.slice(2);
  const b = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const p = await (await b.newContext({ viewport: { width: +w, height: +h } })).newPage();
  const t0 = Date.now();
  await p.goto(url, { waitUntil: 'load', timeout: 120000 });
  await p.waitForTimeout(5000);
  const fps = await p.evaluate(() => new Promise((res) => { let n = 0; const s = performance.now(); const f = () => { n++; if (performance.now() - s < 3000) requestAnimationFrame(f); else res(n / 3); }; requestAnimationFrame(f); }));
  const gl = await p.evaluate(() => { const c = document.createElement('canvas'); const g = c.getContext('webgl2'); return g ? g.getParameter(g.RENDERER) : 'no webgl2'; });
  const max = await p.evaluate(() => document.documentElement.scrollHeight - innerHeight);
  await p.screenshot({ path: 'rec/probe.png' });
  console.log(JSON.stringify({ url, w, h, fps, gl, max, loadS: (Date.now() - t0) / 1000 }));
  await b.close();
})();
