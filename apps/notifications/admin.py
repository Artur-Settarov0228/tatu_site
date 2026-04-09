from django.contrib import admin
from .models import Xabarnoma, XabarnomaSozlamalari

@admin.register(Xabarnoma)
class XabarnomaAdmin(admin.ModelAdmin):
    list_display = ('talaba', 'tur', 'sarlavha', 'yuborildi', 'yaratilgan_vaqt')
    list_filter = ('tur', 'yuborildi')
    search_fields = ('talaba__ism', 'talaba__familiya', 'sarlavha')

@admin.register(XabarnomaSozlamalari)
class XabarnomaSozlamalariAdmin(admin.ModelAdmin):
    list_display = ('ota_ona', 'telegram_xabar', 'sms_xabar', 'nb_chegarasi')
    list_filter = ('telegram_xabar', 'sms_xabar')