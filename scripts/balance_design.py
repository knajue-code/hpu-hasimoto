import re
from pathlib import Path
from PIL import Image
from balance_copy import correct_page

def refine_balance(s):
    s.head.append(s.new_tag('link', rel='stylesheet', href='/balance-spacing.css?v=2'))
    for picture in s.select('img[src^="/assets/"]'):
        file=Path(__file__).resolve().parents[1]/'dist'/picture['src'].lstrip('/')
        if file.exists():
            with Image.open(file) as image:picture['width'],picture['height']=map(str,image.size)
    hero=s.select_one('.section-0')
    hero['class'].append('bc-hero')
    headings=hero.select('h1')
    headings[0].name='p';headings[0]['class']=['bc-eyebrow']
    for h in hero.select('h3'):
        h.name='p';h['class']=['bc-intro-text']
    hero.select_one('img')['loading']='eager'
    hero.select_one('img')['fetchpriority']='high'

    section=s.select_one('.section-5');section['class'].append('bc-curriculum')
    inner=section.select_one('.section-inner')
    block=section.select_one('.text-block > div')
    intro=s.new_tag('div',attrs={'class':'bc-module-intro'})
    intro_copy=s.new_tag('div',attrs={'class':'bc-module-intro-copy'})
    intro.append(intro_copy)
    grid=s.new_tag('div',attrs={'class':'bc-module-grid'})
    card=None
    for node in list(block.children):
        if not getattr(node,'name',None):continue
        if re.match(r'✨\s*Modul\s*\d',node.get_text(' ',strip=True)):
            card=s.new_tag('article',attrs={'class':'bc-module-card'})
            grid.append(card);node.name='h3';card.append(node.extract())
        elif card is not None:card.append(node.extract())
        else:
            if node.name=='h3':node.name='h2'
            intro_copy.append(node.extract())
    visual=section.select_one('.visuals').extract();intro.append(visual)
    action=section.select_one('.action').extract()
    inner.clear();inner.append(intro);inner.append(grid);inner.append(action)

    offer=s.select_one('.section-8');offer['class'].append('bc-offer')
    heading=offer.select_one('h3');heading.name='h2'
    heading.clear()
    label=s.new_tag('span',attrs={'class':'bc-offer-label'});label.string='Dein Angebot: '
    price=s.new_tag('span',attrs={'class':'bc-price'});price.string='497€'
    heading.append(label);heading.append(price)
    correct_page(s)
