# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from cloudinary.uploader import upload
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from home.views import check_validation

from swachBharat.forms import Upload_form

from swachBharat.models import uploadmodel

from clarifai.rest import ClarifaiApp

from swachBharat.forms import Sort_form

from swachBharat.models import sortmodel


def swachbharat_view(request):
    return render(request, 'swachBharat.html')
def upload_view(request):
    user = check_validation(request)
    if user:
        # already logged in
        if request.method == "GET":
            form = Upload_form()
            return render(request, 'upload.html', {'upload_form': form})
        else:
            form = Upload_form(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                result = upload(image)
                new_upload = uploadmodel(user=user, image=image, image_url=result['secure_url'], caption=caption)
                new_upload.save()
                return HttpResponseRedirect("/wall/", "Image Saved in database")
    else:
        return redirect("/login/")


def wall_view(request):
    user = check_validation(request)
    if user:
        # user exists
        posts = uploadmodel.objects.all().order_by('-created_on')
        for post in posts:
            existing_like = sortmodel.objects.filter(upload=post,user=user)
            if existing_like:
                #post liked already
                post.is_sorted=True
        return render(request, 'wall.html', {'all_post': posts})
    else:
        return redirect("/login/")



def sort_view(request):
    user = check_validation(request)
    if user:
        # user logged in
        if request.method == "POST":
            # form is submitted
            sort_form = Sort_form(request.POST)
            if sort_form.is_valid():
                upload_id = sort_form.cleaned_data.get('upload')
                #get api key
                app = ClarifaiApp(api_key='da68da3ad4504bb3a86febe60f658b5b')
                #get the response
                response_data = app.tag_urls([upload_id.image_url])

                tag_urls = []
                #savethe response
                for concept in response_data['outputs'][0]['data']['concepts']:
                    tag_urls.append(concept['name'])

                print tag_urls
                #sort the response
                if "dirty" in tag_urls:
                    sort="dirty"
                else:
                    sort="clean"
                #savein database

                existing_tag= sortmodel.objects.filter(upload=upload_id,user=user).first()

                if not existing_tag:
                    #not sorted
                    sortmodel.objects.create(upload=upload_id, sort_text= sort, user= user)
                    return redirect("/wall/")
                else:
                    existing_tag.delete()
                    return redirect("/wall/")
            else:
                error_msg = sort_form.errors
                print error_msg
                return HttpResponse("Error Saving in database")
        else:
            return redirect("/wall/")
    else:
        return redirect("/login/")