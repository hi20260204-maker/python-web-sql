# syntax=docker/dockerfile:1

#1. python 3.12 slim 버전 사용
FROM python:3.12-slim

#2. 환경 변수 설정
# python 출력 버퍼링 비활성화
ENV PYTHONUNBUFFERED=1
# python 캐시 비활성화
ENV PYTHONDONTWRITEBYTECODE=1

#3. 작업 디렉토리 설정
WORKDIR /app

#4. requirements.txt 복사
COPY requirements.txt /app/requirements.txt

#5. 패키지 설치
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

#6. 코드 복사
COPY . /app

#7. 포트 설정
EXPOSE 8000

#8. Django 개발 서버 실행
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]