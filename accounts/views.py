from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages

from .models import user, language
from .apps import get_client_ip

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from django.core.mail.message import EmailMessage   # 메일보내줌
from django.conf import settings                    # settings.py

from django.contrib.auth.hashers import make_password   # 무작위 SHA256 암호 생성
from django.contrib.auth.hashers import check_password  # SHA256 암호와 string 비교
from django.contrib.auth.hashers import is_password_usable  # 암호화 되어있는지 판단
from django.contrib.auth.password_validation import validate_password, password_validators_help_texts
import bcrypt                                       # 단방향 해시 암호화 기법인 SHA256에서 모든 경우의 수를 대입하면 뚫릴수있는 허점을 보완하기 위해 사용. 해싱+salt기법을 사용함
from django.contrib.auth import update_session_auth_hash    # 세션 초기화시 로그인 유지인데 사용 안하고 auth.login으로 대신함.
import re

from django.core.paginator import Paginator
from board.models import board

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
import os, requests , json
# 사용자에게 악의적인 데이터를 심어 외부링크로 접속하게 하는 행위 방지 
# iframe등을 사용시에는 예외 사용하며, 외부사이트 api사용시에도 예외해야할수 있음
# 그외에는 방지설정이 안전함

# Create your views here.
# 회원가입

# logger = logging.getLogger(__name__)

logger = logging.getLogger('my')

@xframe_options_deny
def signup(request):
    return render(request, 'signup.html')

# @xframe_options_deny
# def info_accept(request):
#     return render(request, 'info_accept.html')

# @xframe_options_deny
# def info_third_accept(request):
#     return render(request, 'info_third_accept.html')

# @xframe_options_deny
# def info_responsibility(request):
#     return render(request, 'info_responsibility.html')

@xframe_options_deny
def signup_logic(request):
    if request.method == 'GET': return render(request, 'signup.html')
    elif request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            # named = request.POST.get('name')
            lang = language.objects.all()
            users = user.objects.all()
            if ((request.POST.get('check1') == 'on') and (request.POST.get('check2') == 'on')):
                if (request.POST.get('language') != None) and (request.POST.get('username') != None) and (len(request.POST.get('password1')) >= 8) and (request.POST.get('email') != None) and (request.POST.get('nickname') != None): # (request.POST.get('pn') != None) 삭제됨
                    if request.POST.get('g-recaptcha-response') == '':
                        return HttpResponse("<script>alert('recaptcha에 체크해주셔야해요.');location.href='/accounts/signup';</script>")
                    # elif re.compile('\d{3}\d{3,4}\d{4}').match(request.POST.get('pn')) == None:
                        # return HttpResponse("<script>alert('휴대폰 번호를 다시 확인해주세요.');location.href='/accounts/signup';</script>")
                    elif re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$').match(request.POST.get('email')) == None:
                        return HttpResponse("<script>alert('이메일을 다시 확인해주세요.');location.href='/accounts/signup';</script>")
                    # elif users.filter(user_phoneNumber = request.POST.get('pn')).exists():
                        # return HttpResponse("<script>alert('이미 등록된 휴대폰 번호입니다.');location.href='/accounts/signup';</script>")
                    elif users.filter(email = request.POST.get('email')).exists():
                        return HttpResponse("<script>alert('이미 등록된 이메일입니다.');location.href='/accounts/signup';</script>")
                    elif users.filter(username = request.POST.get('username')).exists():
                        return HttpResponse("<script>alert('해당아이디는 존재합니다.');location.href='/accounts/signup';</script>")
                    else:
                        try: valid = validate_password(request.POST.get('password1'), request.POST.get('username'))
                        except:return HttpResponse("<script>alert('비밀번호 보안등급이 너무 낮습니다.[아이디/비밀번호 유사성, 영문 대소문자 여부, 8자리이상]]');location.href='/accounts/signup';</script>")
                        if valid != None: return HttpResponse("<script>alert('비밀번호 보안등급이 너무 낮습니다.');location.href='/accounts/signup';</script>")
                        else:
                            lang = lang.get(language_name=request.POST.get('language'))
                            user_info = user.objects.create_user(
                                                            username=request.POST.get('username'),
                                                            password=request.POST.get('password1'),
                                                            email=request.POST.get('email'),
                                                            first_name = request.POST.get('username')[0],
                                                            last_name = request.POST.get('username')[1:],
                                                            is_staff = False,
                                                            is_active = True,
                                                            is_superuser = False,
                                                            last_login = timezone.now(),
                                                            date_joined = timezone.now(),
                                                            user_nickname = request.POST.get('nickname'),
                                                            user_phoneNumber = None,
                                                            user_birthDate = None,
                                                            user_nationality = 'N/A',
                                                            user_sex = 's',
                                                            user_language = lang,
                                                            )
                            logger.info(request.POST.get('username') + '이가 회원가입함 ' + request.POST.get('nickname') + ' ' + request.POST.get('email') + ' ' + get_client_ip(request))
                            auth.login(request, user_info)
                            return redirect('/')
                else: return HttpResponse("<script>alert('필수 입력 조건은 충족해주세요!');location.href='/accounts/signup';</script>")
            else: return HttpResponse("<script>alert('필수 동의에 체크를 해주세요.');location.href='/accounts/signup';</script>")
        else: return HttpResponse("<script>alert('두 비밀번호가 다릅니다.');location.href='/accounts/signup';</script>")
        
