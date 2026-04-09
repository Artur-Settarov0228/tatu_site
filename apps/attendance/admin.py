from django.contrib import admin
from django.utils.html import format_html
from .models import Fan, Jadval, Davomat

@admin.register(Fan)
class FanAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'kodi', 'qisqa_nomi')
    search_fields = ('nomi', 'kodi')

@admin.register(Jadval)
class JadvalAdmin(admin.ModelAdmin):
    list_display = ('guruh', 'fan', 'oqituvchi', 'hafta_kuni', 'boshlanish_vaqti', 'xona', 'aktiv')
    list_filter = ('hafta_kuni', 'aktiv')
    search_fields = ('guruh__nomi', 'fan__nomi')

@admin.register(Davomat)
class DavomatAdmin(admin.ModelAdmin):
    list_display = ('talaba', 'fan', 'sana', 'holat_belgisi', 'sabab')
    list_filter = ('holat', 'sabab', 'sana', 'fan')
    search_fields = ('talaba__ism', 'talaba__familiya')
    date_hierarchy = 'sana'
    
    def holat_belgisi(self, obj):
        if obj.holat == 'KELDI':
            return format_html('<span style="color:green;">✅ Keldi</span>')
        return format_html('<span style="color:red;">❌ Kelmadi</span>')
    holat_belgisi.short_description = "Holat"