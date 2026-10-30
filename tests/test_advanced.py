"""Regression tests for joins, snapshots, rules, reporting and safe checks."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from join_audit import audit
from compare_tables import compare
from rule_check import check
from environment_check import diagnose
from http_smoke import check as http_check
from merge_tables import join
from quality_report import generate

class AdvancedTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)

    def csv(self, name, data):
        path = self.root / name
        path.write_text(data, encoding="utf-8")
        return path

    def spec(self, name, obj):
        path = self.root / name
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return path

    def test_join_audit_detects_row_multiplication(self):
        a = self.csv("a.csv", "id,qty\nX,100\nY,10\n")
        b = self.csv("b.csv", "id,defect\nX,1\nX,2\n")
        out = audit(a, b, ["id"], "many_to_one")
        self.assertFalse(out["valid"])
        self.assertEqual(out["predicted_rows"]["left"], 3)
        self.assertEqual(out["left"]["unmatched_rows"], 1)

    def test_join_audit_does_not_pass_empty(self):
        a = self.csv("a.csv", "id,qty\n")
        b = self.csv("b.csv", "id,qty\nX,2\n")
        self.assertFalse(audit(a, b, ["id"])["valid"])

    def test_merge_keeps_exact_identifiers(self):
        a = self.csv("a.csv", "id,qty\nA ,10\n")
        b = self.csv("b.csv", "id,flag\nA,yes\n")
        rows, _ = join(a, b, "id")
        self.assertEqual(rows[0]["right_flag"], "")

    def test_compare_changes_and_additions(self):
        a = self.csv("a.csv", "id,value\nX,1\n")
        b = self.csv("b.csv", "id,value\nX,2\nY,3\n")
        r = compare(a, b, ["id"])
        self.assertEqual((r["changed_rows"], r["added_rows"]), (1, 1))
        self.assertFalse(r["identical"])

    def test_compare_rejects_duplicate_keys(self):
        a = self.csv("a.csv", "id,value\nX,1\nX,2\n")
        b = self.csv("b.csv", "id,value\nX,1\n")
        with self.assertRaisesRegex(ValueError, "중복"):
            compare(a, b, ["id"])

    def test_compare_empty_is_not_verified(self):
        a = self.csv("a.csv", "id,value\n")
        b = self.csv("b.csv", "id,value\n")
        self.assertFalse(compare(a, b, ["id"])["identical"])

    def test_rules_inclusive_vs_exclusive(self):
        self.csv("data.csv", "v\n95\n")
        rule = {"field": "v", "direction": "min", "limit": 95,
                "inclusive": True, "reference": "명시된 기준"}
        src = self.spec("r.json", {"source": "data.csv", "rules": [rule]})
        self.assertTrue(check(src)["passed"])
        rule["inclusive"] = False
        self.assertFalse(check(self.spec("r2.json", {"source": "data.csv", "rules": [rule]}))["passed"])

    def test_rules_need_reference(self):
        self.csv("data.csv", "v\n95\n")
        src = self.spec("r.json", {"source": "data.csv", "rules": [
            {"field": "v", "direction": "max", "limit": 100, "inclusive": True}]})
        with self.assertRaisesRegex(ValueError, "reference"):
            check(src)

    def test_rules_do_not_pass_zero_rules(self):
        self.csv("data.csv", "v\n95\n")
        src = self.spec("r.json", {"source": "data.csv", "rules": []})
        with self.assertRaisesRegex(ValueError, "0개"):
            check(src)

    def test_rules_invalid_number(self):
        self.csv("data.csv", "v\nunknown\n")
        src = self.spec("r.json", {"source": "data.csv", "rules": [
            {"field": "v", "direction": "min", "limit": 1, "inclusive": True, "reference": "근거"}]})
        self.assertEqual(check(src)["result"]["invalid"], 1)

    def test_group_weighted_rate(self):
        self.csv("data.csv", "line,tested,passed\nA,100,99\nA,2,1\n")
        src = self.spec("report.json", {
            "sources": [{"name": "d", "path": "data.csv"}],
            "groups": [{"name": "라인 비율", "source": "d", "by": "line",
                        "operation": "ratio_percent", "numerator_column": "passed",
                        "denominator_column": "tested"}]})
        self.assertIn("| A | 98.039216 |", generate(src))

    def test_group_ratio_zero_denominator(self):
        self.csv("data.csv", "line,tested,passed\nA,0,1\n")
        src = self.spec("report.json", {
            "sources": [{"name": "d", "path": "data.csv"}],
            "groups": [{"name": "비율", "source": "d", "by": "line",
                        "operation": "ratio_percent", "numerator_column": "passed",
                        "denominator_column": "tested"}]})
        with self.assertRaisesRegex(ValueError, "분모"):
            generate(src)

    def test_environment_diagnostic(self):
        self.assertIn("python", diagnose())

    def test_reject_external_http(self):
        with self.assertRaisesRegex(ValueError, "외부"):
            http_check("http://example.com/")
