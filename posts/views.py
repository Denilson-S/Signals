from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Post
from tags.models import Tag
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def feed_view(request):
    """Página principal: Lista posts de todos."""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts})

@login_required
def tag_feed(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')
    return render(request, 'posts/feed.html', {'posts': posts, 'current_tag': tag})

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'tags']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control border-0', 
                'placeholder': "What's on your mind?", 
                'rows': 2, 
                'style': 'resize: none;'
            }),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'})
        }

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m() # Save many-to-many data (tags)
            return redirect('index')
    else:
        form = PostForm()
        user_name = request.user.first_name or request.user.username or 'Guest'
        form.fields['content'].widget.attrs['placeholder'] = f"What's on your mind, {user_name}?"
    return render(request, 'posts/create.html', {'form': form})

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('index')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/edit.html', {'form': form, 'post': post})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
    return redirect('index')

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('index')