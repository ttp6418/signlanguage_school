from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, Http404
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django.db.models import Q

#from django.template import loader
#from common import reqUtil, dbUtil
#from django.db.models import Q

from .models import board, comment, Like
from .apps import get_client_ip

import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model

from django.core.paginator import Paginator
from accounts.models import user

import datetime

from django.core.files.base import ContentFile

from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

from django.core.mail.message import EmailMessage   # 메일보내줌
from django.conf import settings                    # settings.py
from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger('my')

# def board_index(request):
#     #all_boards = board.objects.all().order_by("-board_date")
#     #return render(request, 'index.html', {'title':'Board List', 'board_list':all_boards})
#     # return render(request,'index.html')
#     board_list = board.objects.all()    
#     search_key = request.GET.get("keyword")
#     if search_key:
#         board_list = board.objects.filter(board_name__icontains=search_key)
#     return render(request, 'board_index.html', {'board_all':board_list, 'q':search_key})
#     # return render(request, 'board_index.html')

def notice(request):
    all_boards = board.objects.all().filter(board_category="notice").order_by('-board_no')
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 5)
    boards = paginator.get_page(page)
    return render(request, 'notice.html', context = {'boards':boards})

@csrf_exempt
def noticeSearch(request):
    all_boards = board.objects.all().filter(board_category="notice").order_by('-board_no')
    search = request.POST.get('search')
    if (all_boards.filter(board_name__contains=search).exists()):
        all_boards = all_boards.filter(board_name__contains=search)
        page = int(request.GET.get('p', 1))
        paginator = Paginator(all_boards, 5)
        boardList = paginator.get_page(page)
        data = []
        for boards in boardList:
            data.append({
                'no'    : boards.board_no,
                'name'  : boards.board_name,
                'date'  : boards.board_date,
                'view'  : boards.board_view
            })
        return JsonResponse(data,safe=False)
    else:
        return

def FAQ(request):
    all_boards = board.objects.all().filter(board_category="faq").order_by('-board_no')
    for b in range(len(all_boards)):
        if all_boards[b].board_author.is_superuser == True or all_boards[b].board_author.id == 0: pass
        elif len(all_boards[b].board_author.user_nickname) >= 3:
            all_boards[b].board_author.user_nickname = all_boards[b].board_author.user_nickname[0] + '*' * (len(all_boards[b].board_author.user_nickname)-2) + all_boards[b].board_author.user_nickname[-1]
        else: all_boards[b].board_author.user_nickname = "**"
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 5)
    boards = paginator.get_page(page)
    return render(request, 'FAQ.html', context = {'boards':boards})

@csrf_exempt
def FAQSearch(request):
    all_boards = board.objects.all().filter(board_category="faq").order_by('-board_no')
    search = request.POST.get('search')
    if (all_boards.filter(board_name__contains=search).exists()):
        all_boards = all_boards.filter(board_name__contains=search)
        for b in range(len(all_boards)):
            if all_boards[b].board_author.is_superuser == True or all_boards[b].board_author.id == 0: pass
            elif len(all_boards[b].board_author.user_nickname) >= 3:
                all_boards[b].board_author.user_nickname = all_boards[b].board_author.user_nickname[0] + '*' * (len(all_boards[b].board_author.user_nickname)-2) + all_boards[b].board_author.user_nickname[-1]
            else: all_boards[b].board_author.user_nickname = "**"
        page = int(request.GET.get('p', 1))
        paginator = Paginator(all_boards, 5)
        boardList = paginator.get_page(page)
        data = []
        for boards in boardList:
            data.append({
                'no'    : boards.board_no,
                'name'  : boards.board_name,
                'username'  : boards.board_author.user_nickname,
                'date'  : boards.board_date,
                'view'  : boards.board_view
            })
        return JsonResponse(data,safe=False)
    else:
        return

def freeboard(request):
    all_boards = board.objects.all().filter(board_category="free").order_by('-board_no')
    for b in range(len(all_boards)):
        if all_boards[b].board_author.is_superuser == True or all_boards[b].board_author.id == 0: pass
        elif len(all_boards[b].board_author.user_nickname) >= 3:
            all_boards[b].board_author.user_nickname = all_boards[b].board_author.user_nickname[0] + '*' * (len(all_boards[b].board_author.user_nickname)-2) + all_boards[b].board_author.user_nickname[-1]
        else: all_boards[b].board_author.user_nickname = "**"
    page = int(request.GET.get('p', 1))
    paginator = Paginator(all_boards, 5)
    boards = paginator.get_page(page)
    return render(request, 'freeboard.html', context = {'boards':boards})

