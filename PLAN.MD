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