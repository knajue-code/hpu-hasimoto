import sys,pathlib,re,urllib.parse,json
sys.path.insert(0,'/private/tmp/hpu-python')
from bs4 import BeautifulSoup
from balance_copy import corrected
from site_design import site_text, ROUTES
root=pathlib.Path(__file__).resolve().parents[1];dist=root/'dist';errors=[];blocks=0
norm=lambda t:re.sub(r'\s+([.,:;])',r'\1',re.sub(r'\s+',' ',t)).strip()
for f in (root/'source').glob('*.html'):
 src=BeautifulSoup(f.read_text(),'html.parser');route='/'+f.stem.replace('__','/');route=ROUTES.get(route,route);target=dist/('index.html' if f.stem=='index' else route.strip('/')+'/index.html');out=BeautifulSoup(target.read_text(),'html.parser')
 for art in out.select('.course-art, [data-mentoring-addition]'):art.decompose()
 text=norm(out.select_one('main').get_text(' ',strip=True))
 for el in src.select('main .sqs-html-content,main .list-item-content__title,main .list-item-content__description,main .blog-item-title,main .blog-title,main .blog-excerpt,main .blog-item-meta-wrapper,main .blog-item-author-profile-wrapper'):
  t=norm(site_text(el.get_text(' ',strip=True)));blocks+=bool(t)
  if t and t not in text:errors.append({'page':f.stem,'missing_text':t})
for f in dist.rglob('*.html'):
 s=BeautifulSoup(f.read_text(),'html.parser')
 for a in s.select('[href],img[src],script[src]'):
  u=urllib.parse.urlparse(a.get('href') or a.get('src'))
  if u.netloc or not u.path.startswith('/'):continue
  target=dist/u.path.lstrip('/');target=target if target.suffix else target/'index.html'
  if not target.exists():errors.append({'page':str(f.relative_to(dist)),'missing_file':u.path})
  elif u.fragment and target.suffix=='.html' and not BeautifulSoup(target.read_text(),'html.parser').find(id=u.fragment):errors.append({'page':str(f.relative_to(dist)),'missing_anchor':u.fragment})
for url,path in json.loads((root/'source/assets.json').read_text()).items():
 f=dist/path.lstrip('/')
 if not f.exists() or f.stat().st_size==0:errors.append({'asset':url})
report={'pages':len(list(dist.rglob('*.html'))),'verified_original_text_blocks':blocks,'original_assets':len(json.loads((root/'source/assets.json').read_text())),'errors':errors}
(root/'source/verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));sys.exit(bool(errors))
