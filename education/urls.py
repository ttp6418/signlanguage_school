from . import views
from django.urls import path
# from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib import admin

app_name = 'education'
urlpatterns = [
    path('list', views.education_morelist, name='education_morelist'),
    path('list/<int:subject_id>/', views.education_moresubject, name='education_moresubject'),
    path('list/<int:subject_id>/<str:video_name>/', views.education_moreview, name='education_moreview'),
    path('list/<int:subject_id>/<str:video_name>/education_password_check', views.education_password_check),
    path('write/<int:subject_id>/', views.education_morewrite, name='education_morewrite'),
    path('write/<int:subject_id>/education_morewrite_done', views.education_morewrite_done, name='education_morewrite_done'),
    path('add', views.subject_add),
    path('add_done', views.subject_add_done),
]