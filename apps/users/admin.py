from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Foydalanuvchi, Oqituvchi, OtaOna

class FoydalanuvchiAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'telefon', 'roli', 'is_active', 'tasdiqlangan')
    list_filter = ('roli', 'is_active', 'tasdiqlangan')
    search_fields = ('username', 'first_name', 'last_name', 'telefon')
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('username', 'password', 'first_name', 'last_name', 'email')
        }),
        ('Kontakt', {
            'fields': ('telefon', 'telegram_chat_id')
        }),
        ('Ruxsatlar', {
            'fields': ('roli', 'is_active', 'is_staff', 'is_superuser', 'tasdiqlangan')
        }),
        ('Vaqt', {
            'fields': ('last_login', 'yaratilgan_vaqt', 'yangilangan_vaqt')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'telefon', 'roli'),
        }),
    )
    
    readonly_fields = ('yaratilgan_vaqt', 'yangilangan_vaqt')


class OqituvchiAdmin(admin.ModelAdmin):
    list_display = ('foydalanuvchi', 'xodim_id', 'mutaxassislik', 'aktiv')
    list_filter = ('aktiv', 'mutaxassislik')
    search_fields = ('foydalanuvchi__first_name', 'foydalanuvchi__last_name', 'xodim_id')
    autocomplete_fields = ['foydalanuvchi']


class OtaOnaAdmin(admin.ModelAdmin):
    list_display = ('foydalanuvchi', 'kasbi', 'xabar_ushlubi')
    list_filter = ('xabar_ushlubi',)
    search_fields = ('foydalanuvchi__first_name', 'foydalanuvchi__last_name', 'foydalanuvchi__telefon')
    autocomplete_fields = ['foydalanuvchi']


admin.site.register(Foydalanuvchi, FoydalanuvchiAdmin)
admin.site.register(Oqituvchi, OqituvchiAdmin)
admin.site.register(OtaOna, OtaOnaAdmin)