from django.contrib import admin
from .models import Custom_User

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_staff', 'is_doctor']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_staff']
    fieldsets = [
    (None, {'fields': ('username', 'email', 'password')}),
    ('Permissions', {'fields': ('is_active', 'is_staff')}),
    ('Custom Fields', {'fields': ('is_doctor',)}),]

admin.site.register(Custom_User, CustomUserAdmin)
