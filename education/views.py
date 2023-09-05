from django.shortcuts import render
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from accounts.models import user, language
from .models import subject, video, video_history, video_like, video_subscribe
from django.dispatch import receiver
from .apps import get_client_ip

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

# from django.core.mail.message import EmailMessage   # 메일보내줌
from django.conf import settings                    # settings.py

from django.contrib.auth.hashers import make_password   # 무작위 SHA256 암호 생성
from django.contrib.auth.hashers import check_password  # SHA256 암호와 string 비교
# import bcrypt                                       # 단방향 해시 암호화 기법인 SHA256에서 모든 경우의 수를 대입하면 뚫릴수있는 허점을 보완하기 위해 사용. 해싱+salt기법을 사용함
# from django.contrib.auth import update_session_auth_hash    # 세션 초기화시 로그인 유지인데 사용 안하고 auth.login으로 대신함.
# import re

# from django.core.paginator import Paginator
# from board.models import board

import datetime
import cv2

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.clickjacking import xframe_options_deny
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
import os, requests , json

from django.core.files.uploadhandler import TemporaryFileUploadHandler, FileUploadHandler, MemoryFileUploadHandler

logger = logging.getLogger('my')

def education_morelist(request):
    subject_list = subject.objects.all()
    video_list = video.objects.all()
    return render(request, 'education_more_list.html', context={'subject' : subject_list, 'video': video_list})

def education_moresubject(request, subject_id):
    try:
        video_list = video.objects.all().filter(video_subject = subject_id).order_by('video_index')
        return render(request, 'education_more_subject.html', context={'video': video_list, 'id':subject_id})
    except: return HttpResponse("<script>alert('없는 교육장입니다.');location.href='/education/list';</script>")

def education_password(request):
    return render(request, 'education_password.html')

def education_password_check(request, subject_id, video_name):
    if request.method == 'POST':
        video_list = video.objects.all().filter(video_subject = subject_id).get(video_title = video_name)
        if check_password(request.POST.get('pw'), video_list.video_pw):
            video_list = video.objects.all().filter(video_subject = subject_id).get(video_title = video_name)
            video_list_all = video.objects.all().filter(video_subject = subject_id).order_by('video_index')
            urls = "mp4/" + str(video_list.video_subject.subject_id) + '/' + video_list.video_title + ".mp4"
            video_list.video_views += 1
            video_list.save()
            return render(request, 'education_more_view.html', context={'video': video_list, 'urls' : urls, 'video_all': video_list_all})
        else: return HttpResponse("<script>alert('비밀번호가 다릅니다.');location.href='/education/list';</script>")
    else: return HttpResponse("<script>alert('잘못된 요청입니다.');location.href='/education/list';</script>")

def education_moreview(request, subject_id, video_name):
    video_list = video.objects.all().filter(video_subject = subject_id).get(video_title = video_name)
    if video_list.video_pw: return render(request, 'education_password.html')
    try:
        video_list_all = video.objects.all().filter(video_subject = subject_id).order_by('video_index')
        urls = "mp4/" + str(video_list.video_subject.subject_id) + '/' + video_list.video_title + ".mp4"
        video_list.video_views += 1
        video_list.save()
        return render(request, 'education_more_view.html', context={'video': video_list, 'urls' : urls, 'video_all': video_list_all})
    except: return HttpResponse("<script>alert('없는 교육장입니다.');location.href='/education/list';</script>")

def education_morewrite(request, subject_id):
    try:
        subject_list = subject.objects.all().get(subject_id = subject_id)
        return render(request, 'education_more_write.html', context={'subject': subject_list})
    except: return HttpResponse("<script>alert('없는 교육장입니다.');location.href='/education/list';</script>")

def education_morewrite_done(request, subject_id):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            vd = request.FILES['video']
            try: os.mkdir(os.getcwd() + '/mysite/static/mp4/' + str(subject_id)) # os.path.exist와 같음
            except:pass
            with open(os.getcwd() + '/mysite/static/mp4/' + str(subject_id) + '/' + request.POST.get('title') + '.mp4', 'wb+') as destination:
                for chunk in vd.chunks(): destination.write(chunk)
            new_video = video.objects.create(video_title=request.POST.get('title'),
                                        video_text = request.POST.get('text'),
                                        video_index = request.POST.get('index'),
                                        video_date = datetime.datetime.now(),
                                        video_pw = make_password(request.POST.get('pw')),
                                        video_views = 0,
                                        video_likes = 0,
                                        video_author = request.user,
                                        video_subject = subject.objects.all().get(subject_id = subject_id),
                                        video_thumb = request.FILES.get('thumb'),
                                        )
            return redirect('/education/')
        else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/accounts/login/';</script>")
    else: return HttpResponse("<script>alert('정상적인 접근이 아닙니다.');location.href='/';</script>")

def subject_add(request):
    if request.user.is_authenticated and request.user.is_superuser: return render(request, 'subject_add.html')
    else: return HttpResponse("<script>alert('특정 인원만 허용된 서비스입니다.');location.href='/education/';</script>")

def subject_add_done(request):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            new_subject = subject.objects.create(subject_name=request.POST.get('title'),
                                        subject_thumb = request.FILES.get('thumb'),
                                        )
            return redirect('/education/')
        else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/accounts/login/';</script>")
    else: return HttpResponse("<script>alert('정상적인 접근이 아닙니다.');location.href='/';</script>")
