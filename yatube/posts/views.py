from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from posts.forms import PostForm

from .models import Group, Post

POST_ON_PAGE = 10


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.filter(group=group)
    paginator = Paginator(post_list, POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_posts = user.posts.all()
    paginator = Paginator(user_posts, POST_ON_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'post_count': user_posts.count(),
        'page_obj': page_obj,
        'author': user,
        'username': username,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    post_count = Post.objects.filter(author=post.author)
    context = {
        'post': post,
        'post_count': post_count.count(),
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        username = post.author.username
        post.save()
        return redirect('posts:profile', username)
    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=post)
    if request.user == post.author and request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            form = PostForm(instance=post)
            post.save()
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(instance=post)
    return render(request, 'posts/create_post.html', {
        'form': form, 'post': post, 'is_edit': True, })
