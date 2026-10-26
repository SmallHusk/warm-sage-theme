#!/usr/bin/env python3
"""Render the repository's vector icon and illustrative palette preview to PNG.

Optional artwork tool: requires PyGObject, librsvg, and pycairo. The rendered PNGs
are committed, so normal builds and packaging do not require these libraries.
"""
import json
from html import escape
from pathlib import Path

import cairo
import gi
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg

ROOT = Path(__file__).resolve().parents[1]
P = json.loads((ROOT / 'palette.json').read_text())
assets = ROOT / 'assets'
assets.mkdir(exist_ok=True)


def render(name, width, height, svg):
    (assets / f'{name}.svg').write_text(svg)
    handle = Rsvg.Handle.new_from_data(svg.encode())
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    context = cairo.Context(surface)
    viewport = Rsvg.Rectangle()
    viewport.x = viewport.y = 0
    viewport.width, viewport.height = width, height
    handle.render_document(context, viewport)
    surface.write_to_png(str(assets / f'{name}.png'))


render('icon', 256, 256, f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256" viewBox="0 0 256 256">
<rect x="3" y="3" width="250" height="250" rx="52" fill="{P['base']}" stroke="{P['outline']}" stroke-width="5"/>
<path d="M65 88 L29 128 L65 168 M191 88 L227 128 L191 168" fill="none" stroke="{P['text']}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M96 166 C72 112 109 67 172 65 C183 125 150 166 96 166Z" fill="{P['sage']}"/>
<path d="M86 191 C100 148 121 119 155 89" fill="none" stroke="{P['base']}" stroke-width="7" stroke-linecap="round"/>
<path d="M86 191 L101 153" fill="none" stroke="{P['sage']}" stroke-width="7" stroke-linecap="round"/>
</svg>''')

COLORS = {
    'text': P['text'], 'comment': P['muted'], 'keyword': P['ansi']['bright']['magenta'],
    'type': P['ansi']['normal']['blue'], 'function': P['sage'],
    'string': P['sage'], 'number': P['warning'], 'property': P['icon'],
    'punctuation': P['muted'], 'operator': P['ansi']['bright']['cyan'],
}
lines = [
    [('comment', '// A quiet palette, with room to think.')],
    [('keyword', 'interface '), ('type', 'Theme'), ('text', ' {')],
    [('property', '  name'), ('punctuation', ': '), ('type', 'string'), ('punctuation', ';')],
    [('property', '  colors'), ('punctuation', ': '), ('keyword', 'readonly '), ('type', 'string'), ('text', '[];')],
    [('text', '}')],
    [],
    [('keyword', 'const '), ('text', 'colors '), ('operator', '= '), ('text', '['), ('string', '"brown", "cream", "sage"'), ('text', '];')],
    [('keyword', 'export function '), ('function', 'describe'), ('text', '('), ('property', 'theme'), ('punctuation', ': '), ('type', 'Theme'), ('text', '): '), ('type', 'string'), ('text', ' {')],
    [('keyword', '  const '), ('text', 'count '), ('operator', '= '), ('text', 'theme.'), ('property', 'colors.length'), ('text', ';')],
    [('keyword', '  return '), ('string', '`${theme.name} · ${count} colors`'), ('text', ';')],
    [('text', '}')],
    [],
    [('function', 'describe'), ('text', '({ '), ('property', 'name'), ('punctuation', ': '), ('string', '"Warm Sage"'), ('text', ', colors });')],
]
svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="920" viewBox="0 0 1440 920">
<rect width="1440" height="920" fill="{P['backdrop']}"/>
<text x="72" y="100" fill="{P['text']}" font-family="DejaVu Sans" font-size="54" font-weight="bold">Warm Sage</text>
<text x="74" y="143" fill="{P['muted']}" font-family="DejaVu Sans" font-size="21">Muted brown. Cream text. A little sage.</text>
<rect x="72" y="191" width="1296" height="540" rx="18" fill="{P['base']}" stroke="{P['outline']}"/>
<path d="M90 191 H1350 Q1368 191 1368 209 V246 H72 V209 Q72 191 90 191" fill="{P['surface']}"/>
<circle cx="102" cy="219" r="5" fill="{P['red']}"/>
<circle cx="122" cy="219" r="5" fill="{P['warning']}"/>
<circle cx="142" cy="219" r="5" fill="{P['sage']}"/>
<text x="184" y="226" fill="{P['text']}" font-family="DejaVu Sans" font-size="16">palette.ts</text>
<text x="1338" y="226" text-anchor="end" fill="{P['muted']}" font-family="DejaVu Sans" font-size="14">PALETTE &amp; SYNTAX PREVIEW</text>''']
for index, parts in enumerate(lines):
    y = 288 + index * 31
    svg.append(f'<text x="114" y="{y}" fill="{P["muted"]}" text-anchor="end" font-family="DejaVu Sans Mono" font-size="17">{index+1}</text>')
    spans = ''.join(f'<tspan fill="{COLORS[role]}">{escape(value)}</tspan>' for role, value in parts)
    svg.append(f'<text x="146" y="{y}" xml:space="preserve" font-family="DejaVu Sans Mono" font-size="22">{spans}</text>')

swatches = [('Brown', P['base']), ('Cream', P['text']), ('Sage', P['sage']), ('Mauve', COLORS['keyword']), ('Blue', COLORS['type']), ('Amber', P['warning']), ('Terracotta', P['red'])]
for index, (label, color) in enumerate(swatches):
    x = 72 + index * 186
    svg.append(f'<rect x="{x}" y="781" width="162" height="34" rx="8" fill="{color}" stroke="{P["outline"]}"/>')
    svg.append(f'<text x="{x}" y="846" fill="{P["text"]}" font-family="DejaVu Sans" font-size="16">{label}</text>')
    svg.append(f'<text x="{x}" y="873" fill="{P["muted"]}" font-family="DejaVu Sans Mono" font-size="14">{color}</text>')
svg.append('</svg>')
render('preview', 1440, 920, ''.join(svg))
print('Rendered vector icon and illustrative palette preview.')
