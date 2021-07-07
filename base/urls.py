from django.urls import path
from .views import(
    experience,
    home,
    contact,
    service,
    about
)

app_name = 'base'

urlpatterns = [
    path ('', home, name='home'),
    path ('contact/', contact, name='contact'),
    path ('service/', service, name='service'),
    path ('experience/', experience, name='experience'),
    path ('about/', about, name='about'),

]