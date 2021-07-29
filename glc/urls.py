from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.conf.urls import url
from base.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls', namespace="base")),
    path('accounts/', include('allauth.urls')),
    #FOR REST FRAMEWORK
    url(r'^getData/', get_data),
    #url(r'^.*', TemplateView.as_view(template_name="index.html"), name="index"),
    #END FOR REST FRAMEWORK
    path("djangoflutterwave/", include("djangoflutterwave.urls", namespace="djangoflutterwave"))
]
