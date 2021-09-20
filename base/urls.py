from django.urls import path
from .views import(
    post_detail,
    session,
    services,
    like,
    book_session_view,
    post_list,
    RegistrationView,
    LoginView,
    LogoutView,
    UserView,
    like_post,
    comment_on_post,
    create_blog_post,
    validate_payment,
    test_view
)

app_name = 'base'

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
    path('test/', test_view, name='test'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('user', UserView.as_view()),
    path('singout/', LogoutView.as_view(), name="signout"),
    path ('blog/', post_list, name='blog'),
    path ('blog/<post_id>', post_list, name='blog'),
    path('validate-transaction/', validate_payment, name="payment-validation"),
    path ('comment-on-blog-post/', comment_on_post, name='comment-on-blog-post'),
    path ('create-blog-post/', create_blog_post, name='comment-on-blog-post'),
    path ('book-consultation/', book_session_view , name='book-a-session'),
    path ('blog-post/<post_id>', post_detail, name='blog-post'),
    path ('services/', services, name='services'),
    path ('book-a-session/', session, name='session'),
    path ('blog/like-post/<slug>/', like, name='like'),
]

