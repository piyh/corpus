"""thumbnailBracket URL Configuration

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
from django.urls import path
from bracket import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='bracket.index'),
    path('vote/', views.vote, name='bracket.vote'),
    path('vote/<str:ytid1>-<str:ytid2>', views.vote, name='bracket.vote-ids'),
    path('leaderboard/', views.leaderboard, name='bracket.leaderboard'),
    path('leaderboard/<int:resultLimit>', views.leaderboard),
    path('stats/<str:ytVidID>', views.stats, name ='bracket.stats'),
    #path('result/', views.voted, name='bracket.result'),
    path('test/', views.test, name='bracket.test'),
    #path('result/', views.result, name='bracket.result'),

]
