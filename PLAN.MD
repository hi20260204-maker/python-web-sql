# RPS Game 프로젝트 통합 구현 및 배포 계획서 (PLAN.MD V2)

이 문서는 `python-web-sql` 프로젝트의 소스 코드 실태 분석 결과를 바탕으로, 기능 구현부터 AWS 운영 배포까지의 전 과정을 팩트 기반으로 설계한 마스터 로드맵입니다.

---

## 1. 정밀 분석 및 검증 (Gap Analysis & Evidence)
이전 분석에서 지적된 사항들을 실제 소스 코드 레벨에서 재검증한 결과입니다.

- **템플릿 부재 근거**: `backend/user/`, `backend/game/`, `backend/ranking/` 내에 `templates` 디렉토리와 `.html` 파일이 물리적으로 존재하지 않음을 확인했습니다 (2026-04-13 14:40 기준).
- **폴더 오타 및 상태**: `fronted/` 디렉토리가 존재하나 내부 파일이 0개인 상태입니다.
- **문서 불일치**: `docs/README.md`는 독립 실행형 `main.py`를 가이드하고 있으나, 실제 코드는 `manage.py` 중심의 Django 4.2 프로젝트로 구성되어 있어 전면 수정이 필요합니다.

## 2. 기능 및 비즈니스 정책 (Feature Specification)

### 2.1 가위바위보 게임 흐름
- **비로그인(Guest)**: 세션 기반으로 임시 전적을 관리하며, 브라우저 종료 시 초기화됩니다.
- **로그인(User)**: 모든 판수가 `GameHistory` 모델에 영구 저장됩니다.
- **승패 판정**: 서버 측 `views.py`에서 무작위 값 생성 및 판정이 이루어지며, 클라이언트 조작을 방지합니다.

### 2.2 랭킹 산정 정책 (Ranking Policy)
- **산정 기준**: 최근 7일 내의 '총 승리 횟수' 기준 Top 100.
- **동률 처리**: 승리 횟수가 같을 경우, 해당 승리 횟수에 먼저 도달한(가장 최근 승리 시점이 빠른) 유저가 상위 랭크.
- **비로그인 유저**: 랭킹 집계에서 제외 (DB 저장 유저 대상).

## 3. 데이터 모델 설계 (Data Modeling)

| 모델명 | 필드명 | 타입 | 설명 |
| :--- | :--- | :--- | :--- |
| **Profile** | `user`, `total_wins`, `total_games`, `streak` | Integer/OneToOne | 전적 집계 테이블 (Cache 역할) |
| **GameHistory** | `player`, `player_choice`, `cpu_choice`, `result`, `created_at` | FK/Enum/DateTime | 게임 로그 원천 데이터 |
| **Ranking** | `user`, `rank_score`, `updated_at` | FK/Integer | 랭킹 스냅샷 (배치 처리용 선택 사항) |

> [!TIP]
> **정합성 유지 전략**: 모든 승률/전적은 `GameHistory`를 통해 검증 가능해야 하며, `Profile` 테이블은 조회 성능 향상을 위해 결과를 기록할 때만 트랜잭션 내에서 업데이트합니다.

## 4. 프론트엔드 아키텍처 전략
AWS 배포 복잡도와 정적 파일 관리 효율성을 고려하여 **Django Template 기반 MPA (Multi-Page Application)** 방식을 채택합니다.

1. **디렉토리 명칭**: `fronted` -> `frontend` (Static Assets 관리용).
2. **템플릿 관리**: `backend/templates/` 전역 폴더 내 `base.html`을 상속받는 구조.
3. **디자인 시스템**: Modern CSS (`static/css/styles.css`) 적용, 미세 애니메이션(Micro-animations) 포함.

## 5. 인프라 및 AWS 배포 로드맵

### 5.1 아키텍처 구성
- **Application**: EC2 (Amazon Linux 2023) + Gunicorn + Nginx
- **Database**: AWS RDS (MySQL 8.0)
- **Static/Media**: AWS S3 + CloudFront (선택 사항, 초기에는 S3/Nginx 조합)

### 5.2 보안 설정 (Security Checklist)
- **`.env` 분리**: `SECRET_KEY`, `DB_CREDENTIALS`, `DEBUG=False` 운영 설정 적용.
- **CORS/CSRF**: ALLOWED_HOSTS 및 CSRF_TRUSTED_ORIGINS 명시.
- **Access Control**: AWS 보안 그룹(Security Group)을 통해 80, 443 포트만 허용, DB는 App 서버만 접근 가능하도록 설정.

## 6. 실행 가이드 (Actionable Commands)

### 6.1 초기 환경 구성 (Local Development)
사용자가 직접 실행해야 할 명령어들입니다.
```powershell
# 1. 환경 변수 파일 생성
copy .env.example .env  # (존재하지 않을 경우 새로 생성 유도)

# 2. 정적 파일 및 미디어 폴더 생성
mkdir backend/static
mkdir backend/templates

# 3. 데이터베이스 초기화
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # 관리자 계정 생성
```

### 6.2 AWS 배포 프로세스
```bash
# 1. Static 파일 수집
python manage.py collectstatic --noinput

# 2. Gunicorn 실행
gunicorn RPS.wsgi:application --bind 0.0.0.0:8000
```

## 7. README.MD 개선 가이드 (Draft)
```markdown
# RPS (Rock Paper Scissors) Game - Django Project

## 시작하기
1. `docker-compose up --build` 를 통해 개발 환경을 즉시 실행합니다.
2. `http://localhost:8000/game/` 에 접속하여 게임을 시작합니다.
3. 상세 설계는 `PLAN.MD` 및 `RESEARCH.MD`를 참조하십시오.
```

---
*본 계획서는 사용자의 피드백을 수렴하여 작성되었으며, 구현 단계에서 실시간 업데이트될 예정입니다.*