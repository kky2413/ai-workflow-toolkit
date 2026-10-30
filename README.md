# AI Workflow — 범용 작업 보조 도구

파일 구조 조사, CSV·JSON 데이터 요약, 결과 파일 확인을 위한 **로컬 Python 도구**와 Codex 사용 설명서를 모은 공개 저장소입니다.
특정 서비스나 문제의 완성품이 아니며, 예제 데이터·개인 자료·인증 정보는 포함하지 않습니다.

## 폴더 구성

| 위치 | 용도 |
| --- | --- |
| `scripts/` | 실행 가능한 Python 프로그램 3개 |
| `tests/` | Python 표준 라이브러리 기반 단위 테스트 |
| `docs/` | 한국어 사용 설명서·코드 리뷰·Codex 명령어·프롬프트 |
| `docs/templates/` | 계획·의사결정·완료 확인용 문서 양식 |
| `AGENTS.md` | 이 저장소에서 Codex가 참고할 작업 원칙 |

## 빠른 시작

Python 3.9 이상 필요. 추가 Python 패키지 설치 없이 실행합니다.

```bash
git clone https://github.com/kky2413/ai-workflow
cd ai-workflow
python3 -m unittest discover -s tests -v
python3 scripts/inventory.py .
```

Windows PowerShell에서는 환경에 따라 `python3` 대신 `python`을 사용하세요.

```powershell
python -m unittest discover -s tests -v
python scripts/inventory.py .
```

다른 폴더나 데이터 파일을 대상으로 분석하려면 명시적인 경로를 전달합니다.

```bash
python3 scripts/inventory.py /path/to/folder
python3 scripts/data_profile.py /path/to/data.csv
python3 scripts/verify_outputs.py --root /path/to/project --manifest /path/to/manifest.json
```

`verify_outputs.py`의 manifest는 `{"files":[{"path":"README.md","min_bytes":10}]}` 형태의 JSON 파일입니다. 확인할 파일을 직접 지정해야 하며, 내용의 정답 여부를 검사하지는 않습니다.

## 설명서

- [한글 퀵스타트](docs/QUICKSTART.md): 실행 순서, 코드 역할, 자주 발생하는 오류
- [Codex 명령어](docs/CODEX_COMMANDS.md): 슬래시 명령어와 터미널 명령어 구분
- [소스코드 리뷰](docs/CODE_REVIEW.md): 각 함수의 동작, 검증 범위, 제한
- [작업용 요청문](docs/WORKFLOW_PROMPTS.md): 분석·구현·디버깅·검증 프롬프트
- [작업 계획 양식](docs/templates/TASK_PLAN.md)
- [판단 기록 양식](docs/templates/DECISION_LOG.md)
- [완료 점검 양식](docs/templates/FINAL_CHECK.md)

## 사용 시 유의사항

- 도구는 로컬 파일을 읽고 표준 출력으로 결과를 보여 줍니다. 외부 API·원격 전송 기능이 없습니다.
- 분석 결과는 구조를 미리 확인하는 용도입니다. 데이터의 업무적 의미나 수치의 타당성은 별도로 검증하세요.
- 이 저장소의 `AGENTS.md`는 다른 상위 폴더나 무관한 프로젝트에 자동 적용되지 않습니다.
- 파일을 다루기 전 해당 환경의 접근 권한과 정보 보호 기준을 확인하세요.

## 여러 데이터 파일을 활용한 계산 및 보고서 작성

아래 두 프로그램은 기존 데이터 조사 도구와 독립적으로 사용할 수 있습니다. 입력 데이터와 보고서 규칙은 **사용자가 별도로 지정**해야 합니다.

- `scripts/merge_tables.py`: 공통 키를 이용해 두 파일의 열을 결합하여 CSV 생성
- `scripts/quality_report.py`: 여러 파일의 합계·평균·최솟값·최댓값·개수·비율 및 그룹별 표를 Markdown 보고서로 생성
- `scripts/tabular_io.py`: CSV·JSON 읽기, XLSX는 `openpyxl`이 설치된 경우에만 읽기

실행법, JSON 설정 파일의 작성 예시는 [다중 데이터 보고서 가이드](docs/REPORT_GUIDE.md)에서 확인하세요.

