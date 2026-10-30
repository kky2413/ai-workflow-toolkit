# Python 스크립트 코드 리뷰

저장소의 **실제 구현을 읽고 정리한 설명**입니다. 함수 동작과 제한을 명확히 구분합니다. 세 프로그램 모두 Python 표준 라이브러리만 사용하고, 외부 네트워크 통신 코드는 없습니다.

## 1. scripts/inventory.py — 파일 목록 조사

### 처리 방식
1. `build_inventory(root, max_files=2000)`가 경로를 정규화하고 폴더인지 확인합니다.
2. `root.rglob('*')`로 하위 파일을 조사합니다.
3. `.git`, `node_modules`, `__pycache__` 등 제외 대상은 목록에서 뺍니다.
4. 심볼릭 링크와 일반 파일이 아닌 항목을 제외합니다.
5. 파일 경로·확장자·크기를 모아 JSON으로 반환합니다.

```bash
python3 scripts/inventory.py .
python3 scripts/inventory.py /path/to/folder --max-files 100
```

### 검토 결과와 한계
- 파일 내용까지 읽거나 의미를 분류하지 않습니다.
- 출력 파일 수는 `--max-files`로 제한하지만 폴더 전체를 탐색하는 작업 자체가 즉시 중단되는 구조는 아닙니다.
- 저장소의 실제 데이터·로그 등을 다른 곳으로 보내지 않습니다.

## 2. scripts/data_profile.py — CSV·JSON 데이터 프로파일

### 처리 방식
1. `load_text()`가 UTF-8(BOM 포함), CP949 순서로 텍스트를 해석합니다.
2. `read_records()`가 CSV의 구분자를 탐지하거나 JSON 객체·객체 배열을 읽습니다.
3. `missing()`은 `null`과 빈 문자열을 결측으로 처리합니다.
4. `to_number()`는 유한한 수치만 숫자로 간주합니다. 숫자 문자열에 포함된 쉼표도 제거해 변환합니다.
5. `profile()`은 행·열 개수, 열별 결측·고유값·샘플값 및 완전히 숫자로 해석되는 열의 최소·최대·평균·합계를 계산합니다.

```bash
python3 scripts/data_profile.py /path/to/data.csv
python3 scripts/data_profile.py /path/to/data.json --max-rows 5000
```

### 검토 결과와 한계
- **전체 파일을 먼저 메모리에 읽고** `--max-rows`만큼만 통계를 계산합니다. 거대한 파일에서 메모리 제한에 유의해야 합니다.
- 결측 표기 `N/A`, `-`, `null`이라는 문자열 등은 자동으로 결측 처리하지 않습니다.
- 숫자와 문자가 혼합된 열에는 숫자 통계를 생성하지 않습니다.
- JSON 최상위 값은 객체 또는 객체들의 배열이어야 합니다. Excel·PDF·Word는 지원하지 않습니다.
- 계산된 통계는 데이터 의미나 모델의 정확성까지 검증하지 않습니다.

## 3. scripts/verify_outputs.py — 파일 존재 확인

### 처리 방식
1. `verify(root, manifest)`가 JSON manifest에서 `files` 배열을 읽습니다.
2. 각 항목에 `path`, 선택적으로 `min_bytes`를 지정합니다.
3. `..`·절대 경로·루트 바깥을 가리키는 경로를 거부합니다.
4. 지정된 파일이 존재하고 최소 크기를 충족하면 해당 항목을 통과 처리합니다.
5. 모든 항목을 통과하면 실행 종료 코드 0, 미통과 항목이 있으면 1을 반환합니다.

예시 manifest (직접 별도 파일로 저장):
```json
{"files":[{"path":"README.md","min_bytes":10}]}
```

```bash
python3 scripts/verify_outputs.py --root . --manifest /path/to/manifest.json
```

### 검토 결과와 한계
- 파일의 **존재와 크기**만 검사합니다. 출력 내용, 형식, 정답 여부는 확인하지 않습니다.
- manifest가 비어 있거나 구조가 잘못되면 오류가 발생합니다.
- 검사 대상은 프로젝트 루트 안의 상대 경로만 허용합니다.

