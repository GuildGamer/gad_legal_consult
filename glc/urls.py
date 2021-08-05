from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import url
from rest_framework import routers
from base.views import *

#router = routers.DefaultRouter()
#router.register(r'blog', BlogPostViewSet)

urlpatterns = [
    #FOR REST FRAMEWORK
    #path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #END FOR REST FRAMEWORK
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace="base")),
    #path('accounts/', include('allauth.urls')),
    path("djangoflutterwave/", include("djangoflutterwave.urls", namespace="djangoflutterwave"))
]



