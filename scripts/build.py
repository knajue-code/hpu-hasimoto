import sys,pathlib,json,hashlib,html,re,urllib.parse
sys.path.insert(0,'/private/tmp/hpu-python')
from bs4 import BeautifulSoup
from balance_design import refine_balance
from site_design import refine_site, ROUTES
ROOT=pathlib.Path(__file__).resolve().parents[1];DIST=ROOT/'dist'; ASSETS={}; corpus={}
def esc(s):return html.escape(str(s),quote=True)
def asset(url):
 url=urllib.parse.urljoin('https://www.hpu-hashimoto.de',url)
 if 'squarespace' in url:
  url=re.sub(r'\?format=[^&]+','',url)
  url+='?format=1500w' if not url.endswith('.ico') else ''
 ext=pathlib.PurePosixPath(urllib.parse.urlparse(url).path).suffix.lower()
 if ext not in ['.jpg','.jpeg','.png','.webp','.svg','.ico','.woff2','.woff','.ttf']:ext='.jpg'
 path='/assets/'+hashlib.sha256(url.encode()).hexdigest()[:16]+ext;ASSETS[url]=path;return path
def href(url):
 u=urllib.parse.urlparse(url)
 if u.netloc in ['www.hpu-hashimoto.de','hpu-hashimoto.de']:url=u.path+('?' +u.query if u.query else '')+('#'+u.fragment if u.fragment else '')
 return {'/home':'/','/hpu-hashimoto-programm':'/balance-code-2026-fullversion'}.get(url,url)
def clean(node):
 if node is None:return ''
 s=BeautifulSoup(str(node),'html.parser')
 for a in s.select('script,style,.visually-hidden,.item-pagination-icon'):a.decompose()
 for a in s.find_all(True):
  a.attrs={k:v for k,v in a.attrs.items() if k in ['href','target','rel','id','title','colspan','rowspan','src','data-src','alt']}
  if a.name=='a':a['href']=href(a.get('href',''));a['rel']='noopener' if a.get('target') else a.get('rel','')
 return str(s)
def img(node):
 url=node.get('data-src') or node.get('src')
 if not url:return ''
 alt=node.get('alt','')
 if not alt and node.parent:alt=node.parent.get('data-image-title','')
 return '<img src="'+asset(url)+'" alt="'+esc(alt)+'" loading="lazy" decoding="async">'
