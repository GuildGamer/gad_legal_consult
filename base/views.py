from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from rest_framework.exceptions import AuthenticationFailed
from .forms import SessionForm, PostForm
from django.db.models import Q
#for REST FRAMEWORK
from base.models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# FOR API VIEWS
from rest_framework.views import APIView
from base.serializers import (
    BlogModelSerializer,
    SessionModelSerializer, 
    CommentModelSerializer,
    UserSerializer
)

from base.models import Session, APost
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import status
from rest_framework.views import APIView
import jwt, datetime

#START API VIEWS

# Register API
class RegistrationView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        data  = {
            'success': True,
            'reason':"",
            'token ': ""
        }

        return Response(data) 

class LoginView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            data  = {
                'success': False,
                'reason':'User not found!',
                'token ': ""
            }

            return Response(data)
            
        if not user.check_password(password):
            data  = {
                'success': False,
                'reason':'Incorrect Password!',
                'token ': ""
            }

            return Response(data)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        data  = {
                'success': True,
                'reason':'None',
                'token ': token
            }
        login(request, user)
        response = Response()

        response.set_cookie(key='token', value=token, httponly=True)
        response.data = data

        return response

class UserView(APIView):
    @method_decorator(csrf_exempt)
    def get(self, request):
        token = request.COOKIES.get('token')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try: 
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id'].first())    
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "success": True
        }

        return response

# Blog API
@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = APost.objects.all()
        serializer = BlogModelSerializer(posts, many=True)
        data = {
            "success": posts != None,
            "reason": "",
            "isAdmin": request.user.is_staff,
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

        exec('email.py')

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

            



   

        





