from . import views
from django.urls import path, include
# from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib import admin
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
     path('admin/', admin.site.urls),
    
    path('signup/', views.signup, name='signup'),
    path('signup/signup_logic', views.signup_logic, name='signup_logic'),
    path('signup/idCheck', views.idCheck, name='idCheck'),
    
    path('login/', views.login, name='login'),
    path('login/login_logic', views.login_logic, name='login_logic'),
    path('logout/', views.logout, name='logout'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/delete_ok', views.delete_ok, name='delete_ok'),
    path('<int:pk>/delete', views.delete, name='delete'),
    path('<int:pk>/update', views.update, name='update'),
    path('<int:pk>/my_board', views.my_board, name='my_board'),
    path('<int:pk>/update_done', views.update_done, name='update'),
    path('login/password_reset', views.password_reset, name='password_reset'),
    path('login/password_reset_done', views.password_reset_done, name='password_reset_done'),
    path('signup/info_accept', views.view_info_accept, name='info_accept'),
    path('signup/info_third_accept', views.view_info_third_accept, name='info_third_accept'),
    
    path('kakaoLoginLogic/', views.kakaoLoginLogic, name='kakaoLoginLogic'),
    path('kakaoLoginLogicRedirect/', views.kakaoLoginLogicRedirect, name='kakaoLoginLogicRedirect'),
    path('kakaoLogout/', views.kakaoLogout , name='kakaoLogout'),
]