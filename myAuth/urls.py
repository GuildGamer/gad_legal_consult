from django.urls import path
from .views import(
    sign in,
    home,
    service,
    about,
    session
)

app_name = 'base'

urlpatterns = [
    path ('', home, name='home'),
    path ('service/', service, name='service'),
    path ('blog/', blog, name='blog'),
    path ('about/', about, name='about'),
    path ('book_a_session/', session, name='session'),

]