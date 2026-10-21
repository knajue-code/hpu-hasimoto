"""Reviewed heading hierarchy corrections, applied after page generation."""
from bs4 import BeautifulSoup

CSS = '''
/* Preserve presentation when correcting heading levels. */
main .seo-was-h4 {font-family:var(--heading);font-weight:400;line-height:1.17;font-size:1.3rem;letter-spacing:normal;margin:0 0 28px}
main .editorial-card .seo-was-h4 {font-size:26px;margin:0 0 18px}
main .section-12 .seo-was-h4 {font-size:25px;margin:0 0 20px}
main .partner-card .seo-was-h3 {letter-spacing:normal}
main .seo-was-h3 {font-size:1.65rem;letter-spacing:normal;margin:32px 0 28px}
main .partner-card .seo-was-h3 {font-size:25px;margin:0}
main.article-page .seo-was-h3,.article-page main .seo-was-h3 {border:0;padding-top:0}
@media(max-width:760px){main .seo-was-h3{font-size:1.5rem}main .partner-card .seo-was-h3{font-size:25px}main .section-12 .seo-was-h4{font-size:23px}}
'''

def refine_headings(dist):
    routes = ['index.html','rabatte/index.html','hpu-hashimoto-mentoring/index.html','ueber-mich/index.html','wissen/nahrungsergaenzungsmittel/index.html','wissen/hpu-symptome/index.html','wissen/begleitung/index.html']
    for route in routes:
        path=dist/route
        soup=BeautifulSoup(path.read_text(),'html.parser')
        def rename(h,name):
            h['class']=h.get('class',[])+['seo-was-'+h.name]
            h.name=name
        if route=='index.html':
            for h in soup.main.select('h2'):
                if h.get_text(' ',strip=True).startswith('Mach Schluss damit:'):
                    h.clear();h.string='Dein HPU & Hashimoto Mentoring für mehr Leichtigkeit und Energie'
        elif route=='rabatte/index.html':
            for h in soup.main.select('h3'):rename(h,'h2')
        elif route in ['hpu-hashimoto-mentoring/index.html','ueber-mich/index.html']:
            for h in soup.main.select('h4'):
                rename(h,'p' if h.get_text().startswith('Hi, ich bin Rieke') else 'h3')
        elif route=='wissen/nahrungsergaenzungsmittel/index.html':
            for h in soup.main.select('h2'):
                if h.get_text().startswith('HPU (Hämopyrrollaktamurie)'):
                    h.name='p'
                    title=soup.new_tag('h2');title.string='Mikronährstoffe bei HPU im Überblick';h.insert_before(title)
        else:
            for h in soup.main.select('h3'):
                if h.get_text(' ',strip=True) in ['Dokumentation: So bereitest du dich vor','Fazit']:rename(h,'h2')
        if not soup.select_one('#seo-heading-presentation'):
            style=soup.new_tag('style',id='seo-heading-presentation');style.string=CSS;soup.head.append(style)
        path.write_text(str(soup))
