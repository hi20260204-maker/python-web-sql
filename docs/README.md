# RPS Game (Rock-Paper-Scissors) - Python Web SQL

이 프로젝트는 **Django 4.2**, **MySQL 8.0**, **Docker**를 기반으로 구축된 프리미엄 가위바위보 게임 웹 애플리케이션입니다. 

---

## 🚀 빠른 시작 (Quick Start)

가장 권장되는 실행 방법은 **Docker Compose**를 사용하는 것입니다.

```bash
# 1. 컨테이너 빌드 및 백그라운드 실행
docker-compose up -d --build

# 2. 데이터베이스 초기화 (최초 1회 필수)
docker-compose exec app python manage.py makemigrations
docker-compose exec app python manage.py migrate

# 3. 브라우저 접속
http://localhost:8000/
```

## 🛠️ 개발 환경 설정 (Local Setup)

로컬에서 직접 실행할 경우 다음 단계를 따르십시오.

1.  **의존성 설치**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2.  **환경 변수 설정**
    `.env` 파일을 생성하고 DB 연결 정보를 입력하십시오. (기본값: `DB_HOST=127.0.0.1`)

3.  **정적 파일 수집 및 서버 실행**
    ```bash
    python manage.py collectstatic --noinput
    python manage.py runserver
    ```

## 🏗️ 프로젝트 구조 (Structure)

- **`backend/`**: Django Core 애플리케이션 (user, game, ranking, core 등).
- **`backend/static/`**: 프리미엄 CSS/JS 에셋 (Vibrant Dark Mode Theme).
- **`backend/templates/`**: 전역 Django Templates (Glassmorphism UI).
- **`docker-compose.yml`**: 서비스 오케스트레이션 (Python + MySQL).

## ☁️ AWS 배포 전략 (Deployment)

AWS 배포 시에는 다음과 같은 표준 아키텍처를 권장합니다.

- **Frontend/App**: AWS EC2 (Gunicorn + Nginx)
- **Database**: AWS RDS for MySQL (컨테이너 외부 데이터 정합성 보장)
- **Static Assets**: AWS S3 + CloudFront (고성능 데이터 서빙)
- **Security**: `.env.prod` 설정을 통해 `DEBUG=False` 및 `SECRET_KEY` 분리 관리 필수.

---
*Last Updated: 2026-04-13*