## 4. tests/test_toolkit.py — 자동 테스트

현재 테스트는 총 5개입니다.

| 테스트 | 확인하는 동작 |
| --- | --- |
| `test_inventory_excludes_git` | `.git` 폴더 내용이 파일 목록에서 제외됨 |
| `test_csv_profile_statistics_and_missing` | CSV 숫자 통계 및 결측 계산 |
| `test_json_profile` | JSON 숫자 합계 계산 |
| `test_verify_outputs_pass_fail` | 존재하는 파일과 없는 파일을 구분 |
| `test_verify_rejects_parent_traversal` | 상위 경로 이동 문자열을 거부 |

실행:
```bash
python3 -m unittest discover -s tests -v
```

위 테스트가 통과하더라도 대용량 처리·모든 문자 인코딩·업무 데이터의 의미·복잡한 파일 형식까지 보장하지는 않습니다.

## 5. 활용 원칙
- 분석용 입력 경로를 명확히 지정하고, 생성된 JSON을 직접 확인하세요.
- 중요한 결과는 실제 데이터와 별도 계산·실행 테스트로 교차 검증하세요.
- 지원하지 않는 파일 형식은 전용 파서가 필요하며, 이 저장소에 해당 기능이 있다고 가정하지 마세요.

## 6. scripts/tabular_io.py — 파일 형식 통합 입력

- `read_table(path, max_rows, sheet)`는 CSV·JSON을 열과 행의 형태로 돌려줍니다. 중복·빈 열 이름, 너무 큰 행 수를 거부합니다.
- XLSX는 설치된 `openpyxl`을 이용해 첫 번째 시트 또는 지정 시트를 읽습니다. 수식 계산은 하지 않으며 저장된 캐시값만 읽습니다.

## 7. scripts/merge_tables.py — 명시적인 키로 열 결합

- `join(left_path,right_path,key,how,prefix)`는 두 파일에서 같은 이름의 키를 사용합니다.
- 오른쪽 키가 중복되거나 비어 있으면 오류를 반환하고, 오른쪽 열에는 접두사를 붙여 충돌을 방지합니다.
- 기본 `left` 방식은 왼쪽 모든 행을 유지합니다. 연결되지 않은 오른쪽 값은 빈 칸이므로 별도 확인이 필요합니다.
- 계산의 의미나 서로 다른 단위의 호환성은 검사하지 않습니다.

## 8. scripts/quality_report.py — 계산·Markdown 보고서

- `generate(spec_path)`는 설정 JSON의 `sources`, `metrics`, `groups`를 읽습니다.
- `sum`, `mean`, `min`, `max`, `count`, `count_nonmissing`, `ratio_percent`를 지원합니다.
- 숫자 계산에는 `Decimal`을 사용하고 숫자 아닌 값, 없는 열, 분모 0 등의 오류를 표시합니다.
- 파일별 원본 경로와 계산 방법을 Markdown 표에 기록합니다.
- 표의 정확한 업무적 해석, 외부 기준값과의 적합성, 품질 합격 판정은 자동 생성하지 않습니다.

## 9. tests/test_reporting.py — 신규 검증 5개

- CSV·JSON 읽기, 행 제한, 공통 키 결합·중복 감지, 복수 파일 비율·그룹별 보고서, 비정상 숫자 거부를 검사합니다.
- 기존 테스트와 새로운 검증 테스트를 합쳐 총 31개 단위 테스트를 정의했습니다. 실제 실행 결과는 테스트 명령으로 확인해야 합니다. XLSX 실제 파일·대용량 성능 검사는 자동 테스트 범위 밖입니다.


## 10. scripts/join_audit.py — 조인 위험 사전 예측
read_table로 두 데이터 파일을 읽고 지정한 복합키의 빈 값과 빈도를 계산합니다. 예상 inner/left/right/full 출력 행 수는 같은 키가 양쪽에 몇 번 나타나는지에 따라 계산합니다. 관계 유형의 유일성 조건을 검사합니다. 원본 파일은 수정하지 않으며, 조인 결과의 값 자체는 계산하지 않습니다.

