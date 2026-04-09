from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Foydalanuvchi, Oqituvchi, OtaOna

class FoydalanuvchiAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'telefon', 'roli', 'is_active')
    list_filter = ('roli', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'telefon')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy', {'fields': ('first_name', 'last_name', 'email', 'telefon')}),
        ('Ruxsatlar', {'fields': ('roli', 'is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(Foydalanuvchi, FoydalanuvchiAdmin)
admin.site.register(Oqituvchi)
admin.site.register(OtaOna)