@csrf_exempt
def idCheck(request):
    singup_db=user.objects.all()
    if singup_db.filter(username = request.POST.get('userID')).exists(): context={'msg': '이미 해당 아이디가 존재합니다.'}
    else: context={'msg': '아이디 사용이 가능합니다.'}
    return HttpResponse(json.dumps(context))

def myaccounts(request):
    pass

@xframe_options_deny
def login(request):
    if request.COOKIES.get('username') is not None:
        users = auth.authenticate(request, username=request.COOKIES.get('username'), password=request.COOKIES.get('password'))
        if users is not None:
            logger.info(request.COOKIES.get('username') + '이가 로그인함 ' + get_client_ip(request))
            auth.login(request, users)
            return redirect("/")
    else: return render(request, 'login.html')

@xframe_options_deny
def login_logic(request):
    if request.method == 'GET': return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = auth.authenticate(request, username=username, password=password)
        # ip = request.META.get('REMOTE_ADDR')
        # logger.debug('login user: {user} via ip: {ip}'.format(user=user,ip=ip))
        if users is not None:
            logger.info(request.POST.get('username') + '이가 로그인함 ' + get_client_ip(request))
            auth.login(request, users)
            if request.POST.get("login_cookie") == "TRUE":
                response = render(request, 'index.html')
                response.set_cookie('username',username)
                response.set_cookie('password',password)
            # return redirect('home')
            return HttpResponse("<script>alert('"+ users.user_nickname+ "님 환영합니다:)');location.href='/';</script>")
        elif not user.objects.all().filter(username = request.POST.get('username')).exists(): return HttpResponse("<script>alert('존재하지 않는 아이디입니다.');location.href='/accounts/login';</script>")
        else: return HttpResponse("<script>alert('비밀번호가 일치하지 않습니다.');location.href='/accounts/login';</script>")
    else: return render(request, 'login.html')

@xframe_options_deny
def logout(request):
    logger.info(request.user.username + '이가 로그아웃함 ' + get_client_ip(request))
    auth.logout(request)
    response = render(request, 'index.html')
    response.delete_cookie('username')
    response.delete_cookie('password')
    return HttpResponse("<script>alert('퇴장하셨습니다!');location.href='/';</script>")

@xframe_options_deny
def detail(request, pk):
    if (request.user.id != pk): return HttpResponse("<script>alert('잘못된 요청입니다.');location.href='/';</script>")
    elif (request.user.is_authenticated == True):
        User = get_user_model()
        user = get_object_or_404(User, pk=pk)
        context = {'user': user}
        return render(request, 'accounts_detail.html', context)
    else: return HttpResponse("<script>alert('로그인 정보가 없습니다.');location.href='/accounts/login';</script>")