## 11. scripts/compare_tables.py — 이전/이후 변경 개수
같은 열 이름을 가진 두 표에서 중복 없는 식별키를 만듭니다. 추가·삭제·변경된 행 수 및 변경 열별 개수를 출력합니다. 원시 데이터값과 ID 목록은 내보내지 않습니다. 숫자의 표기 방식이나 공백 정리는 하지 않습니다.

## 12. scripts/rule_check.py — 명시적인 숫자 상하한
규칙 JSON의 field/direction/limit/inclusive/reference를 모두 확인한 다음 숫자 행을 검사합니다. 숫자로 해석할 수 없는 행은 invalid로 구분합니다. 빈 규칙·빈 데이터는 통과가 아닙니다. 기준의 법적·업무적 적합성은 프로그램이 판단하지 못합니다.

## 13. scripts/environment_check.py — 실행 환경 확인
파이썬 버전, 명령어 존재 여부, 선택형 패키지를 읽기 전용으로 조회합니다. 패키지를 설치하거나 사용자 계정을 연결하지 않습니다.

## 14. scripts/http_smoke.py — 제한된 로컬 웹 점검
사용자가 명시한 localhost HTTP URL에만 GET 요청을 보내고 응답 상태를 읽습니다. 외부 호스트·프록시·자동 리다이렉트를 막습니다. 상태 코드가 정상이어도 앱의 화면·데이터 정확성이 보장되는 것은 아닙니다.

## 15. tests/test_advanced.py
복합키 중복, 결합 행 수 증가, 변경 비교, 숫자 기준 포함/제외, 그룹 비율, 외부 URL 차단 등 14개 상황을 검증하도록 구성했습니다. 테스트 파일이 존재한다는 사실과 실제 실행 통과는 구분합니다.

## 16. 자동 검증의 범위
.github/workflows/python-tests.yml은 Python 3.10·3.11·3.12에서 컴파일과 단위 테스트를 수행하도록 선언했습니다. GitHub Actions 설정 자체가 있다는 사실로 실행 통과를 보장하지 않습니다.

## 코드 작성 원칙
새 프로그램은 공개 저장소에서 확인한 범용적인 검증 아이디어를 참고해 **독립 구현**했습니다. 제3자 라이브러리 소스·자동 설치기·원격 MCP·외부 서비스 연동을 복사해 넣지 않았습니다.


## 17. scripts/json_structure_check.py — JSON 필드 계약

- JSON 객체 또는 객체들의 배열을 처리합니다.
- 설정의 fields(자료형), required(필수 필드), allow_extra(추가 필드 허용)를 확인합니다.
- 문자열·정수·일반 숫자·불리언·객체·배열·null을 구분합니다. boolean을 integer로 통과시키지 않습니다.
- 필드가 없거나 타입이 다르면 레코드 위치와 필드 이름만 보고합니다. 실제 원시 값을 출력하지 않습니다.
- 빈 배열은 통과 처리하지 않으며 JSON Schema 표준의 중첩·패턴·조합 등 고급 기능은 구현하지 않습니다.

## 18. tests/test_json_structure.py

JSON 구조 정상 입력, 필수 키 누락, 정수와 boolean의 구분, 빈 배열, 불허된 추가 필드의 5가지 테스트를 정의합니다. 기존 24개와 합쳐 총 31개입니다. 테스트가 정의됐다는 사실만으로 특정 머신에서의 통과를 주장하지 않습니다.


## 19. 수치 집계 누락값 정책

quality_report.py는 숫자 합계·평균·최솟값·최댓값에 누락값이 있으면 기본적으로 오류를 반환합니다. 해당 항목에 allow_missing: true를 명시해야 결측 제외 계산을 수행합니다. 데이터 프로파일을 먼저 보고 결측을 제외할 타당한 근거를 확인하세요. 가중 비율의 분자와 분모는 결측을 허용하지 않습니다.
