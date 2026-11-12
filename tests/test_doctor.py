import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


DOCTOR = Path(__file__).resolve().parents[1] / 'scripts/doctor.py'


class DoctorTests(unittest.TestCase):
    def test_later_skill_selector_wins_without_exposing_other_config(self):
        with tempfile.TemporaryDirectory() as scratch:
            home = Path(scratch)
            legacy = home / '.codex/skills/agent-desktop/SKILL.md'
            legacy.parent.mkdir(parents=True)
            legacy.write_text('existing tool', encoding='utf-8')
            config = home / '.codex/config.toml'
            config.write_text('private_setting = "do-not-print-this-value"\n'
                              '[[skills.config]]\nname = "agent-desktop"\nenabled = false\n'
                              '[[skills.config]]\nname = "agent-desktop"\nenabled = true\n', encoding='utf-8')
            before = config.read_bytes()
            result = subprocess.run([sys.executable, str(DOCTOR), '--home', str(home)], capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('agent-desktop', json.loads(result.stdout)['legacySkillsPossiblyEnabled'])
            self.assertNotIn('do-not-print-this-value', result.stdout)
            self.assertEqual(config.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
