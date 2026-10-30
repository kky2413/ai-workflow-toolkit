"""Unit tests for reusable tabular report / join functions."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from tabular_io import read_table
from quality_report import generate
from merge_tables import join


class ReportingTests(unittest.TestCase):
    def test_csv_json_reading(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / 'a.csv').write_text('id,qty\na,10\nb,20\n', encoding='utf-8')
            (folder / 'b.json').write_text('[{"id":"a", "qty":2}]', encoding='utf-8')
            self.assertEqual(len(read_table(folder / 'a.csv')[0]), 2)
            self.assertEqual(read_table(folder / 'b.json')[1], ['id', 'qty'])

    def test_max_rows_rejects_instead_of_truncating(self):
        with tempfile.TemporaryDirectory() as folder:
            src = Path(folder) / 'a.csv'
            src.write_text('qty\n1\n2\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, '초과'):
                read_table(src, max_rows=1)

    def test_join_and_duplicate_key(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            left, right = folder / 'a.csv', folder / 'b.csv'
            left.write_text('id,qty\na,10\nb,20\n', encoding='utf-8')
            right.write_text('id,defect\na,2\n', encoding='utf-8')
            rows, cols = join(left, right, 'id')
            self.assertEqual(cols, ['id', 'qty', 'right_defect'])
            self.assertEqual(rows[0]['right_defect'], '2')
            self.assertEqual(rows[1]['right_defect'], '')
            right.write_text('id,defect\na,2\na,4\n', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, '중복'):
                join(left, right, 'id')

    def test_markdown_report_ratio_groups(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / 'production.csv').write_text('line,quantity\nA,60\nB,40\n', encoding='utf-8')
            (folder / 'defects.csv').write_text('line,defect_count\nA,2\nB,3\n', encoding='utf-8')
            (folder / 'spec.json').write_text('''{
              "title":"품질 요약", "sources":[
                 {"name":"production","path":"production.csv"},
                 {"name":"defects","path":"defects.csv"}],
              "metrics":[
                 {"name":"총생산","source":"production","column":"quantity","operation":"sum"},
                 {"name":"총불량","source":"defects","column":"defect_count","operation":"sum"},
                 {"name":"불량률","operation":"ratio_percent","numerator":"총불량","denominator":"총생산"}],
              "groups":[{"name":"라인별 불량","source":"defects","by":"line","column":"defect_count","operation":"sum"}]}
            ''', encoding='utf-8')
            report = generate(folder / 'spec.json')
            self.assertIn('| 불량률 | 총불량 / 총생산 × 100 | 5 | % |', report)
            self.assertIn('| A | 2 |', report)
            self.assertIn('| B | 3 |', report)

    def test_report_refuses_invalid_numeric_data(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            (folder / 'data.csv').write_text('qty\nabc\n', encoding='utf-8')
            (folder / 'spec.json').write_text('''{"sources":[{"name":"data","path":"data.csv"}],"metrics":[{"name":"합계","operation":"sum","source":"data","column":"qty"}]}''', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, '숫자가 아닌'):
                generate(folder / 'spec.json')


if __name__ == '__main__':
    unittest.main()
