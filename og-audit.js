const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const pages = fs.readdirSync('.').filter(f=>f.endsWith('.html'));
  let bad = 0;
  for (const f of pages) {
    await p.goto('file://' + process.cwd() + '/'+f);
    const m = await p.evaluate(()=>({
      ogi: (document.querySelector('meta[property="og:image"]')||{}).content,
      twi: (document.querySelector('meta[name="twitter:image"]')||{}).content,
      oga: (document.querySelector('meta[property="og:image:alt"]')||{}).content,
      twa: (document.querySelector('meta[name="twitter:image:alt"]')||{}).content,
      t:   (document.querySelector('meta[property="og:title"]')||{}).content,
    }));
    const img = (m.ogi||'').split('/').pop();
    const ok = m.ogi && m.ogi===m.twi && m.oga && m.twa && fs.existsSync(img);
    if(!ok) bad++;
    console.log((ok?'  ✓ ':'  ✗ ') + f.padEnd(22) + (img||'NONE'));
  }
  console.log(bad? `\n  ${bad} page(s) with problems` : '\n  All OG tags consistent, alt text present, files exist ✓');
  await b.close();
})();
