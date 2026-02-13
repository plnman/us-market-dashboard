# US Market Dashboard

AI 기반 미국 주식 시장 분석 대시보드

## 기능
- 📊 Smart Money Picks - AI와 퀀트 분석 결합
- 💰 ETF Fund Flows - 실시간 자금 흐름 분석
- 🎯 AI 투자 분석 - 종목별 상세 분석

## 라이브 데모
- 일반 모드: https://your-app.onrender.com
- 뷰어 모드: https://your-app.onrender.com/?mode=viewer

## 로컬 실행

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경 변수 설정
# .env 파일 생성 후 GOOGLE_API_KEY 추가

# 3. 서버 시작
python flask_app.py

# 4. 브라우저 접속
http://localhost:5001
```

## 배포
Render.com에 자동 배포됨

## 환경 변수
- `GOOGLE_API_KEY`: Google Generative AI API 키

## 뷰어 모드
읽기 전용 모드: URL에 `?mode=viewer` 추가

## 라이선스
MIT
