import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = REPO_ROOT / "skill"


class SkillIntegrityTests(unittest.TestCase):
    def test_no_tracked_tts_script_contains_embedded_session_credentials(self):
        checked = []
        credential_patterns = (
            r"\btoken\s*:\s*['\"][^'\"]+['\"]",
            r"\bcookie\s*:\s*['\"][^'\"]+['\"]",
            r"\b(?:api[_-]?key|authorization)\s*[:=]\s*['\"][^'\"]+['\"]",
            r"\bBearer\s+[A-Za-z0-9._-]{16,}",
        )
        for root in (SKILL_ROOT / "scripts", SKILL_ROOT / "assets"):
            for path in root.rglob("*"):
                if path.suffix not in {".py", ".js"}:
                    continue
                checked.append(path)
                source = path.read_text(encoding="utf-8")
                for pattern in credential_patterns:
                    self.assertIsNone(
                        re.search(pattern, source, flags=re.IGNORECASE),
                        f"embedded credential in {path}",
                    )
        self.assertTrue(checked)

    def test_video_templates_do_not_depend_on_this_workstation(self):
        template_root = SKILL_ROOT / "assets"
        checked = []
        for path in template_root.rglob("*"):
            if path.suffix not in {".py", ".js"}:
                continue
            checked.append(path)
            source = path.read_text(encoding="utf-8")
            self.assertIsNone(
                re.search(r"(?<![A-Za-z0-9_])[A-Za-z]:[/\\\\]", source),
                f"absolute Windows path in {path}",
            )
            self.assertNotIn("AppData/Local/npm-cache", source)
            self.assertNotIn("Skills推荐第1期：这个Skill让你的AI变成顶级工程师.mp4", source)
        self.assertTrue(checked)

    def test_unspecified_output_form_consistently_defaults_to_longform(self):
        examples = (SKILL_ROOT / "examples" / "prompt-examples.md").read_text(encoding="utf-8")
        metadata = (SKILL_ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("没指定输出形式，先追问", examples)
        self.assertNotIn("If the output form is missing, ask the user", metadata)
        self.assertIn("默认长文", examples)
        self.assertIn("default to 长文", metadata)


if __name__ == "__main__":
    unittest.main()
