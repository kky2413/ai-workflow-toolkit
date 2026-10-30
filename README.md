# AI Workflow — 범용 로컬 작업 키트

낯선 프로젝트의 요구사항을 확인하고, 데이터를 분석하고, 코드를 검증하고, 결과를 설명하도록 돕는 **한국어 문서와 독립형 Python 도구**를 모았습니다. 특정 산업·평가·문제의 정답은 포함하지 않습니다.

## 30초 시작

~~~bash
git clone --depth 1 https://github.com/kky2413/ai-workflow
cd ai-workflow
python3 scripts/environment_check.py
python3 -m unittest discover -s tests -v
~~~

PowerShell에서는 Python 명령이 python일 수 있습니다. **가장 먼저 [처음 시작](docs/START_HERE.md)을 읽으세요.**

## 구성

| 폴더·파일 | 역할 |
| --- | --- |
| **scripts/** | 데이터·파일·로컬 서비스 점검용 Python 도구 12개(공통 라이브러리 포함) |
| **tests/** | 임시 데이터를 만들어 검사하는 단위 테스트 4개 파일 |
| **docs/** | 한국어 실행법·코드 검토·업무 유형별 흐름·안전 안내 |
| **docs/templates/** | 필요할 때만 선택하는 빈 기록 양식 |
| **skills/** | Codex에 직접 읽혀줄 수 있는 선택형 작업 절차서 |
| **AGENTS.md** | 이 저장소의 작업 원칙 |
| **.github/workflows/** | 공개 저장소 유지 관리용 자동 테스트 |
| **.gitignore** | 일부 임시·비밀 파일의 Git 추적 제외 규칙 |

## 작업별 바로 가기

- [도구 전체 사용법](docs/TOOL_CATALOG.md): 12개 Python 코드와 명령어
- [작업 유형별 업무 흐름](docs/WORKFLOWS.md): 데이터·보고서·웹·자동화·문서
- [데이터 정확성](docs/DATA_INTEGRITY.md): 결합 전 행 수, 중복·분모·단위 검사
- [Codex 명령어](docs/CODEX_COMMANDS.md): 모델·상태·리뷰·종료
- [Codex 프롬프트 예시](docs/PROMPT_EXAMPLES.md): 작업 분석 → 구현 → 이해도 확인 → 스스로 설명
- [파일별 설명](docs/FILE_BY_FILE.md): 모든 파일의 구성과 활용
- [안전 사용 안내](docs/SAFE_USE.md): 권한, 전송, 원본 보존, 금지 동작
- [소스코드 검토](docs/CODE_REVIEW.md): 코드의 실제 기능과 한계

## 핵심 안전 원칙

1. 현재 작업의 README·기존 프로젝트·사용 권한이 이 저장소보다 우선합니다.
2. 원본 데이터와 비밀 정보를 공개 저장소나 외부 서비스로 전송하지 않습니다.
3. 기준값과 계산 단위를 추측하지 않고, 확인된 식을 적용합니다.
4. 실제로 실행하지 않은 테스트를 성공했다고 기록하지 않습니다.
5. 승인 우회·전역 설정 변경·MCP 자동 설치·외부 모델 연결 기능이 없습니다.
6. 도구 사용 시 선택한 파일만 활용하며 기존 프로젝트를 덮어쓰지 않습니다.

Python 3.10 이상을 기본 대상으로 하며, 대부분 표준 라이브러리만 사용합니다. XLSX 입력은 openpyxl이 **이미 설치된 경우**만 지원합니다. PDF·DOCX·시각적 차트 완성 기능은 기본 제공하지 않습니다.

- JSON 구조 검증: **json_structure_check.py** (필수 필드·자료형·추가 필드 확인, JSON Schema 전체 구현은 아님)