@csrf_exempt
def freeboardSearch(request):
    search = request.POST.get('search')
    searchCategory = request.POST.get('searchCategory')
    all_boards = board.objects.all().filter(board_category="free").order_by('-board_no')
    if (searchCategory == '제목'):
        if (all_boards.filter(board_name__contains=search).exists()):
            all_boards = all_boards.filter(board_name__contains=search)
            for b in range(len(all_boards)):
                if all_boards[b].board_author.is_superuser == True or all_boards[b].board_author.id == 0: pass
                elif len(all_boards[b].board_author.user_nickname) >= 3:
                    all_boards[b].board_author.user_nickname = all_boards[b].board_author.user_nickname[0] + '*' * (len(all_boards[b].board_author.user_nickname)-2) + all_boards[b].board_author.user_nickname[-1]
                else: all_boards[b].board_author.user_nickname = "**"
            page = int(request.GET.get('p', 1))
            paginator = Paginator(all_boards, 5)
            boardList = paginator.get_page(page)
            data = []
            for boards in boardList:
                data.append({
                    'no'        : boards.board_no,
                    'name'      : boards.board_name,
                    'username'  : boards.board_author.user_nickname,
                    'date'      : boards.board_date,
                    'view'      : boards.board_view
                })
            return JsonResponse(data,safe=False)
        else:
            return
    elif(searchCategory == '글쓴이'):
        if (all_boards.filter(board_author__username__contains=search).exists()):
            all_boards = all_boards.filter(board_author__username__contains=search)
            for b in range(len(all_boards)):
                if all_boards[b].board_author.is_superuser == True or all_boards[b].board_author.id == 0: pass
                elif len(all_boards[b].board_author.user_nickname) >= 3:
                    all_boards[b].board_author.user_nickname = all_boards[b].board_author.user_nickname[0] + '*' * (len(all_boards[b].board_author.user_nickname)-2) + all_boards[b].board_author.user_nickname[-1]
                else: all_boards[b].board_author.user_nickname = "**"
            page = int(request.GET.get('p', 1))
            paginator = Paginator(all_boards, 5)
            boardList = paginator.get_page(page)
            data = []
            for boards in boardList:
                data.append({
                    'no'        : boards.board_no,
                    'name'      : boards.board_name,
                    'username'  : boards.board_author.user_nickname,
                    'date'      : boards.board_date,
                    'view'      : boards.board_view
                })
            return JsonResponse(data,safe=False)
        else:
            return
    else:
        return

def noticeDetail(request):
    if request.user.is_superuser and request.user.is_staff and request.user.is_authenticated:
        return render(request, 'noticeDetail.html')
    else: return HttpResponse("<script>alert('관리자만 접근가능합니다.');location.href='/';</script>")

def FAqdetail(request):
    if request.user.is_authenticated:
        return render(request, 'FAqDetail.html')
    else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/accounts/login/';</script>")

def freedetail(request):
    if request.user.is_authenticated:
        return render(request, 'freeDetail.html')
    else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/accounts/login/';</script>")

def faq_admin_view(request, board_id):
    if request.user.is_authenticated and request.user.is_superuser: 
        board_list = board.objects.all()
        boardd = board_list.get(board_no=board_id)
        return render(request, 'faq_admin_view.html', context={'board': boardd})
    else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/accounts/login/';</script>")

def faq_admin_view_done(request, board_id):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            board_list = board.objects.all()
            boardd = board_list.get(board_no=board_id)
            to = boardd.board_text.split('#')[-1]
            title = boardd.board_name
            text = boardd.board_text
            logger.info(request.user.username + '이가 ' + boardd.board_author.username + '의 ' + title + '질문을 답변함 '+ to + ' ' + get_client_ip(request))
            EmailMessage(subject=title+'에 대한 답변내용입니다.', body=text + '에 대한 문의 답변입니다.\n\n' + request.POST.get('answer') + '\n\n이 답변은 답장을 보낼수 없으며, 이후 문의사항은 새로 문의를 해주시기 바랍니다.', to=[to], from_email=settings.EMAIL_HOST_USER).send()
            boardd.delete()
            return HttpResponse("<script>alert('답변 완료.');location.href='/board/FAQ';</script>")
        else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/accounts/login/';</script>")
    else: return HttpResponse("<script>alert('정상적인 접근이 아닙니다.');location.href='/';</script>")

