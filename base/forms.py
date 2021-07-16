from django import forms
from base.models import Session, Buyer, a_Post
from django.contrib.auth.models import User


class SessionForm(forms.ModelForm):
     name = forms.CharField(widget=forms.TextInput())
     phone= forms.CharField(widget=forms.TextInput())
     business_type= forms.CharField(widget=forms.TextInput())
     email= forms.EmailField(widget=forms.TextInput())

     class Meta():
          model = Session
          fields = ('name','email', 'phone', 'business_type')
          widgets = {
          'name' : forms.TextInput(attrs={}),
          'email' : forms.TextInput(attrs={}),
          'phone' : forms.TextInput(attrs={}),
          'business_type' : forms.TextInput(attrs={}),
          }

class EbookForm(forms.ModelForm):
     name = forms.CharField(widget=forms.TextInput())
     phone= forms.CharField(widget=forms.TextInput())
     email= forms.EmailField(widget=forms.TextInput())

     class Meta():
          model = Buyer
          fields = ('name','email', 'phone')
          widgets = {
          'name' : forms.TextInput(attrs={}),
          'email' : forms.TextInput(attrs={}),
          'phone' : forms.TextInput(attrs={}),
          }
class PostForm(forms.ModelForm):
     author = forms.CharField(widget=forms.TextInput())
     message = forms.CharField()

     class Meta():
          model = a_Post
          fields = ('message',)
          widgets = {
          'message' : forms.TextInput(attrs={}),
          }