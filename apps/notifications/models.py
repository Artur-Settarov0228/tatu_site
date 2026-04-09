from django.db import models
from apps.students.models import Talaba
from apps.users.models import OtaOna

class Xabarnoma(models.Model):
    TUR_TANLOVI = (
        ('WARNING', 'Ogohlantirish'),
        ('ALERT', 'Xabar'),
        ('REPORT', 'Hisobot'),
    )
    
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE, related_name='xabarnomalar')
    ota_ona = models.ForeignKey(OtaOna, on_delete=models.CASCADE, null=True, blank=True, related_name='xabarnomalar')
    tur = models.CharField(max_length=10, choices=TUR_TANLOVI, default='ALERT')
    sarlavha = models.CharField(max_length=200)
    matn = models.TextField()
    yuborildi = models.BooleanField(default=False)
    yuborilgan_vaqt = models.DateTimeField(null=True, blank=True)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'xabarnomalar'
        ordering = ['-yaratilgan_vaqt']
    
    def __str__(self):
        return f"{self.talaba.toliq_ism} - {self.get_tur_display()}"


class XabarnomaSozlamalari(models.Model):
    ota_ona = models.OneToOneField(OtaOna, on_delete=models.CASCADE, related_name='xabarnoma_sozlamalari')
    telegram_xabar = models.BooleanField(default=True)
    nb_chegarasi = models.IntegerField(default=5)
    
    class Meta:
        db_table = 'xabarnoma_sozlamalari'
    
    def __str__(self):
        return f"{self.ota_ona} sozlamalari"