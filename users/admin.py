from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    exclude = ('last_login', 'date_joined', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'is_active')

admin.site.register(User, UserAdmin)