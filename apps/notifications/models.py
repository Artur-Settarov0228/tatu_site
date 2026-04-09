from django.db import models
from apps.students.models import Talaba
from apps.users.models import OtaOna

class Xabarnoma(models.Model):
    TUR = (('WARNING', '⚠️ Ogohlantirish'), ('ALERT', '🔴 Xabar'), ('REPORT', '📊 Hisobot'))
    
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE, related_name='xabarnomalar')
    ota_ona = models.ForeignKey(OtaOna, on_delete=models.CASCADE, null=True, blank=True, related_name='xabarnomalar')
    tur = models.CharField(max_length=20, choices=TUR)
    sarlavha = models.CharField(max_length=200)
    matn = models.TextField()
    nb_soni = models.IntegerField(default=0)
    ketma_ket_nb = models.IntegerField(default=0)
    yuborildi = models.BooleanField(default=False)
    yuborilgan_vaqt = models.DateTimeField(null=True, blank=True)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xabarnomalar'
        ordering = ['-yaratilgan_vaqt']
        verbose_name = 'Xabarnoma'
        verbose_name_plural = 'Xabarnomalar'
    
    def __str__(self):
        return f"{self.talaba.toliq_ism} - {self.get_tur_display()}"

class XabarnomaSozlamalari(models.Model):
    ota_ona = models.OneToOneField(OtaOna, on_delete=models.CASCADE, related_name='xabarnoma_sozlamalari')
    telegram_xabar = models.BooleanField(default=True)
    sms_xabar = models.BooleanField(default=False)
    nb_chegarasi = models.IntegerField(default=3)
    kunlik_hisobot = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'xabarnoma_sozlamalari'
        verbose_name = 'Xabarnoma sozlamasi'
        verbose_name_plural = 'Xabarnoma sozlamalari'
    
    def __str__(self):
        return f"{self.ota_ona} sozlamalari"