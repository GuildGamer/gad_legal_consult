from base.models import Session, APost, Comment
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_staff', 'is_active', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }

        def create(self, validated_data):
           return User.objects.create_user(**validated_data)

class SessionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'full_name', 'email', 'phone', 'reason']

class BlogModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = APost
        fields = ['post_id', 'author', 'date_created', 'heading', 'content', 'like_count', 'comments','users',]

class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author', 'comment', 'timestamp']
