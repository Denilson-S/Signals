from django.shortcuts import render
from .models import Message
from django import forms
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model

# Create your views here.
def list_messages(request):
    messages = Message.objects.all()
    return render(request, 'messages/list.html', {'messages': messages})


User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'sender', 'content']  # ajuste conforme seu modelo

def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    return render(request, 'messages/detail.html', {'message': message})

def message_create(request, recipient_id):
    recipient = get_object_or_404(User, pk=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if hasattr(msg, 'sender') and request.user.is_authenticated:
                msg.sender = request.user
            msg.recipient = recipient
            msg.save()
            return redirect('list_messages')
    else:
        form = MessageForm(initial={'recipient': recipient})
    return render(request, 'messages/form.html', {'form': form, 'action': 'create'})

def message_update(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            return redirect('message_detail', pk=pk)
    else:
        form = MessageForm(instance=message)
    return render(request, 'messages/form.html', {'form': form, 'action': 'edit'})

def message_delete(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if request.method == 'POST':
        message.delete()
        return redirect('list_messages')
    return render(request, 'messages/confirm_delete.html', {'message': message})