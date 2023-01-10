from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post, User, Following
import json


# Route "/login"
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


# Route "/logout"
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# Route "/register"
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# Returns the page through page number input
def paging(posts, pageNum):
    list = []
    for post in posts:
        list.append(post.id)

    p = Paginator(list, 10)
    return p.get_page(pageNum)


# Route "/"
def index(request):

    # Creates new post and saves it
    if request.method == "POST":
        content = request.POST["content"]
        new = Post(len(Post.objects.all()) + 1, request.user.id, content)
        new.save()

    # Gets page number through url and returns the posts on that page
    num = request.GET.get("page")
    page = paging(Post.objects.all().order_by('-date'), num)
    posts = Post.objects.filter(id__in = page.object_list).order_by('-date')
    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page,
    })


# Route "/newpost"
@login_required
def new_post(request):
    return render(request, "network/newpost.html")


# Route "/users/name"
@login_required
def users(request, name):

    # Get the id of the user's profile your are visiting
    id = User.objects.get(username=name).id

    if request.method == "POST":

        # Check if you already follow him
        if (len(Following.objects.filter(user=request.user.id, person=id)) == 1):

            # If you do, it means you pressed the unfollow button
            Following.objects.filter(user=request.user.id, person=id).delete()
        else:

            # If you dont, it means you pressed the follow button
            newFollowerID = request.user.id
            new = Following(len(Following.objects.all()) + 1, newFollowerID, id)
            new.save()

    btn = ""

    # Set name of the button to unfollow if you already follow him
    if (len(Following.objects.filter(user=request.user.id, person=id)) == 1):
        btn = "Unfollow"

    # Get the user's posts and ensure they are paginated
    posts = Post.objects.filter(user=id).order_by('-date')
    num = request.GET.get("page")
    page = paging(posts, num)
    posts = Post.objects.filter(id__in = page.object_list).order_by('-date')

    return render(request, "network/users.html", {
        "name": name,
        "posts": posts,
        "followers": len(Following.objects.filter(person=id)),
        "following": len(Following.objects.filter(user=id)),
        "btn": btn,
        "page_obj": page,
    })


# Route "/following"
@login_required
def following(request):

    # Get all the posts of the users you follow
    users = Following.objects.filter(user=request.user.id).values_list('person_id', flat=True)
    posts = Post.objects.filter(user__in = users).order_by('-date')

    # Gets page number through url and returns the posts on that page
    num = request.GET.get("page")
    page = paging(posts, num)
    posts = Post.objects.filter(id__in = page.object_list).order_by('-date')

    return render(request, "network/following.html", {
        "posts": posts,
        "page_obj": page
    })


def posts(request, id):

    # Check if there is a valid post. If not return error
    try:
        post = Post.objects.get(id=id)
    except:
        return JsonResponse({"error": "Post not found"}, status=404)
    
    # Show post details
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # If PUT request
    elif request.method == "PUT":
        data = json.loads(request.body)

        # User must have clicked Save Post after editing it
        if data.get("content") is not None:
            post.content = data["content"]
            post.save()

        # User must have clicked the like button
        elif data.get("likes") is not None:
            list = set()

            # Puts the id of all the users that are still liking the post in a set
            for i in data["likes"]:
                try:
                    list.add(int(i))
                except:
                    pass
            
            # Clear all the previous likes
            post.likes.clear()

            # Add back all the users that still like the post
            for x in list:
                post.likes.add(User.objects.get(id=x))
                post.save()

        return HttpResponse(status=204)

    # Ensure only GET or PUT requests are made
    else:
        return JsonResponse({"error": "GET or PUT request required"}, status=400)
