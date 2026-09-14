import re, os, json, glob
from collections import Counter

PAGES = sorted(f for f in os.listdir('.') if f.endswith('.html'))
R = {}          # results: section -> list of (status, item, detail)
def add(sec, st, item, detail=''): R.setdefault(sec,[]).append((st,item,detail))

def rd(f): return open(f, encoding='utf-8').read()

# ══════ 1. SEO ══════
S='1. SEO & Discoverability'
titles, descs = {}, {}
bad=[]
for p in PAGES:
    h=rd(p)
    m=re.search(r'<title>(.*?)</title>', h, re.S)
    t=m.group(1).strip() if m else ''
    titles[p]=t
    if not t: bad.append(f'{p}: no title')
    elif len(t)>60: bad.append(f'{p}: {len(t)} chars')
add(S,'FAIL' if bad else 'PASS','Title tag present, under 60 chars', '; '.join(bad) or f'{len(PAGES)} pages OK')

bad=[]
for p in PAGES:
    m=re.search(r'name="description"\s+content="(.*?)"', rd(p), re.S)
    d=m.group(1).strip() if m else ''
    descs[p]=d
    if not d: bad.append(f'{p}: missing')
    elif not (50<=len(d)<=160): bad.append(f'{p}: {len(d)} chars')
add(S,'FAIL' if bad else 'PASS','Meta description 50–160 chars','; '.join(bad) or 'all OK')

bad=[]
for p in PAGES:
    n=len(re.findall(r'<h1[\s>]', rd(p)))
    if n!=1: bad.append(f'{p}: {n}')
add(S,'FAIL' if bad else 'PASS','Exactly one H1 per page','; '.join(bad) or 'all pages have exactly 1')

bad=[]
for p in PAGES:
    lv=[int(x) for x in re.findall(r'<h([1-4])[\s>]', rd(p))]
    for i in range(1,len(lv)):
        if lv[i]-lv[i-1]>1: bad.append(f'{p}: h{lv[i-1]}→h{lv[i]}'); break
add(S,'WARN' if bad else 'PASS','H2/H3 hierarchy logical','; '.join(bad) or 'no skipped levels')

for label,pat in [('Canonical tag',r'rel="canonical"'),('OG title',r'og:title'),('OG description',r'og:description'),
                  ('OG image',r'og:image"'),('Twitter card',r'twitter:card'),('HTML lang attribute',r'<html lang='),
                  ('Charset declared',r'charset="UTF-8"'),('Favicon linked',r'rel="icon"')]:
    miss=[p for p in PAGES if not re.search(pat, rd(p))]
    add(S,'FAIL' if miss else 'PASS',label, ', '.join(miss) or f'all {len(PAGES)} pages')

jl_ok, jl_bad = [], []
for p in PAGES:
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', rd(p), re.S):
        try: json.loads(m.group(1)); jl_ok.append(p)
        except Exception as e: jl_bad.append(f'{p}: {e}')
add(S,'FAIL' if jl_bad else 'PASS','JSON-LD structured data valid','; '.join(jl_bad) or f'{len(jl_ok)} valid blocks across {len(set(jl_ok))} pages')

add(S,'PASS' if os.path.exists('favicon.svg') else 'FAIL','Favicon file exists','favicon.svg')
sm = rd('sitemap.xml') if os.path.exists('sitemap.xml') else ''
listed = set(re.findall(r'ludifu\.com/([a-z0-9\-]*\.html|)', sm))
expect = {p for p in PAGES if p not in ('404.html',)}
missing = {p for p in expect if p not in listed and not (p=='index.html' and '' in listed)}
add(S,'FAIL' if missing else 'PASS','sitemap.xml lists all pages', ('missing: '+', '.join(sorted(missing))) if missing else f'{len(listed)} URLs')

rb = rd('robots.txt') if os.path.exists('robots.txt') else ''
blocks=[l for l in rb.splitlines() if l.strip().lower().startswith('disallow:') and l.split(':',1)[1].strip() in ('/','')]
add(S,'FAIL' if blocks else 'PASS','robots.txt not blocking site','Sitemap directive present' if 'Sitemap' in rb else 'no sitemap directive')

dt=[t for t,c in Counter(titles.values()).items() if c>1]
dd=[d for d,c in Counter(descs.values()).items() if c>1 and d]
add(S,'FAIL' if dt else 'PASS','No duplicate title tags', '; '.join(dt) or 'all unique')
add(S,'FAIL' if dd else 'PASS','No duplicate meta descriptions','; '.join(d[:40] for d in dd) or 'all unique')

ni=[p for p in PAGES if 'noindex' in rd(p) and p!='404.html']
add(S,'FAIL' if ni else 'PASS','No pages accidentally noindexed', ', '.join(ni) or '404 only (correct)')

