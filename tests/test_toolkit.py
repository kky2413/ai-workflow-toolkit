"""Local tests: python -m unittest discover -s tests -v"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inventory = load_script("inventory")
data_profile = load_script("data_profile")
verify_outputs = load_script("verify_outputs")


class ToolkitTests(unittest.TestCase):
    def test_inventory_excludes_git(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "data.csv").write_text("a\n1\n", encoding="utf-8")
            (root / ".git").mkdir()
            (root / ".git" / "secret").write_text("x", encoding="utf-8")
            report = inventory.build_inventory(root)
            self.assertEqual(report["file_count"], 1)
            self.assertEqual(report["files"][0]["path"], "data.csv")

    def test_csv_profile_statistics_and_missing(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data.csv"
            path.write_text("name,value\nA,10\nB,20\nC,\n", encoding="utf-8-sig")
            report = data_profile.profile(path)
            self.assertEqual(report["rows_profiled"], 3)
            self.assertEqual(report["columns"]["value"]["missing"], 1)
            self.assertEqual(report["columns"]["value"]["numeric"]["mean"], 15.0)

    def test_json_profile(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "data.json"
            path.write_text('[{"v": 1}, {"v": 3}]', encoding="utf-8")
            self.assertEqual(data_profile.profile(path)["columns"]["v"]["numeric"]["sum"], 4)

    def test_verify_outputs_pass_fail(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "done.txt").write_text("ok", encoding="utf-8")
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"files": [{"path": "done.txt", "min_bytes": 2}]}))
            self.assertTrue(verify_outputs.verify(root, manifest)["passed"])
            manifest.write_text(json.dumps({"files": [{"path": "absent.txt"}]}))
            self.assertFalse(verify_outputs.verify(root, manifest)["passed"])

    def test_verify_rejects_parent_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            manifest = root / "manifest.json"
            manifest.write_text(json.dumps({"files": [{"path": "../outside.txt"}]}))
            with self.assertRaises(ValueError):
                verify_outputs.verify(root, manifest)


if __name__ == "__main__":
    unittest.main()
