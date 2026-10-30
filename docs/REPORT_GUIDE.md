# 여러 파일 분석·Markdown 보고서 가이드

이 문서는 별도의 설치가 거의 없는 로컬 데이터 처리 흐름을 설명합니다. 프로그램이 보고서의 업무적 기준이나 합격 여부를 자동으로 추정하지는 않습니다.

## 1. 지원 범위

| 입력 | 지원 | 비고 |
| --- | --- | --- |
| CSV | 기본 지원 | UTF-8(BOM 포함) 또는 CP949 |
| JSON | 기본 지원 | 객체 또는 객체 배열 |
| XLSX | 선택 지원 | 해당 Python 환경에 `openpyxl`이 이미 설치되어 있어야 함 |
| XLS·PDF·DOCX | 미지원 | 별도 도구가 필요함 |

XLSX 수식은 이 프로그램이 다시 계산하지 않습니다. 파일에 저장된 캐시 값만 읽습니다.

## 2. 데이터 2개 연결하기

예를 들어 생산 데이터와 검사 데이터 모두 `lot_id` 열이 있을 때:

```bash
python3 scripts/merge_tables.py --left /data/production.csv --right /data/inspection.csv --key lot_id --output /data/merged.csv
```

- `--how left`(기본): 왼쪽 행을 모두 유지하고 오른쪽과 매칭하지 못한 값은 빈 칸입니다.
- `--how inner`: 두 파일 모두에 키가 있는 행만 남깁니다.
- `--right-prefix inspection_`: 오른쪽 열에 붙일 접두사를 변경합니다.
- 오른쪽 데이터에 중복된 키나 빈 키가 있으면 오류가 납니다.
- 같은 의미의 키인데 열 이름이 다르면, 이름 정리 등 사전 처리가 필요합니다.
- 이미 존재하는 출력 파일은 덮어쓰지 않습니다.

## 3. 여러 파일로 지표·보고서 만들기

**설정 JSON**을 사용자 데이터와 같은 작업 폴더에 별도로 작성합니다. 아래 JSON은 문법 안내일 뿐 실제 데이터 파일은 저장소에 포함되어 있지 않습니다.

```json
{
  "title": "데이터 요약",
  "sources": [
    {"name": "production", "path": "production.csv"},
    {"name": "defects", "path": "defects.csv"}
  ],
  "metrics": [
    {"name": "총생산", "source": "production", "column": "quantity", "operation": "sum", "unit": "개"},
    {"name": "총불량", "source": "defects", "column": "defect_count", "operation": "sum", "unit": "개"},
    {"name": "불량률", "operation": "ratio_percent", "numerator": "총불량", "denominator": "총생산", "unit": "%"}
  ],
  "groups": [
    {"name": "라인별 불량", "source": "defects", "by": "line", "column": "defect_count", "operation": "sum"}
  ]
}
```

두 CSV 파일이 실제로 존재하고 각 열 이름이 정확히 일치해야 합니다. **불량수량 / 생산수량 × 100**이 해당 데이터의 올바른 불량률 정의인지도 먼저 확인해야 합니다.

```bash
python3 scripts/quality_report.py --config /data/report_spec.json --output /data/report.md
```

생성된 `report.md`에는 원본 파일, 행·열 수, 계산식, 지표값, 그룹별 Markdown 표가 들어갑니다. 해당 파일을 에디터에서 열어 확인하세요.

## 4. 지원 계산식

| 연산 | 뜻 | 주의할 점 |
| --- | --- | --- |
| `count` | 행 수 | 수량 합계와 다름 |
| `count_nonmissing` | 열의 비어 있지 않은 값 수 | 결측 정의 확인 |
| `sum` | 숫자 합계 | 숫자가 아닌 값이 있으면 오류 |
| `mean` | 비어 있지 않은 숫자의 평균 | 가중 평균이 아님 |
| `min`, `max` | 최소·최대 | 단위 확인 |
| `ratio_percent` | 앞선 두 지표의 비율 ×100 | 분모 0이면 오류 |
| `groups` | 선택 열별 그룹 집계 | 그룹 열 이름 필수 |

사용 가능한 파일 하나당 최대 행 수 기본값은 100,000행입니다. 이를 초과하면 **부분 계산 대신 오류**를 반환합니다. 필요시 설정 JSON의 `max_rows` 값을 조정하세요. 매우 큰 데이터는 메모리 한계가 있을 수 있습니다.

## 5. 결과의 의미 검증

- 생산수량과 불량수량이 같은 기간·공정·대상에 해당하는지 확인하세요.
- 데이터별 집계 수준(행 하나가 제품 1개인지 로트 1개인지)을 확인하세요.
- 불량이 중복 집계되거나 검사 표본만 포함되어 있는지 점검하세요.
- 규격 상한·하한이나 합격 기준이 없으면 합격·불합격을 임의로 표시하지 마세요.
- 표의 값과 직접 계산한 값, 원본 데이터의 합계를 교차 확인하세요.

## 6. 자동 테스트

```bash
python3 -m unittest discover -s tests -v
```

총 24개 단위 테스트를 정의했습니다. 사용 환경에서 직접 실행해 실제 결과를 확인하세요. 별도의 샘플 데이터 파일을 공개 저장소에 저장하지 않고, 테스트 실행 중 임시 파일을 만들어 사용합니다.


## 7. 그룹별 가중 비율

단순한 행별 비율 평균이 아니라 그룹의 분자·분모를 합산하는 계산을 지원합니다. 아래 예시의 실제 데이터에는 line, tested, passed 열이 존재해야 합니다.

~~~json
{
  "title": "그룹별 통과율",
  "sources": [{"name": "records", "path": "records.csv"}],
  "groups": [{
    "name": "라인별 통과율",
    "source": "records",
    "by": "line",
    "operation": "ratio_percent",
    "numerator_column": "passed",
    "denominator_column": "tested"
  }]
}
~~~

각 그룹의 계산은 SUM(passed)/SUM(tested)×100입니다. 분모가 0이면 오류로 처리합니다. 분자·분모가 같은 모집단인지, 중복 검사 기록인지 등을 확인해야 합니다.

## 8. 잘못된 병합을 피하는 방법

병합 전에 join_audit.py로 연결 키 유일성, 미매칭, 예상 행 수를 먼저 확인하세요. merge_tables.py는 **단일 키** 결합만 지원하므로 복합키가 필요하면 명시적으로 맞는 구현을 추가해야 합니다.

별도 저장소에 합성 예제 파일을 넣지 않았습니다. 테스트 파일은 unittest 실행 시 임시 디렉터리 안에서 생성합니다.
