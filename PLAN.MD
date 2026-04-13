# RPS Game 프로젝트 통합 구현 및 배포 계획서 (PLAN.MD V4)

이 문서는 `python-web-sql` 프로젝트의 소스 코드 실태 분석 결과를 바탕으로, 기능 구현부터 AWS 운영 배포까지의 전 과정을 팩트 기반으로 설계한 마스터 로드맵입니다.

---

## 1. 정밀 분석 및 검증 (Gap Analysis & Evidence)
초기 분석에서 확인된 사항들을 바탕으로 최적화를 완료한 결과입니다.

- **기능 구현 완료**: `user`, `game`, `ranking` 앱의 핵심 로직 및 데이터 모델 구현 완료.
- **UI/UX 고도화**: Glassmorphism 테마와 Premium CSS 시스템 구축 완료.
- **인증 시스템**: 회원가입, 로그인, 접근 제어 정책 적용 완료.

## 2. 기능 및 비즈니스 정책 (Feature Specification)

### 2.1 가위바위보 게임 흐름
- **로그인(User)**: 모든 판수가 `GameHistory` 모델에 영구 저장되며 프로필에 승률이 반영됩니다.
- **비로그인(Guest)**: 랭킹 및 랜딩 페이지 조회는 가능하나, 게임 플레이 시 로그인이 필요합니다.
- **승패 판정**: 서버 측 `views.py`에서 무작위 값 생성 및 판정이 이루어집니다.

### 2.2 랭킹 산정 정책 (Ranking Policy)
- **산정 기준**: 최근 7일 내의 '총 승리 횟수' 기준 Top 100.
- **동률 처리**: 승리 횟수가 같을 경우, 고유 ID 순(먼저 가입한 유저 우선)으로 정렬합니다.

## 3. 데이터 모델 설계 (Data Modeling)

| 모델명 | 필드명 | 타입 | 설명 |
| :--- | :--- | :--- | :--- |
| **Profile** | `user`, `total_wins`, `total_games`, `streak` | Integer/OneToOne | 전적 집계 테이블 (Cache 역할) |
| **GameHistory** | `player`, `player_choice`, `cpu_choice`, `result`, `created_at` | FK/Enum/DateTime | 게임 로그 원천 데이터 |

## 4. 프론트엔드 아키텍처
- **MPA 방식**: Django Template을 활용한 멀티 페이지 애플리케이션.
- **Global Assets**: `backend/static` 및 `backend/templates`에서 전역 디자인 관리.
- **프리미엄 디자인**: `static/css/style.css`에 정의된 Glassmorphism 및 그라데이션 시스템 사용.

## 5. 인프라 및 배포 로드맵
- **Container**: Docker + Docker Compose (Python 3.12 + MySQL 8.0)
- **Production**: AWS EC2 + AWS RDS (운영 환경 권장 아키텍처)

## 6. Phase 6: 인증 및 접근 제어 (완료)
- **회원가입/로그인**: `UserCreationForm` 기반의 세련된 인증 페이지 구축.
- **접근 제어**: 게임 플레이 `POST` 요청 시 로그인 여부 강제 체크.

## 7. 최종 프로젝트 디렉토리 구조
정리가 완료된 현재 프로젝트의 물리적 구조입니다.

```text
python-web-sql/
├── backend/                # Django 백엔드 핵심 소스
│   ├── RPS/                # 프로젝트 설정 및 라우팅
│   ├── user/               # 유저 프로필 및 인증 앱
│   ├── game/               # 게임 로직 및 기록 앱
│   ├── ranking/            # 랭킹 시스템 앱
│   ├── static/             # 공통 CSS/JS (Premium UI Asset)
│   ├── templates/          # 공통 HTML (Glassmorphism Layout)
│   ├── manage.py           # Django 실행 스크립트
│   ├── Dockerfile          # 애플리케이션 빌드 설정
│   └── docker-compose.yml  # 서비스 통합 관리 (App + DB)
├── docs/                   # 프로젝트 문서 가이드
│   └── README.md           # 상세 실행 가이드
├── PLAN.MD                 # 최종 로드맵 (V4)
└── RESEARCH.MD             # 초기 분석 리포트
```

---
*본 계획서는 프로젝트의 모든 구현 단계가 완료되어 최종 업데이트되었습니다.*
# 추가 할 사항
## 8. 외부 접근 가능한 운영 배포 구성 (Public Deployment Architecture)

본 프로젝트는 로컬 개발 환경을 넘어, 외부 사용자가 인터넷을 통해 직접 접속할 수 있는 운영 서비스 형태로 배포하는 것을 목표로 합니다.

### 8.1 운영 배포 목표
- 사용자는 브라우저를 통해 퍼블릭 URL로 서비스에 접속할 수 있어야 합니다.
- Django 서버는 AWS 상에서 24시간 실행 가능한 상태로 운영됩니다.
- 데이터베이스는 로컬 Docker MySQL이 아닌 AWS RDS를 사용하여 영속성과 안정성을 확보합니다.
- 정적 파일(CSS, JS, 이미지)은 운영 환경에서도 정상적으로 서빙되어야 합니다.
- 인증, 게임 기록, 랭킹 조회 기능이 외부 환경에서도 동일하게 동작해야 합니다.

