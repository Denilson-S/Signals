from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Post

# Create your views here.
def feed_view(request):
    """Página principal: Lista posts de todos."""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts})

class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = '__all__'

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            posts = Post.objects.all().order_by('-created_at')
            return render(request, 'posts/feed.html', {'posts': posts})
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            posts = Post.objects.all().order_by('-created_at')
            return render(request, 'posts/index.html', {'posts': posts})
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'posts/index.html', {'posts': posts})

    class PostForm(forms.ModelForm):
        class Meta:
            model = Post
            fields = '__all__'
