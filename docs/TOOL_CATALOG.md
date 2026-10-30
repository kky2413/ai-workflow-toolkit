# Python 도구 11개 — 입력·출력·실행 방법

**실행 위치:** 아래 명령어는 ai-workflow 저장소 루트 기준입니다. 명령어의 /data 등은 예시이며 실제 파일 경로로 바꾸세요. Linux는 python3, PowerShell은 python을 사용할 수 있습니다.

## 1. 환경 점검: environment_check.py

~~~bash
python3 scripts/environment_check.py
~~~

Python 버전·Git·Node·Codex 명령어 존재 여부와 선택형 Python 패키지 설치 여부를 JSON으로 출력합니다. *설치는 하지 않습니다.*

## 2. 폴더 조사: inventory.py

~~~bash
python3 scripts/inventory.py /data
~~~

파일명·크기·확장자·파일 수를 확인합니다. 파일 내용은 분석하지 않습니다. Git·캐시·의존성 폴더 일부를 제외합니다.

## 3. 단일 파일 구조: data_profile.py

~~~bash
python3 scripts/data_profile.py /data/production.csv
~~~

CSV·JSON 행/열, 결측, 고유값, 숫자 통계를 출력합니다. 대량 파일을 메모리에 올려 읽으며, 출력 수치는 값의 업무 의미를 보증하지 않습니다.

## 4. 표 데이터 공통 모듈: tabular_io.py

직접 실행하지 않는 **내부 라이브러리**입니다. 다른 스크립트가 read_table()을 호출합니다. CSV와 JSON 기본 지원, XLSX는 openpyxl이 기존에 설치된 경우 지원합니다. 입력 파일의 행 제한 초과·빈 헤더·중복 헤더를 거부합니다.

## 5. 이전/이후 비교: compare_tables.py

~~~bash
python3 scripts/compare_tables.py /data/before.csv /data/after.csv --keys item_id
python3 scripts/compare_tables.py /data/before.csv /data/after.csv --keys lot_id,wafer_id
~~~

같은 열 이름을 가진 파일 두 개의 **추가 행·삭제 행·변경 행·변경 열 개수**를 비교합니다. 원시 값·식별자를 결과에 포함하지 않습니다. 키 중복이나 열 구성 차이가 있으면 중단합니다. 숫자 표기, 앞자리 0, 공백을 임의 정규화하지 않습니다.

## 6. 두 표 연결 전 진단: join_audit.py

~~~bash
python3 scripts/join_audit.py --left /data/orders.csv --right /data/clients.csv --keys client_id --relationship many_to_one
~~~

오른쪽 키의 중복, 왼쪽 미매칭, 예상 출력 행 수를 계산합니다. 관계 유형: one_to_one / one_to_many / many_to_one / many_to_many. **실제로 데이터를 병합하지 않는 읽기 전용 도구**입니다.

## 7. 두 표 실제 병합: merge_tables.py

~~~bash
python3 scripts/merge_tables.py --left /data/a.csv --right /data/b.csv --key id --how left --output /data/merged.csv
~~~

공통 단일 키로 병합합니다. 오른쪽 키 중복은 오류로 처리합니다. left(기본)는 왼쪽 행 유지, inner는 양쪽 일치 행만 반환합니다. 연결된 오른쪽 열 이름에는 right_ 접두사가 붙습니다. 복합키 병합은 지원하지 않습니다.

## 8. 계산과 보고서: quality_report.py

~~~bash
python3 scripts/quality_report.py --config /data/report_spec.json --output /data/report.md
~~~

JSON 설정에서 지정된 파일과 열을 기준으로 합계·평균·개수·최솟값·최댓값·비율 및 Markdown 표를 생성합니다. 그룹별 ratio_percent는 **그룹 내부 분자 합계 / 분모 합계 ×100**입니다. 설정 파일 작성법은 [보고서 가이드](REPORT_GUIDE.md)를 참고하세요.

## 9. 규칙 기반 수치 판정: rule_check.py

~~~bash
python3 scripts/rule_check.py --config /data/rules.json
~~~

규칙 JSON 예시:
~~~json
{
  "source": "data.csv",
  "rules": [
    {
      "name": "명시된 상한",
      "field": "measurement",
      "direction": "max",
      "limit": 100,
      "inclusive": true,
      "reference": "사용자가 확인한 실제 기준 문서의 조항"
    }
  ]
}
~~~

100은 문법을 설명하기 위한 가상 수치입니다. 기준을 확인한 경우에만 실제 적용하세요. 규칙 수 0, 입력 0행은 정상 합격으로 처리하지 않습니다.

## 10. 필수 파일 존재 확인: verify_outputs.py

~~~bash
python3 scripts/verify_outputs.py --root /path/to/project --manifest /path/to/manifest.json
~~~

manifest 예시:
~~~json
{"files": [{"path": "report.md", "min_bytes": 10}]}
~~~

파일 존재·최소 용량만 확인합니다. **내용 정확성이나 출력 형식 전체를 검사하는 기능은 아닙니다.**

## 11. 로컬 서버 확인: http_smoke.py

~~~bash
python3 scripts/http_smoke.py http://127.0.0.1:3000/health
~~~

명시한 localhost의 HTTP 응답 상태를 확인합니다. 사용자가 실행을 요청한 경우에만 수행하세요. 외부 도메인·외부 네트워크·자동 리다이렉트 추적은 허용하지 않습니다.

## 반환값 이해하기

- 파일 비교: 0 동일, 1 차이, 2 실행 입력 오류
- 키 진단: 0 선언한 관계 충족, 1 관계 위반 또는 빈 입력, 2 입력 오류
- 규칙 검사: 0 확인된 규칙 통과, 1 위반·유효하지 않은 행·빈 입력, 2 규칙 오류
- 로컬 HTTP 점검: 0 2xx·3xx 정상 응답(자동 이동하지 않음), 1 HTTP 실패, 2 인수 또는 연결 오류
- 파일 점검: 0 선언한 경로·크기 충족, 1 실패, 2 잘못된 manifest

위의 '통과'는 도구가 확인한 조건만 가리킵니다. 별도의 사업·품질·보안상 완전성을 뜻하지 않습니다.