@xframe_options_deny
def update(request, pk):
    if (request.user.id != pk): return HttpResponse("<script>alert('잘못된 요청입니다.');location.href='/';</script>")
    elif (request.user.is_authenticated == True):
        User = get_user_model()
        user = get_object_or_404(User, pk=pk)
        context = {'user': user}
        return render(request, 'update.html', context)
    else: return HttpResponse("<script>alert('로그인 정보가 없습니다.');location.href='/accounts/login';</script>")

@xframe_options_deny
def update_done(request, pk):
    if request.method == 'GET' or (request.user.id != pk): return HttpResponse("<script>alert('잘못된 요청입니다.');location.href='/';</script>")
    elif request.method == 'POST':
        if check_password(request.POST.get('password'), request.user.password) == False: return HttpResponse("<script>alert('비밀번호가 불일치합니다.');location.href='./update';</script>")
        else:
            if len(request.POST.get('new_password')) < 8: return HttpResponse("<script>alert('새 비밀번호는 8자리이상입니다.');location.href='./update';</script>")
            else:
                try: valid = validate_password(request.POST.get('new_password'), request.user.username)
                except: return HttpResponse("<script>alert('비밀번호 보안등급이 너무 낮습니다.');location.href='.';</script>")
                if valid != None: return HttpResponse("<script>alert('비밀번호 보안등급이 너무 낮습니다.');location.href='.';</script>")
                else:
                    if (request.POST.get('nickname') == '') or (request.POST.get('email') == ''): # (request.POST.get('pn') == '') or (request.POST.get('birthday') == '') 삭제
                        return HttpResponse("<script>alert('빈칸없이 입력해주세요.');location.href='./update';</script>")
                    # elif re.compile('\d{3}\d{3,4}\d{4}').match(request.POST.get('pn')) == None: return HttpResponse("<script>alert('휴대폰 번호를 다시 확인해주세요.');location.href='./update';</script>")
                    elif re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$').match(request.POST.get('email')) == None: return HttpResponse("<script>alert('이메일을 다시 확인해주세요.');location.href='./update';</script>")
                    else:
                        user_ = (user.objects.all()).get(id=request.user.id)
                        user_.user_nickname = request.POST.get('nickname')
                        user_.email = request.POST.get('email')
                        user_.user_birthDate = None
                        user_.user_phoneNumber = None
                        user_.user_nationality = 'N/A'
                        user_.user_sex = 's'
                        user_.user_language = language.objects.all().get(language_name=request.POST.get('language'))
                        user_.password = make_password(request.POST.get('new_password'))
                        user_.save()
                        logger.info(request.user.username + '이가 회원정보를 수정함 ' + request.POST.get('nickname') + ' ' + request.POST.get('email') +' '+ get_client_ip(request))
                        auth.logout(request)
                        userd = auth.authenticate(request, username=user_.username, password=request.POST.get('new_password'))
                        auth.login(request, userd)
                        return HttpResponse("<script>alert('내정보 변경완료.');location.href='/';</script>")
    else: return HttpResponse("<script>alert('잘못된 요청입니다.');location.href='/';</script>")

@xframe_options_deny
def delete_ok(request, pk): return render(request, 'delete.html')

@xframe_options_deny
def delete(request, pk):
    if request.method == 'POST':
        User = get_user_model()
        user = get_object_or_404(User, pk=pk)
        logger.info(request.user.username + '이가 회원탈퇴함 ' + request.user.user_nickname + ' ' + request.user.email +' '+ get_client_ip(request))
        user.delete()
        response = render(request, 'index.html')
        response.delete_cookie('username')
        response.delete_cookie('password')
        return HttpResponse("<script>alert('계정이 삭제되었습니다!');location.href='/';</script>")
    return render(request, 'delete.html')

@xframe_options_deny
def my_board(request, pk):
    # .get(board_author_id=pk)
    all_boards = board.objects.all().filter(board_author_id=pk).order_by('-board_no')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 6)
    boards = paginator.get_page(page)
    return render(request, 'my_board.html', context = {'boards':boards})

@xframe_options_deny
def password_reset(request): return render(request, 'password_reset.html')

