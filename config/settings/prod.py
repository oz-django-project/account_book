import os

from config.settings import *

DEBUG = False
ALLOWED_HOSTS = [] # 도메인 주소

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

DATABASES = {} # 배포 데이터베이스 설정
