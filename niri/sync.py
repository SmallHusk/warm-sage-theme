#!/usr/bin/env python3
"""Copy the explicitly listed desktop configs from a home directory into the repo."""
import argparse
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path, default=Path.home(), help='Home directory to capture (default: current user).')
    parser.add_argument('--check', action='store_true', help='Check that the snapshot matches, without copying.')
    args = parser.parse_args()
    paths = [Path(line) for line in (ROOT / 'files.txt').read_text().splitlines() if line and not line.startswith('#')]
    for path in paths:
        if path.is_absolute() or '..' in path.parts:
            parser.error(f'Invalid manifest path: {path}')
        source = args.home / path
        if source.is_symlink() or not source.is_file():
            parser.error(f'Expected a regular configuration file: {source}')
    differences = []
    for path in paths:
        source, target = args.home / path, ROOT / 'home' / path
        if args.check:
            if not target.is_file() or target.is_symlink() or source.read_bytes() != target.read_bytes() or (source.stat().st_mode & 0o111) != (target.stat().st_mode & 0o111):
                differences.append(str(path))
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    if differences:
        print('Snapshot differs:\n' + '\n'.join(differences))
        return 1
    print(f'{len(paths)} desktop files {"match the live configuration" if args.check else "copied into niri/home"}.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
