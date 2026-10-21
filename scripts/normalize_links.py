"""Normalize known internal page URLs without changing text or external links."""
import html
import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode


def normalize_links(dist):
    routes = {'/' + str(p.parent.relative_to(dist)).strip('./') + '/'
              for p in dist.rglob('index.html')}
    routes.discard('//')
    routes.add('/')
    route_map = {route.lower(): route for route in routes}
    route_map['/wissen/tag/symptome/'] = '/wissen/tag/symptome/'

    def normalize(value):
        u = urlsplit(html.unescape(value))
        if u.scheme not in ('', 'http', 'https') or (u.netloc and u.hostname not in ('hpu-hashimoto.de', 'www.hpu-hashimoto.de')):
            return value
        if not u.path.startswith('/'):
            return value
        path = route_map.get(u.path.rstrip('/').lower() + '/')
        if path is None:
            return value
        query = u.query
        if path == '/wissen/':
            query = urlencode([(k, v) for k, v in parse_qsl(query, keep_blank_values=True) if k != 'author'])
        return html.escape(urlunsplit((u.scheme, u.netloc, path, query, u.fragment)), quote=True)

    # Limit replacements to link hrefs and social URL metadata.
    def replace_tag(match):
        tag = match.group()
        if tag.lower().startswith('<meta') and not re.search(r'(?:property|name)=["\'](?:og:url|twitter:url)["\']', tag, re.I):
            return tag
        attr = 'content' if tag.lower().startswith('<meta') else 'href'
        return re.sub(r'(' + attr + r'\s*=\s*)(["\'])(.*?)\2',
                      lambda m: m[1] + m[2] + normalize(m[3]) + m[2], tag, flags=re.I | re.S)

    changed = []
    for path in dist.rglob('*.html'):
        old = path.read_text()
        new = re.sub(r'<(?:a|link|meta)\b[^>]*>', replace_tag, old, flags=re.I)
        if new != old:
            path.write_text(new)
            changed.append(str(path))
    return changed
