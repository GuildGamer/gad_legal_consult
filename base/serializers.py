from base.models import Session, APost, Comment
from rest_framework import serializers
from django.contrib.auth.models import User

class SessionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'full_name', 'email', 'phone', 'reason', 'business_type']

class BlogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = APost
        fields = ['post_id', 'author', 'date_created', 'heading', 'content', 'like_count', 'comments','users',]

class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'comment', 'timestamp']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','email','password']

        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
            return user
