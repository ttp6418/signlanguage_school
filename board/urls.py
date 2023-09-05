from . import views
from django.urls import path
# from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib import admin

app_name = 'board'
urlpatterns = [
    path('notice/', views.notice, name='notice'),
    path('notice/search', views.noticeSearch, name='noticeSearch'),

    path('FAQ/', views.FAQ, name='FAQ'),
    path('FAQ/search', views.FAQSearch, name='FAQSearch'),

    path('freeboard/', views.freeboard, name='freeboard'),
    path('freeboard/search', views.freeboardSearch, name='freeboardSearch'),

    path('<int:board_id>/board_delete', views.board_delete),
    path('<int:board_id>/board_delete_ok', views.board_delete_ok),

    path('<int:board_id>/board_update', views.board_update),
    path('<int:board_id>/board_update_done', views.board_update_done),

    path('noticeDetail', views.noticeDetail),
    path('noticedetail_save', views.noticedetail_save),

    path('FAqDetail', views.FAqdetail),
    path('faqdetail_save', views.faqdetail_save),
    path('<int:board_id>/faq_admin_view', views.faq_admin_view),
    path('<int:board_id>/faq_admin_view_done', views.faq_admin_view_done),
    path('faq_admin_write', views.faq_admin_write),
    path('faq_admin_write_save', views.faq_admin_write_save),
    
    path('freeDetail', views.freedetail),
    path('freedetail_save', views.freedetail_save),

    path('<int:board_id>/', views.view),
    path('<int:board_id>/board_comment_write', views.board_comment_write, name='board_comment_write'),

    path('<int:board_id>/like',views.like),
    
]