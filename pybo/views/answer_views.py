from datetime import datetime       

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer
from .auth_views import login_required    # 로그인 필요 데코레이터

bp = Blueprint('answer', __name__, url_prefix='/answer')    

@bp.route('/create/<int:question_id>', methods=('POST',))   # 답변 생성 페이지
@login_required
def create(question_id):    
    form = AnswerForm()     # 답변 폼 생성
    question = Question.query.get_or_404(question_id)   # 질문 ID로 질문 객체 조회
    if form.validate_on_submit():   # 폼 유효성 검사
        content = request.form['content']       # 폼에서 입력된 답변 내용
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)        # 답변 객체 생성
        question.answer_set.append(answer)  # 질문 객체에 답변 추가
        db.session.commit() # 데이터베이스에 변경 사항 저장
        return redirect('{}#answer_{}'.format(
            url_for('question.detail', question_id=question_id), answer.id))        # 질문 상세 페이지로 리다이렉트 (답변 ID를 URL에 포함)
    return render_template('question/question_detail.html', question=question, form=form) # 답변 폼을 포함한 질문 상세 페이지 렌더링

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))   # 답변 수정 페이지
@login_required   # 로그인 필요 데코레이터
def modify(answer_id):  
    answer = Answer.query.get_or_404(answer_id)  # 답변 ID로 답변 객체 조회
    if g.user != answer.user:     # 로그인한 사용자와 답변 작성자가 다른 경우
        flash('수정권한이 없습니다')    # 사용자에게 메시지 표시
        return redirect(url_for('question.detail', question_id=answer.question.id))   # 질문 상세 페이지로 리다이렉트
    if request.method == "POST":    # POST 요청
        form = AnswerForm()  # 답변 수정 폼 생성
        if form.validate_on_submit():   # 폼 유효성 검사
            form.populate_obj(answer)   # 폼 데이터를 답변 객체에 채우기
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit() # 데이터베이스에 변경 사항 저장
            return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))
    else:   # GET 요청
        form = AnswerForm(obj=answer)   # 답변 수정 폼 생성 (기존 답변 데이터로 초기화)
    return render_template('answer/answer_form.html', form=form)    # 답변 수정 폼을 포함한 질문 상세 페이지 렌더링

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id)
    if g.user == _answer.user:
        flash('본인이 작성한 답변은 추천할 수 없습니다.')
    elif g.user in _answer.voter:
        flash('이미 추천한 답변입니다.')
    else:
        _answer.voter.append(g.user)
        db.session.commit()
    return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=_answer.question.id), _answer.id))
