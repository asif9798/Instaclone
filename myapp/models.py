# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from uuid import uuid4

from django.db import models


# Create your models here.

class UserModel(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __repr__(self):
        return "<usermodel : %s >" %(self.username)


class SessionToken(models.Model):
    user = models.ForeignKey(UserModel)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token=str(uuid4())

class PostModel(models.Model):
    user = models.ForeignKey(UserModel)
    image = models.FileField(upload_to='user_images')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=240)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def like_count(self):
        return self.likemodel_set.count()
    def liked_by_user(self,user):
        l = self.likemodel_set.filter(user=user)
        return len(l)>0


class LikeModel(models.Model):
    user = models.ForeignKey(UserModel)
    post = models.ForeignKey(PostModel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)







