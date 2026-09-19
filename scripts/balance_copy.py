"""Approved Balance Code copy corrections; original source snapshots stay intact."""
import re

def corrected(text):
    replacements = {
        'ChatGpt': 'ChatGPT',
        'Facebook Gruppen': 'Facebook-Gruppen',
        'HPU&Hashimoto': 'HPU & Hashimoto',
        'Blutabnahme Guide': 'Blutentnahme-Guide',
        'vorallem': 'vor allem',
        'dran bleibst': 'dranbleibst',
        'weiter machen kannst': 'weitermachen kannst',
        'Stell dir vor du': 'Stell dir vor, du',
        'Bist du bereit, für': 'Bist du bereit für',
        'Er ist auf 8 Wochen': 'Es ist auf 8 Wochen',
        'Du kannst ihn aber ganz': 'Du kannst es aber ganz',
        'probiert .': 'probiert.',
        '20 - 30 Minuten': '20–30 Minuten',
        'Es ist Zeit aus': 'Es ist Zeit, aus',
        'Eine erprobte Anleitung die': 'Eine erprobte Anleitung, die',
        'so dass du weißt wo du': 'sodass du weißt, wo du',
        'damit verbringen dir Infos': 'damit verbringen, dir Infos',
        'fühle mich jetzt tatsächlich, wie': 'fühle mich jetzt tatsächlich wie',
        'Breathwork Mini-Kurs': 'Breathwork-Mini-Kurs',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r'Entspannungsreise \+ Blutentnahme-Guide(?! \+ Breathwork-Mini-Kurs)', 'Entspannungsreise + Blutentnahme-Guide + Breathwork-Mini-Kurs', text)
    text = text.replace('“Ich', '„Ich').replace('.”', '.“').replace('."', '.“')
    text = re.sub(r'€\s*(\d[\d.]*)', r'\1 €', text)
    text = re.sub(r'(\d[\d.]*)\s*€', lambda m: ('1.597' if m[1] == '1597' else m[1]) + '\u00a0€', text)
    text = re.sub(r'Modul[\s\u00a0]+(\d)', r'Modul \1', text)
    text = re.sub(r'(?<=\w)\s*…', ' …', text)
    return text

def correct_page(soup):
    for node in list(soup.select_one('main').find_all(string=True)):
        if node.parent.name not in ('script', 'style'):
            new = corrected(str(node))
            if new != str(node):
                node.replace_with(new)
