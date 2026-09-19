import pathlib,json,subprocess,concurrent.futures,urllib.parse,re,hashlib
root=pathlib.Path(__file__).resolve().parents[1]
def get(pair):
 url,path=pair; dest=root/'dist'/path.lstrip('/');dest.parent.mkdir(parents=True,exist_ok=True)
 if dest.exists() and dest.stat().st_size:return
 url=urllib.parse.quote(url,safe=':/?=&%+')
 p=subprocess.run(['curl','-sS','-L','--fail','--retry','2','--max-time','45',url,'-o',str(dest)],capture_output=True)
 print(('OK ' if p.returncode==0 else 'ERROR ')+path,flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(get,json.loads((root/'source/assets.json').read_text()).items()))
url='https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Marcellus&family=PT+Serif&display=swap'
p=subprocess.run(['curl','-sS','-L','--fail',url],capture_output=True,text=True);css=p.stdout
for url in set(re.findall(r'url\((https[^)]+)\)',css)):
 path='/assets/font-'+hashlib.sha256(url.encode()).hexdigest()[:12]+'.woff2';get((url,path));css=css.replace(url,path)
(root/'dist/assets/fonts.css').write_text(css)