@xframe_options_deny
def password_reset_done(request):
    if request.method == 'GET': return render(request, 'password_reset.html')
    elif request.method == 'POST':
        email_list = user.objects.all()
        try: email_send = email_list.get(email=request.POST.get('email')).email
        except: email_send = None
        if email_send == None: return HttpResponse("<script>alert('회원정보에 없는 이메일주소입니다.');location.href='/accounts/login/password_reset';</script>")
        else:
            new_pw = user.objects.make_random_password()
            user_ = email_list.get(email=request.POST.get('email'))
            user_.password = make_password(new_pw)
            logger.info(user_.username + '이가 비밀번호 찾기 실행 ' + get_client_ip(request))
            user_.save()
            email_list.get(email=request.POST.get('email')).set_password(new_pw)
            email_list.get(email=request.POST.get('email')).save(update_fields=['password'])
            EmailMessage(subject='이메일 변경 내역입니다.', body='수어 스쿨의 새 비밀번호는 '+new_pw +'입니다. 다시 로그인해주세요.', to=[email_send], from_email=settings.EMAIL_HOST_USER).send()
            return render(request, 'password_reset_done.html')

@xframe_options_deny
def view_info_accept(request): return render(request, 'info_accept.html')

@xframe_options_deny
def view_info_third_accept(request): return render(request, 'info_third_accept.html')

############# 카카오 로그인 ####################
def kakaoLoginLogic(request):
    _restApiKey = '1835de27a954f8bcf665f2f9bfa68412'
    _redirectUrl = 'http://127.0.0.1:8000/accounts/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/authorize?client_id={_restApiKey}&redirect_uri={_redirectUrl}&response_type=code'
    return redirect(_url)

def kakaoLoginLogicRedirect(request):
    _qs = request.GET['code']
    _restApiKey = '1835de27a954f8bcf665f2f9bfa68412' 
    _redirect_uri = 'http://127.0.0.1:8000/accounts/kakaoLoginLogicRedirect'
    _url = f'https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={_restApiKey}&redirect_uri={_redirect_uri}&code={_qs}'
    #response = requests.get(_url, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    #print(response)
    _res = requests.post(_url)
    _result = _res.json()
    request.session['access_token'] = _result['access_token']
    request.session.modified = True
    
    _token = request.session['access_token']
    REQUEST_URL = "https://kapi.kakao.com/v2/user/me"
    _header = {'Authorization': f'bearer {_token}'}

    profile_request = requests.get(REQUEST_URL, headers=_header)
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    profile = kakao_account.get("profile")
    
    nickname = profile.get("nickname")
    email = kakao_account.get("email")
    # gender = kakao_account.get("gender")
    # birthday = kakao_account.get("birthday")

    """if gender == 'male':gender = 'm'
    elif gender == 'female':gender = 'f'
    else: gender = 's'"""

    if email == None: email = 'none@none.com'
    
    singup_db=user.objects.all()
    lang = language.objects.all()
    lang = lang.get(language_name='한국어')
    
    if singup_db.filter(username = nickname).exists() or singup_db.filter(email = email).exists(): users = auth.authenticate(request, username=nickname, password='a0000')
    else:
        users = user.objects.create_user(
                                    username=nickname,
                                    password='a0000',
                                    email=email,
                                    first_name = nickname[0],
                                    last_name = nickname[1:],
                                    is_staff = False,
                                    is_active = True,
                                    is_superuser = False,
                                    last_login = timezone.now(),
                                    date_joined = timezone.now(),
                                    user_nickname = nickname,
                                    user_sex = 's',
                                    user_language = lang,
                                    user_birthDate = None,
                                    user_nationality='N/A',
                                    user_phoneNumber = None,
                                    )
    logger.info(users.username + '이가 카카오로그인함 ' + get_client_ip(request))                                
    auth.login(request, users)
    return HttpResponse("<script>alert('초기비밀번호는 a0000입니다. 개인정보 수정해주세요.');location.href='/';</script>")

def kakaoLogout(request):
    _token = request.session['access_token']
    _url = 'https://kapi.kakao.com/v1/user/unlink'
    _header = {'Authorization': f'bearer {_token}'}
    _res = requests.post(_url, headers=_header)
    _result = _res.json()
    if _result.get('id'):
        del request.session['access_token']
        return render(request, 'index.html')
    else: return render(request, 'login.html')