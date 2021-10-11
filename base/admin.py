from django.contrib import admin
from .models import Session, APost, User, Comment

admin.site.register(Session)
admin.site.register(APost)
admin.site.register(User)
admin.site.register(Comment)
