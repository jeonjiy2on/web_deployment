
import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'web_project.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 설정 다시 해야 함
SECRET_KEY = "dev"