import re
from bs4 import BeautifulSoup
from balance_copy import corrected

ROUTES = {
    '/balance-code-2026-fullversion': '/hpu-hashimoto-code',
    '/balancecode-checkout-full-version': '/hpu-hashimoto-code-checkout',
}

def site_text(text):
    text = corrected(text)
    for old, new in {
        'Juergen Knappich': 'Rieke Knappich',
        'Balance Code': 'HPU und Hashimoto Mentoring',
        'Balance-Code': 'HPU und Hashimoto Mentoring',
        'HPU & Hashimoto Code': 'HPU und Hashimoto Mentoring',
        'Begleiterscheinungen, der HPU': 'Begleiterscheinungen der HPU',
        'unter folgende Symptomen': 'unter folgenden Symptomen',
        '8-Wochen Selbstlernkurs': '8-Wochen-Selbstlernkurs',
        '8 Wochen  Mentoring': '8-Wochen-Mentoring',
        '8 Wochen Mentoring': '8-Wochen-Mentoring',
        'Lebensstil Mentoring': 'Lebensstil-Mentoring',
        'jede Morgen': 'jeden Morgen',
        'Jod-Statusbestimmung .': 'Jod-Statusbestimmung.',
        '(Lebensmittel; Anbieterangaben.': '(Lebensmittel; Anbieterangaben).',
        'bzw Rieke5': 'bzw. Rieke5',
        'NT-RIEKE10 .': 'NT-RIEKE10.',
        'Rezepten und NEMs Empfehlungen': 'Rezepte und NEM-Empfehlungen',
        'du erfährst welche': 'du erfährst, welche',
        'Tipps mit denen': 'Tipps, mit denen',
        'fühlen  dabei': 'fühlen, dabei',
        'schlafe durch .': 'schlafe durch.',
        'Dosierungsanweisungen .': 'Dosierungsanweisungen.',
        'eine Email in der': 'eine E-Mail, in der',
        'diese Email': 'diese E-Mail',
        'eMail-Adressen': 'E-Mail-Adressen',
        'z.B.': 'z. B.',
        'u.v.m.': 'u. v. m.',
        '“Werbung”': '„Werbung“',
        '“Spam”': '„Spam“',
        '“Nachdem': '„Nachdem',
        '"Ich habe': '„Ich habe',
    }.items():
        text = text.replace(old, new)
    from mentoring import mentoring_text
    text = mentoring_text(text)
    text = re.sub(r'(\d)\s*%', lambda m: m[1]+'\u00a0%', text)
    text = re.sub(r'\bbzw(?!\.)(?=\s|$)', 'bzw.', text)
    text = re.sub(r'[ \u00a0]+([.,:;])', r'\1', text)
    text = text.replace('Anbieterangaben.', 'Anbieterangaben).') if '(Lebensmittel;' in text and 'Anbieterangaben).' not in text else text
    return text

def product(s):
    return BeautifulSoup('''<img class="mentoring-mockup" src="/assets/mentoring-mockup.png" width="1080" height="1080" loading="lazy" decoding="async" alt="Selbstlernmaterialien zum HPU und Hashimoto Mentoring: acht Videomodule, Workbook, Tracker, Checklisten und Boni">''', 'html.parser').img