def faq_admin_write(request):
    if request.user.is_authenticated and request.user.is_superuser: return render(request, 'faq_admin_write.html')
    else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/accounts/login/';</script>")

def faq_admin_write_save(request):
    if request.method == 'GET':
        return render(request, 'FAqDetail.html')
    elif request.method == 'POST':
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
        else: ip = request.META.get('REMOTE_ADDR')
        new_board = board.objects.create(board_name=request.POST.get('title'),
                                    board_text = request.POST.get('comment'),
                                    board_author = request.user,
                                    board_category = 'faq',
                                    board_img = request.FILES.get('img'),
                                    board_date = datetime.datetime.now(),
                                    board_view = 0,
                                    board_like = 0,
                                    board_score = 0,
                                    board_ip = ip)
        logger.info(new_board.board_name + new_board.board_text + new_board.board_author.username + '가 faq 공지로 등록됨 ' + get_client_ip(request))
        return HttpResponse("<script>alert('글 등록 완료.');location.href='/board/FAQ';</script>")
    else: return render(request, 'freeDetail.html')

def noticedetail_save(request):
    if request.method == 'GET':
        return render(request, 'noticeDetail.html')
    elif request.method == 'POST':
        new_board = board.objects.create(board_name=request.POST.get('title'),
                                    board_text = request.POST.get('comment'),
                                    board_author = request.user,
                                    board_category = 'notice',
                                    board_img = request.FILES.get('img'),
                                    board_date = datetime.datetime.now(),
                                    board_view = 0,
                                    board_like = 0,
                                    board_score = 0)
        logger.info(new_board.board_name + new_board.board_text + new_board.board_author.username + '가 공지사항을 등록함 ' + get_client_ip(request))
        return HttpResponse("<script>alert('글 등록 완료.');location.href='/board/noticeDetail';</script>")
    else: return render(request, 'noticeDetail.html')

def freedetail_save(request):
    if request.method == 'GET':
        return render(request, 'freeDetail.html')
    elif request.method == 'POST':
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
        else: ip = request.META.get('REMOTE_ADDR')
        new_board = board.objects.create(board_name=request.POST.get('title'),
                                    board_text = request.POST.get('comment'),
                                    board_author = request.user,
                                    board_category = 'free',
                                    board_img = request.FILES.get('img'),
                                    board_date = datetime.datetime.now(),
                                    board_view = 0,
                                    board_like = 0,
                                    board_score = 0,
                                    board_ip = ip)
        logger.info(new_board.board_name + new_board.board_text + new_board.board_author.username + '가 자유글을 등록함 ' + get_client_ip(request))
        return HttpResponse("<script>alert('글 등록 완료.');location.href='/board/freeboard';</script>")
    else: return render(request, 'freeDetail.html')

def faqdetail_save(request):
    if request.method == 'GET':
        return render(request, 'FAqDetail.html')
    elif request.method == 'POST':
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
        else: ip = request.META.get('REMOTE_ADDR')
        new_board = board.objects.create(board_name=request.POST.get('title'),
                                    board_text = request.POST.get('comment') + '#' + request.POST.get('email'),
                                    board_author = request.user,
                                    board_category = 'faq',
                                    board_img = request.FILES.get('img'),
                                    board_date = datetime.datetime.now(),
                                    board_view = 0,
                                    board_like = 0,
                                    board_score = 0,
                                    board_ip = ip)
        logger.info(new_board.board_name + new_board.board_text + new_board.board_author.username + '가 질문게시판에 글 올림 ' + get_client_ip(request))
        return HttpResponse("<script>alert('글 등록 완료.');location.href='/board/FAqDetail';</script>")
    else: return render(request, 'freeDetail.html')

def view(request, board_id):
    try:
        board_list = board.objects.all()
        boardd = board_list.get(board_no=board_id)
        boardd.board_view += 1
        boardd.save()
        if boardd.board_author.is_superuser == True or boardd.board_author.id == 0: pass
        elif len(boardd.board_author.user_nickname) >= 3:
            boardd.board_author.user_nickname = boardd.board_author.user_nickname[0] + '*' * (len(boardd.board_author.user_nickname)-2) + boardd.board_author.user_nickname[-1]
        else: boardd.board_author.user_nickname = "**"
        comment_list = comment.objects.all()
        commentd = comment_list.filter(comment_board_no=board_id)
        return render(request, 'board_view.html', {'board': boardd, 'comment':commentd})
    except:
        return HttpResponse("<script>alert('글이 삭제되었거나 없습니다.');location.href='/';</script>")

