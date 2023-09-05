from django.db import models
from django.urls import reverse
from accounts.models import user

# Create your models here.

class board(models.Model):
    board_no = models.BigAutoField(primary_key=True)
    board_img = models.ImageField(upload_to='images/',blank=True, null=True)
    board_name = models.CharField('제목', max_length=100, default='Title')
    board_date = models.DateField(auto_now_add=True) 
    board_like = models.IntegerField(default=0)
    board_view = models.IntegerField(default=0)
    board_score = models.TextField(default=0)
    board_text = models.TextField('내용', null=True)
    board_category = models.CharField(max_length=10, default='free')
    board_ip = models.GenericIPAddressField(null=True)
    board_author = models.ForeignKey(user, on_delete=models.SET(0))

    def __str__(self):
        return self.board_name

    def get_absolute_url(self):
        return reverse('blog:detail', args=[self.id])

class comment(models.Model):
    comment_no = models.BigAutoField(primary_key=True)
    comment_user_id = models.ForeignKey(user, on_delete=models.SET(0))
    comment_board_no = models.ForeignKey(board, on_delete=models.CASCADE, related_name='comments')
    comment_date = models.DateField(auto_now_add=True) 
    comment_content = models.TextField()
    comment_high = models.IntegerField(null=True)

class Like(models.Model):
    like_no = models.BigAutoField(primary_key=True)
    board_no = models.IntegerField(null=True)
    like_user_id =  models.ForeignKey(user, on_delete=models.SET(0))
    like_date = models.DateField(auto_now_add=True) 