def refine_site(s, route):
    s.head.append(s.new_tag('link', rel='stylesheet', href='/site-design.css?v=4'))
    from mentoring import prepare_mentoring, add_mentoring
    prepare_mentoring(s)
    if route == '/balancecode-checkout-full-version':
        wrapper = s.select_one('#embedable-form-wrapper')
        script = s.select_one('#embedable-form-script')
        if wrapper and script:
            placeholder = BeautifulSoup('<div class="checkout-placeholder" aria-live="polite"><strong>Checkout wird geladen …</strong><span>Sichere Verbindung zu Ablefy</span></div>', 'html.parser').div
            wrapper.insert_before(placeholder)
            observer = BeautifulSoup("""<script>(function(){var p=document.querySelector('.checkout-placeholder'),w=document.getElementById('embedable-form-wrapper');if(!p||!w)return;var done=function(){if(w.children.length){p.hidden=true;obs.disconnect();}};var obs=new MutationObserver(done);obs.observe(w,{childList:true,subtree:true});done();})();</script>""", 'html.parser').script
            wrapper.insert_after(observer)
    for node in list(s.find_all(string=True)):
        if node.parent.name not in ('script', 'style'):
            value = site_text(str(node))
            if value != str(node): node.replace_with(value)
    for el in s.find_all(True):
        for attr in ('alt','title','aria-label','content'):
            if el.has_attr(attr):el[attr] = site_text(el[attr])
        for attr in ('href', 'content'):
            if el.has_attr(attr):
                for old,new in ROUTES.items():el[attr] = el[attr].replace(old,new)
    if route == '/rabatte':
        hero = s.select_one('.section-0')
        if hero:
            visuals = hero.select_one('.visuals')
            if visuals: visuals.decompose()
            hero['class'] = [c for c in hero.get('class', []) if c not in ('with-images','has-backdrop')]
    for img in s.select('img[src="/assets/7a4af6658e21bc5c.png"]'):
        img.replace_with(product(s))
    if route == '/':
        sec=s.select_one('.section-3'); inner=sec.select_one('.section-inner')
        intro=s.new_tag('div', attrs={'class':'symptom-intro'})
        copy=s.new_tag('div'); intro.append(copy)
        cards=s.new_tag('div', attrs={'class':'editorial-grid'})
        current=None
        for node in list(sec.select('.copy .text-block > div > *')):
            if node.name == 'h3':
                current=s.new_tag('article',attrs={'class':'editorial-card'});cards.append(current)
            (current if current is not None else copy).append(node.extract())
        intro.append(sec.select_one('.visuals').extract())
        inner.clear();inner.append(intro);inner.append(cards)
    if route == '/ueber-mich':
        inner=s.select_one('.section-0 .section-inner');copy=s.select_one('.section-0 .copy')
        ps=list(copy.select('p')); lead=s.new_tag('div',attrs={'class':'mentor-lead'})
        leadcopy=s.new_tag('div');lead.append(leadcopy)
        leadcopy.append(copy.select_one('h1').extract())
        for p in ps[:2]:leadcopy.append(p.extract())
        lead.append(inner.select_one('.visuals').extract())
        story=s.new_tag('div',attrs={'class':'mentor-story'})
        starts=['Doch mein Weg hierher','Doch Wissen allein','Und genau das','Und warum ich']
        panel=None
        for p in ps[2:]:
            if panel is None or any(p.get_text().startswith(x) for x in starts):
                panel=s.new_tag('article',attrs={'class':'story-panel'});story.append(panel)
                p.name='h2'
            panel.append(p.extract())
        inner.clear();inner.append(lead);inner.append(story)
        copy=s.select_one('.section-1 .copy');children=list(copy.children)
        grid=s.new_tag('div',attrs={'class':'editorial-grid'})
        for start in [1,3]:
            card=s.new_tag('article',attrs={'class':'editorial-card'})
            for node in children[start:start+2]:card.append(node.extract())
            grid.append(card)
        copy.append(grid)
    if route == '/rabatte':
        for index in [1,2]:
            sec=s.select_one('.section-'+str(index));copy=sec.select_one('.copy')
            images=list(sec.select('.visuals > *'));grid=s.new_tag('div',attrs={'class':'partner-grid'})
            children=list(copy.children);cursor=1 if index==1 else 0
            for image in images:
                card=s.new_tag('article',attrs={'class':'partner-card'});card.append(image.extract())
                while cursor<len(children):
                    node=children[cursor];cursor+=1;card.append(node.extract())
                    if 'action' in node.get('class',[]):break
                grid.append(card)
                # Preserve optional embeds outside the product card sequence.
                while cursor<len(children) and 'embed' in children[cursor].get('class',[]):cursor+=1
            copy.insert(1 if index==1 else 0,grid)
            if index == 1:
                heading = next((h for h in copy.select(':scope > .text-block h3') if 'Alb filter' in h.get_text()), None)
                if heading:
                    card=s.new_tag('article',attrs={'class':'partner-card'})
                    embed=copy.select_one(':scope > .embed')
                    if embed: card.append(embed.extract())
                    node=heading.find_parent(class_='text-block')
                    while node:
                        nxt=node.find_next_sibling()
                        card.append(node.extract())
                        if nxt is None or 'action' in nxt.get('class',[]):
                            if nxt is not None: card.append(nxt.extract())
                            break
                        node=nxt
                    grid.append(card)
            sec.select_one('.visuals').decompose()
            sec['class']=[c for c in sec['class'] if c!='with-images']
        # Keep all shops in one grid so every row shares the same spacing.
        grid = s.select_one('.section-1 .partner-grid')
        last_section = s.select_one('.section-2')
        last_card = last_section.select_one('.partner-card')
        last_card['id'] = last_section['id']
        grid.append(last_card.extract())
        last_section.select_one('.partner-grid').decompose()
        for note in list(last_section.select('.copy > .text-block')):
            s.select_one('.section-1 .copy').append(note.extract())
        last_section.decompose()
    if route == '/wissen' or '/wissen/' in route:
        for card in s.select('.blog-card'):
            h=card.select_one('h1')
            if h:h.name='h2'
    # All pages retain their text; only structural heading levels change.
    if route == '/wissen':
        h=s.new_tag('h1');h.string='Wissen';s.select_one('.copy').insert(0,h)
    for a in s.select('a[href="https://www.hpu-hashimoto/impressum"]'):
        a['href']='/impressum'
    add_mentoring(s, route)
