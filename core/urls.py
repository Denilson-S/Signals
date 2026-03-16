"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from posts.views import feed_view as feed
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from users.api.viewsets import UserViewSet
from posts.api.viewsets import PostViewSet
from comments.api.viewsets import CommentViewSet
from tags.api.viewsets import TagViewSet
from profiles.api.viewsets import ProfileViewSet
from u_messages.api.viewsets import MessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', feed, name='home'),
    path("users/", include("users.urls")),
    path("comments/", include("comments.urls")),
    path("messages/", include("u_messages.urls")),
    path("profiles/", include("profiles.urls")),
    path("posts/", include("posts.urls")),
    path("tags/", include("tags.urls")),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
