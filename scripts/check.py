#!/usr/bin/env python3
"""Check release metadata, resources, licenses, color formats, and contrast."""
import argparse
import json
from pathlib import Path
import re
import struct
import tomllib

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--zed-schema', type=Path, help='Also validate against an official downloaded Zed schema (requires jsonschema).')
args = parser.parse_args()


def load(path):
    return json.loads((ROOT / path).read_text())


meta = load('release.json')
palette = load('palette.json')
vscode = load('vscode/package.json')
zed_manifest = tomllib.loads((ROOT / 'zed/extension.toml').read_text())
zed = load('zed/themes/warm-sage.json')
theme = load('vscode/themes/warm-sage-color-theme.json')

assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', meta['zedId'])
assert meta['zedId'].endswith('-theme')
assert re.fullmatch(r'\d+\.\d+\.\d+', meta['version'])
assert meta['repository'].startswith('https://github.com/')
assert meta['license'] == 'MIT'
assert vscode['publisher'] == meta['publisher']
assert vscode['author']['name'] == meta['author'] == zed['author']
assert vscode['version'] == zed_manifest['version'] == meta['version']
assert zed_manifest['authors'] == [meta['author']]
assert zed_manifest['id'] == meta['zedId']
assert zed_manifest['repository'] == meta['repository']
assert zed_manifest['schema_version'] == 1
assert vscode['license'] == meta['license']
assert 'main' not in vscode and 'browser' not in vscode
assert 'activationEvents' not in vscode and 'dependencies' not in vscode
assert theme['semanticHighlighting'] is True
assert theme['name'] == zed['themes'][0]['name'] == meta['displayName']
assert theme['colors']['editor.background'] == zed['themes'][0]['style']['editor.background'] == palette['base']
assert theme['colors']['editor.foreground'] == zed['themes'][0]['style']['editor.foreground'] == palette['text']

for package in ['vscode', 'zed']:
    folder = ROOT / package
    assert (folder / 'LICENSE').read_bytes() == (ROOT / 'LICENSE').read_bytes()
    assert (folder / 'CHANGELOG.md').read_bytes() == (ROOT / 'CHANGELOG.md').read_bytes()
    assert 'Copyright (c) 2026 ' + meta['author'] in (folder / 'LICENSE').read_text()
    assert (folder / 'README.md').is_file()
    for filename in ['icon.png', 'preview.png']:
        data = (folder / 'assets' / filename).read_bytes()
        assert data.startswith(b'\x89PNG\r\n\x1a\n')
        width, height = struct.unpack('>II', data[16:24])
        assert width >= 128 and height >= 128
    for file in folder.rglob('*'):
        assert not file.is_symlink(), file
        if file.is_file() and file.suffix in ['.json', '.toml', '.md']:
            content = file.read_text()
            assert '/home/$USER' not in content, file
            assert 'niri-backups' not in content, file
            assert 'UNLICENSED' not in content, file

for contribution in vscode['contributes']['themes']:
    assert (ROOT / 'vscode' / contribution['path']).is_file()
    assert contribution['label'] == meta['displayName']

for name, color in theme['colors'].items():
    assert re.fullmatch(r'#[\da-fA-F]{6}([\da-fA-F]{2})?', color), (name, color)
for token in theme['tokenColors']:
    assert token['scope'] and re.fullmatch(r'#[\da-fA-F]{6}', token['settings']['foreground'])
for family, prefix in [('normal', 'ansi'), ('bright', 'ansiBright')]:
    for name, color in palette['ansi'][family].items():
        assert theme['colors']['terminal.' + prefix + name.capitalize()] == color


def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return sum(weight * (value / 12.92 if value <= .04045 else ((value + .055) / 1.055) ** 2.4)
               for weight, value in zip((.2126, .7152, .0722), channels))


def contrast(a, b):
    low, high = sorted([luminance(a), luminance(b)])
    return (high + .05) / (low + .05)


for capture, style in zed['themes'][0]['style']['syntax'].items():
    assert contrast(style['color'], palette['base']) >= 4.5, capture
for color in [palette['text'], palette['muted'], palette['sage']]:
    assert contrast(color, palette['surface']) >= 4.5
assert contrast(palette['text'], palette['selection_solid']) >= 4.5

if args.zed_schema:
    import jsonschema
    schema = json.loads(args.zed_schema.read_text())
    jsonschema.Draft7Validator(schema).validate(zed)
    assert not set(zed['themes'][0]['style']) - set(schema['definitions']['ThemeStyleContent']['properties'])
    print('Official Zed schema validation passed.')
print('Release metadata, MIT licenses, PNG assets, syntax contrast, terminal colors, and package paths passed.')
