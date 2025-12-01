from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django import forms
from .models import Profile

# Create your views here.
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'profiles/detail.html', {'profile': profile})

def profile_create(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES or None)
        if form.is_valid():
            profile = form.save()
            return render(request, 'profiles/detail.html', {'profile': profile})
    else:
        form = ProfileForm()
    return render(request, 'profiles/form.html', {'form': form})

def profile_update(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES or None, instance=profile)
        if form.is_valid():
            profile = form.save()
            return render(request, 'profiles/detail.html', {'profile': profile})
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/form.html', {'form': form, 'profile': profile})

def profile_delete(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.method == 'POST':
        profile.delete()
        return render(request, 'profiles/deleted.html')
    return render(request, 'profiles/confirm_delete.html', {'profile': profile})