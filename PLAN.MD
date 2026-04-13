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
- **Production**: Vercel (Hosting) + Supabase (Database)
- **Notice**: AWS 배포 및 운영은 프로젝트 고도화 단계의 향후 과제로 변경되었습니다.

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
*본 계획서는 프로젝트의 구현 목표를 Vercel + Supabase 기반의 모던 클라우드 배포로 수정하여 최종 업데이트되었습니다.*
# 추가 할 사항
## 8. 외부 접근 가능한 운영 배포 구성 (Public Deployment Architecture)

본 프로젝트는 로컬 개발 환경을 넘어, 외부 사용자가 인터넷을 통해 직접 접속할 수 있는 운영 서비스 형태로 배포하는 것을 목표로 합니다.

### 8.1 운영 배포 목표
- 사용자는 Vercel에서 제공하는 퍼블릭 URL을 통해 서비스에 접속합니다.
- Django 서버는 Vercel의 Serverless Functions 또는 Edge Runtime을 활용하여 배포됩니다.
- 데이터베이스는 클라우드 기반의 Supabase(PostgreSQL)를 사용하여 영속성과 안정성을 확보합니다. (기존 MySQL에서 PostgreSQL로의 전환 포함)
- 정적 파일(CSS, JS, 이미지)은 Vercel의 CDN을 통해 전 세계에 최적화된 상태로 서빙됩니다.
- 모든 기능(인증, 게임, 랭킹)은 Vercel + Supabase 환경에서도 로컬과 동일하게 작동해야 합니다.

### 8.2 권장 운영 아키텍처 (Vercel + Supabase)
효율적인 비용과 관리를 위해 다음과 같은 서버리스 아키텍처를 구성합니다.

- **사용자(Client)** → **Vercel URL (HTTPS)**
- **Vercel (Compute)** → Django 애플리케이션 실행 (Runtime 환경)
- **Supabase (Database)** → PostgreSQL 운영 데이터베이스 (Managed 서비스)
- **GitHub** → CI/CD 자동 배포 (Main 브랜치 Push 시 Vercel 자동 빌드)

즉, 복잡한 인프라 관리(EC2, Nginx 설정 등) 없이 **Vercel + Supabase** 조합으로 기동성 있는 운영 배포를 구성합니다.

### 8.3 외부 접근을 위한 필수 설정
외부 접속이 가능하려면 아래 항목이 반드시 반영되어야 합니다.

#### (1) ALLOWED_HOSTS 설정
- Django의 `settings.py`에 Vercel에서 할당받은 도메인과 로컬 호스트를 등록합니다.

#### (2) DEBUG 비활성화
- 운영 환경(`.env` 활용)에서는 `DEBUG = False`로 설정해야 합니다.

#### (3) 정적 파일 수집 및 WhiteNoise 활용
- Vercel 환경에서 Django 정적 파일을 서빙하기 위해 `WhiteNoise` 라이브러리를 적용하거나 Vercel 설정을 최적화합니다.

#### (4) 데이터베이스 마이그레이션 (MySQL → PostgreSQL)
- 로컬 개발은 MySQL을 유지할 수 있으나, Supabase 사용을 위해 `psycopg2-binary` 라이브러리를 설치하고 PostgreSQL 호환성을 확보합니다.
- 운영 환경의 `DATABASES` 설정을 Supabase 연결 정보로 업데이트합니다.

#### (5) 보안 그룹(Security Group) 설정
- EC2:
  - 80 포트(HTTP)
  - 443 포트(HTTPS)
  - 22 포트(SSH, 관리자 IP 제한 권장)
- RDS:
  - 3306 포트는 EC2에서만 접근 가능하도록 제한해야 합니다.
  - 외부 공개는 지양합니다.

### 8.4 HTTPS 및 도메인 자동화
Vercel을 사용하면 별도의 설정 없이 SSL(HTTPS)이 자동 적용됩니다.

- **도메인**: Vercel 기본 주소(`*.vercel.app`) 사용 또는 커스텀 도메인 간편 연결.
- **SSL**: Let's Encrypt를 통한 자동 갱신 및 보안 연결.

이를 통해 별도의 Nginx 인증서 작업 없이 안전한 세션 처리가 가능합니다.
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

### 8.6 배포 절차 초안 (Vercel + Supabase)
1. Supabase 프로젝트 생성 및 PostgreSQL 데이터베이스 준비
2. `settings.py`를 PostgreSQL 대응으로 수정 (dj-database-url 등 검토)
3. Vercel 프로젝트 생성 및 GitHub 저장소 연결
4. 환경 변수 등록 (`SECRET_KEY`, `DATABASE_URL`, `DEBUG=False` 등)
5. Vercel 빌드 설정 (`vercel.json` 구성 및 Django 런타임 설정)
6. 데이터베이스 Migration 수행 (Vercel Build step 또는 로컬 원격 접속)
7. Vercel 배포 완료 및 퍼블릭 URL 접속 확인
8. 로그인 및 게임 기능 최종 검증

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

### 8.8 향후 과제 (AWS 및 고도화)
사용자 증가 및 복잡한 아키텍처 요구 시 나중에 검토할 항목들입니다.

- **AWS 마이그레이션**: EC2, RDS, S3 기반의 아키텍처로 확장
- **CI/CD 고도화**: GitHub Actions를 통한 정교한 배포 파이프라인
- **성능 모니터링**: CloudWatch 또는 외부 APM 도구 도입
- **데이터 백업 및 복구**: 엔터프라이즈급 DB 관리 정책 수립

*본 계획서는 Vercel 및 Supabase를 활용한 신속한 배포 전략을 우선순위에 두며, AWS 관련 업데이트는 향후 필요 시 진행합니다.*