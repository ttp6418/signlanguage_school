"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.translation),
    path('web', views.translation_web),
    path('web/text', views.translation_text),
    path('web/sign', views.translation_sign),
    path('mp4_upload', views.mp4_upload),
    path('mp4_download', views.mp4_download),
    path('url_upload', views.url_upload),
    path('url_download', views.url_download),

    path('download', views.translation_download),
    path('download/<str:os_name>', views.translation_download_os),

    path('view/<str:video_no>', views.translation_view),
    path('view_download/<str:video_no>', views.translation_view_download),
    
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
                          