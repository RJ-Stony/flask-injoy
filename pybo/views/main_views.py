from flask import Blueprint, url_for, current_app    # url_for: URL을 생성하는 함수, 주어진 뷰 함수의 URL을 생성
from flask import render_template  # render_template: HTML 템플릿을 렌더링하는 함수
from werkzeug.utils import redirect # redirect: URL로 리다이렉트하는 함수

from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')
# Blueprint: Flask에서 제공하는 기능으로, 여러 개의 뷰를 모아 관리할 수 있는 객체
# __name__: 현재 모듈의 이름을 나타내는 내장 변수
# url_prefix: Blueprint가 담당하는 공통 URL 경로 접두어(prefix)

@bp.route('/')  # 메인 페이지
def index():
    current_app.logger.info("INFO 레벨로 출력")
    return redirect(url_for('question._list'))  # 메인 페이지에서 질문 목록 페이지로 리다이렉트