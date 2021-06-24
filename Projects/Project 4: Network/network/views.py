import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Profile, Post


def index(request):
    '''
    The default route which lists all posts from all users, 
    with the most recent posts first.
    '''
    return render(request, 'network/index.html')


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'network/login.html', {
                'message': 'Invalid username and/or password.'
            })
    else:
        return render(request, 'network/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            return render(request, 'network/register.html', {
                'message': 'Passwords must match.'
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Profile(user=user).save()
        except IntegrityError:
            return render(request, 'network/register.html', {
                'message': 'Username already taken.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'network/register.html')


def posts_view(request):
    '''
    It renders a page that displays all posts from all users.
    '''
    user = request.GET.get('user', None)
    if user:
        posts = Post.objects.filter(author=user).all()
    else:
        posts = Post.objects.all()

    return posts_paginated_view(request, posts)


def posts_paginated_view(request, posts):
    '''
    It renders a page that displays all posts from all users.
    Posts are paginated and displayed 10 on a page.
    '''
    post_list = posts.order_by('-date_created').all()
    paginator = Paginator(post_list, 10)
    page = paginator.get_page(request.GET['page'])

    return JsonResponse({
        'posts': [post.serialize(request.user) for post in page],
        'num_pages': paginator.num_pages
    }, safe=False)


@login_required
def posts_followed_view(request):
    '''
    It renders a page that displays all posts made by users 
    that the current user follows.
    Posts are paginated and displayed 10 on a page.
    '''
    followed = request.user.get_followers.all()
    posts = Post.objects.filter(author__in=followed).all()

    return posts_paginated_view(request, posts)


@login_required
def post_create_edit(request):
    '''
    It allows the user to create a new post 
    and edit any their own posts.
    '''
    if request.method == 'POST':
        post_form = Post(post=request.POST['post'])
        post_form.author = Profile.objects.get(user=request.user)
        post_form.save()
    elif request.method == 'PUT':
        data = json.loads(request.body)
        post_id = int(data['post_id'])
        new_post = data['new_post']
        post = Post.objects.filter(id=post_id).first()

        if request.user != post.author.user:
            return HttpResponse(
                'You do not have permission to edit this post', 
                status=401)
        
        post.post = new_post
        post.save()
        
        return JsonResponse({'result': True}, status=200)
    else:
        return JsonResponse({
            'error': 'Supported request methods are GET and POST'
        }, status=400)

    return index(request)


@login_required
def post_like(request, post_id):
    '''
    It allows the user to toggle whether or not 
    they 'like' a particular post.
    '''
    user = Profile.objects.filter(user=request.user).first()
    post = Post.objects.get(id=post_id)

    if post in user.likes.all():
        new_status = False
        post.likes.remove(user)
    else:
        new_status = True
        post.likes.add(user)
    post.save()

    return JsonResponse({
        'liked': new_status, 'new_number': post.likes.count()
    }, status=200)


def user_details_view(request, user_id):
    '''
    It renders a page that displays the details of a selected user.
    '''
    user = Profile.objects.filter(id=user_id).first()

    return JsonResponse(user.serialize(request.user), status=200)


@login_required
def user_follow(request, user_id):
    '''
    It allows the user to toggle whether or not 
    they are following another user’s posts.
    '''
    user = Profile.objects.get(id=user_id)

    if user in request.user.get_followers.all():
        new_status = False
        user.followers.remove(request.user)
    else:
        new_status = True
        user.followers.add(request.user)
    user.save()

    return JsonResponse({
        'new_follower': new_status, 'new_number': user.followers.count()
    }, status=200)