### 8.2 권장 운영 아키텍처
운영 환경에서는 다음과 같은 구조를 권장합니다.

- **사용자(Client)** → **도메인 또는 EC2 퍼블릭 주소**
- **Nginx** → 외부 HTTP/HTTPS 요청 수신 및 정적 파일 서빙
- **Gunicorn + Django** → 실제 애플리케이션 실행
- **AWS RDS(MySQL)** → 운영 데이터베이스
- **EC2** → 애플리케이션 서버 인스턴스

즉, 단순히 `runserver`로 띄우는 방식이 아니라,  
**Nginx + Gunicorn + Django + RDS** 구조로 운영 배포를 구성해야 합니다.

### 8.3 외부 접근을 위한 필수 설정
외부 접속이 가능하려면 아래 항목이 반드시 반영되어야 합니다.

#### (1) ALLOWED_HOSTS 설정
- Django의 `settings.py`에 EC2 퍼블릭 IP, 도메인 주소를 등록해야 합니다.
- 예:
  - EC2 퍼블릭 IP
  - Elastic IP
  - 연결된 도메인 주소

#### (2) DEBUG 비활성화
- 운영 환경에서는 `DEBUG = False`로 설정해야 합니다.
- 디버그 정보 노출 방지 및 보안 강화를 위해 필수입니다.

#### (3) 정적 파일 수집 및 서빙
- `collectstatic` 수행 후 Nginx가 정적 파일을 서빙하도록 구성해야 합니다.
- 현재 Premium CSS 시스템을 운영 환경에서도 그대로 사용하려면 정적 파일 경로 설계가 명확해야 합니다.

#### (4) 데이터베이스 분리
- 로컬 Docker MySQL은 개발용으로 사용하고,
- 운영 환경은 AWS RDS MySQL로 분리해야 합니다.
- 환경별 DB 설정을 분리하여 개발/운영 혼선을 방지해야 합니다.

#### (5) 보안 그룹(Security Group) 설정
- EC2:
  - 80 포트(HTTP)
  - 443 포트(HTTPS)
  - 22 포트(SSH, 관리자 IP 제한 권장)
- RDS:
  - 3306 포트는 EC2에서만 접근 가능하도록 제한해야 합니다.
  - 외부 공개는 지양합니다.

### 8.4 HTTPS 및 도메인 연결
운영 서비스로 배포할 경우, 단순 퍼블릭 IP 접속보다 도메인 및 HTTPS 적용이 권장됩니다.

- **도메인 연결**: Route 53 또는 외부 도메인 서비스 사용 가능
- **HTTPS 인증서 적용**:
  - Nginx + Certbot
  - 또는 AWS Load Balancer + ACM 방식 검토 가능

이를 통해 로그인 기능 및 세션 처리 시 보안성을 강화할 수 있습니다.

### 8.5 운영 환경 설정 분리
운영 배포를 위해 개발 환경과 운영 환경을 분리해야 합니다.

분리 대상 예시:
- `DEBUG`
- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `DATABASES`
- `CSRF_TRUSTED_ORIGINS`
- 정적 파일 경로
- 보안 쿠키 설정

환경 변수(.env)를 사용하여 민감 정보와 운영 설정을 코드에서 분리하는 방식을 권장합니다.

### 8.6 배포 절차 초안
운영 배포는 아래 순서로 진행합니다.

1. AWS EC2 인스턴스 생성
2. AWS RDS MySQL 인스턴스 생성
3. EC2에 Docker, Docker Compose, Nginx, Gunicorn 환경 구성
4. 프로젝트 소스 배포 및 환경 변수 설정
5. Django migration 수행
6. `collectstatic` 수행
7. Gunicorn 실행
8. Nginx reverse proxy 연결
9. 퍼블릭 IP 또는 도메인으로 외부 접속 확인
10. 로그인, 게임 플레이, 랭킹 조회 정상 동작 검증

### 8.7 운영 검증 체크리스트
외부 공개 전 아래 항목을 점검해야 합니다.

- 회원가입 가능 여부
- 로그인/로그아웃 정상 동작 여부
- 로그인하지 않은 사용자의 게임 접근 차단 여부
- 게임 결과 저장 여부
- 프로필 전적 반영 여부
- 최근 7일 랭킹 조회 여부
- CSS/JS 정적 파일 깨짐 여부
- 새로고침/직접 URL 접근 시 오류 여부
- EC2 재시작 이후 서비스 자동 복구 여부

### 8.8 추후 확장 가능 항목
운영 안정성을 높이기 위해 아래 항목도 추후 반영 가능성이 있습니다.

- CI/CD 자동 배포(GitHub Actions)
- CloudWatch 로그 모니터링
- S3 기반 정적 파일 또는 미디어 파일 저장
- AWS ALB 도입
- 장애 대응 및 DB 백업 정책
- 사용자 증가 대응을 위한 인스턴스 스케일 업/아웃

*본 계획서는 현재 구현 상태를 반영한 최신 통합 계획서이며, AWS 운영 배포 및 외부 접근 검증 단계가 후속으로 진행됩니다.*