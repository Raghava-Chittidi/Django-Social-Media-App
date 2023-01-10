
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.new_post, name="newpost"),
    path("user/<str:name>", views.users, name="user"),
    path("following", views.following, name="following"),

    # API Routes
    path("posts/<int:id>", views.posts, name="posts"),
]
