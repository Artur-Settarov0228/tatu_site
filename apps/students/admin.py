from django.contrib import admin
from .models import Kurs, Yonalish, Guruh, Talaba, OtaOnaTalaba

@admin.register(Kurs)
class KursAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'tartib')
    list_editable = ('tartib',)

@admin.register(Yonalish)
class YonalishAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'kodi')

@admin.register(Guruh)
class GuruhAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'yonalish', 'kurs', 'oquv_yili', 'rahbar', 'aktiv')
    list_filter = ('kurs', 'yonalish', 'aktiv')
    search_fields = ('nomi',)

@admin.register(Talaba)
class TalabaAdmin(admin.ModelAdmin):
    list_display = ('talaba_id', 'familiya', 'ism', 'guruh', 'telefon', 'nb_soni', 'aktiv')
    list_filter = ('guruh__kurs', 'guruh', 'aktiv')
    search_fields = ('talaba_id', 'ism', 'familiya', 'telefon')
    list_editable = ('aktiv',)
    
    def nb_soni(self, obj):
        return obj.nb_soni
    nb_soni.short_description = "NB soni"

@admin.register(OtaOnaTalaba)
class OtaOnaTalabaAdmin(admin.ModelAdmin):
    list_display = ('ota_ona', 'talaba', 'qarindoshlik', 'asosiy')
    list_filter = ('qarindoshlik', 'asosiy')