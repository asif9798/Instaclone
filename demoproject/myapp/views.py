# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render, redirect
from uuid import uuid4
from datetime import datetime
from .forms import SignupForm, LoginForm, PostForm, LikeForm
from .models import UserModel, SessionToken, PostModel, LikeModel
from imgurpython import ImgurClient
from demoproject.settings import BASE_DIR
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.


def signup_view(request):
    today = datetime.now()
    if request.method == "GET":
        form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            hashed_password=make_password(password)
            #save data in database
            user = UserModel(name = name,email= email,username=username,password=make_password(password))
            user.save()
            return render(request,"success.html")
    return render(request, 'index.html', {
         'today': today,
         'method': request.method,
         'form': form

    })

def login_view(request):
    response_data={}
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html',{
            'form':form
        })

    if request.method== "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=UserModel.objects.filter(username=username).first()
            print "user is ..." , user

            if user:
                if check_password(password, user.password):
                    session= SessionToken(user=user)
                    session.create_token()
                    session.save()
                    response = redirect("/feed")
                    response.set_cookie(key="session_token",value=session.session_token)
                    return response
                    print 'User is valid'
                else:
                    print 'User is invalid'
                    response_data['message'] = 'Incorrect Password!Please try again'



def check_validation(request):
  if request.COOKIES.get('session_token'):
    session = SessionToken.objects.filter(session_token=request.COOKIES.get('session_token')).first()
    if session:
      return session.user
  else:
    return None




def post_view(request):
      user = check_validation(request)
      print user


      if user:
          print 'Authentic user'
      else:
          return redirect('/login/')

      if request.method=="GET":
          form = PostForm()
          return render(request,"post.html", {
              "form":form
          })


      elif request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.cleaned_data.get('image')
                caption = form.cleaned_data.get('caption')
                post = PostModel(user=user, image=image, caption=caption)
                post.save()
                path = str(BASE_DIR + "\\" + post.image.url)
                client = ImgurClient("8a689cbefa8509d", "7b2ea987dc594f54a6180c4e5efb876e84242af5")
                post.image_url = client.upload_from_path(path, anon=True)['link']
                print post.image_url
                post.save()
                return redirect("/feed")


def feed_view(request):
    user = check_validation(request)
    if user:
        posts = PostModel.objects.all().order_by('created_on')
        return render(request, 'feed.html', {
            'posts':posts
        })
    else:
        return redirect('/login/')


def like_view(request):
    user = check_validation(request)
    if user and request.method == 'POST':
        form = LikeForm(request.POST)
        if form.is_valid():
            post_id = form.cleaned_data.get('post').id

            existing_like = LikeModel.objects.filter(post_id=post_id, user=user).first()

            if not existing_like:
                LikeModel.objects.create(post_id=post_id, user=user)
            else:
                existing_like.delete()

            return redirect('/feed/')

    else:
        return redirect('/login/')












