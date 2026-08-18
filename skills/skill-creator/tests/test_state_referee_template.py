import os
import sys
import json
import subprocess
import unittest
import tempfile
import shutil
from pathlib import Path

TEMPLATE_PATH = Path("/home/rcrede/.gemini/config/skills/skill-creator/templates/state_referee_template.py")

class TestStateReferee(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.scripts_dir = Path(self.test_dir) / "scripts"
        self.scripts_dir.mkdir(parents=True)
        
        self.referee_script = self.scripts_dir / "my_skill_referee.py"
        self.referee_script.write_text(TEMPLATE_PATH.read_text())
        
        self.config_path = self.scripts_dir / "referee_config.json"
        self.state_file = self.scripts_dir / "state.json"
        
        config = {
            "phases": ["INIT", "RESEARCH", "DRAFTING", "REVIEW", "COMPLETED"],
            "instructions": {
                "INIT": {"action": "Identify goal", "constraints": "NO_TOOLS"},
                "RESEARCH": {"action": "Use search", "constraints": "SEARCH_ONLY"},
                "DRAFTING": {"action": "Write code", "constraints": "WRITE_ONLY"},
                "REVIEW": {"action": "Review code", "constraints": "READ_ONLY"},
                "COMPLETED": {"action": "Done", "constraints": "NONE"}
            }
        }
        with open(self.config_path, "w") as f:
            json.dump(config, f)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def run_referee(self, cmd_args):
        result = subprocess.run(
            [sys.executable, str(self.referee_script)] + cmd_args,
            cwd=str(self.scripts_dir),
            capture_output=True,
            text=True
        )
        return result

    def test_init_state(self):
        res = self.run_referee(["init"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("STATE: INIT", res.stdout)
        self.assertIn("ACTION: Identify goal", res.stdout)
        self.assertIn("NO_TOOLS", res.stdout)
        
        self.assertTrue(self.state_file.exists())
        state = json.loads(self.state_file.read_text())
        self.assertEqual(state["current_phase"], "INIT")

    def test_valid_advance(self):
        self.run_referee(["init"])
        res = self.run_referee(["advance", "--to", "RESEARCH"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("STATE: RESEARCH", res.stdout)
        
        state = json.loads(self.state_file.read_text())
        self.assertEqual(state["current_phase"], "RESEARCH")

    def test_invalid_skip_advance(self):
        self.run_referee(["init"])
        res = self.run_referee(["advance", "--to", "DRAFTING"])
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Cannot skip phase RESEARCH", res.stderr)

    def test_invalid_backward_advance(self):
        self.run_referee(["init"])
        self.run_referee(["advance", "--to", "RESEARCH"])
        res = self.run_referee(["advance", "--to", "INIT"])
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("Cannot advance to INIT from RESEARCH", res.stderr)

    def test_advance_without_init(self):
        res = self.run_referee(["advance", "--to", "RESEARCH"])
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("No active state. Please run 'init' first.", res.stderr)

if __name__ == "__main__":
    unittest.main()
