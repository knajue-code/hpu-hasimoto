import sys, pathlib, urllib.request, urllib.parse, json, concurrent.futures
sys.path.insert(0,'/private/tmp/hpu-python')
from bs4 import BeautifulSoup
root=pathlib.Path(__file__).resolve().parents[1]; out=root/'source';out.mkdir(exist_ok=True)
base='https://www.hpu-hashimoto.de'
def fetch(path):
 url=base+path
 try:
  data=urllib.request.urlopen(url,timeout=35).read().decode(); (out/((path.strip('/') or 'index').replace('/','__')+'.html')).write_text(data)
  s=BeautifulSoup(data,'html.parser')
  links={urllib.parse.urlparse(urllib.parse.urljoin(base,a['href'])).path for a in s.select('a[href]') if urllib.parse.urlparse(urllib.parse.urljoin(base,a['href'])).netloc in ['www.hpu-hashimoto.de','hpu-hashimoto.de']}
  print(path, 'sections',len(s.select('main section[data-section-id]')),'links',len(links),flush=True)
  return links
 except Exception as e: print('ERROR',path,str(e),flush=True);return set()
todo={'/'};seen=set()
while todo:
 batch=todo-seen;seen|=batch;todo=set()
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
  for links in pool.map(fetch,sorted(batch)): todo|=links
 todo={p for p in todo-seen if p and not p.startswith(('/cart','/universal','/api')) and '.' not in p and p!='/home'}
 if len(seen)>65:break
(out/'routes.json').write_text(json.dumps(sorted(seen)))
