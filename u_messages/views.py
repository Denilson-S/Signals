from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from users.models import User
from .models import Message
from django.http import JsonResponse

@login_required
def chat_view(request, user_id=None):
    users = User.objects.exclude(id=request.user.id)
    active_chat = None
    messages = []

    # Get recent conversations (simplified logic for now)
    # In a real app, you'd aggregate distinct users from sent/received messages
    # Here we just list all users or users with history
    
    # Let's get users we have chatted with
    chat_users_ids = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values_list('sender', 'receiver')
    
    # Flatten list and get unique IDs
    ids = set()
    for u1, u2 in chat_users_ids:
        ids.add(u1)
        ids.add(u2)
    
    # Remove self
    if request.user.id in ids:
        ids.remove(request.user.id)
        
    recent_users = User.objects.filter(id__in=ids)

    if user_id:
        active_chat = get_object_or_404(User, id=user_id)
        messages = Message.objects.filter(
            Q(sender=request.user, receiver=active_chat) | 
            Q(sender=active_chat, receiver=request.user)
        ).order_by('timestamp')
        
        # Mark as read
        Message.objects.filter(sender=active_chat, receiver=request.user, is_read=False).update(is_read=True)

    context = {
        'recent_users': recent_users,
        'active_chat': active_chat,
        'messages': messages,
        'all_users': users # For search
    }
    return render(request, 'messages/chat.html', context)

@login_required
def search_users(request):
    query = request.GET.get('q', '')
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)[:10]
        
        results = []
        for user in users:
            avatar_url = user.profile.avatar.url if hasattr(user, 'profile') and user.profile.avatar else None
            results.append({
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'avatar': avatar_url,
                'username': user.username
            })
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})
