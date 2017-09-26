from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User

class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    inlines = [
        ProfileInline,
    ]

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']

admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
