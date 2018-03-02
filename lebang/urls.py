"""lebang URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url,include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from myapp.views import *
router = routers.DefaultRouter()
router.register(r'users',UserViewSet)

urlpatterns = [
	url(r'^',include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^user/register/',UserRegisterAPIView.as_view()),
   	url(r'^user/login/',UserLoginAPIView.as_view()),
    url(r'^user/update/',UserUpdateAPIView.as_view()),
    url(r'^task/publish/',TaskPublishAPIView.as_view()),
    url(r'^task/delete/',TaskDeleteAPIView.as_view()),
    url(r'^task/summary/',TaskSummaryAPIView.as_view()),
    url(r'^task/detail/',TaskDetailAPIView.as_view()),
    url(r'^task/like/',TaskLikeAPIView.as_view()),
    url(r'^task/take/',TaskTakeAPIView.as_view()),
    url(r'^user/like/',UserLikeAPIView.as_view()),
    url(r'^user/take/',UserTakeAPIView.as_view()),
    url(r'^user/mypublish/',UserMyPublishAPIView.as_view()),
    url(r'^task/by/',TaskByAPIView.as_view()),
    url(r'^user/action/',UserActionAPIView.as_view()),
    url(r'^user/cancel/',UserCancelAPIView.as_view()),
    url(r'^report/',ReportAPIView.as_view()),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
