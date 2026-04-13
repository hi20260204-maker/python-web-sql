# 프로젝트 심층 분석 보고서 (Research Report)

이 보고서는 `python-web-sql` 프로젝트의 현재 구조, 기술 스택, 데이터 흐름 및 개선 필요 사항에 대한 상세 분석 결과를 담고 있습니다.

---

## 1. 프로젝트 개요 (Project Overview)
본 프로젝트는 **Django** 프레임워크와 **MySQL** 데이터베이스를 활용한 **가위바위보(Rock-Paper-Scissors, RPS)** 게임 웹 애플리케이션입니다. Docker를 통한 컨테이너화가 되어 있어 일관된 개발 및 운영 환경을 지향하고 있습니다.

## 2. 기술 스택 (Technology Stack)
- **Framework**: Django 4.2+ (Python 3.12 기준)
- **Database**: MySQL 8.0
- **Infrastructure**: Docker, Docker Compose
- **Language**: Python 3.12
- **Key Packages**:
  - `django-dotenv`: 환경 변수 관리
  - `mysqlclient`: MySQL 연동용 DB 드라이버

## 3. 시스템 아키텍처 (System Architecture)

### 3.1 Django Apps 구조
프로젝트는 기능별로 4개의 주요 앱으로 분리되어 있습니다:

- **`user`**: 사용자 인증 및 프로필 관리 관련 뼈대.
- **`game`**: 게임 진행 로직 및 상태 관리 담당.
- **`ranking`**: 사용자별 점수 합산 및 순위 정보 제공.
- **`core`**: 공통 유틸리티 포함. 특히 `wait_for_db` 커스텀 명령을 통해 데이터베이스가 준비될 때까지 대기하는 안정성 확보.

### 3.2 데이터 흐름 (Data Flow)
1. 사용자가 특정 URL(예: `/game/`)에 접속하면 해당 앱의 `views.py`가 호출됩니다.
2. 뷰에서는 필요한 로직을 처리(현재는 렌더링만 시도)하고 템플릿을 반환합니다.
3. 데이터베이스 연동은 `.env` 설정값에 따라 `RPS/settings.py`에서 중앙 집중식으로 관리됩니다.

## 4. 인프라 및 환경 설정 (Infrastructure)
- **`Dockerfile`**: `python:3.12-slim` 이미지를 기반으로 경량화된 환경을 구축합니다.
- **`docker-compose.yml`**:
  - `app`: Django 애플리케이션 서비스.
  - `db`: MySQL 8.0 서비스. 볼륨 마운트를 통해 데이터 영속성을 보장합니다.
- **`.env`**: DB 이름, 유저, 암호 등 민감 정보를 분리 관리합니다.

## 5. 심층 분석 및 문제점 진단 (Gap Analysis)

### 5.1 템플릿 파일 부재 (Critical Issue)
- **현상**: 각 앱의 `views.py`에서는 `user.html`, `game.html`, `ranking.html`을 렌더링 하려 하지만, 프로젝트 내 실질적인 `.html` 파일이 발견되지 않습니다.
- **원인 추정**: 템플릿이 아직 작성되지 않았거나, `fronted` 폴더로 분리하려다 초기 상태에 머물러 있을 가능성이 높습니다.

### 5.2 Frontend 디렉토리 구조
- **현상**: `fronted`라는 폴더가 존재하나 내부가 비어 있으며, 이름에 오타(`frontend`가 아님)가 있습니다.
- **영향**: 프론트엔드 개발 환경이 구성되지 않아 현재로서는 실제 UI 확인이 불가능합니다.

### 5.3 문서와 실제 코드의 불일치
- `docs/README.md`에는 `main.py`를 실행하라고 되어 있으나, 실제 구조는 Django 표준 (`manage.py`)을 따르고 있어 문서 갱신이 필요합니다.

## 6. 향후 개선 분석 및 제언 (Future Recommendations)
1. **프론트엔드 통합**: 비어 있는 `fronted` 폴더를 `frontend`로 변경하고 React/Vue 등의 모던 프레임워크를 도입하거나, Django 템플릿 시스템을 완성해야 합니다.
2. **게임 로직 구현**: `game` 앱 내에 실제 점수를 계산하고 결과를 DB에 저장하는 기능을 구현해야 합니다.
3. **디자인 강화**: 사용자 경험을 높이기 위해 Vibrant Colors, Dark Mode, 미세 애니메이션이 포함된 프리미엄 디자인 시스템 적용이 필요합니다.

---
*보고서 작성 일자: 2026-04-13*
*작성자: Antigravity*
