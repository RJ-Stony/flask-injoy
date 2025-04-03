from flask import Blueprint, url_for, render_template, flash, request, session, g
'''
Flask: Flask 웹 프레임워크의 핵심 클래스
url_for: URL을 생성하는 함수
render_template: HTML 템플릿을 렌더링하는 함수
flash: 사용자에게 메시지를 표시하는 함수
request: 클라이언트 요청을 처리하는 객체
session: 클라이언트와 서버 간의 세션 정보를 저장하는 객체
g: Flask의 전역 객체로, 요청 간에 데이터를 저장하는 데 사용
'''
from werkzeug.security import generate_password_hash, check_password_hash
# generate_password_hash: 비밀번호를 해시화하는 함수
# check_password_hash: 해시화된 비밀번호와 입력된 비밀번호를 비교하는 함수
from werkzeug.utils import redirect
# redirect: URL로 리다이렉트하는 함수
import functools    # functools: 고차 함수와 관련된 기능을 제공하는 모듈

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')    # 블루프린트 객체 생성 (auth라는 이름의 블루프린트)

@bp.route('/signup/', methods=('GET', 'POST'))  # 회원가입 페이지
def signup():   # signup: 회원가입을 처리하는 뷰 함수
    form = UserCreateForm() # 회원가입 폼 생성
    if request.method == 'POST' and form.validate_on_submit():  # POST 요청이고 폼이 유효한 경우
        user = User.query.filter_by(username=form.username.data).first()    # 사용자 이름으로 사용자 조회
        if not user:    # 사용자가 존재하지 않는 경우
            user = User(username=form.username.data,    # 사용자 이름
                        password=generate_password_hash(form.password1.data),   # 비밀번호 해시화
                        email=form.email.data)  # 이메일
            db.session.add(user)    # 사용자 추가
            db.session.commit()     # 데이터베이스에 커밋
            return redirect(url_for('main.index'))  # 회원가입 후 메인 페이지로 리다이렉트
        else:   # 사용자가 이미 존재하는 경우
            flash('이미 존재하는 사용자입니다.')    # 사용자에게 메시지 표시
    return render_template('auth/signup.html', form=form)   # 회원가입 페이지 렌더링

@bp.route('/login/', methods=('GET', 'POST'))   # 로그인 페이지
def login():    # login: 로그인 처리를 위한 뷰 함수
    form = UserLoginForm()  # 로그인 폼 생성
    if request.method == 'POST' and form.validate_on_submit():  # POST 요청이고 폼이 유효한 경우
        error = None    # 오류 메시지 초기화
        user = User.query.filter_by(username=form.username.data).first()    # 사용자 이름으로 사용자 조회
        # filter_by: 조건에 맞는 레코드를 조회하는 메서드
        # first: 조건에 맞는 첫 번째 레코드를 반환
        if not user:    # 사용자가 존재하지 않는 경우
            error = "존재하지 않는 사용자입니다."   # 오류 메시지 설정
        elif not check_password_hash(user.password, form.password.data):    # 비밀번호가 일치하지 않는 경우
            # check_password_hash: 해시화된 비밀번호와 입력된 비밀번호를 비교하는 함수
            # user.password: 해시화된 비밀번호
            error = "비밀번호가 올바르지 않습니다." # 오류 메시지 설정
        if error is None:   # 오류가 없는 경우
            session.clear()   # 세션 초기화
            session['user_id'] = user.id    # 사용자 ID를 세션에 저장
            _next = request.args.get('next', '')    # 다음 URL 가져오기 (GET 요청의 경우)
            if _next:   # 다음 URL이 있는 경우
                return redirect(_next)  # 다음 URL로 리다이렉트
            else:   # 다음 URL이 없는 경우
                return redirect(url_for('main.index'))  # 메인 페이지로 리다이렉트
        ############# 오류 처리 #############
        flash(error)    # 오류 메시지 표시
    return render_template('auth/login.html', form=form)    # 로그인 페이지 렌더링

@bp.before_app_request  # 애플리케이션 요청 전에 실행되는 함수
def load_logged_in_user():  # 로그인된 사용자 정보를 로드하는 함수
    user_id = session.get('user_id')    # 세션에서 사용자 ID 가져오기
    if user_id is None:   # 사용자 ID가 없는 경우
        g.user = None   # g.user에 None 설정 (로그인되지 않은 상태)
    else:   # 사용자 ID가 있는 경우
        g.user = User.query.get(user_id)    # 사용자 ID로 사용자 조회
        # g: Flask의 전역 객체로, 요청 간에 데이터를 저장하는 데 사용
        # User.query.get: 기본키로 사용자 조회

@bp.route('/logout/')   # 로그아웃 페이지
def logout():   # logout: 로그아웃 처리를 위한 뷰 함수
    session.clear() # 세션 초기화 (로그아웃)
    return redirect(url_for('main.index'))  # 로그아웃 후 메인 페이지로 리다이렉트

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.login', next=_next))
        return view(*args, **kwargs)
    return wrapped_view