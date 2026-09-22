"""Approved September 2026 offer: personal mentoring plus self-study materials."""
import re
from bs4 import BeautifulSoup

REPLACEMENTS = {
    'Der HPU und Hashimoto Mentoring': 'Das HPU und Hashimoto Mentoring',
    'Das HPU und Hashimoto Mentoring:': 'Das HPU & Hashimoto Mentoring:',
    'der HPU und Hashimoto Mentoring': 'das HPU und Hashimoto Mentoring',
    'den HPU und Hashimoto Mentoring': 'das HPU und Hashimoto Mentoring',
    'zum HPU und Hashimoto Mentoring': 'Zum HPU und Hashimoto Mentoring',
    '8-Wochen-Selbstlernkurs': '8-Wochen-Mentoring mit zwei persönlichen 1:1-Sessions à 90 Minuten und ergänzenden Selbstlern-Tools',
    'Mit meinem klar aufgebauten 8-Wochen-Programm, mit dem du die Zusammenhänge in deinem Körper verstehst, Struktur in deine nächsten Schritte bringst und dir einen alltagstauglichen Werkzeugkasten aufbaust – ohne Druck, dafür mit System.':
        'In meinem 8-Wochen-Mentoring verbindest du persönliche 1:1-Begleitung mit Selbstlern-Tools: Zwei Mentoring-Sessions à 90 Minuten, Videos, ein Workbook, Checklisten und Tracker helfen dir, Wissen in deinen Alltag zu bringen – in deinem Tempo und mit klaren nächsten Schritten.',
    'Aktuell ist das HPU und Hashimoto Mentoring ein Selbstlernprogramm . Du kannst sofort loslegen und in deinem Tempo arbeiten.':
        'Ja. Du bekommst zwei persönliche 1:1-Mentoring-Sessions à 90 Minuten mit mir. Gemeinsam besprechen wir deine Fragen und nächsten Schritte. Ergänzend arbeitest du mit den Videos und Selbstlern-Tools in deinem eigenen Tempo.',
    'Aktuell ist es ein Selbstlernprogramm. Ein Gruppenmentoring ist zukünftig geplant und kann dann hinzugebucht werden.':
        'Ja. Zwei persönliche 1:1-Mentoring-Sessions à 90 Minuten mit mir sind im Gesamtpreis enthalten. Der gemeinsame Wert der beiden Sessions beträgt 450 €. Die Videos, Checklisten und Tracker nutzt du ergänzend in deinem eigenen Tempo.',
    'Plane lieber klein und realistisch. Du bekommst Tools und Tracker, um die Umsetzung in deinen Alltag einzubauen. Die meisten Videos dauern 20–30 Minuten.':
        'Plane lieber klein und realistisch. Die meisten Videos dauern 20–30 Minuten. Tools und Tracker helfen dir bei der Umsetzung im Alltag. Plane zusätzlich Zeit für deine zwei persönlichen Mentoring-Sessions à 90 Minuten ein.',
    'Genau dahin führt dich der ': 'Genau dahin führt dich das ',
    'Der Kurs ist so gedacht, dass er': 'Das Mentoring ist so gedacht, dass es',
    'du 1:1 medizinische Behandlung im Kursformat suchst (der Kurs ersetzt keine ärztliche Betreuung)':
        'du eine medizinische Behandlung suchst (auch das persönliche Mentoring ersetzt keine ärztliche Betreuung)',
    'Ersetzt der Kurs eine ärztliche Behandlung?': 'Ersetzt das Mentoring eine ärztliche Behandlung?',
    'Nein. Der Kurs ist ein edukatives Programm zur Wissensvermittlung und Selbstorganisation und ersetzt keine medizinische Diagnose oder Therapie.':
        'Nein. Das Mentoring verbindet persönliche Begleitung mit Wissensvermittlung und Selbstorganisation. Es ersetzt keine medizinische Diagnose oder Therapie.',
}

def mentoring_text(text):
    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)
    text = text.replace('HPU und Hashimoto Mentoring', 'HPU & Hashimoto Mentoring')
    text = text.replace('Dann ist  das HPU & Hashimoto Mentoring - das 8-Wochen-Mentoring bei HPU & Hashimoto - dein Weg zu mehr Energie, Stabilität und Leichtigkeit genau das Richtige für dich:', 'Das HPU & Hashimoto Mentoring verbindet persönliche Begleitung mit einem Selbstlernkurs über acht Wochen – für mehr Orientierung, Struktur und alltagstaugliche nächste Schritte.')
    text = text.replace('Ein 8-Wochen-Mentoring mit zwei persönlichen 1:1-Sessions à 90 Minuten und ergänzenden Selbstlern-Tools, in dem du Kompass und Karte erhältst, um aus dem HPU & Hashimoto Dschungel zu finden.', 'Du bekommst zwei persönliche 1:1-Mentoring-Sessions à 90 Minuten mit mir. Ergänzend unterstützt dich der Selbstlernkurs mit acht Videomodulen, Workbook, Checklisten und Trackern dabei, das Wissen in deinem eigenen Tempo umzusetzen.')
    return re.sub(r'\b497(?=[\s\u00a0]*€)', '997', text)

