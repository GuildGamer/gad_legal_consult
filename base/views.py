from decimal import DivisionUndefined
from glc.settings import SEC_KEY, ADMIN_USERNAME
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.utils.functional import empty
from rest_framework.exceptions import AuthenticationFailed, bad_request
from rest_framework.serializers import Serializer
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
    UserSerializer,
    ValidatedSerializer
)

from django.contrib.auth.decorators import login_required
from base.models import Session, APost
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import status
from rest_framework.views import APIView
import requests
from django.conf import settings
from .email import send_email
import json

@api_view(['GET','POST'])
def test_view(request):
    if request.method == 'POST':
        data = {
            'method':'post',
            'value':request.data
        }
        return Response(data)

    elif request.method == 'GET':
        return Response({'method':'get'})

#START API VIEWS

# Register API
class RegistrationView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.filter(email=serializer.data['email']).first()
        data  = {
            'success': True,
            'reason':"",
            'u_id': user.u_id
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
        '''
        payload = {
            'u_id': user.u_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response.set_cookie(key='token', value=token, httponly=True)
        '''
        data  = {
                'success': True,
                'reason':'None',
                'u_id': user.u_id
            }
        login(request, user)
        response = Response()
        response.data = data

        return response
'''
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

        user = User.objects.filter(u_id=payload['id'].first())    
        serializer = UserSerializer(user)

        return Response(serializer.data)
'''

class LogoutView(APIView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "success": True
        }

        return response

#admin-login view

class AdminLoginView(APIView):
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
        if user.is_superuser and user.username == ADMIN_USERNAME:
            data  = {
                    'success': True,
                    'reason':'None',
                    'u_id': user.u_id
                }
            login(request, user)
        else:
            data  = {
                'success': False,
                'reason':'Not admin user',

            }

        response = Response()
        response.data = data

        return response

# Blog API
@csrf_exempt
@api_view(['GET', 'POST'])
def validate_admin(request):
    admin = User.objects.filter(username = ADMIN_USERNAME).first()
    if admin.is_authenticated:
        return Response({"success":True})
    else:
        return Response({"success":False})

@api_view(['GET', 'POST']) 
def create_blog_post(request):
    try:
        if request.method =='POST': 
                admin = User.objects.filter(username = ADMIN_USERNAME).first()
                serializer = BlogModelSerializer(data=request.data)
                serializer.initial_data['author'] = admin.u_id
                serializer.is_valid(raise_exception=True)

                try:
                    serializer.save()

                    data = {
                        "success":True,
                        "reason":"Form is Valid",
                        "post_id": serializer.data['post_id']
                    }
                except serializer.is_valid() is False:
                    data = {
                        "success":False,
                        "reason":serializer.error,
                        "post_id": "None"
                    }
                return Response(data)
    except bad_request:
        print(bad_request)

        
            

@api_view(['GET', 'POST', 'DELETE'])
def post_list(request, post_id=None):
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
        '''
        print(request.data)
        return Response('done')
        '''

        posts = APost.objects.all()
        post_serializer = BlogModelSerializer(posts, many=True)
        serializer = UserSerializer(data=request.data)
        user = User.objects.filter(u_id = serializer.initial_data['u_id']).first()
 
        data = {
            "success": posts != None,
            "reason": "",
            "isAdmin": user.is_superuser,
            "posts": post_serializer.data,
            "user":user.username
            }
        return Response(data)

    elif request.method == 'DELETE':
        post = APost.objects.get(post_id=int(post_id))
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

      

# Post Detail API 
@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def post_detail(request, post_id):        
    try:
        post = APost.objects.get(post_id=int(post_id))
    except APost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BlogModelSerializer(post)
        comment_qs = Comment.objects.filter(post_id=post_id)
        c_list = []
        for c in comment_qs: 
            c_list.append({"content":str(c.comment),
                            "comment_id":str(c.comment_id),
                            "date_created":str(c.timestamp),
                            "username":str(c.author.username),
                            "post_id":str(c.post_id)
                            })
        data = {
            "post": serializer.data ,
            "comments": c_list,
            "success": post != None,
            "reason": "",
            "logged_in": False,
            "username": request.user.username,
            "isAdmin": False,
            "liked": request.user in list(serializer.data["users"])
            }
        return Response(data)
    
    if request.method == 'POST':
        post_serializer = BlogModelSerializer(post)
        serializer = UserSerializer(data=request.data)
        user = User.objects.filter(u_id = serializer.initial_data['u_id']).first() 

        comment_qs = Comment.objects.filter(post_id=post_id)
        c_list = []
        for c in comment_qs: 
            c_list.append({"content":str(c.comment),
                            "comment_id":str(c.comment_id),
                            "date_created":str(c.timestamp),
                            "username":str(c.author.username),
                            "post_id":str(c.post_id)
                            })

        data = {
            "post": post_serializer.data ,
            "comments": c_list,
            "success": post != None,
            "reason": "",
            "logged_in": user.is_authenticated,
            "username": user.username,
            "isAdmin": user.is_superuser,
            "liked": user in list(post_serializer.data["users"])
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


@api_view(['GET','POST'])
def delete_post(request, post_id):
    try:
        post = APost.objects.get(post_id=int(post_id))
    except APost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    post.delete()
    data = {
        "success":True,
        "reason":"post has been deleted"
        }
    return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def like_post(request):
    u_serializer = UserSerializer(data=request.data)
    serializer = BlogModelSerializer(data=request.data)
    post = APost.objects.filter(post_id = int(serializer.initial_data['post_id'])).first()
    user = User.objects.filter(u_id =  u_serializer.initial_data['u_id']).first()
    user_list = post.users.all()
    if user in user_list and post.like_count != 0:
    #if request.user in post.users:
        post.like_count -= 1
        post.users.remove(user)
        post.save()

        return Response({"success":True, "reason":""})
    else: 
        post.like_count += 1
        post.users.add(user)
        post.save()

        return Response({"success":True, "reason":""})

@api_view(['POST'])    
def comment_on_post(request):
    u_serializer = UserSerializer(data=request.data)
    serializer = CommentModelSerializer(data=request.data)
    serializer.initial_data['author'] = u_serializer.initial_data['u_id']
    if serializer.is_valid():
        serializer.save()
        data = {
            "comment": serializer.data['comment'],
            "reason": "",
            "success": True,
        }
        return Response(data, status=status.HTTP_201_CREATED)
    else:
        print(f"error:{serializer.errors}")
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

        time = Session.objects.filter(id=serializer.data['id']).first().timestamp
        full_name=serializer.data['full_name'], 
        email=serializer.data['email'], 
        time=time, 
        content=serializer.data['reason']
        subject = 'A session has been booked'
        message = f"{full_name} has booked a session at {time} with the following content: *{content}*. Please do well do get back to them at {email}, Thank you. "
        send_email(subject=subject, message=message, recipient_list = ['victormomodu25@gmail.com',], send_ebook=False)

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
    user_list = post.users.all().filter(Q(u_id__icontains=request.user.u_id))
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

@api_view(['POST'])
def validate_payment(request):
    #print('REQUEST IS REACHING HERE!')
    serializer = ValidatedSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    trans_id = serializer.data['trans_id']
    
    url = f"https://api.flutterwave.com/v3/transactions/{trans_id}/verify"
    auth_value = f"Bearer {SEC_KEY}"

    response = requests.get(url, headers={'Authorization': auth_value, 'Content-Type': 'application/json'})
    if response.json()['status'] == 'success':
        customer = response.json()['data']['customer']
        send_email(recipient_list = customer['email'], send_ebook=True)
        serializer.save()

        data = {
            "success":"True",
            "reason":response.json()['message']
        }

        return Response(data, status=status.HTTP_201_CREATED)
    else:
        data = {
            "success":"False",
            "reason":response.json()['message']
        }

        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    

    

            



   

        