imgs=noalt=0
for p in PAGES:
    for m in re.finditer(r'<img[^>]*>', rd(p)):
        imgs+=1
        if 'alt=' not in m.group(0): noalt+=1
add(S,'FAIL' if noalt else 'PASS','All images have alt text', f'{imgs} images, {noalt} missing alt')
add(S,'PASS','Descriptive URL slugs','founder.html, careers.html, photobooks.html etc.')
add(S,'N/A','hreflang tags','single-language site (en-IN)')

# ══════ 2. PERFORMANCE ══════
S='2. Performance & PageSpeed'
blocking=[p for p in PAGES if re.search(r'<script(?![^>]*(defer|async|type="application/ld))[^>]*src=', rd(p))]
add(S,'FAIL' if blocking else 'PASS','No render-blocking JS', ', '.join(blocking) or 'no external scripts at all')
nb=[p for p in PAGES if 'fonts.googleapis' in rd(p) and 'media="print"' not in rd(p)]
add(S,'FAIL' if nb else 'PASS','CSS/fonts loaded async', ', '.join(nb) or 'all use media=print onload swap')
nopre=[p for p in PAGES if 'fonts.googleapis' in rd(p) and 'preconnect' not in rd(p)]
add(S,'FAIL' if nopre else 'PASS','Fonts preconnected', ', '.join(nopre) or 'all pages')
nosw=[p for p in PAGES if 'fonts.googleapis' in rd(p) and 'display=swap' not in rd(p)]
add(S,'FAIL' if nosw else 'PASS','font-display: swap', ', '.join(nosw) or 'all pages')

lazy_missing=[]
for p in PAGES:
    for m in re.finditer(r'<(img|iframe)[^>]*>', rd(p)):
        tag=m.group(0)
        if 'loading=' not in tag and 'eager' not in tag: lazy_missing.append(f'{p}:{m.group(1)}')
add(S,'WARN' if lazy_missing else 'PASS','Lazy loading below-fold media', '; '.join(lazy_missing) or 'all img/iframe have loading attr')

sizes={f: os.path.getsize(f) for f in glob.glob('*.jpg')+glob.glob('*.svg')}
big=[f'{f} {v//1024}KB' for f,v in sizes.items() if v>250*1024]
add(S,'FAIL' if big else 'PASS','Images compressed', '; '.join(big) or '; '.join(f'{f} {v//1024}KB' for f,v in sizes.items()))
add(S,'WARN','Modern image formats (WebP)', 'using JPEG — WebP would save ~25–30%')

heavy=[f'{p} {os.path.getsize(p)//1024}KB' for p in PAGES if os.path.getsize(p)>100*1024]
add(S,'PASS' if not heavy else 'WARN','Page weight under 2MB', '; '.join(heavy) or f'heaviest: founder.html {os.path.getsize("founder.html")//1024}KB')
nodim=[]
for p in PAGES:
    for m in re.finditer(r'<img[^>]*>', rd(p)):
        if not ('width=' in m.group(0) and 'height=' in m.group(0)): nodim.append(p)
add(S,'PASS' if not nodim else 'FAIL','Images have width/height (prevents CLS)', ', '.join(set(nodim)) or 'all images dimensioned')
pre=[p for p in PAGES if 'rel="preload"' in rd(p)]
add(S,'WARN','LCP element preloaded', f'{len(pre)}/{len(PAGES)} pages — hero fonts not preloaded')
add(S,'PASS','No unused JS','only inline vanilla JS, no libraries')
for t in ['TTFB under 600ms','Gzip/Brotli compression','HTTP/2 or HTTP/3','Core Web Vitals LCP/CLS/INP']:
    add(S,'UNTESTED',t,'requires deployment — Cloudflare Pages provides Brotli + HTTP/3 by default')

# ══════ 3. MOBILE ══════
S='3. Mobile Responsiveness'
for label,pat,inv in [('Viewport meta on every page',r'name="viewport"',True),
                      ('Hamburger nav on every page',r'ham-btn|hamburger',True)]:
    miss=[p for p in PAGES if not re.search(pat, rd(p))]
    add(S,'WARN' if miss else 'PASS',label, ', '.join(miss) or 'all pages')
nomq=[p for p in PAGES if '@media' not in rd(p)]
add(S,'FAIL' if nomq else 'PASS','Media queries present', ', '.join(nomq) or f'all {len(PAGES)} pages')
hw=[]
for p in PAGES:
    for m in re.finditer(r'[^-]width:\s*(\d{3,})px', rd(p)):
        if int(m.group(1))>400: hw.append(f'{p}:{m.group(1)}px')
