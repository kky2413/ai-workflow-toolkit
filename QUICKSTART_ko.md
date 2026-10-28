# 10분 시작 가이드 (Windows PowerShell / VS Code)

## 1. 먼저 로컬에서 실행하기

1. 받은 `ai-workflow-toolkit.zip` 파일의 압축을 풀어 `ai-workflow-toolkit` 폴더를 만든다.
2. VS Code에서 해당 폴더를 연다: **파일 > 폴더 열기**.
3. **터미널 > 새 터미널**을 열고 아래 명령을 순서대로 실행한다.

```powershell
python --version
python -m unittest discover -s tests -v
python scripts/inventory.py examples
python scripts/data_profile.py examples/sample_sales.csv
python scripts/verify_outputs.py --root . --manifest examples/manifest.sample.json
```

실패 시에는 오류 메시지를 그대로 확인하고 원인을 찾아 수정한다. 파일이 없는 폴더에서 실행하면 실패한다. `pwd`로 현재 위치를 확인한다.

## 2. 개인 GitHub에 새 공개 저장소 만들기 (시험 **전**에만)

1. GitHub에 로그인해 https://github.com/new 로 이동한다.
2. Repository name: `ai-workflow-toolkit`
3. Visibility: **Public** 선택.
4. **Add a README**, `.gitignore`, license 자동 생성 옵션은 **체크하지 않는다** (이미 파일이 포함돼 있음).
5. **Create repository** 클릭.
6. 터미널에서 현재 폴더가 `ai-workflow-toolkit`인지 `pwd`로 확인하고 아래 명령 실행.

```powershell
git init -b main
git add .
git status
git commit -m "Add public AI workflow toolkit"
git remote add origin https://github.com/kky2413/ai-workflow-toolkit.git
git push -u origin main
```

- Git 사용자 이름·이메일이 설정되지 않았으면 Git의 안내에 따라 설정한다.
- `git push`에는 GitHub 인증이 필요할 수 있다.
- `git status`에서 **예상치 못한 파일이 staged되지 않았는지 반드시 확인**한다. 특히 비공개 파일, 키, 토큰을 절대 공개하지 않는다.
- GitHub 저장소가 만들어진 뒤 URL `https://github.com/kky2413/ai-workflow-toolkit`을 열어 파일 목록을 확인한다.
- 이미 같은 이름의 저장소가 있거나 remote가 설정돼 있으면 `git remote add`를 반복하지 않는다. 기존 설정을 확인한다.

## 3. 공개 코드 가져오기 연습

로컬 연습 환경 또는 GitHub 공개 도구 다운로드가 명시적으로 허용된 환경에서만:

```powershell
git clone https://github.com/kky2413/ai-workflow-toolkit.git
```

실제 시험에서 플랫폼에서 제공하는 규칙과 작업환경 설정을 우선 적용한다. **시험 문제·데이터·답안·결과물을 GitHub에 올리거나 외부로 전송하지 않는다.** 시험 중 Git Push는 금지다. 또한 제공된 환경에서 추가 설치나 외부 접근이 제한될 수 있다.

## 4. Codex 활용 연습

Codex가 설치·인증된 **개인 연습 환경**에서:

```powershell
codex
```

예시 프롬프트:

> 이 폴더의 README.md와 AGENTS.md를 읽고 목적을 한 문단으로 요약해 줘. scripts 폴더의 CLI 도구 3개를 파악하고, 각 도구가 무엇을 검사하는지 알려줘. 파일을 수정하지 말고 테스트 실행 결과를 알려줘.

GitHub에 공개하기 전에는 오직 범용 도구와 합성 예시 데이터만 남겨야 한다.
