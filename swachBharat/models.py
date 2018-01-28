# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from home.models import users


class uploadmodel(models.Model):
    user=models.ForeignKey(users)
    image = models.FileField(upload_to='swach_image')
    image_url = models.CharField(max_length=255)
    caption = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    is_sorted = models.BooleanField(default=False)
    @property
    def sortresult(self):
        return sortmodel.objects.filter(upload=self)


class sortmodel(models.Model):
    user = models.ForeignKey(users)
    upload = models.ForeignKey(uploadmodel)
    sort_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)