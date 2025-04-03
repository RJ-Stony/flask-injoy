import os   # os 모듈을 임포트하여 파일 경로를 다루기 위함

BASE_DIR = os.path.dirname(__file__)    # 현재 파일의 디렉토리 경로

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db')) # SQLite 데이터베이스 URI
SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemy의 이벤트 시스템을 사용하지 않도록 설정
SECRET_KEY = "dev"