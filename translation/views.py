from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.storage import FileSystemStorage
from django.views.generic.detail import SingleObjectMixin
from django.http import FileResponse
import json
import os
import random
import time
import urllib.request
from models.function import main as video_func

logger = logging.getLogger('my')

# Create your views here.

def translation(request):
    return render(request, 'translation.html')

def translation_web(request):
    return render(request, 'translation_web.html')

def translation_text(request):
    return render(request, 'translation_text.html')

def translation_sign(request):
    return HttpResponse("<script>alert('아직 지원되지 않네요');location.href='/';</script>")

def translation_download(request):
    return render(request, 'translation_download.html')

def translation_download_os(request, os_name):
    file_path = os.getcwd() + '/mysite/static/programs/translation/' + os_name + '/_main.exe'
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path, 'rb'), content_type='.exe')
    response['Content-Disposition'] = f'attachment; filename={"translation.exe"}'
    return response

def mp4_upload(request):
    return render(request, 'translation_mp4_upload.html')

def mp4_download(request):
    if request.method == 'POST':
        if request.POST.get('check_'):
        # if request.POST.get('video'):
            # if request.POST.get('video').split('.')[-1] == 'mp4':
            try: vd = request.FILES['video']
            except: return HttpResponse("<script>alert('mp4파일이 아니에요.');location.href='/translation/mp4_upload';</script>")
            try: os.mkdir(os.getcwd() + '/mysite/static/request/') # os.path.exist와 같음
            except: pass
            filepath = os.getcwd() + '/mysite/static/request/'
            writepath = os.getcwd() + '/mysite/static/request/'
            filename = str(random.randint(0, 999999999999)).zfill(12)
            with open(writepath + filename + '_original.mp4', 'wb+') as destination:
                for chunk in vd.chunks(): destination.write(chunk)
            video_func.video_source_function(filepath=filepath, writepath=writepath, filename=filename)

            """file_path = os.getcwd() + '/mysite/static/request/' + filename + '_complete.mp4'

            fs = FileSystemStorage(file_path)
            response = FileResponse(fs.open(file_path, 'rb'), content_type='.mp4')
            response['Content-Disposition'] = f'attachment; filename={"translation.mp4"}'
            return response"""

            return redirect('view/'+str(filename))
            # else: return HttpResponse("<script>alert('mp4파일이 아니에요.');location.href='/';</script>")
        # else: return HttpResponse("<script>alert('파일을 올려주세요.');location.href='/';</script>")
        else: return HttpResponse("<script>alert('체크박스 동의는 필수사항입니다.');location.href='/translation/mp4_upload';</script>")
    else: return HttpResponse("<script>alert('잘못된 접근입니다.');location.href='/';</script>")

def url_upload(request):
    return render(request, 'translation_url_upload.html')

def url_download(request):
    if request.method == 'POST':
        if request.POST.get('check_'):
        # if request.POST.get('video'):
            # if request.POST.get('video').split('.')[-1] == 'mp4':
            vd = request.POST.get('url')
            if vd == '': return HttpResponse("<script>alert('url을 입력해주세요.');location.href='/translation/url_upload';</script>")
            else:
                try: res = urllib.request.urlopen(vd)
                except: return HttpResponse("<script>alert('url을 확인해주세요.');location.href='/translation/url_upload';</script>")
                if res.status == 200:
                    if 'youtube' in vd:
                        try: os.mkdir(os.getcwd() + '/mysite/static/request/') # os.path.exist와 같음
                        except: pass
                        filepath = os.getcwd() + '/mysite/static/request/'
                        writepath = os.getcwd() + '/mysite/static/request/'
                        filename = str(random.randint(0, 999999999999)).zfill(12)
                        video_func.youtube_source_function(url=vd, writepath=writepath, filename=filename)

                        """file_path = os.getcwd() + '/mysite/static/request/' + filename + '_complete.mp4'

                        fs = FileSystemStorage(file_path)
                        response = FileResponse(fs.open(file_path, 'rb'), content_type='.mp4')
                        response['Content-Disposition'] = f'attachment; filename={"translation.mp4"}'
                        return response"""
                        # urls = "request/" + filename + "_complete.mp4"
                        return redirect('view/'+str(filename))
                        # return render(request, 'translation_view.html', context={'video_no': str(filename), 'urls' : urls})
                        # else: return HttpResponse("<script>alert('mp4파일이 아니에요.');location.href='/';</script>")
                    else: return HttpResponse("<script>alert('유튜브 url이 아닌것 같아요.');location.href='/translation/url_upload';</script>")
                else: return HttpResponse("<script>alert('url을 확인해주세요.');location.href='/translation/url_upload';</script>")
            # else: return HttpResponse("<script>alert('파일을 올려주세요.');location.href='/';</script>")
        else: return HttpResponse("<script>alert('체크박스 동의는 필수사항입니다.');location.href='/translation/url_upload';</script>")
    else: return HttpResponse("<script>alert('잘못된 접근입니다.');location.href='/';</script>")

def translation_view(request, video_no):
    return render(request, 'translation_view.html', context={'video_no': str(video_no), 'urls' : "request/" + str(video_no) + "_complete.mp4"})

def translation_view_download(request, video_no):
    file_path = os.getcwd() + '/mysite/static/request/' + str(video_no) + '_complete.mp4'

    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_path, 'rb'), content_type='.mp4')
    name_download = "translation_" + str(video_no) + ".mp4"
    response['Content-Disposition'] = f'attachment; filename={name_download}'
    try: os.remove(os.getcwd() + '/mysite/static/request/' + str(video_no) + '_merge.mp4')
    except: pass
    try: os.remove(os.getcwd() + '/mysite/static/request/' + str(video_no) + '_original.mp4')
    except: pass
    try: os.remove(os.getcwd() + '/mysite/static/request/' + str(video_no) + '_output.mp4')
    except: pass
    try: os.remove(os.getcwd() + '/mysite/static/request/' + str(video_no) + '_script.txt')
    except: pass
    try: os.remove(os.getcwd() + '/mysite/static/request/' + str(video_no) + '.wav')
    except: pass
    try: os.remove(os.getcwd() + '/mysite/static/request/' + str(video_no) + '_sentence.txt')
    except: pass
    try: os.remove(os.getcwd() + '/mysite/static/request/' + str(video_no) + '_subtitle.srt')
    except: pass
    return response