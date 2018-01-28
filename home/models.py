# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models


# Create your models here.
class users(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(primary_key=True,unique= True)
    password = models.CharField(max_length=120)
    username = models.CharField(max_length=120)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

class session_token(models.Model):
    user_email= models.ForeignKey(users)
    session_token = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def create_token(self):
        self.session_token=uuid.uuid4()

class postmodel(models.Model):
    user=models.ForeignKey(users)
    image = models.FileField(upload_to='user_image')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_liked=models.BooleanField(default=False)
    @property
    def like_count(self):
        return len(likemodel.objects.filter(post=self))

    @property
    def comments(self):
        return commentmodel.objects.filter(post=self)


class likemodel(models.Model):
    user = models.ForeignKey(users)
    post = models.ForeignKey(postmodel)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class commentmodel(models.Model):
    user = models.ForeignKey(users)
    post = models.ForeignKey(postmodel)
    comment_text=models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class upvotemodel(models.Model):
    user = models.ForeignKey(users)
    comment=models.ForeignKey(commentmodel)
    upvotes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)