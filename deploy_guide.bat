@echo off
echo ====================================
echo GitHub 업로드 준비
echo ====================================
echo.

echo [단계별 가이드]
echo.

echo 1. GitHub 리포지토리 생성
echo    - https://github.com/new 접속
echo    - Repository name: us-market-dashboard
echo    - Public 선택
echo    - "Create repository" 클릭
echo.

echo 2. Git 초기화 및 커밋
echo.
cd /d %~dp0

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Git이 설치되지 않았습니다!
    echo https://git-scm.com/download/win 에서 다운로드
    echo.
    pause
    exit /b
)

if not exist .git (
    echo Git 초기화 중...
    git init
    echo.
)

echo 파일 추가 중...
git add .
echo.

echo 커밋 생성 중...
git commit -m "Initial commit: US Market Dashboard"
echo.

echo 3. GitHub 연결 및 푸시
echo.
echo 다음 명령어를 실행하세요 (YOUR_USERNAME을 본인 GitHub 아이디로):
echo.
echo git remote add origin https://github.com/YOUR_USERNAME/us-market-dashboard.git
echo git branch -M main
echo git push -u origin main
echo.

echo ====================================
echo 다음 단계: Render.com 배포
echo ====================================
echo.
echo 1. https://render.com 가입/로그인
echo 2. "New" - "Web Service" 클릭
echo 3. GitHub 리포지토리 연결
echo 4. 설정:
echo    - Name: us-market-dashboard
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: gunicorn flask_app:app
echo 5. Environment Variables 추가:
echo    - GOOGLE_API_KEY: [당신의 API 키]
echo 6. "Create Web Service" 클릭
echo.

pause
