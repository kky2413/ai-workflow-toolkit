"""Contract validation tests without permanent demo data."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from json_structure_check import check

class JsonContractTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def write(self, name, obj):
        path = self.root / name
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return path

    def spec(self, **kw):
        src = {"source": "data.json", "fields": {"id": "string", "count": "integer"},
               "required": ["id", "count"]}
        src.update(kw)
        return self.write("contract.json", src)

    def test_valid_contract(self):
        self.write("data.json", [{"id": "001", "count": 5}])
        self.assertTrue(check(self.spec())["passed"])

    def test_missing_key(self):
        self.write("data.json", [{"id": "001"}])
        self.assertEqual(check(self.spec())["examples"][0]["problem"], "missing")

    def test_boolean_is_not_integer(self):
        self.write("data.json", [{"id": "001", "count": True}])
        self.assertEqual(check(self.spec())["examples"][0]["problem"], "wrong_type")

    def test_empty_array_does_not_pass(self):
        self.write("data.json", [])
        self.assertFalse(check(self.spec())["passed"])

    def test_extra_field_rejected_when_requested(self):
        self.write("data.json", [{"id": "001", "count": 3, "other": "x"}])
        self.assertFalse(check(self.spec(allow_extra=False))["passed"])
