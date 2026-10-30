# 빠른 시작 — Git·Python·Codex

이 문서는 로컬 개발 작업에서 저장소를 내려받고 포함된 프로그램을 실행하는 방법을 설명합니다.

## 1. 현재 위치와 파일 확인

Linux Bash:
```bash
pwd
ls -la
```

Windows PowerShell:
```powershell
pwd
ls
```

## 2. 저장소 내려받기

```bash
git clone https://github.com/kky2413/ai-workflow
cd ai-workflow
ls
```

`git clone`은 원격 저장소를 복제합니다. `.git` URL 접미사는 생략할 수 있습니다. 같은 이름의 폴더가 이미 있다면 다른 목적지 이름을 지정하세요.

```bash
git clone https://github.com/kky2413/ai-workflow ai-workflow-copy
```

## 3. 포함된 프로그램 실행

```bash
python3 --version
python3 scripts/inventory.py .
python3 -m unittest discover -s tests -v
```

`python3`가 없으면 `python --version`으로 Python 명령어를 확인하세요.

| 프로그램 | 용도 | 입력 | 확인할 출력 |
| --- | --- | --- | --- |
| `scripts/inventory.py` | 폴더의 파일 현황 | 폴더 경로 | 개수·크기·확장자·파일 목록(JSON) |
| `scripts/data_profile.py` | CSV·JSON의 데이터 구조 | `.csv` 또는 `.json` 경로 | 행·열·결측·숫자 통계(JSON) |
| `scripts/verify_outputs.py` | 필요한 파일의 존재·최소 크기 | 프로젝트 폴더 및 manifest JSON | 파일별 통과 여부(JSON) |

### 원하는 CSV·JSON 분석
```bash
python3 scripts/data_profile.py /path/to/data.csv
python3 scripts/data_profile.py /path/to/data.json
```

### 필요한 파일 확인
manifest JSON을 직접 만든 뒤 아래처럼 실행합니다.
```json
{"files":[{"path":"README.md","min_bytes":10}]}
```
```bash
python3 scripts/verify_outputs.py --root . --manifest /path/to/manifest.json
```

`passed: true`는 파일 존재·크기 검사 통과라는 뜻이며, 파일 내용까지 올바르다는 뜻은 아닙니다.

## 4. Codex 기본 사용

```bash
codex
```

Codex 입력창에서 `/status`로 현재 상태를 보고 `/model`로 제공되는 모델을 확인합니다. 자세한 설명은 [Codex 명령어](CODEX_COMMANDS.md)를 참고하세요.

예시 요청:
> 현재 작업 폴더의 구조와 README를 확인해 주세요. 사용할 수 있는 프로그램을 요약하고, 변경 없이 테스트를 실행해 실제 결과와 한계를 알려 주세요.

일반 터미널로 나가려면 Codex 입력창에서 `/exit` 또는 `/quit`을 사용합니다.

## 5. 자주 발생하는 오류

- `command not found`: 명령어가 설치되어 있지 않거나 PATH에 없습니다. 웹 기반 에디터에서는 파일 탐색기로 문서를 열 수 있습니다.
- `No such file`: `pwd`, `ls`로 현재 폴더와 대상 파일을 확인하세요.
- `Permission denied`: 권한과 파일 경로를 확인하고, 허용되지 않은 권한 변경으로 우회하지 마세요.
- `git clone` 폴더 충돌: 기존 폴더를 바로 삭제하지 말고 다른 목적지 이름을 사용하세요.

## 6. 더 읽어보기

- [소스코드 리뷰](CODE_REVIEW.md)
- [작업 요청문 모음](WORKFLOW_PROMPTS.md)
- [프로젝트 계획 양식](templates/TASK_PLAN.md)