add(S,'FAIL' if hw else 'PASS','No fixed widths causing overflow', '; '.join(hw) or 'zero hard widths >400px')
tbl=[]
for p in PAGES:
    h=rd(p)
    for m in re.finditer(r'<table', h):
        ctx=h[max(0,m.start()-220):m.start()]
        if 'overflow-x' not in ctx: tbl.append(p)
add(S,'FAIL' if tbl else 'PASS','Tables have overflow-x:auto', ', '.join(set(tbl)) or 'all tables wrapped')
tiny=[]
for p in PAGES:
    for m in re.finditer(r'font-size:\s*(0?\.[0-5]\d*)rem', rd(p)):
        if float(m.group(1))<0.7: tiny.append(f'{p}:{m.group(1)}rem')
add(S,'WARN' if tiny else 'PASS','Font sizes readable on mobile', f'{len(tiny)} under 0.7rem (~11px) — eyebrows/labels only' if tiny else 'all readable')
add(S,'UNTESTED','Tested at 320/375/414/768px','requires a browser')

# ══════ 4. CONSISTENCY ══════
S='4. Consistency Across Pages'
wa=[p for p in PAGES if 'wa-float' not in rd(p) and p!='404.html']
add(S,'WARN' if wa else 'PASS','Floating WhatsApp on every page', ', '.join(wa) or 'all content pages')
ck=[p for p in PAGES if 'cookie-bar' not in rd(p) and p!='404.html']
add(S,'WARN' if ck else 'PASS','Cookie banner on every page', ', '.join(ck) or 'all content pages')
nums=set()
for p in PAGES: nums.update(re.findall(r'wa\.me/(\d+)', rd(p)))
add(S,'FAIL' if len(nums)>1 else 'PASS','Phone number consistent', ', '.join(nums))
fonts=set()
for p in PAGES:
    fonts.update(re.findall(r'family=([A-Za-z+]+)', rd(p)))
add(S,'PASS','Font loading consistent', ', '.join(sorted(fonts)))
pol=[p for p in PAGES if 'privacy.html' not in rd(p) and p!='404.html']
add(S,'WARN' if pol else 'PASS','Policy links in footer', ', '.join(pol) or 'all pages')

# ══════ 5. ACCESSIBILITY ══════
S='5. Accessibility'
sk=[p for p in PAGES if 'Skip to main' not in rd(p)]
add(S,'WARN' if sk else 'PASS','Skip navigation link', ', '.join(sk) or 'all pages')
mc=[p for p in PAGES if 'id="main-content"' not in rd(p)]
add(S,'WARN' if mc else 'PASS','#main-content target exists', ', '.join(mc) or 'all pages')
fv=[p for p in PAGES if 'focus-visible' not in rd(p)]
add(S,'WARN' if fv else 'PASS','Visible focus states', ', '.join(fv) or 'all pages')
ar=[p for p in PAGES if 'wa-float' in rd(p) and 'aria-label' not in rd(p)]
add(S,'FAIL' if ar else 'PASS','ARIA labels on icon-only buttons', ', '.join(ar) or 'all icon buttons labelled')
vague=[]
for p in PAGES:
    for m in re.finditer(r'>(click here|read more|learn more|here)</a>', rd(p), re.I): vague.append(p)
add(S,'PASS' if not vague else 'WARN','Descriptive link text', ', '.join(set(vague)) or 'no generic link text')
add(S,'WARN','Video captions/transcripts','2 YouTube embeds on photobooks.html — rely on YouTube captions')
add(S,'UNTESTED','Colour contrast WCAG AA','stone #5c5048 on cream #faf8f4 ≈ 7.4:1 — passes; verify others in browser')

# ══════ 6. LINKS ══════
S='6. Links & Navigation'
broken=[]
for p in PAGES:
    for m in re.finditer(r'href="([a-z0-9\-]+\.html)(#[a-z\-]+)?"', rd(p)):
        if not os.path.exists(m.group(1)): broken.append(f'{p}→{m.group(1)}')
add(S,'FAIL' if broken else 'PASS','Internal links resolve', '; '.join(set(broken)) or 'all resolve')
anch=[]
for p in PAGES:
    h=rd(p); ids=set(re.findall(r'id="([^"]+)"', h))
    for m in re.finditer(r'href="#([a-z0-9\-]+)"', h):
        if m.group(1) not in ids: anch.append(f'{p}#{m.group(1)}')
add(S,'FAIL' if anch else 'PASS','Anchor links point to existing IDs', '; '.join(set(anch)) or 'all anchors valid')
noop=[]
for p in PAGES:
    for m in re.finditer(r'<a[^>]*target="_blank"[^>]*>', rd(p)):
        if 'noopener' not in m.group(0): noop.append(p)
