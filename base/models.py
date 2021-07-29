from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from phone_field import PhoneField

BUSINESS_TYPES = (
    ('CL', 'Clothing'),
    ('ED', 'Electronics & Devices'),
    ('KD', 'Kids'),
    ('FI', 'Food Items'),
    ('KI', 'Kitchen'),
    ('FH', 'Furniture & Housing'),
)

class Session(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    business_type = models.CharField(choices=BUSINESS_TYPES, max_length=2)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Buyer(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return self.name

class APost(models.Model):
    author= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    #post_id = models.AutoField(primary_key=True)
    slug = models.SlugField(unique=True)
    message = models.TextField()
    likes = models.IntegerField(default=0)
    comments = models.TextField(null=True, blank=True)
    users = models.ManyToManyField(User, related_name='likes',blank=True)
        
    def __str__(self):
        return self.message

