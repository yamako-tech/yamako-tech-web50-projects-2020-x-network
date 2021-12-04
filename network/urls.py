
from django.urls import path

from . import views
from .views import PostView, EditView, ProfileView, AddFollower, RemoveFollower, FollowingList

urlpatterns = [
    path("", views.PostView, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post/", views.new_post, name="new_post"),
    path("like", views.LikeView, name="like"),
    path("edit_post/<int:pk>", EditView.as_view(), name="edit_post"),
    path("profile/<int:pk>", ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/followers/add", AddFollower.as_view(), name="add_follower"),
    path("profile/<int:pk>/followers/remove", RemoveFollower.as_view(), name="remove_follower"),
    path("following_list", FollowingList.as_view(), name="following_list"),
]
