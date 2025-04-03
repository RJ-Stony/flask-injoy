from pybo import db # SQLAlchemy 객체를 임포트하여 데이터베이스 모델을 정의하기 위함

question_voter = db.Table(      # 질문 투표자 테이블 정의 (다대다 관계)
    'question_voter',   # 테이블 이름
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),   # 사용자 ID (외래키, 기본키)
    # db.ForeignKey: 다른 테이블의 기본키를 참조하는 외래키를 설정하는 메서드
    # ondelete='CASCADE': 사용자가 삭제될 때 관련된 투표도 함께 삭제되도록 설정
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)    # 질문 ID (외래키, 기본키)
)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)    # 기본키 설정
    subject = db.Column(db.String(200), nullable=False) # 질문 제목
    content = db.Column(db.Text(), nullable=False)  # 질문 내용
    create_date = db.Column(db.DateTime(), nullable=False)  # 질문 생성일
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)  # 외래키 설정 (사용자 ID)
    # db.ForeignKey: 다른 테이블의 기본키를 참조하는 외래키를 설정하는 메서드
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set'))

answer_voter = db.Table(        # 답변 투표자 테이블 정의 (다대다 관계)
    'answer_voter', # 테이블 이름
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),   # 사용자 ID (외래키, 기본키)
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)    # 답변 ID (외래키, 기본키)
)

class Answer(db.Model): 
    id = db.Column(db.Integer, primary_key=True)    # 기본키 설정
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))   # 외래키 설정 (질문 ID)
    # db.ForeignKey: 다른 테이블의 기본키를 참조하는 외래키를 설정하는 메서드
    # ondelete='CASCADE': 질문이 삭제될 때 관련된 답변도 함께 삭제되도록 설정
    # CASCADE: 부모 레코드가 삭제될 때 자식 레코드도 함께 삭제되는 동작을 의미

    question = db.relationship('Question', backref=db.backref('answer_set'))    # 질문과의 관계 설정 (질문에 대한 답변 집합)
    # backref: 관계의 반대 방향을 설정하는 속성
    # db.relationship: SQLAlchemy의 ORM 기능을 사용하여 관계를 설정하는 메서드

    # question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    # cascade='all, delete-orphan': 부모 레코드가 삭제될 때 자식 레코드도 함께 삭제되도록 설정 (고아 레코드 삭제)
    # 고아 레코드: 부모와의 관계가 끊어진 자식 레코드

    content = db.Column(db.Text(), nullable=False)  # 답변 내용
    create_date = db.Column(db.DateTime(), nullable=False)  # 답변 생성일
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

class User(db.Model):   # 사용자 모델 정의
    id = db.Column(db.Integer, primary_key=True)    # 기본키 설정
    username = db.Column(db.String(150), unique=True, nullable=False)   # 사용자 이름
    # unique=True: 사용자 이름이 유일해야 함
    # nullable=False: 사용자 이름이 비어있으면 안 됨
    password = db.Column(db.String(200), nullable=False)    # 비밀번호
    email = db.Column(db.String(120), unique=True, nullable=False)  # 이메일