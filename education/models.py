from django.db import models
from accounts.models import user

# Create your models here.

class subject(models.Model):
    subject_id = models.BigAutoField(primary_key=True) # 나중에 관리용으로 폴더를 static/id형태로 구분할것
    subject_name = models.CharField(max_length=20)
    subject_thumb = models.ImageField(upload_to='subject/',blank=True, null=True)
    subject_original = models.CharField(max_length=40, null=True, blank=True, default=None)

class video(models.Model):
    video_title = models.CharField(max_length=200, primary_key=True) # .mp4 파일명
    video_text = models.TextField(null=True, default='')
    video_author = models.ForeignKey(user, on_delete=models.SET(0))
    video_subject = models.ForeignKey(subject, on_delete=models.CASCADE, null=True, blank=True)
    video_index = models.IntegerField()
    video_date = models.DateField(auto_now_add=True)
    video_pw = models.TextField(null=True, default='')
    video_views = models.IntegerField(default=0)
    video_likes = models.IntegerField(default=0)
    video_thumb = models.ImageField(upload_to='video/',blank=True, null=True)

    def __str__(self):
        return self.video_title

class video_history(models.Model):
    history_no = models.BigAutoField(primary_key=True)
    history_user = models.ForeignKey(user, on_delete=models.CASCADE)
    history_video = models.ForeignKey(video, on_delete=models.CASCADE)
    history_date = models.DateField(auto_now_add=True)

class video_like(models.Model):
    like_no = models.BigAutoField(primary_key=True)
    video_no = models.IntegerField(null=True)
    like_user_id =  models.ForeignKey(user, on_delete=models.SET(0))
    like_date = models.DateField(auto_now_add=True) 

class video_subscribe(models.Model):
    sub_no = models.BigAutoField(primary_key=True)
    video_no = models.IntegerField(null=True)
    sub_user_id =  models.ForeignKey(user, on_delete=models.SET(0))
    sub_date = models.DateField(auto_now_add=True)