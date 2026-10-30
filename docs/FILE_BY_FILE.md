# 파일별 설명 — 무엇이며 언제 읽고 실행하나요?

모든 항목은 **기능·사용 시점·한계** 순서로 설명합니다.

## 최상위 파일
1. **README.md** — 전체 구성도와 주요 문서 링크. 저장소 첫 진입 시 읽습니다. 실제 프로젝트 README를 대체하지 않습니다.
2. **AGENTS.md** — Codex의 작업 원칙: 원본 보존, 작은 수정, 독립 검증, 권한 준수. 이 폴더 밖의 지침으로 자동 적용되지 않습니다.
3. **.gitignore** — 캐시·임시 결과·환경 파일 등 일부 항목을 Git 추적에서 제외합니다. 이미 추적된 파일의 안전성을 보장하지 않습니다.

## Python 실행·공통 모듈
4. **scripts/inventory.py** — 폴더 파일 개수·크기·확장자 파악. 파일 목록이 낯설 때 사용하며 데이터 해석은 하지 않습니다.
5. **scripts/data_profile.py** — CSV·JSON의 숫자 통계와 결측 구조 요약. 데이터를 받자마자 열 이름을 확인할 때 좋습니다. 대규모 파일 성능에 주의하세요.
6. **scripts/tabular_io.py** — CSV·JSON·선택형 XLSX를 읽는 공통 부품. 직접 CLI 실행하지 않고 다른 코드가 가져다 씁니다. Excel은 openpyxl 필요.
7. **scripts/compare_tables.py** — 두 데이터 버전의 추가·삭제·변경 행 개수. 변경 이력 점검에 쓰고, raw 값은 출력하지 않습니다.
8. **scripts/join_audit.py** — 데이터 연결 전에 키 중복·미매칭·출력 행 증가를 예측합니다. 실제 병합은 하지 않습니다.
9. **scripts/merge_tables.py** — 단일 키 기준으로 CSV로 실제 병합합니다. 복합키를 지원하지 않고 오른쪽 키의 중복은 거부합니다.
10. **scripts/quality_report.py** — JSON 설정으로 수치 계산·그룹별 집계·Markdown 표 작성. 사용자가 직접 열과 계산식을 지정해야 합니다.
11. **scripts/rule_check.py** — 상한·하한·경계 포함 여부·근거가 주어진 행별 숫자 판정. 규격이 없으면 사용하지 않습니다.
12. **scripts/verify_outputs.py** — 원하는 결과 경로와 최소 파일 크기 검사. 파일 내용의 정답 여부는 알 수 없습니다.
13. **scripts/environment_check.py** — Python 버전·명령·설치 모듈 현황을 읽기 전용으로 조사합니다. 프로그램을 설치하지 않습니다.
14. **scripts/http_smoke.py** — localhost의 HTTP 상태 확인. 웹/API 개발 과제일 때만 이용하고 원격 웹은 접근하지 않습니다.

## 자동 테스트·유지 관리
15. **tests/test_toolkit.py** — 원래의 파일 조사·프로파일·출력 검사 5개 테스트입니다.
16. **tests/test_reporting.py** — 데이터 읽기·병합·보고서 작성과 실패 입력 5개 테스트입니다.
17. **tests/test_advanced.py** — 중복 키, 변경 비교, 규격 경계, 그룹 비율, 안전한 로컬 점검을 포함한 추가 테스트입니다.
18. **.github/workflows/python-tests.yml** — 저장소 코드가 바뀌면 GitHub에서 Python 버전별 정적 컴파일·테스트를 실행하도록 정의한 유지 관리 설정입니다. 실제 과제 파일은 포함하지 않습니다.

## 한국어 설명 문서
19. **docs/START_HERE.md** — 처음 시작할 때 따라갈 길잡이. 무엇을 먼저 읽고 어떤 도구를 골라야 하는지 설명합니다.
20. **docs/QUICKSTART.md** — Bash·PowerShell 실행 명령, 폴더 경로, 기본 도구와 흔한 오류를 다룹니다.
21. **docs/CODEX_COMMANDS.md** — Codex 슬래시 명령어와 터미널 명령어의 차이. 현재 설치 버전의 지원 여부가 우선입니다.
22. **docs/TOOL_CATALOG.md** — 11개 코드의 실제 실행 명령어·입력과 출력·주의사항을 모았습니다.
23. **docs/CODE_REVIEW.md** — Python 함수가 하는 일, 지원 형식, 검증 범위, 제한사항을 코드 관점에서 설명합니다.
24. **docs/REPORT_GUIDE.md** — report_spec.json 작성과 비율·그룹별 보고서 예제입니다.
25. **docs/DATA_INTEGRITY.md** — 데이터 집계 단위, 조인 중복, 분모, 식별번호, 기준값 검증 방법을 설명합니다.
26. **docs/WORKFLOWS.md** — 데이터·변경 비교·웹 앱·자동화·문서 작업을 구분해 실제 수행 순서를 제안합니다.
27. **docs/WORKFLOW_PROMPTS.md** — 요구 분석·구현·오류 수정·검증 등을 Codex에 요청하는 짧은 문장 모음입니다.
28. **docs/SAFE_USE.md** — 외부 전송·권한·원본 보존과 검증하지 않은 성공 주장 방지 원칙입니다.
29. **docs/FILE_BY_FILE.md** — 바로 지금 읽는 전체 파일 사용 설명서입니다.

## 빈 작업 양식
30. **docs/templates/TASK_PLAN.md** — 목표·입력·검증·단계별 진행 계획 기록.
31. **docs/templates/DECISION_LOG.md** — 선택 이유, 고려한 대안, 실제 근거 기록.
32. **docs/templates/FINAL_CHECK.md** — 파일·검증·누락·비밀 정보 최종 점검.
33. **docs/templates/DATA_CONTRACT.md** — 키·행 단위·분자/분모·결측·날짜·단위의 합의 기록.
34. **docs/templates/REQUIREMENTS.md** — 필수조건과 검증 증거를 1:1 연결.
35. **docs/templates/HANDOFF.md** — 새 대화·교대 인원에게 실제 진행 상태 전달.

## 선택형 Codex Skill
36. **skills/task-framing/SKILL.md** — 요구사항을 사실·가정·질문·완료 조건으로 분리.
37. **skills/data-integrity/SKILL.md** — 데이터 누락·중복·분모·조인 관계를 점검.
38. **skills/verify-evidence/SKILL.md** — 실행한 테스트와 미검증 항목을 구분.
39. **skills/session-handoff/SKILL.md** — 세션 변경 때 실제 코드와 기록을 대조해 인계.

Skill은 자동 설치되지 않습니다. 필요한 하나만 Codex에게 **그 파일을 읽어 달라**고 요청할 수 있습니다. 특정 Skill의 자동 발견은 환경·설치 경로에 따라 달라집니다.

**빠르게 쓰는 순서:** START_HERE → TOOL_CATALOG → 현재 유형의 WORKFLOWS → 해당 스크립트 → 필요한 경우 CODE_REVIEW 또는 Skill. 불필요한 문서는 열지 않아도 됩니다.
