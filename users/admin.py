from django.contrib import admin
from .models import UserProfile
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ('user', 'messages', 'avatar')

admin.site.register(UserProfile, UserProfileAdmin)