def prepare_mentoring(s):
    # This answer spans bold markup in the original. Consolidate only its body.
    for p in s.select('p'):
        if 'Aktuell ist der Balance Code ein' in p.get_text(' ', strip=True):
            heading = p.find('strong').extract()
            p.clear(); p.append(heading); p.append(s.new_tag('br'))
            p.append('Aktuell ist das HPU und Hashimoto Mentoring ein Selbstlernprogramm . Du kannst sofort loslegen und in deinem Tempo arbeiten.')

def fragment(html):
    return BeautifulSoup(html, 'html.parser').find()

def add_mentoring(s, route):
    for link in s.select('#navigation a[href="/hpu-hashimoto-mentoring"]'):
        link.string = 'Mentoring'
    if route == '/':
        section = s.select_one('.section-2')
        heading = section.select_one('h2').extract()
        section.select_one('.section-inner').insert(0, heading)
        heading['class'] = ['hpu-symptoms-heading']
        body = section.select_one('.text-block:nth-child(2) > div')
        symptoms = s.new_tag('ul', attrs={'class': 'hpu-symptoms-list'})
        for paragraph in list(body.find_all('p', recursive=False)):
            text = paragraph.get_text(' ', strip=True)
            if not text:
                paragraph.decompose()
            elif not text.startswith('Hinweis:'):
                item = s.new_tag('li')
                item.append(paragraph.extract()); symptoms.append(item)
            else:
                paragraph['class'] = ['hpu-symptoms-note']
        body.insert(0, symptoms)
        section.select_one('.text-block').decompose()
        from site_design import product
        s.select_one('.section-1 .visuals img').replace_with(product(s))
    if route != '/balance-code-2026-fullversion':
        return
    benefits = s.select_one('.section-4 .text-block p:nth-of-type(2)')
    benefits.insert_after(fragment('<p data-mentoring-addition="true">✅ <strong>persönliches 1:1-Mentoring mit mir</strong>: zwei Sessions à 90 Minuten im gemeinsamen Wert von 450 € – für deine Fragen und deine nächsten Schritte</p>'))
    intro = s.select_one('.bc-module-intro-copy')
    intro.append(fragment('''<div class="mentoring-session-card" data-mentoring-addition="true"><span class="mentoring-kicker">Persönlich begleitet</span><h3>Dein 1:1-Mentoring mit mir</h3><p><strong>2 × 90 Minuten · Wert insgesamt 450 €</strong></p><p>In zwei persönlichen Einzelterminen besprechen wir deine Fragen und entwickeln klare nächste Schritte für deinen Alltag. Die acht Videomodule, das Workbook, Checklisten und Tracker ergänzen unsere Gespräche als Selbstlern-Tools.</p></div>'''))
    module_heading = s.new_tag('div', attrs={'class': 'mentoring-modules-heading'})
    for paragraph in list(intro.find_all('p', recursive=False)):
        module_heading.append(paragraph.extract())
    title = module_heading.find('strong')
    if title:
        title.name = 'h3'
        module_heading.insert(0, title.extract())
    s.select_one('.bc-module-grid').insert_before(module_heading)
    offer = s.select_one('.bc-offer ul')
    offer.insert(0, fragment('<li data-mentoring-addition="true"><p><strong>2 persönliche 1:1-Mentoring-Sessions à 90 Minuten mit mir</strong><br>Gemeinsamer Wert: 450 € · im Gesamtpreis enthalten</p></li>'))
    s.select_one('.bc-offer h2').insert_after(fragment('<p class="mentoring-offer-summary" data-mentoring-addition="true">Persönliche Begleitung und Selbstlern-Tools in einem Angebot.</p>'))
    for button in s.select('a.button'):
        if button.get('href', '').rstrip('/') == '/hpu-hashimoto-code-checkout':
            button['href'] = 'https://hpu-hashimoto.my-ablefy.com/s/hpu-hashimoto/mentoring/payment'
            button['target'] = '_blank'
            button['rel'] = ['noopener', 'noreferrer']
        if 'HPU & Hashimoto Mentoring' in button.get_text():
            button.string = 'Mentoring für 997 € sichern' if '997' in button.get_text() else 'Jetzt Mentoring sichern'