def board_comment_write(request, board_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('comment') == '':
                return HttpResponse("<script>alert('댓글을 입력해주세요.');location.href='/';</script>")
            else:
                b = board.objects.all().get(board_no = board_id)
                new_comment = comment.objects.create(comment_content=request.POST.get('comment'),
                                        comment_date = datetime.datetime.now(),
                                        comment_user_id = request.user,
                                        comment_board_no = b
                                        )
                logger.info(new_comment.comment_board_no.board_name + new_comment.comment_content + new_comment.comment_user_id.username + '가 댓글을 등록함 ' + get_client_ip(request))
                # b.reply_set.create(comment=request.POST['comment'], rep_date=timezone.now())
            return HttpResponse("<script>alert('등록되었습니다.');location.href='.';</script>")
        else:
            return redirect('.')
    else:
        return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/';</script>")

@csrf_exempt
def like(request, board_id):
    res_data={}
    if request.user.is_authenticated:
        q = Q()
        q.add(Q(board_no=board_id), Q.OR)
        q.add(Q(like_user_id = request.user), Q.AND)
        like_obj = Like.objects.filter(q).values()
        if not like_obj:
            board_list = board.objects.all()
            boardd = board_list.get(board_no=board_id)
            boardd.board_like += 1
            boardd.save()
            Like.objects.create(board_no=board_id, 
                                like_user_id = request.user,)
            res_data['rescd']= '00'
            res_data['resdesc']= ''
            res_data['board_like']= boardd.board_like
            res_data['board_view']= boardd.board_view
        else:
            res_data['rescd']= '-1'
            res_data['resdesc']= '추천을 이미 누르셨습니다.'    
    else: 
        res_data['rescd']= '-99'
        res_data['resdesc']= '로그인이 필요한 서비스입니다.'
    return HttpResponse(json.dumps(res_data, cls=DjangoJSONEncoder), content_type='application/json')

def board_delete_ok(request, board_id):
    return render(request, 'board_delete.html')

def board_delete(request, board_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            boarda = board.objects.all().get(board_no=board_id)
            logger.info(boarda.board_name + boarda.board_text + boarda.board_author.username + '가 게시글 삭제 ' + get_client_ip(request))
            boarda.delete()
            return redirect('/board/freeboard')
        else: return HttpResponse("<script>alert('로그인이 필요한 서비스입니다.');location.href='/';</script>")
    else: return HttpResponse("<script>alert('잘못된 접근입니다.');location.href='/';</script>")

def board_update(request, board_id):
    if request.user.is_authenticated:
        boarda = board.objects.all().get(board_no=board_id)
        if (request.user.is_superuser) or (boarda.board_author.id == request.user.id):
            if boarda.board_category == 'faq': email = boarda.board_text.split('#')[-1]
            else: email = ''
            return render(request, 'board_update.html', {'board': boarda, 'email' : email})
        else: return HttpResponse("<script>alert('계정정보가 옳바르지 않습니다.');location.href='/';</script>")
    else: return HttpResponse("<script>alert('로그인은 필수입니다.');location.href='.';</script>")

def board_update_done(request, board_id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            boarda = board.objects.all().get(board_no=board_id)
            if (request.user.is_superuser) or (boarda.board_author.id == request.user.id):
                boarda.board_text = request.POST.get('comment')
                if boarda.board_category == 'faq':
                    boarda.board_text = boarda.board_text + '#' + request.POST.get('email')
                boarda.board_name = request.POST.get('title')
                if boarda.board_name[-4:] != '(수정됨)':
                    boarda.board_name = boarda.board_name + '(수정됨)'
                if request.FILES.get('img'):
                    boarda.board_img = request.FILES.get('img')
                logger.info(boarda.board_name + boarda.board_text + boarda.board_author.username + '가 게시글 수정 ' + get_client_ip(request))
                boarda.save()
                return HttpResponse("<script>alert('성공적으로 저장됨.');location.href='./';</script>")
            else: return HttpResponse("<script>alert('계정정보가 옳바르지 않습니다.');location.href='/';</script>")
        else: return HttpResponse("<script>alert('로그인은 필수입니다.');location.href='./accounts/login';</script>")
    else: return HttpResponse("<script>alert('잘못된 접근입니다.');location.href='/';</script>")