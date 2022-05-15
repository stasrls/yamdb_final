from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name')
    list_editable = ('role',)
    search_fields = ('username', 'role')
    empty_value_display = '-пусто-'
