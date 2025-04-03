# InJoy - 질문 답변 커뮤니티 플랫폼

* **InJoy**는 사용자들이 질문을 등록하고, 답변을 공유할 수 있는 웹 기반 Q&A 커뮤니티 플랫폼입니다.  
* Flask 프레임워크와 SQLAlchemy ORM을 기반으로 구축되었으며, 다크/라이트 모드 전환 기능을 지원합니다.

---

## 🖼️ 구현 예시

![image](https://github.com/user-attachments/assets/2ee91486-fbd6-42e7-a7f7-129cefc52f57)
![image](https://github.com/user-attachments/assets/3cb8570e-e54e-48a2-84d3-dabf29dc1a99)
![image](https://github.com/user-attachments/assets/d7a492c7-6b3f-4634-8324-b33b793ce68f)

---

## 🔑 주요 기능

### ✅ 사용자 관리
- 회원가입 및 로그인 시스템
- 사용자 인증 및 권한 관리
- 세션 기반 사용자 관리

### ❓ 질문 기능
- 질문 등록, 수정, 삭제
- 질문 목록 조회 (페이징 처리)
- 질문 검색 기능
- 질문 좋아요

### 💬 답변 기능
- 답변 등록, 수정, 삭제
- 답변 페이징 처리
- 답변 좋아요

### 🎨 UI/UX
- 반응형 디자인 (Bootstrap 활용)
- 다크모드/라이트모드 전환
- 사용자 친화적인 인터페이스

---

## 🗂 프로젝트 구조

### 📁 템플릿
- `base.html`: 전체 공통 레이아웃
- `navbar.html`: 상단 네비게이션 바
- `question_list.html`: 질문 목록
- `question_detail.html`: 질문 상세
- `question_form.html`: 질문 등록/수정 폼
- `answer_form.html`: 답변 등록/수정 폼
- `login.html`, `signup.html`: 인증 관련 템플릿
- `form_errors.html`: 폼 오류 메시지 출력

### 🧩 뷰 (Views)
- `main_views.py`: 인덱스 및 기본 라우팅
- `question_views.py`: 질문 CRUD 기능
- `answer_views.py`: 답변 CRUD 기능
- `auth_views.py`: 사용자 인증 관련 기능

---

## ⚙️ 기술 스택

- **Backend**: Flask, SQLAlchemy
- **Frontend**: HTML, Bootstrap, JavaScript
- **Template Engine**: Jinja2
- **Authentication**: Flask-WTF, Werkzeug Security
- **Database**: SQLite 또는 PostgreSQL

---

## 🔐 보안 기능

- 비밀번호 해싱 (Werkzeug Security)
- CSRF 보호 (Flask-WTF)
- 로그인 필수 데코레이터로 권한 제어

---

## 🌟 사용자 경험

- 페이지 새로고침 없는 다크/라이트 모드 전환
- 로컬 스토리지 기반 테마 유지
- 검색 및 정렬 기능 제공

---

## 🌐 다국어 지원

- 한국어 UI 제공

---

## 🚀 설치 및 실행 방법

```bash
# 저장소 클론
git clone https://github.com/RJ-Stony/flask-injoy.git
cd injoy

# 가상환경 설정 및 의존성 설치
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 애플리케이션 실행
flask run
```



