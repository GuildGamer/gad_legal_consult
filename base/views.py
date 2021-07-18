from base.models import APost
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
import requests 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import SessionForm, EbookForm, PostForm
from django.views.generic import View
#from django.views.generic import View

def home(request):
    return render(request, "index.html")

def services(request):
    return render(request, "service.html")

def about(request):
    return render(request, "about.html")
   
class BlogView(View, LoginRequiredMixin):

    def get(self, *args, **kwargs):
        #form
        post_form = PostForm()
        context = {
            'p_form': post_form, 'o_posts': APost.objects.all(),
        }

        return render(self.request, "blog.html", context)

    def post(self, *args, **kwargs):
        post_form = PostForm(self.request.POST or None)
        if post_form.is_valid():
            message=post_form.cleaned_data.get('message')

            post = APost(
                    message = message,
                    author=self.request.user,
            )

            post.save()
                    
            '''
            post = post_form.save(commit=False)
            post.author = request.user.username
            post.save()
            '''
            context = {
            'p_form': post_form, 'o_posts': APost.objects.all(),
            }

            messages.info(self.request, "post made sucessfully!")
            return render(self.request, "blog.html", context)
        else:
            messages.error(self.request, post_form.errors)
       

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

'''class BlogView(View, LoginRequiredMixin):

    def get(self, *args, **kwargs):
        #form
        post_form = PostForm()
        posts = a_Post.objects.all()
        #posts = get_object_or_404(a_Post)
        context = {
            'post_form': post_form, 'posts':posts
        }

        return render(self.request, "blog.html", context)
    def post(self, *args, **kwargs):
        post_form = PostForm(self.request.POST or None)

        posts =a_Post.objects.all()
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = self.request.user
            post.save()

        context = {
        'post_form': post_form, 'posts':posts
        }
        return redirect('base:blog')
'''
        
    


import requests
def buy_ebook(request):

    

    """ebook_form = EbookForm(data=request.POST)
    if ebook_form.is_valid():

        eb = ebook_form.save()
        eb.save()"""

    current_user = request.user
            

    url = 'https://api.flutterwave.com/v3/payments'
    myobj = {
                "tx_ref":"glc-tx-"+str(current_user.id),
                "amount":"2000",
                "currency":"NGN",
                "redirect_url":"https://localhost:8000/successful.html",
                "customer":{
                    "email":current_user.email,
                    "name":current_user.username,
                },
                "customizations":{
                    "title":"Ebook Name",
                    "description":"It's worth the purchase",
                    "logo":"https://assets.piedpiper.com/logo.png"
                }
        }
    
    buyer_details = requests.post(url, data = myobj)
        

    messages.info(request, "You have sucessfully booked a session with the attorney")
    return buyer_details

#like view
@login_required
def like_view():
    pass


   

        





