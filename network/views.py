from datetime import datetime

from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView

from .forms import PostForm
from .models import User, Post, Like, Profile


def PostView(request):
    """Show All Posts and Likes"""
    posts = Post.objects.all()
    form = PostForm()
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    liked_list = []
    for post in posts:
        liked = post.like_set.filter(user=request.user.id)
        if liked.exists():
            liked_list.append(post.id)

    context = {
        'posts': posts,
        'form': form,
        'liked_list': liked_list,
    }
    return render(request, 'network/index.html', context)


class NewPostForm(forms.Form):
    """Textarea for New Post"""
    new_post = forms.Textarea()


@login_required
def new_post(request):
    """Add New Post to List"""
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            new_post = form.data["new_post"]
            created = datetime.now()
        else:
            message = "Something went wrong..."
            return render(request,"network/index.html")            
        new_post = Post(content=new_post, created=created, user=request.user)
        new_post.save()
        return redirect('index')       
    return redirect('index')


class EditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Edit Post"""
    model = Post
    template_name = 'network/edit_post.html'
    fields = ['content']
    success_url = reverse_lazy('index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.user


@login_required
def LikeView(request):
    """One Like for One Post"""
    if request.method =="POST":
        post = get_object_or_404(Post, pk=request.POST.get('post_id'))
        user = request.user
        liked = False
        like = Like.objects.filter(post=post, user=user)
        if like.exists():
            like.delete()
        else:
            like.create(post=post, user=user)
            liked = True
    
        context={
            'post_id': post.id,
            'liked': liked,
            'count': post.like_set.count(),
        }

    if request.is_ajax():
        return JsonResponse(context)


class ProfileView(LoginRequiredMixin, View):
    """Profile for Loggedin User, Shows the Number of Followers"""
    def get(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(user=user).order_by('-created')
        paginator = Paginator(posts, 10)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        followers = profile.followers.all()
        if len(followers) == 0:
            is_following = False
        for follower in followers:
            if follower == request.user:
                is_following = True
                break
            else:
                is_following = False
        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'posts': posts,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }
        return render(request, 'network/profile.html', context)


class AddFollower(LoginRequiredMixin, View):
    """Follow Other Users"""
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('profile', pk=profile.pk)


class RemoveFollower(LoginRequiredMixin, View):
    """Unfollow Following Users"""
    def post(self, request, pk, *args, **kwargs):
        profile = Profile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('profile', pk=profile.pk)
        

class FollowingList(LoginRequiredMixin, ListView):
    """Show Posts from ONLY Following Users"""
    model = Post
    template_name = 'network/following_list.html'
    paginate_by = 10

    def get_queryset(self):
        """Returns the query set only if the follow list contains the user"""
        profile = Profile.objects.get_or_create(user=self.request.user)
        all_follow = profile[0].followers.all()
        return Post.objects.filter(user__in=all_follow)

    def get_context_data(self, *args, **kwargs):
        """Add object information about the connection to the context"""
        context = super().get_context_data(*args, **kwargs)
        context['profile'] = Profile.objects.get_or_create(user=self.request.user)
        return context


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
