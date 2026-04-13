## 🚀 기능 및 접근 정책 (Features & Access Control)

- **비로그인 사용자**: 메인 페이지 및 전체 랭킹 조회가 가능합니다.
- **로그인 사용자**: 
  - 가위바위보 게임 플레이 가능 (전적 실시간 저장).
  - 개인별 통계 및 전적 히스토리 확인 가능.
  - 연승(Streak) 기록 유지 및 랭킹 반영.

## 🛠️ 개발 환경 설정 (Local Setup)

1.  **의존성 설치**
    ```bash
    cd backend
    pip install -r requirements.txt
    ```

2.  **데이터베이스 초기화 및 서버 실행**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

3.  **회원가입 및 로그인**
    웹 화면 상단의 `Signup` 메뉴를 통해 계정을 생성하거나, 관리자 페이지(`/admin/`)에서 계정을 관리할 수 있습니다.

---
*Last Updated: 2026-04-13*
