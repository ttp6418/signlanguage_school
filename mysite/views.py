from django.shortcuts import render
from django.utils import timezone
import logging
from django.conf import settings
from django.core.files.storage import default_storage
import numpy as np
import cv2
import string
from keras.models import load_model
from education.models import subject, video
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import json

def main(request):
    subject_list = subject.objects.all()
    return render(request, 'index.html',context={'subject' : subject_list})

def good(request):
    return render(request, 'components.html')

@csrf_exempt
def subjectList(request):
    subject_list = subject.objects.all()
    data = []
    for subjects in subject_list:
        data.append({
            'name'      : subjects.subject_name,
            'image'     : subjects.subject_thumb.path,
            'id'        : subjects.subject_id
        })
        
    return JsonResponse(data,safe=False)
    # return HttpResponse(json.dumps(subject_list, cls=DjangoJSONEncoder) , content_type='application/json')
    
@csrf_exempt
def basicEduList(request):
    sebject_id = request.POST.get('sebject_id')
    
    video_list = video.objects.all().filter(video_subject = sebject_id).order_by('video_index')
    data = []
    
    for videos in video_list:
        data.append({
            'name'          : videos.video_title,
            'text'          : videos.video_text,
            'image'         : videos.video_thumb.path,
            'sebject_id'    : sebject_id
        })
        
    return JsonResponse(data,safe=False)  