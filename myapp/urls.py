from django.conf.urls import url, include
from django.contrib import admin
from .views import *
from views import signup_view,login_view,feed_view,post_view,like_view

urlpatterns = [
    url(r'signup', signup_view),
    url(r'login/', login_view),
    url(r'feed', feed_view),
    url(r'post/', post_view),
    url(r'like/',like_view)
]
