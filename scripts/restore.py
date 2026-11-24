#!/usr/bin/env python3
"""Restore repository-owned files; never edit the host's config.toml."""

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import uuid


REPO = Path(__file__).resolve().parents[1]


@dataclass
class PlannedFile:
    source: Path
    target: Path
    content: bytes
    previous: bytes | None
    status: str


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--agent', choices=['codex', 'claude', 'generic'], default='codex')
    parser.add_argument('--home', type=Path, help='Explicit target user directory; useful for isolated testing')
    parser.add_argument('--rules-file', type=Path)
    parser.add_argument('--skills-dir', type=Path)
    parser.add_argument('--with-pstack', action='store_true', help='Install optional Codex pstack entry and preferences')
    parser.add_argument('--apply', action='store_true', help='Write the previewed files')
    parser.add_argument('--overwrite', action='store_true', help='Back up and replace differing repository-owned target files')
    args = parser.parse_args(argv)
    if args.agent == 'generic' and not (args.rules_file and args.skills_dir):
        parser.error('generic requires --rules-file and --skills-dir')
    if args.with_pstack and args.agent != 'codex':
        parser.error('--with-pstack is Codex-specific; use the host-specific port instead')
    return args


def destinations(args):
    home = (args.home or Path.home()).expanduser().absolute()
    codex_home = home / '.codex'
    if args.home is None and os.environ.get('CODEX_HOME'):
        codex_home = Path(os.environ['CODEX_HOME']).expanduser().absolute()
    default_rules = codex_home / 'AGENTS.md' if args.agent == 'codex' else home / '.claude' / 'CLAUDE.md'
    default_skills = home / ('.claude' if args.agent == 'claude' else '.agents') / 'skills'
    return home, (args.rules_file or default_rules).expanduser().absolute(), (args.skills_dir or default_skills).expanduser().absolute()


def reject_linked_target(path):
    # Do not write through a user's symlink/junction into an unrelated tree.
    for candidate in [path, *path.parents]:
        try:
            info = candidate.lstat()
        except FileNotFoundError:
            continue
        reparse = getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)
        if stat.S_ISLNK(info.st_mode) or reparse:
            raise ValueError(f'Refusing linked destination: {candidate}; choose a real target directory or merge manually')


def build_plan(args):
    home, rules, skills = destinations(args)
    rules_template = 'AGENTS.md' if args.agent == 'codex' else 'CLAUDE.md'
    pairs = [(REPO / 'templates' / rules_template, rules)]
    names = ['restore-dev-environment', 'ego-browser', 'setup-cua-driver']
    if args.with_pstack:
        names.append('pstack-auto')
        pairs.append((REPO / 'templates' / 'pstack-models.md', home / '.agents' / 'pstack-models.md'))
    for name in names:
        source_dir = REPO / 'skills' / name
        pairs.extend((source, skills / name / source.relative_to(source_dir)) for source in sorted(source_dir.rglob('*')) if source.is_file())
    plan = []
    targets = set()
    for source, target in pairs:
        reject_linked_target(target)
        if target in targets:
            raise ValueError(f'Conflicting destination options: {target}')
        targets.add(target)
        content = source.read_bytes()
        previous = target.read_bytes() if target.exists() else None
        status = 'unchanged' if previous == content else ('create' if previous is None else 'conflict')
        plan.append(PlannedFile(source, target, content, previous, status))
    return home, plan


def atomic_write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix='.skill-tool-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(content)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def run(args):
    home, plan = build_plan(args)
    result = {'mode': 'apply' if args.apply else 'preview', 'agent': args.agent, 'files': [
        {'source': str(item.source.relative_to(REPO)), 'target': str(item.target), 'status': item.status} for item in plan
    ], 'backup': None, 'written': 0}
    conflicts = [item for item in plan if item.status == 'conflict']
    if not args.apply:
        return result, 0
    if conflicts and not args.overwrite:
        result['error'] = 'Existing files differ. Nothing was written. Merge them, or explicitly use --overwrite after review.'
        return result, 2
    for item in plan:
        reject_linked_target(item.target)
        current = item.target.read_bytes() if item.target.exists() else None
        if current != item.previous:
            raise ValueError(f'Target changed after preview: {item.target}')
    if conflicts:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:8]
        backup = home / '.local' / 'state' / 'skill-tool' / 'backups' / stamp
        reject_linked_target(backup)
        records = []
        for index, item in enumerate(conflicts):
            saved = backup / f'{index:03d}-{item.target.name}'
            atomic_write(saved, item.previous)
            records.append({'target': str(item.target), 'backup': str(saved), 'sha256': hashlib.sha256(item.previous).hexdigest()})
        atomic_write(backup / 'manifest.json', json.dumps(records, ensure_ascii=False, indent=2).encode('utf-8'))
        result['backup'] = str(backup)
    for item in plan:
        if item.status != 'unchanged':
            reject_linked_target(item.target)
            current = item.target.read_bytes() if item.target.exists() else None
            if current != item.previous:
                raise ValueError(f'Target changed before write: {item.target}')
            atomic_write(item.target, item.content)
            result['written'] += 1
    return result, 0


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    args = parse_args()
    try:
        result, code = run(args)
    except (OSError, ValueError) as error:
        result, code = {'error': str(error), 'note': 'If a filesystem failure occurred mid-apply, inspect written files and the backup before retrying.'}, 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == '__main__':
    raise SystemExit(main())
