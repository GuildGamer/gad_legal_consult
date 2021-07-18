from django.urls import path
from .views import(
    home,
    about,
    session,
    services,
    buy_ebook,
    ebook_view,
    BlogView
)

app_name = 'base'

urlpatterns = [
    path ('', home, name='home'),
    path ('blog/', BlogView.as_view(), name='blog'),
    path ('about/', about, name='about'),
    path ('services/', services, name='services'),
    path ('buy_e-book/', buy_ebook, name='ebook'),
    path ('e-book/', ebook_view, name='ebook_view'),
    path ('book_a_session/', session, name='session'),

]