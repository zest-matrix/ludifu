// Regenerates every social card + the logo.
//   cd social-cards && node render.js
// Renders each HTML at 2x in headless Chromium, then writes .jpg + .webp
// into the parent folder. Fonts are LOCAL (Lora / Poppins) — Google Fonts is
// blocked in the build sandbox, so do NOT swap in Cormorant Garamond / Outfit
// unless you first confirm the fetch works.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const path = require('path');

const JOBS = [
  { html: 'og-main.html',    out: 'og-image',   w: 1200, h: 630 },
  { html: 'og-founder.html', out: 'og-founder', w: 1200, h: 630 },
  { html: 'og-careers.html', out: 'og-careers', w: 1200, h: 630 },
  { html: 'logo.html',       out: 'logo',       w: 512,  h: 512, png: true },
];

(async () => {
  const b = await chromium.launch();
  for (const j of JOBS) {
    const p = await b.newPage({ viewport: { width: j.w, height: j.h }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.resolve(j.html));
    await p.waitForTimeout(700);
    await p.screenshot({ path: `.tmp-${j.out}.png` });
    await p.close();

    const py = j.png
      ? `from PIL import Image
im=Image.open('.tmp-${j.out}.png').convert('RGB').resize((${j.w},${j.h}), Image.LANCZOS)
im.save('../${j.out}.png','PNG',optimize=True)`
      : `from PIL import Image
im=Image.open('.tmp-${j.out}.png').convert('RGB').resize((${j.w},${j.h}), Image.LANCZOS)
im.save('../${j.out}.jpg','JPEG',quality=90,optimize=True,progressive=True)
im.save('../${j.out}.webp','WEBP',quality=88,method=6)`;
    execFileSync('python3', ['-c', py], { stdio: 'inherit' });
    console.log('  ✓', j.out);
  }
  await b.close();
  console.log('\n  All cards regenerated. Remember to keep the copy on them in sync with the site.');
})();
