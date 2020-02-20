"""sortask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url
from django.views import static
from django.conf import settings
import home.urls, course.urls, assignment.urls, account.urls, submission.urls
from .settings import MEDIA_ROOT

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # home
    path('', include('home.urls')),
    # course
    path('course/', include('course.urls')),
    # assignment
    path('assignment/', include('assignment.urls')),
    # account
    path('account/', include('account.urls')),
    # submission
    path('submission/', include('submission.urls')),
    # captcha
    path('captcha/', include('captcha.urls')),

    # temporary use this
    # static files
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    # media files
    url(r'^media/(?P<path>.*)$', static.serve, {"document_root": MEDIA_ROOT}, name='media'),
]
