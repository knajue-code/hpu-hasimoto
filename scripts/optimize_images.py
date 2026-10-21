"""Apply reviewed image descriptions, intrinsic dimensions and optimized assets."""
import html
import json
import re
from pathlib import Path


def optimize_images(dist):
    metadata = json.loads((Path(__file__).resolve().parents[1] / 'source/image-metadata.json').read_text())
    metadata.update({v['src']: v for v in list(metadata.values()) if 'src' in v})

    def update(match):
        tag = match.group()
        src = re.search(r'\bsrc=["\']([^"\']+)["\']', tag)
        if not src or src[1] not in metadata:
            return tag
        values = metadata[src[1]]
        for attr, value in values.items():
            attribute = attr + '="' + html.escape(str(value), quote=True) + '"'
            pattern = r'\b' + attr + r'\s*=\s*(["\']).*?\1'
            if re.search(pattern, tag):
                tag = re.sub(pattern, lambda m: attribute, tag)
            else:
                tag = re.sub(r'\s*/?>$', lambda m: ' ' + attribute + m.group(), tag)
        return tag

    for path in dist.rglob('*.html'):
        old = path.read_text()
        new = re.sub(r'<img\b[^>]*>', update, old, flags=re.I)
        if new != old:
            path.write_text(new)
