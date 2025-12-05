from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Tag
from .forms import TagForm
from django.contrib import messages

def is_staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_staff)
def dashboard_tags(request):
    tags = Tag.objects.all().order_by('-created_at')
    return render(request, 'tags/dashboard.html', {'tags': tags})

@user_passes_test(is_staff)
def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.author = request.user
            tag.save()
            messages.success(request, 'Tag created successfully!')
            return redirect('dashboard_tags')
    else:
        form = TagForm()
    return render(request, 'tags/form.html', {'form': form, 'title': 'Create Tag'})

@user_passes_test(is_staff)
def edit_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated successfully!')
            return redirect('dashboard_tags')
    else:
        form = TagForm(instance=tag)
    return render(request, 'tags/form.html', {'form': form, 'title': 'Edit Tag'})

@user_passes_test(is_staff)
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == 'POST':
        tag.delete()
        messages.success(request, 'Tag deleted successfully!')
    return redirect('dashboard_tags')