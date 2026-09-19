from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element, SubElement, tostring
BASE = 'https://hpu-hashimoto.de'
PAGES = {
'/': ('HPU & Hashimoto Mentoring mit Rieke Knappich', 'Persönliche Begleitung bei HPU und Hashimoto: Entdecke das Mentoring mit Rieke Knappich, verständliches Wissen und praktische Hilfen für deinen Alltag.'),
'/hpu-hashimoto-code/': ('HPU & Hashimoto Mentoring – 8 Wochen mit Rieke Knappich', 'Persönliches HPU & Hashimoto Mentoring: 8 Wochen mit zwei 1:1-Terminen à 90 Minuten, acht Videomodulen, Checklisten und Trackern. Jetzt informieren.'),
'/hpu-hashimoto-starter-guide/': ('Kostenloser HPU & Hashimoto Starter Guide', 'Dein Einstieg ins Thema HPU und Hashimoto: Fordere den kostenlosen Starter Guide an und erhalte verständliche Informationen für deine ersten Schritte.'),
'/ueber-mich/': ('Über Rieke Knappich | HPU & Hashimoto Mentoring', 'Lerne Rieke Knappich kennen: ihre persönlichen Erfahrungen mit HPU und Hashimoto und ihren Ansatz für die Begleitung im Mentoring.'),
'/rabatte/': ('Partner-Rabatte | HPU & Hashimoto', 'Entdecke ausgewählte Partner-Shops und Rabattcodes von Rieke Knappich. Alle Angebote und Links findest du hier im Überblick.'),
'/wissen/': ('Wissen zu HPU & Hashimoto | Rieke Knappich', 'Artikel von Rieke Knappich zu HPU und Hashimoto: Informationen über Symptome, Mikronährstoffe und persönliche Begleitung im Alltag.'),
'/wissen/hpu-symptome/': ('HPU: Symptome und Zusammenhänge | Rieke Knappich', 'Welche Beschwerden werden mit HPU in Verbindung gebracht? Erfahre mehr über mögliche Symptome und Zusammenhänge in diesem Wissensartikel.'),
'/wissen/begleitung/': ('Persönliche Begleitung bei HPU | Rieke Knappich', 'Warum kann persönliche Begleitung bei HPU hilfreich sein? Ein Wissensartikel über Orientierung, individuelle Schritte und Unterstützung im Alltag.'),
'/wissen/nahrungsergaenzungsmittel/': ('Mikronährstoffe bei HPU: Orientierung | Rieke Knappich', 'Orientierung zum Thema Mikronährstoffe bei HPU: Erfahre mehr über Nahrungsergänzungsmittel und die Bedeutung einer individuell abgestimmten Vorgehensweise.'),
'/datenschutz/': ('Datenschutzerklärung | HPU & Hashimoto', 'Informationen zum Datenschutz bei HPU & Hashimoto: Website, Newsletter, GetResponse, Bestellabwicklung und deine Rechte.'),
'/impressum/': ('Impressum | HPU & Hashimoto', 'Anbieterkennzeichnung und Kontaktdaten von Ulrike Knappich für die Website HPU & Hashimoto.'),
'/disclaimer/': ('Medizinischer Hinweis | HPU & Hashimoto', 'Hinweise zu den Grenzen der Informationen und Angebote von HPU & Hashimoto. Die Inhalte ersetzen keine medizinische Beratung oder Behandlung.')
}
def apply_seo(dist):
    urls=[]
    for path in dist.rglob('*.html'):
        s=BeautifulSoup(path.read_text(),'html.parser')
        if not s.head or not s.main:continue
        route='/' + str(path.parent.relative_to(dist)).strip('.') .strip('/') + '/'
        if route=='//':route='/'
        indexable=route in PAGES and route not in ['/datenschutz/','/impressum/','/disclaimer/']
        def meta(key,value,attr='name'):
            for old in s.head.find_all('meta',attrs={attr:key}):old.decompose()
            s.head.append(s.new_tag('meta',attrs={attr:key,'content':value}))
        if route in PAGES:title,description=PAGES[route]
        elif route.startswith('/wissen/tag/'):
            tag=route.rstrip('/').split('/')[-1]
            title=f'Artikel zum Thema {tag.upper() if tag.lower()=="hpu" else tag} | HPU & Hashimoto'
            description=f'Wissensartikel zum Thema {tag}: Beiträge von Rieke Knappich im Überblick.'
        elif route.startswith('/confirm'):
            title=s.title.get_text();description='Bestätigung deiner Anmeldung oder Bestellung bei HPU & Hashimoto.'
        else:title='Zum Mentoring-Checkout | HPU & Hashimoto';description='Weiter zur Buchung des HPU & Hashimoto Mentorings bei Ablefy.'
        if s.title:s.title.string=title
        meta('description',description);meta('robots','index,follow' if indexable else 'noindex,follow')
        for tag in s.select('link[rel="canonical"]'):tag.decompose()
        s.head.append(s.new_tag('link',rel='canonical',href=BASE+route))
        for k,v in [('og:title',title),('og:description',description),('og:url',BASE+route),('og:locale','de_DE')]:meta(k,v,'property')
        for k,v in [('twitter:title',title),('twitter:description',description),('twitter:url',BASE+route)]:meta(k,v)
        path.write_text(str(s))
        if indexable:urls.append(BASE+route)
    root=Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for url in sorted(urls):SubElement(SubElement(root,'url'),'loc').text=url
    (dist/'sitemap.xml').write_bytes(tostring(root,encoding='utf-8',xml_declaration=True))
    (dist/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
