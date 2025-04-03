from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect
from sqlalchemy import func

from .. import db
from pybo.models import Question, Answer, User
from pybo.forms import QuestionForm, AnswerForm
from pybo.views.auth_views import login_required    # 로그인 필요 데코레이터

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    sort = request.args.get('sort', 'recent')

    question_query = Question.query

    # 정렬 조건
    if sort == 'recommend':
        question_query = question_query.outerjoin(Question.voter) \
            .group_by(Question.id) \
            .order_by(func.count().desc(), Question.create_date.desc())
    elif sort == 'popular':
        question_query = question_query.outerjoin(Question.answer_set) \
            .group_by(Question.id) \
            .order_by(func.count().desc(), Question.create_date.desc())
    else:
        question_query = question_query.order_by(Question.create_date.desc())

    # 검색 조건
    if kw:
        search = f"%%{kw}%%"
        from pybo.models import Answer, User  # ensure Answer, User are imported

        sub_query = db.session.query(
            Answer.question_id, Answer.content, User.username
        ).join(User, Answer.user_id == User.id).subquery()

        question_query = question_query \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(
                Question.subject.ilike(search) |
                Question.content.ilike(search) |
                User.username.ilike(search) |
                sub_query.c.content.ilike(search) |
                sub_query.c.username.ilike(search)
            ).distinct()

    question_list = question_query.paginate(page=page, per_page=10)

    return render_template(
        'question/question_list.html',
        question_list=question_list,
        page=page,
        kw=kw,
        sort=sort
    )

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    page = request.args.get('page', type=int, default=1)
    sort = request.args.get('sort', 'recent')
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    # 답변 정렬 조건 분기
    if sort == 'recommend':
        # 추천 많은 순: voter 개수 기준 정렬
        answer_query = Answer.query.filter(Answer.question_id == question.id).outerjoin(Answer.voter).group_by(Answer.id).order_by(func.count().desc(), Answer.create_date.desc())
    elif sort == 'old':
        # 오래된 순
        answer_query = Answer.query.filter(Answer.question_id == question.id).order_by(Answer.create_date.asc())
    else:
        # 최신순 (기본값)
        answer_query = Answer.query.filter(Answer.question_id == question.id).order_by(Answer.create_date.desc())

    answer_list = answer_query.paginate(page=page, per_page=5)

    return render_template('question/question_detail.html',
                           question=question, form=form,
                           answer_list=answer_list, sort=sort)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required # 로그인 필요 데코레이터
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)   # 질문 ID로 질문 객체 조회
    if g.user != question.user:        # 로그인한 사용자와 질문 작성자가 다른 경우
        flash('수정권한이 없습니다')    # 사용자에게 메시지 표시
        return redirect(url_for('question.detail', question_id=question_id))    # 질문 상세 페이지로 리다이렉트
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()   # 질문 수정 폼 생성
        if form.validate_on_submit():   # 폼 유효성 검사
            form.populate_obj(question) # 폼 데이터를 질문 객체에 채우기
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit() # 데이터베이스에 변경 사항 저장
            return redirect(url_for('question.detail', question_id=question_id))
    else:  # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>')  # 질문 삭제
@login_required # 로그인 필요 데코레이터
def delete(question_id):    
    question = Question.query.get_or_404(question_id)   # 질문 ID로 질문 객체 조회
    if g.user != question.user:         # 로그인한 사용자와 질문 작성자가 다른 경우
        flash('삭제권한이 없습니다')    # 사용자에게 메시지 표시
        return redirect(url_for('question.detail', question_id=question_id))    # 질문 상세 페이지로 리다이렉트
    db.session.delete(question)   # 질문 객체 삭제
    db.session.commit() # 데이터베이스에 변경 사항 저장
    return redirect(url_for('question._list'))  # 질문 목록 페이지로 리다이렉트

@bp.route('/vote/<int:question_id>/')
@login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)

    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할 수 없습니다.')
    elif g.user in _question.voter:
        flash('이미 추천한 글입니다.')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

    