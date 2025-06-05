# 맥OS, 리눅스, WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# 윈도우
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 가상 환경 만들기
uv venv .venv

# 파이썬 버전 설정
uv venv -p 3.13

# 가상 환경 진입
source .venv/bin/activate

# 깃허브 커밋 템플릿 등록
# git commit 시 .gitmessage.txt 출력
git config --local commit.template .gitmessage.txt 

# 라이브러리 설치
uv pip install