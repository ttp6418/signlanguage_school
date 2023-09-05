# 해당 문서는 이메일을 이용한 비밀번호 재설정하는 도구 추가로 깃에서 그냥 받을시 다양한 이유로 실행이 안되기에 작성한 해결 방법입니다.

0. 사전준비
2차 휴대폰 인증이 되지않은 네이버 계정 하나 준비하고
네이버 메일 - 환경설정 - POP3/IMAP 설정 - 두개다 사용후 저장(문서에서는 IMAP만 사용해도된다함)

1. 터미널
python -m pip install django-environ   
pip install django-rest-auth-forked  

2. .gitignore 확인(git에서 받았으면 기본적으로 존재합니다) - manage.py와 같은 폴더에 있습니다.
!!! 만약에 이거 어기면 개인정보를 저희조끼리 열람가능하니 조심하기 바랍니다.
secrets.json
.env
login.txt

3. manage.py랑 같은 경로내에 .env파일 생성 및 입력
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = '587'
EMAIL_HOST = 'smtp.naver.com'
EMAIL_HOST_USER = '[본인네이버아이디]@naver.com'
EMAIL_HOST_PASSWORD = '[본인비밀번호]'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '[본인네이버아이디]@naver.com'

4. login.txt 를 manage.py와 같은 경로에 생성후 입력
[본인네이버아이디]@naver.com
[본인비밀번호]