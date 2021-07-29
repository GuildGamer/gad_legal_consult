from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib import messages
import requests 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .forms import SessionForm, EbookForm, PostForm
from django.views.generic import View
from django.utils.text import slugify 
from django.db.models import Q
#for REST FRAMEWORK
from django.http import HttpResponse, JsonResponse
from base.models import *
from base.serializers import PostModelSerializer
from django.views.decorators.csrf import csrf_exempt
#from django.views.generic import View

@csrf_exempt
def get_data(request):
	data = APost.objects.all()
	if request.method == 'GET':
		serializer = PostModelSerializer(data, many=True)
		return JsonResponse(serializer.data, safe=False)

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
                    slug = slugify(message[:5]),
                    author=self.request.user,
            )

            post.save()
                    
            context = {
            'p_form': post_form, 'o_posts': APost.objects.all(),
            }

            messages.info(self.request, "post made sucessfully!")
            return render(self.request, "blog.html", context)
        else:
            messages.error(self.request, post_form.errors)

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


   

        





