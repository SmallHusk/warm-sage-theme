#!/usr/bin/env python3
"""Package the themes locally; this script never publishes or pushes anything."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--vsce', help='Path to the official vsce executable, if not installed locally.')
args = parser.parse_args()
meta = json.loads((ROOT / 'release.json').read_text())
subprocess.run(['python3', str(ROOT / 'scripts/check.py')], check=True)
vsce = args.vsce or str(ROOT / 'node_modules/.bin/vsce')
if not Path(vsce).is_file():
    vsce = shutil.which('vsce')
if not vsce:
    raise SystemExit('Install packaging tools with npm ci --ignore-scripts, then run npm run package.')

dist = ROOT / 'dist'
dist.mkdir(exist_ok=True)
version = meta['version']
vsix = dist / f'warm-sage-{version}.vsix'
subprocess.run([
    vsce, 'package', '--no-dependencies', '--githubBranch', 'main',
    '--baseContentUrl', meta['repository'] + '/blob/main/vscode/',
    '--baseImagesUrl', meta['repository'] + '/raw/main/vscode/',
    '--out', str(vsix),
], cwd=ROOT / 'vscode', check=True, timeout=90)


def zip_files(destination, prefix, paths):
    with ZipFile(destination, 'w', compression=ZIP_DEFLATED) as archive:
        for file, name in sorted(paths, key=lambda entry: entry[1]):
            assert file.is_file() and not file.is_symlink(), file
            archive.write(file, prefix + '/' + name)


zed_files = [(path, path.relative_to(ROOT / 'zed').as_posix())
             for path in (ROOT / 'zed').rglob('*') if path.is_file()]
zed_zip = dist / f'warm-sage-zed-{version}.zip'
zip_files(zed_zip, f'warm-sage-zed-{version}', zed_files)

source_files = []
for name in ['README.md', 'LICENSE', 'CHANGELOG.md', 'PUBLISHING.md', '.gitignore',
             'release.json', 'palette.json', 'package.json', 'package-lock.json']:
    source_files.append((ROOT / name, name))
for name in ['scripts', 'assets', 'vscode', 'zed']:
    for path in (ROOT / name).rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts:
            source_files.append((path, path.relative_to(ROOT).as_posix()))
source_zip = dist / f'warm-sage-source-{version}.zip'
zip_files(source_zip, 'warm-sage-themes', source_files)

artifacts = [vsix, zed_zip, source_zip]
checksums = dist / 'SHA256SUMS'
checksums.write_text(''.join(f'{sha256(path.read_bytes()).hexdigest()}  {path.name}\n' for path in artifacts))
for path in artifacts + [checksums]:
    print(path.relative_to(ROOT))
