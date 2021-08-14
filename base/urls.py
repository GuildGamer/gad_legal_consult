from django.urls import path
from .views import(
    post_detail,
    session,
    services,
    ebook_view,
    like,
    book_session_view,
    post_list,
    RegistrationView,
    LoginView,
    LogoutView,
    UserView,
    like_post,
    comment_on_post
)

app_name = 'base'

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('user', UserView.as_view()),
    path('singout/', LogoutView.as_view(), name="signout"),
    path ('blog/', post_list, name='blog'),
    path ('comment-on-blog-post/', comment_on_post, name='comment-on-blog-post'),
    path ('book-consultation/', book_session_view , name='book-a-session'),
    path ('blog-post/<post_id>', post_detail, name='blog-post'),
    path ('services/', services, name='services'),
    path ('e-book/', ebook_view, name='ebook_view'),
    path ('book-a-session/', session, name='session'),
    path ('blog/like-post/<slug>/', like, name='like'),
]

