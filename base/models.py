from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.contrib.auth.models import AbstractUser

BUSINESS_TYPES = (
    ('CL', 'Clothing'),
    ('ED', 'Electronics & Devices'),
    ('KD', 'Kids'),
    ('FI', 'Food Items'),
    ('KI', 'Kitchen'),
    ('FH', 'Furniture & Housing'),
)


class User(AbstractUser):
    username = models.CharField(max_length=255, unique= True)
    email = models.CharField(max_length=255, unique= True)
    password =  models.CharField(max_length=255)
    token = models.CharField(max_length=255,)
    u_id = models.AutoField(primary_key=True)


    REQUIRED_FIELDS = ['email']

class Session(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    reason = models.CharField(max_length=256)
    #phone = PhoneField(blank=True, help_text='Contact phone number')
    timestamp = models.DateTimeField(auto_now_add=True)
    #business_type = models.CharField(choices=BUSINESS_TYPES, max_length=2)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

class Buyer(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.CharField(max_length=225)
    timestamp = models.DateField(auto_now_add=True)
    post_id = models.CharField(max_length=255)
    comment_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.comment

class APost(models.Model):
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    post_id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    heading = models.TextField(default='default heading')
    content = models.TextField()
    like_count = models.IntegerField(default=0)
    comments = models.ManyToManyField(Comment, related_name = 'comments', blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes',blank=True)
        
    def __str__(self):
        return self.content
class Validated(models.Model):
    tx_ref =  models.TextField()
    trans_id = models.TextField()

    def __str__(self):
        return self.trans_id


