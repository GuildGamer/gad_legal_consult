from django.urls import path
from knox import views as knox_views
from .views import(
    post_detail,
    session,
    services,
    ebook_view,
    like,
    book_session_view,
    post_list,
    RegisterAPI,
    LoginAPI,
    like_post,
    comment_on_post
)

app_name = 'base'

urlpatterns = [
    path('signup/', RegisterAPI.as_view(), name='signup'),
    path('signin/', LoginAPI.as_view(), name='signin'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path ('blog/', post_list, name='blog'),
    path ('comment-on-blog-post/', comment_on_post, name='comment-on-blog-post'),
    path ('book-consultation/', book_session_view , name='book-a-session'),
    path ('blog-post/<post_id>', post_detail, name='blog-post'),
    path ('services/', services, name='services'),
    path ('e-book/', ebook_view, name='ebook_view'),
    path ('book-a-session/', session, name='session'),
    path ('blog/like-post/<slug>/', like, name='like'),
]