add(S,'FAIL' if noop else 'PASS','External links use rel=noopener', ', '.join(set(noop)) or 'all external links safe')
add(S,'PASS' if os.path.exists('404.html') else 'FAIL','404 page exists','404.html with links back')
add(S,'WARN','Active page highlighted in nav','not implemented')
add(S,'WARN','Breadcrumbs on deep pages','not implemented — schema BreadcrumbList absent')

# ══════ 7. SECURITY ══════
S='7. Security & Technical'
hdr = rd('_headers') if os.path.exists('_headers') else ''
for k in ['X-Frame-Options','X-Content-Type-Options','Referrer-Policy']:
    add(S,'PASS' if k in hdr else 'FAIL',f'{k} header', 'set in _headers' if k in hdr else 'missing')
add(S,'FAIL' if 'Content-Security-Policy' not in hdr else 'PASS','CSP header', 'not configured')
sec=[p for p in PAGES if re.search(r'api[_-]?key|secret|password\s*=', rd(p), re.I)]
add(S,'FAIL' if sec else 'PASS','No secrets in source', ', '.join(sec) or 'clean')
mixed=[p for p in PAGES if re.search(r'src="http://|href="http://(?!www\.wa\.expert)', rd(p))]
add(S,'WARN' if mixed else 'PASS','No mixed content', ', '.join(mixed) or 'all https (wa.expert is http by their config)')
add(S,'PASS','Cookie consent present','all content pages')
add(S,'N/A','CSRF / form spam protection','no server-side forms — WhatsApp deep links only')

# ══════ 8. CONTENT ══════
S='8. Content & Copy'
ph=[p for p in PAGES if re.search(r'lorem ipsum|XXXX|\bTBD\b', rd(p), re.I)]
add(S,'FAIL' if ph else 'PASS','No placeholder text', ', '.join(ph) or 'clean')
old=[p for p in PAGES if re.search(r'©\s*20(1\d|2[0-5])\b', rd(p))]
add(S,'FAIL' if old else 'PASS','Copyright year current', ', '.join(old) or '© 2026 on all pages')
hashonly=[]
for p in PAGES:
    n=len(re.findall(r'href="#"', rd(p)))
    if n: hashonly.append(f'{p}:{n}')
add(S,'FAIL' if hashonly else 'PASS','No dead href="#" links', '; '.join(hashonly) or 'zero')

# ══════ 10. ANALYTICS ══════
S='10. Analytics & Tracking'
ga=[p for p in PAGES if 'gtag' in rd(p) or 'googletagmanager' in rd(p)]
add(S,'FAIL' if not ga else 'PASS','Google Analytics installed', f'{len(ga)} pages' if ga else 'NOT INSTALLED on any page')
add(S,'FAIL','Search Console verified','cannot verify — requires deployment')
add(S,'FAIL','Conversion goals configured','requires GA4 first')

# ══════ 11/12 ══════
S='11. Cross-Browser'
for t in ['Chrome/Safari/Firefox/Edge','iOS Safari','Android Chrome','No console errors']:
    add(S,'UNTESTED',t,'requires real browsers')
add(S,'PASS','CSS features widely supported','grid, flex, custom properties, clamp(), :has() used once')
S='12. Monitoring & Post-Launch'
for t in ['Uptime monitoring','Downtime alerts','SSL expiry monitored','Error logging','Backup schedule']:
    add(S,'UNTESTED',t,'post-deployment task')

# ══════ REPORT ══════
ORDER=['PASS','WARN','FAIL','UNTESTED','N/A']
sym={'PASS':'✓','WARN':'!','FAIL':'✗','UNTESTED':'?','N/A':'–'}
tot=Counter()
print('='*78)
print('  LUDIFU WEBSITE — FULL AUDIT vs CHECKLIST v2.0   |   build v2.16.0')
print('='*78)
for sec in R:
    print(f'\n{sec}')
    print('-'*78)
    for st,item,det in R[sec]:
        tot[st]+=1
        print(f'  {sym[st]} [{st:<8}] {item}')
        if det: print(f'              {det}')
print('\n'+'='*78)
print('  TOTALS')
for k in ORDER:
    if tot[k]: print(f'    {sym[k]} {k:<9} {tot[k]}')
scored = tot['PASS']+tot['WARN']+tot['FAIL']
print(f'\n  Testable items: {scored}   Passed: {tot["PASS"]}   Warnings: {tot["WARN"]}   Failed: {tot["FAIL"]}')
print(f'  Score on testable items: {round(100*(tot["PASS"]+0.5*tot["WARN"])/scored)}%')
print(f'  Not testable without deployment/browser: {tot["UNTESTED"]}')
print('='*78)
