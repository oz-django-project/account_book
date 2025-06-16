# 🧾 가계부 API

이 프로젝트는 Django 및 DRF, Celery, Redis 등을 활용한 가계부 애플리케이션으로, 백엔드 전반에 대한 학습과 실습을 목적으로 개발되었습니다.
수입/지출 데이터 관리, 기간별 소비 분석, AI 요약 생성, 알림 기능 등을 포함하여, 실제 서비스 수준의 구조를 고려하며 설계하였습니다.

---

## 📦 주요 기술 스택

- **Python** 3.13+
- **Django** 5.2
- **Django REST Framework** 3.16
- **drf-spectacular** / **drf-yasg**: API 문서 자동화
- **Pandas + Matplotlib** (데이터 처리 및 시각화)
- **Celery + Redis** (비동기 처리)
- **Google Gemini** (AI 요약)
- **MySQL** 연동 (`mysqlclient`, `pymysql`)
- **Black**, **isort**: 코드 포맷팅 / 정렬

---

## 🚀 설치 및 실행

```bash
# 1. 가상환경 설정
git clone https://github.com/oz-django-project/account_book.git
cd account_book
uv venv .venv

# 2. 패키지 설치
uv pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env  # 또는 직접 작성
# 예: DB 정보, SECRET_KEY 등

# 4. 마이그레이션
python manage.py migrate
python manage.py createsuperuser

# 5. celery 실행
celery -A config worker --loglevel=info

# 6. 서버 실행
python manage.py runserver

# 7. 테스트 실행
python manage.py test
````
![ERD 다이어그램](images/erd.png)

## user 테이블
- 사용자 계정을 저장하는 테이블입니다. 
로그인에 사용되는 이메일, 비밀번호 및 연락처 등의 정보를 포함합니다.
또한 관리자 / 스태프 여부 및 활성화 / 비활성화 여부도 포함되어 있습니다.

## account 테이블
- 사용자가 보유한 실제 계좌 정보를 저장하는 테이블입니다.
각 계좌는 특정 사용자와 연결되며, 은행 코드, 계좌 유형 및 잔액 등의 정보를 포함합니다.

## transactionhistory 테이블
- 각 계좌의 거래 내역을 저장하는 테이블입니다.
거래 금액, 거래 후 잔액, 거래 내역 및 입출금 타입 등의 정보를 포함합니다.

## analysis 테이블
- 거래 내역 기반으로 분석 내용을 저장하는 테이블입니다.
분석 기간, 소비 / 수입, ai 요약, 그래프 이미지 등의 정보를 포함합니다.

## notification 테이블
- 분석 그래프가 생성되면 알림을 생성하고 저장하는 테이블입니다.
메세지, 읽음 여부 등의 정보를 포함합니다.

```
users (1)
  ├──< accounts (N)
  │       └──< transaction_history (N)
  └──< analysis (N)
  └──< notifications (N)

```

![서비스 플로우차트](images/flowchart.png)

## 회원가입 / 로그인 / 로그아웃 로직 설명

### 회원가입(Sign Up)
1. 사용자가 이메일, 비밀번호 등 정보 입력
2. 서버는 유효성 검사 수행
3. 이메일 중복 여부 확인
4. 문제가 없으면 DB에 저장
5. 성공 메시지 반환

### 로그인(Login)
1. 사용자 입력 → 이메일 / 비밀번호 확인
2. 정보가 일치하면 JWT 토큰 발급
3. 클라이언트에 토큰 반환

### 로그아웃(Logout)
1. 클라이언트 측에서 토큰 삭제
2. (옵션) 서버에서 블랙리스트 처리
3. 성공 응답

# ☑️ 주요 기능
- 회원가입 / JWT 토큰 로그인 / 로그아웃

- 마이페이지 조회 / 수정

- 비밀번호 변경

- 계좌 생성 / 삭제 / 조회

- 거래 내역 등록 / 조회 / 수정 / 삭제

- 거래 필터링 (타입, 금액 범위 등)

- 비활성 계정 복구

- 거래 내역 기반으로 주간 및 월간 분석 그래프 생성

- ai를 이용한 분석 내용 요약 및 피드백

# 📁 프로젝트 구조
```
account_book/
├── accounts/         # 계좌 및 거래 내역 관리
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── urls.py

├── analysis/         # 수입/지출 분석 기능
│   ├── models.py
│   ├── analyzers.py
│   ├── tasks.py      # Celery 비동기 작업
│   ├── views.py
│   └── urls.py

├── notification/     # 알림 기능
│   ├── models.py
│   ├── signals.py
│   └── views.py

├── users/            # 사용자 인증 및 정보
│   ├── models.py
│   ├── authentication.py
│   └── views.py

├── config/           # 설정 및 앱 구동
│   ├── settings/
│   │   ├── base.py
│   │   ├── local.py
│   │   └── prod.py
│   └── celery.py     # Celery 구성

├── media/            # 분석 이미지 등 업로드 파일
│   └── analysis_results/

├── requirements.txt  # 의존성 목록
├── README.md         # 프로젝트 설명서
└── manage.py         # Django 실행 명령 진입점


````
# 🛠️ 환경변수 (.env 예시)
```
SECRET_KEY='your_secret_key'
AI_API_KEY='your_ai_key' 
DB_NAME='your_db_name'
DB_USER='your_db_user'
DB_PASSWORD='your_db_password'
DB_HOST='localhost'
DB_PORT='3306'
```