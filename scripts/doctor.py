#!/usr/bin/env python3
"""Read-only discovery. Never launches a browser, app, driver, or model."""

import argparse
import json
import os
from pathlib import Path
import shutil
import sys
import tomllib


def inspect(home, codex_home):
    ego = shutil.which('ego-browser')
    cua = shutil.which('cua-driver')
    if sys.platform == 'win32':
        ego_fallback = home / '.local/share/ego/active_version_dir/ego-browser.exe'
        local = Path(os.environ.get('LOCALAPPDATA', home / 'AppData/Local'))
        cua_fallback = local / 'Programs/Cua/cua-driver/bin/cua-driver.exe'
        ego = ego or (str(ego_fallback) if ego_fallback.is_file() else None)
        cua = cua or (str(cua_fallback) if cua_fallback.is_file() else None)
    config_path = codex_home / 'config.toml'
    settings = tomllib.loads(config_path.read_text(encoding='utf-8-sig')) if config_path.is_file() else {}
    agents = settings.get('agents', {})
    overrides = {key: agents[key] for key in ['default_subagent_model', 'default_subagent_reasoning_effort'] if key in agents}
    enabled_legacy = []
    for name in ['agent-desktop', 'agent-desktop-windows']:
        path = codex_home / 'skills' / name / 'SKILL.md'
        if path.is_file():
            enabled = True
            for entry in settings.get('skills', {}).get('config', []):
                selector = entry.get('path')
                matches_path = isinstance(selector, str) and os.path.normcase(os.path.normpath(selector)) == os.path.normcase(os.path.normpath(path))
                if matches_path or entry.get('name') == name:
                    enabled = entry.get('enabled', True)
            if enabled:
                enabled_legacy.append(name)
    return {
        'platform': sys.platform,
        'commands': {'ego': ego, 'cua': cua, 'codex': shutil.which('codex')},
        'codexRulesPresent': (codex_home / 'AGENTS.md').is_file(),
        'cuaMcpConfigured': 'cua-driver' in settings.get('mcp_servers', {}),
        'cuaOfficialSkillPresent': (home / '.agents/skills/cua-driver/SKILL.md').is_file(),
        'pstackPreferencesPresent': (home / '.agents/pstack-models.md').is_file(),
        'subagentDefaultOverrides': overrides,
        'legacySkillsPossiblyEnabled': enabled_legacy,
        'limits': 'Discovery only. No GUI, MCP handshake, model routing or browser task was tested.',
    }


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', type=Path)
    args = parser.parse_args()
    home = (args.home or Path.home()).expanduser().absolute()
    codex_home = home / '.codex'
    if args.home is None and os.environ.get('CODEX_HOME'):
        codex_home = Path(os.environ['CODEX_HOME']).expanduser().absolute()
    try:
        result = inspect(home, codex_home)
    except (OSError, ValueError) as error:
        print(json.dumps({'error': str(error)}))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