source=BeautifulSoup((ROOT/'source/index.html').read_text(),'html.parser')
logo=asset(source.select_one('.header-title-logo img').get('src'))
favicon=asset(source.select_one('link[rel*="icon"]')['href'])
nav=[('Balance Code','/balance-code-2026-fullversion'),('Wissen','/wissen'),('Über mich','/ueber-mich'),('Rabatte','/rabatte'),('Starter Guide','/hpu-hashimoto-starter-guide')]
footer='<footer><div class="footer-inner"><a class="footer-brand" href="/">HPU &amp; Hashimoto Mentoring</a><nav>'+''.join('<a href="'+p+'">'+t+'</a>' for t,p in [('Impressum','/impressum'),('Datenschutzerklärung','/datenschutz'),('Medizinischer Disclaimer','/disclaimer')])+'</nav><div><a href="mailto:rieke@hpu-hashimoto.de">rieke@hpu-hashimoto.de</a><a href="https://www.instagram.com/hpu.hashimoto/" target="_blank" rel="noopener">Instagram</a></div></div></footer>'
for file in sorted((ROOT/'source').glob('*.html')):
 s=BeautifulSoup(file.read_text(),'html.parser');route='/' if file.stem=='index' else '/'+file.stem.replace('__','/');chunks=[];texts=[]
 header='<a class="skip" href="#page">Zum Inhalt springen</a><header><div class="header-inner"><a href="/" class="brand"><img src="'+logo+'" alt="HPU &amp; Hashimoto Mentoring"></a><button class="menu-toggle" aria-expanded="false" aria-controls="navigation" aria-label="Menü öffnen"><span></span><span></span></button><nav id="navigation">'+''.join('<a '+('aria-current="page" ' if p==route else '')+'class="'+('nav-cta' if t=='Starter Guide' else '')+'" href="'+p+'">'+t+'</a>' for t,p in nav)+'</nav></div></header>'
 for i,sec in enumerate(s.select('main section[data-section-id]')):
  content=[];images=[];theme=sec.get('data-section-theme','');bg=sec.select_one('.section-background img')
  if bg:images.append(img(bg))
  for b in sec.select('.sqs-block'):
   classes=b.get('class',[])
   if 'sqs-block-html' in classes:
    inner=b.select_one('.sqs-html-content') or b.select_one('.sqs-block-content')
    txt=clean(inner)
    if BeautifulSoup(txt,'html.parser').get_text(strip=True):content.append('<div class="text-block">'+txt+'</div>');texts.append(BeautifulSoup(txt,'html.parser').get_text(' ',strip=True))
   elif 'sqs-block-button' in classes:
    a=b.select_one('a[href]')
    if a:content.append('<div class="action"><a class="button" href="'+esc(href(a['href']))+'">'+a.get_text(strip=True)+'</a></div>')
   elif 'sqs-block-image' in classes:
    image=b.select_one('img')
    if image:
     imagehtml=img(image);a=b.select_one('a[href]')
     if a:
      label='Starter Guide' if 'starter-guide' in a['href'] else 'Balance Code' if ('balance' in a['href'] or 'programm' in a['href']) else urllib.parse.unquote_plus(urllib.parse.urlparse(image.get('data-src') or image.get('src')).path.split('/')[-1])
      imagehtml='<a aria-label="'+esc(label)+'" href="'+esc(href(a['href']))+'">'+imagehtml+'</a>'
     images.append(imagehtml)
   elif 'sqs-block-code' in classes or 'sqs-block-embed' in classes:
    container=b.select_one('.sqs-code-container,.sqs-embed-container')
    if container:content.append('<div class="embed">'+''.join(str(x) for x in container.contents)+'</div>')
   elif b.get_text(strip=True):
    content.append('<div class="text-block">'+clean(b.select_one('.sqs-block-content'))+'</div>')
  listing=sec.select_one('.user-items-list')
  if listing:
   title=listing.select_one('.list-section-title');content.append('<div class="quote-title">'+clean(title)+'</div>');cards=[]
   context=listing.select_one('[data-current-context]')
   data=json.loads(context['data-current-context']) if context else {}
   for item in data.get('userItems',[]):
    cards.append('<blockquote>'+item.get('title','')+'<cite>'+item.get('description','')+'</cite></blockquote>')
   content.append('<div class="quotes">'+''.join(cards)+'</div>')
  blogs=sec.select('article.blog-item')
  if blogs:
   cards=[]
   for b in blogs:
    image=b.select_one('img'); title=b.select_one('.blog-title'); excerpt=b.select_one('.blog-excerpt');more=b.select_one('.blog-more-link');meta=b.select_one('.blog-meta-section')
    cards.append('<article class="blog-card">'+(img(image) if image else '')+clean(meta)+clean(title)+clean(excerpt)+clean(more)+'</article>')
   content.append('<div class="blog-grid">'+''.join(cards)+'</div>')
  if (route=='/ueber-mich' and i==0) or (route=='/balance-code-2026-fullversion' and i==1):
   content=[content[-1]]+content[:-1]
  cls='section theme-'+(theme or 'rose')+' section-'+str(i)
  if i==0:cls+=' first-section'
  if bg:cls+=' has-backdrop'
  if images:cls+=' with-images'
  if route in ['/impressum','/datenschutz','/disclaimer']:cls+=' legal'
  if route=='/balance-code-2026-fullversion' and i in [5,6]:cls+=' modules'
  if listing:cls+=' testimonials'
  ident=sec.get('id') or sec.get('data-section-id')
  chunks.append('<section id="'+esc(ident)+'" class="'+cls+'"><div class="section-inner"><div class="copy">'+''.join(content)+'</div>'+('<div class="visuals">'+''.join(images)+'</div>' if images else '')+'</div></section>')
 if '/wissen/' in route:
  b=s.select_one('.blog-item-wrapper') or s.select_one('main')
  title=b.select_one('.blog-item-title'); body=b.select_one('.blog-item-content')
  if body:chunks=['<section class="section legal article-page"><div class="section-inner"><div class="copy">'+clean(title)+'<div class="article-meta">'+clean(b.select_one('.blog-item-meta-wrapper'))+'</div>'+clean(body)+'<div class="article-tags">'+''.join(clean(x) for x in b.select('.blog-item-tag'))+'</div><div class="article-author">'+clean(b.select_one('.blog-item-author-profile-wrapper'))+'</div><nav class="article-pagination">'+''.join(clean(x) for x in s.select('.item-pagination-link'))+'</nav>'+'</div></div></section>']
 if 'starter-guide' in route:
  chunks.append('<script src="https://us-wbe.gr-cdn.com/dynamic/gr-popups.js" defer onload="PopupsRenderer.registerCustomElements()"></script>')
 title=s.title.get_text() if s.title else 'HPU & Hashimoto Mentoring';desc=s.select_one('meta[name="description"]')
 doc='<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'+esc(title)+'</title>'+('<meta name="description" content="'+esc(desc.get('content',''))+'">' if desc else '')+'<link rel="icon" href="'+favicon+'"><link rel="stylesheet" href="/assets/fonts.css"><link rel="stylesheet" href="/style.css?v=balance-design-4"><script src="/app.js" defer></script></head><body class="'+('home' if route=='/' else 'page-'+file.stem)+'">'+header+'<main id="page">'+''.join(chunks)+'</main>'+footer+'</body></html>'
 # Rebuild images in legacy article bodies, removing Squarespace lazy-loader attributes.
 parsed=BeautifulSoup(doc,'html.parser')
 if route=='/balance-code-2026-fullversion':refine_balance(parsed)
 for meta in s.select('meta[property^="og:"],meta[name^="twitter:"]'):
  parsed.head.append(BeautifulSoup(str(meta),'html.parser'))
 for node in parsed.select('img'):
  if not node.get('src','').startswith('/assets/'):
   url=node.get('data-src') or node.get('src')
   if url:node['src']=asset(url)
   for key in list(node.attrs):
    if key not in ['src','alt','loading','decoding']:del node[key]
 refine_site(parsed,route)
 output_route=ROUTES.get(route,route)
 dest=DIST/output_route.strip('/')/'index.html' if output_route!='/' else DIST/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(str(parsed));corpus[route]=texts
 if route in ROUTES:
  legacy=DIST/route.strip('/')/'index.html';legacy.parent.mkdir(parents=True,exist_ok=True)
  legacy.write_text('<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>HPU und Hashimoto Mentoring</title><meta http-equiv="refresh" content="0;url='+output_route+'/"></head><body><a href="'+output_route+'/">HPU und Hashimoto Mentoring</a><script>location.replace('+json.dumps(output_route+'/')+'+location.search+location.hash)</script></body></html>')
(ROOT/'source/assets.json').write_text(json.dumps(ASSETS,indent=2));(ROOT/'source/text-corpus.json').write_text(json.dumps(corpus,ensure_ascii=False,indent=2))
print('Built',len(corpus),'pages;',len(ASSETS),'original assets')

# Preserve existing topic archive navigation using the captured article membership.
for tag in ['hpu','HPU','Symptome']:
 listing=BeautifulSoup((DIST/'wissen/index.html').read_text(),'html.parser')
 for card in listing.select('.blog-card'):
  link=card.select_one('h2 a')
  article=ROOT/'source'/((link['href'].strip('/').replace('/','__'))+'.html') if link else None
  if not article or not article.exists() or ('/wissen/tag/'+tag).lower() not in [a.get('href','').lower() for a in BeautifulSoup(article.read_text(),'html.parser').select('.blog-item-tag')]:card.decompose()
 target=DIST/'wissen/tag'/tag/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(str(listing))

# Standalone tool destination pages intentionally have no navigation entries.
for page in (ROOT/'source/extra-pages').glob('*.html'):
 target=DIST/page.stem/'index.html'
 target.parent.mkdir(parents=True,exist_ok=True)
 target.write_text(page.read_text())
