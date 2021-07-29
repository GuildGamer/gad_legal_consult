from django.contrib.auth.models import User
from base.models import APost, Buyer, Session
from rest_framework import serializers


class UserModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class SessionModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ['url', 'name', 'email', 'phone', 'business_type']

class BuyerModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Buyer
        fields = ['url', 'name', 'email', 'phone']

class PostModelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APost
        fields = ['url', 'author', 'timestamp', 'slug', 'messages', 'likes', 'comments']