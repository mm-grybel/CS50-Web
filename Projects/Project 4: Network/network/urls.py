from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('posts', views.posts_view, name='posts_view'),
    path('posts/followed', views.posts_followed_view, name='posts_followed_view'),
    path('post/create_edit', views.post_create_edit, name='post_create_edit'),
    path('post/<str:post_id>/like', views.post_like, name='post_like'),
    path('user/<int:user_id>', views.user_details_view, name='user_details_view'),
    path('user/<int:user_id>/follow', views.user_follow, name='user_follow'),
]