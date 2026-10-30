# 처음 시작하기

## 1. 도구보다 실제 작업 내용이 먼저입니다

일반 터미널에서 현재 위치와 파일을 확인합니다.

~~~bash
pwd
ls -la
cat README.md
~~~

웹 IDE에서 일부 명령어가 없다면 파일 탐색기에서 README를 직접 열면 됩니다.

## 2. 별도 참고 폴더에 받아 둡니다

~~~bash
git clone --depth 1 https://github.com/kky2413/ai-workflow ai-workflow-reference
~~~

동일 이름의 폴더가 있으면 기존 파일을 삭제하지 말고 경로를 확인합니다. 참고 도구의 README와 실제 프로젝트의 README는 구분해야 합니다.

## 3. 필요한 도구만 고릅니다

| 상황 | 도구 |
| --- | --- |
| 파일 구조를 모른다 | inventory.py |
| CSV·JSON 상태를 알고 싶다 | data_profile.py |
| 데이터 파일이 두 버전이다 | compare_tables.py |
| 서로 다른 표를 연결해야 한다 | join_audit.py → merge_tables.py |
| 계산과 표가 필요하다 | quality_report.py |
| 명확한 상한·하한 기준이 있다 | rule_check.py |
| 출력 파일을 확인한다 | verify_outputs.py |
| 개발 환경이 낯설다 | environment_check.py |
| 로컬 웹 서버가 동작하는지 본다 | http_smoke.py |

Python 파일은 scripts/ 폴더 안에 있습니다. 구체적인 명령은 [TOOL_CATALOG.md](TOOL_CATALOG.md)를 참고하세요.

## 4. Codex에 지시하는 방법

다음은 **Codex 채팅에 보내는 문장**입니다.

> 현재 프로젝트의 README와 파일을 먼저 살펴봐 주세요. 참고 폴더 ai-workflow-reference/docs/TOOL_CATALOG.md를 읽고 이번 작업에 필요한 도구만 제안해 주세요. 수정하기 전에 필수 산출물과 불명확한 기준을 알려 주세요. 근거 없는 계산이나 외부 자료 전송은 하지 마세요.

폴더 이름이 다르면 실제 경로로 바꾸세요. 다른 폴더에 있는 AGENTS 지침은 자동 적용된다고 가정하면 안 됩니다.

## 5. 기본 질문 다섯 개
- 무엇을 만들어야 하나요?
- 입력의 출처·행 의미·단위는 무엇인가요?
- 어떤 조건은 확정이고 어떤 조건은 확인이 필요한가요?
- 무엇을 실행하면 결과를 검증할 수 있나요?
- 어디에 어떤 이름으로 결과를 저장해야 하나요?

작업이 단순하다면 양식을 모두 작성하기보다 바로 필요한 기능을 수행하세요.

## API나 자동화의 JSON 출력이 필요하면

**scripts/json_structure_check.py**로 JSON 필수 키·자료형을 점검할 수 있습니다. 설정 JSON 작성법은 [도구 설명](TOOL_CATALOG.md)의 12번을 참고하세요.
