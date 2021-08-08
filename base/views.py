from django import forms
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import requests 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from requests.api import post

from base import serializers
from .forms import SessionForm, PostForm
from django.views.generic import View
from django.utils.text import slugify 
from django.db.models import Q
#for REST FRAMEWORK
from django.http import JsonResponse
from base.models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# FOR API VIEWS
from rest_framework import viewsets
from base.serializers import BlogModelSerializer, SessionModelSerializer, UserSerializer, RegisterSerializer, CommentModelSerializer
from base.models import Session, APost
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import authenticate



#START API VIEWS
#API VIEW FOR ALL POSTS

# Blog API
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = APost.objects.all()
        serializer = BlogModelSerializer(posts, many=True)
        data = {
            "success": posts != None,
            "reason": "",
            "isAdmin": request.user.is_superuser,
            "posts": serializer.data,
            }
        return Response(data)

    elif request.method == 'POST':
        serializer = BlogModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Post Detail API 
@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, post_id):
    try:
        post = APost.objects.get(post_id=int(post_id))
    except APost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogModelSerializer(post)
        data = {
            "post": serializer.data ,
            "comments": list(serializer.data["comments"]),
            "success": post != None,
            "reason": "",
            "logged_in": request.user.is_authenticated,
            "username": request.user.username,
            "isAdmin": request.user.is_superuser,
            "liked": request.user in list(serializer.data["users"])
            }
        return Response(data)

    elif request.method == 'PUT':
        serializer = BlogModelSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def like_post(request):
    serializer = CommentModelSerializer(data=request.data)
    post = APost.objects.filter(post_id = int(serializer.data['post_id']))[0]
    user_list = post.users.all()
    if request.user in user_list and post and post.likes != 0:
    #if request.user in post.users:
        post.likes -= 1
        post.users.remove(request.user)
        post.save()
    else: 
        post.likes += 1
        post.users.add(request.user)
        post.save()

@api_view(['POST'])    
def comment_on_post(request):
    serializer = CommentModelSerializer(data=request.data)
    post = APost.objects.filter(post_id = int(serializer.data['post_id']))[0]
    if serializer.is_valid():
        serializer.author = request.user
        serializer.save()
        post.comments.add(serializer.data['comment'])
        data = {
            "comment": serializer.data['comment'],
            "reason": "",
            "success": True,
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Register API

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user in User.objects.all():
            return Response(
                {
                    #"user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "success": True,
                    "reason": "",
                    "token": AuthToken.objects.create(user)[1]
                }
            )
        else: 
             return Response(
                {
                    #"user": UserSerializer(user, context=self.get_serializer_context()).data,
                    "success": False,
                    "reason": serializer.errors,
                    "token": AuthToken.objects.create(user)[1]
                }
            )

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            authenticate(user)
            login(request, user)
            data = {
                "success": True,
                "reason": "",
                "token":  AuthToken.objects.create(user)[1]
            }
            return Response(data)
        else: 
            data = {
                "success": False,
                "reason":  serializer.errors,
                "token":  ""
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
       
# Session API
@api_view(['POST'])
def book_session_view(request):
    serializer = SessionModelSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        data = {
            "success":True,
            "reason": "",
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {
            "success":False,
            "reason": serializer.errors,
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


#END API VIEWS

def like(request, slug):
    post = get_object_or_404(APost, slug=slug)
    post_form = PostForm()
    #post = APost.objects.filter(slug=slug)
    user_list = post.users.all().filter(Q(id__icontains=request.user.id))
    if request.user in user_list and post and post.likes != 0:
    #if request.user in post.users:
        post.likes -= 1
        post.users.remove(request.user)
        post.save()
    else: 
        post.likes += 1
        post.users.add(request.user)
        post.save()

    context = {
    'p_form': post_form,'o_posts': APost.objects.all(),
    }

    return redirect("base:blog")


def services(request):
    return render(request, "service.html")

def session(request):

    if request.method == 'POST':

        session_form = SessionForm(data=request.POST)
        if session_form.is_valid():

            sess = session_form.save()
            sess.save()

            messages.info(request, "You have sucessfully booked a session with the attorney")
            return redirect("base:home")
        else:
            messages.error(request, session_form.errors)
    else:
        session_form = SessionForm()

    context = {
            's_form': session_form,
    }

    return render(request, "session.html", context)

def ebook_view(request):
    return render(request, "ebook.html")
            



   

        





