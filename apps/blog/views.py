from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from .old_models import Post


class HomeView(View):

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        ctx = {
            'posts': posts
        }
        return render(request, 'blog/home.html', ctx)


class DetailView(View):

    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        ctx = {
            'post': post
        }
        return render(request, 'blog/detail.html', ctx)


class CreateView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'blog/create.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        content = request.POST.get('content')
        obj = Post.objects.create(title=title, content=content)
        return redirect('blog:homepage')
