from flask import Flask     # Flask: Flask 웹 프레임워크의 핵심 클래스
from flask_migrate import Migrate  # Migrate: 데이터베이스 마이그레이션을 위한 Flask 확장 모듈
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy: Flask와 함께 사용할 수 있는 ORM(Object Relational Mapping) 라이브러리
from sqlalchemy import MetaData # MetaData: SQLAlchemy에서 데이터베이스 메타데이터를 정의하는 클래스

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()
'''
flask db migrate	모델을 새로 생성하거나 변경할 때 사용 (실행하면 리비전 파일이 생성된다.)
flask db upgrade	모델의 변경 내용을 실제 데이터베이스에 적용할 때 사용 (위에서 생성된 리비전 파일을 실행하여 데이터베이스를 변경한다.)
'''

def create_app():
    app = Flask(__name__)   # Flask 애플리케이션 객체 생성
    app.config.from_envvar('APP_CONFIG_FILE')  # 환경 변수에서 설정 파일 경로를 가져와서 Flask 애플리케이션에 설정을 로드

    # ORM
    db.init_app(app)    # SQLAlchemy 객체를 Flask 애플리케이션에 연결
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):  # SQLite 데이터베이스를 사용할 경우
        migrate.init_app(app, db, render_as_batch=True) # SQLite의 경우 외래키 제약 조건을 지원하지 않기 때문에 render_as_batch=True로 설정
    else:
        migrate.init_app(app, db)   # 다른 데이터베이스를 사용할 경우 일반적으로 사용되는 설정
    from . import models   # models 모듈을 임포트하여 데이터베이스 모델을 정의
    # models.py에서 정의한 데이터베이스 모델을 가져와서 초기화

    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views # views 모듈에서 블루프린트를 임포트
    app.register_blueprint(main_views.bp)   # main_views 블루프린트를 Flask 애플리케이션에 등록
    # 블루프린트: Flask에서 제공하는 기능으로, 여러 개의 뷰를 모아 관리할 수 있는 객체
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app  # Flask 애플리케이션 객체를 반환