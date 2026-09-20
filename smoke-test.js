/* Runtime smoke test — loads every page in a real browser and reports JS errors.
   Run:  node smoke-test.js
   This catches what static checks cannot: unclosed <script>, runtime TypeErrors,
   missing functions. An unclosed script tag silently kills ALL JS on a page. */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

(async () => {
  const dir = __dirname;
  const pages = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
  const browser = await chromium.launch();
  let failed = 0;

  for (const file of pages) {
    const p = await browser.newPage();
    const errs = [];
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => {
      const t = m.text();
      if (m.type() === 'error' && !t.includes('ERR_TUNNEL') && !t.includes('net::')) errs.push(t);
    });

    await p.goto('file://' + path.join(dir, file));
    await p.waitForTimeout(350);

    // every onclick/oninput handler must resolve to a real function
    const broken = await p.evaluate(() => {
      const out = [];
      document.querySelectorAll('[onclick],[oninput],[onchange]').forEach(el => {
        ['onclick','oninput','onchange'].forEach(a => {
          const v = el.getAttribute(a);
          if (!v) return;
          const m = v.match(/^\s*([A-Za-z_$][\w$]*)\s*\(/);
          if (m && typeof window[m[1]] !== 'function' && typeof document[m[1]] !== 'function') {
            if (!['document','window','this','try','return'].includes(m[1])) out.push(a + '="' + m[1] + '(...)"');
          }
        });
      });
      return [...new Set(out)];
    });

    const closed = (await p.content()).trim().endsWith('</html>');
    const ok = errs.length === 0 && broken.length === 0 && closed;
    if (!ok) failed++;
    console.log(`  ${ok ? '✓' : '✗'} ${file.padEnd(22)}${ok ? 'clean' : ''}`);
    if (!closed) console.log('      ✗ document does not close with </html> — likely truncated');
    errs.slice(0,3).forEach(e => console.log('      JS: ' + e.split('\n')[0]));
    broken.slice(0,5).forEach(b => console.log('      undefined handler: ' + b));
    await p.close();
  }

  await browser.close();
  console.log(failed ? `\n  ${failed} page(s) with problems` : '\n  All pages clean ✓');
  process.exit(failed ? 1 : 0);
})();
