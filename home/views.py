# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from forms import SignUp_form, LogIn_form, Post_form, Like_form, Comment_form,Upvote_form
from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render, redirect
from models import users, postmodel, likemodel,commentmodel,upvotemodel
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from models import session_token
from cloudinary.uploader import upload
from django.core.mail import send_mail

# Create your views here.
def home_view(request):
    if request.method == "GET":
        form = SignUp_form()
        return render(request, 'home.html', {'form': form})
    else:
        form = SignUp_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            if len(username) >= 4 and len(password) >= 5:
                    password = make_password(password)
                    new_user = users(name=name, email=email, username=username, password=password)
                    send_mail('Welcome Onboard',
                              'Welcome to the great world of instagram clone where you can post like and comment instantaneously!',
                              'instacloneskj@gmail.com',
                              [email],
                              fail_silently=False,
                              )
                    new_user.save()
                    success_msg = 'Email sent to your email address!'
                    return render(request, 'login.html',{'success': success_msg})
            else:
                    error_msg = 'Name or password is too short!'
                    return render(request, 'home.html', {'error': error_msg})

        else:
            error_msg = form.errors
            new_error=""
            for error in error_msg:
                new_error=new_error+" "+error
                for msg in error_msg[error]:
                    new_error = new_error + ":" +msg+"  "
            print new_error
            form = SignUp_form()
            return render(request, 'home.html', {'form': form,'error': new_error})

def check_validation(request):
  if request.COOKIES.get('session_key'):
    session = session_token.objects.filter(session_token=request.COOKIES.get('session_key')).first()
    if session:
      return session.user_email
  else:
    return None

def  post_view(request):
    user=check_validation(request)
    if user:
        #already logged in
        if request.method == "GET":
            form = Post_form()
            return render(request, 'post.html',{'post_form':form})
        else:
            form=Post_form(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                result = upload(image)
                new_post = postmodel(user=user, image=image, image_url=result['secure_url'], caption=caption)
                new_post.save()
                return HttpResponseRedirect("/feed/","Image Saved in database")
            else:
                return HttpResponse("Error Saving in database")
    else:
        return redirect("/login/")

def feed_view(request):
    user = check_validation(request)
    if user:
        #user exists
        posts=postmodel.objects.all().order_by('-created_on')
        for post in posts:
            existing_like = likemodel.objects.filter(post=post,user=user)
            if existing_like:
                #post liked already
                post.is_liked=True
        return render(request, 'feed.html',{'all_post': posts})
    else:
        return redirect("/login/")

def comment_view(request):
    user = check_validation(request)
    if user:
        # user logged in
        if request.method == "POST":
            comment_form=Comment_form(request.POST)
            if comment_form.is_valid():
                post_id =comment_form.cleaned_data.get('post')
                comment_text=comment_form.cleaned_data.get('comment_text')

                commentmodel.objects.create(user=user, post=post_id,comment_text=comment_text)
                send_mail('Comment on Post!',
                          'Hi there! There\'s a comment on your post by ' + user.name,
                          'instacloneskj@gmail.com',
                          [post_id.user.email],
                          fail_silently=False,
                          )
                return redirect("/feed/")
        else:
            return redirect("/feed/")

    else:
        return redirect("/login/")

def login_view(request):
    now_time = datetime.now()
    response_data = {}
    if request.method == "GET":
        form = LogIn_form()
        return render(request,'login.html',{'now': now_time, 'form':form})
    elif request.method == "POST":

        form =LogIn_form(request.POST)
        #validate the form
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            #read data from db
            return_user = users.objects.filter(username=username).first()
            if return_user:
                #compare password
                if check_password(password,return_user.password):
                    #login successfull
                    #create session token
                    token = session_token(user_email=return_user)
                    token.create_token()
                    token.save()
                    #redirect to feed in django
                    response = redirect('/feed/')
                    response.set_cookie(key ='session_key', value=token.session_token)
                    return response

                else:
                    #password doesn't match
                    error_msg='Wrong Password'
                    return render(request,'login.html',{'error':error_msg})
            else:
                #user doesnt exists
                error_msg = 'User doesn\'t exists'
                return render(request, 'login.html', {'error': error_msg})

        else:
            form = LogIn_form()
            error_msg = 'We could not process your request at this time.'
            response_data['form'] = form
            return render(request, 'login.html', response_data,{'error': error_msg})

def logout_view(request):
    if request.COOKIES.get('session_key'):
        user = session_token.objects.filter(session_token=request.COOKIES.get('session_key')).first()
        if user:
            response=HttpResponseRedirect("/login/")
            response.delete_cookie('session_key')
            user.delete()
            return response
        else:
            return redirect("/login/")
    else:
        return redirect("/login/")

def user_view(request,username="sjstreetchamp@gmail.com"):
    user = check_validation(request)
    if user:
        # user exists
        posts = postmodel.objects.filter(user=username)
        for post in posts:
            existing_like = likemodel.objects.filter(post=post, user=user)
            if existing_like:
                # post liked already
                post.is_liked = True
        return render(request, 'feed.html', {'all_post': posts})
    else:
        return redirect("/login/")

def like_view(request):
    user=check_validation(request)
    if user:
        #user logged in
        if request.method == "POST":
            #form is submitted
            #like_form=Like_form(request.POST)
            #if like_form.is_valid():
               # post_id=like_form.cleaned_data.get('post')
            post_id = request.POST.get('post_id')
            current_post=postmodel.objects.filter(id=post_id).first()
            existing_like = likemodel.objects.filter(post_id=current_post, user=user).first()
            if not existing_like:
                likemodel.objects.create(post=current_post,user=user)
                data={
                    'flag':True
                }
                send_mail('Post Liked!',
                          'Hi there! Your post has been liked by '+user.name,
                          'instacloneskj@gmail.com',
                          [current_post.user.email],
                          fail_silently=False,
                          )
                #return redirect("/feed/")
            else:
                existing_like.delete()
                data = {
                    'flag': False
                }
               # return redirect("/feed/")
            return JsonResponse(data)
        else:
            return redirect("/feed/")
    else:
        return redirect("/login/")

def upvote_view(request):
    user = check_validation(request)
    if user:
        if request.method == "POST":
            upvote_form = Upvote_form(request.POST)
            if upvote_form.is_valid():
                comment_id = upvote_form.cleaned_data.get('comment')
                existing_upvote = upvotemodel.objects.filter(comment=comment_id, user=user).first()
                if not existing_upvote:
                    upvotemodel.objects.create(user=user,comment=comment_id)
                    return redirect("/feed/")
                else:
                    newupvote=existing_upvote.upvotes+1
                    upvotemodel.objects.filter(comment=comment_id, user=user).update(upvotes=newupvote)
                    return redirect("/feed/")
            else:
                return HttpResponse("Error")
        else:
            return redirect("/feed/")
    else:
        return redirect("/login/")