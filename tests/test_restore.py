import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
RESTORE = ROOT / 'scripts' / 'restore.py'


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.scratch = tempfile.TemporaryDirectory()
        self.addCleanup(self.scratch.cleanup)
        self.home = Path(self.scratch.name) / 'user'

    def run_restore(self, *args, expected=0):
        result = subprocess.run([sys.executable, str(RESTORE), '--home', str(self.home), *args], capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_preview_writes_nothing(self):
        result = self.run_restore('--with-pstack')
        self.assertGreater(len(result['files']), 3)
        self.assertFalse(self.home.exists())

    def test_fresh_restore_and_repeat_preserve_config(self):
        config = self.home / '.codex/config.toml'
        config.parent.mkdir(parents=True)
        sentinel = b'model = "my-existing-model"\r\n'
        config.write_bytes(sentinel)
        first = self.run_restore('--with-pstack', '--apply')
        self.assertGreater(first['written'], 0)
        rules = self.home / '.codex/AGENTS.md'
        self.assertEqual(rules.read_bytes(), (ROOT / 'templates/AGENTS.md').read_bytes())
        self.assertTrue((self.home / '.agents/skills/pstack-auto/SKILL.md').is_file())
        before = rules.stat().st_mtime_ns
        second = self.run_restore('--with-pstack', '--apply')
        self.assertEqual(second['written'], 0)
        self.assertIsNone(second['backup'])
        self.assertEqual(rules.stat().st_mtime_ns, before)
        self.assertEqual(config.read_bytes(), sentinel)

    def test_conflict_refuses_before_creating_other_files(self):
        rules = self.home / '.codex/AGENTS.md'
        rules.parent.mkdir(parents=True)
        rules.write_bytes(b'Existing personal instructions\r\n')
        result = self.run_restore('--apply', expected=2)
        self.assertEqual(result['written'], 0)
        self.assertFalse((self.home / '.agents').exists())
        self.assertEqual(rules.read_bytes(), b'Existing personal instructions\r\n')

    def test_explicit_overwrite_keeps_exact_backup(self):
        rules = self.home / '.codex/AGENTS.md'
        rules.parent.mkdir(parents=True)
        original = b'original\r\n\xff'
        rules.write_bytes(original)
        result = self.run_restore('--apply', '--overwrite')
        manifest = json.loads((Path(result['backup']) / 'manifest.json').read_text(encoding='utf-8'))
        entry = next(item for item in manifest if item['target'] == str(rules))
        self.assertEqual(Path(entry['backup']).read_bytes(), original)
        self.assertEqual(rules.read_bytes(), (ROOT / 'templates/AGENTS.md').read_bytes())

    def test_claude_uses_claude_paths_without_codex_entry(self):
        self.run_restore('--agent', 'claude', '--apply')
        rules = self.home / '.claude/CLAUDE.md'
        self.assertEqual(rules.read_bytes(), (ROOT / 'templates/CLAUDE.md').read_bytes())
        self.assertTrue((self.home / '.claude/skills/ego-browser/SKILL.md').is_file())
        self.assertFalse((self.home / '.codex').exists())
        self.assertFalse((self.home / '.claude/skills/pstack-auto').exists())

    def test_custom_destination_is_honored(self):
        rules = self.home / 'custom/instructions.md'
        skills = self.home / 'custom/skills'
        self.run_restore('--agent', 'generic', '--rules-file', str(rules), '--skills-dir', str(skills), '--apply')
        self.assertEqual(rules.read_bytes(), (ROOT / 'templates/CLAUDE.md').read_bytes())
        self.assertTrue((skills / 'setup-cua-driver/SKILL.md').is_file())

    def test_symlink_destination_is_not_followed(self):
        external = Path(self.scratch.name) / 'external'
        external.mkdir()
        self.home.mkdir()
        link = self.home / '.codex'
        try:
            link.symlink_to(external, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is unavailable for this test process')
        self.run_restore('--apply', '--overwrite', expected=1)
        self.assertFalse((external / 'AGENTS.md').exists())

    @unittest.skipUnless(sys.platform == 'win32', 'Windows junction regression')
    def test_windows_junction_destination_is_not_followed(self):
        external = Path(self.scratch.name) / 'external-junction-target'
        external.mkdir()
        self.home.mkdir()
        link = self.home / '.codex'
        quote = lambda path: "'" + str(path).replace("'", "''") + "'"
        command = f'New-Item -ItemType Junction -Path {quote(link)} -Target {quote(external)} | Out-Null'
        created = subprocess.run(['powershell.exe', '-NoProfile', '-Command', command], capture_output=True)
        self.assertEqual(created.returncode, 0, created.stderr.decode(errors='replace'))
        self.run_restore('--apply', '--overwrite', expected=1)
        self.assertFalse((external / 'AGENTS.md').exists())


if __name__ == '__main__':
    unittest.main()
