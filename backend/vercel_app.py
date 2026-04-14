import os
import sys

# 프로젝트 루트(backend)를 파이썬 경로에 추가
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

from RPS.wsgi import app

# Vercel은 이 'app' 객체를 실행합니다.
handler = app
