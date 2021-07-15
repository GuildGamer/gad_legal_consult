from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
import requests 
from django.contrib.auth.decorators import login_required
from .forms import SessionForm, EbookForm
#from django.views.generic import View

def home(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def blog(request):
    return render(request, "blog.html")

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


   

        





