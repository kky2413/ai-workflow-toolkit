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
