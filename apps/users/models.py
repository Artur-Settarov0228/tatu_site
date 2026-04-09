from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class Foydalanuvchi(AbstractUser):
    ROL_TANLOVI = (
        ('ADMIN', 'Administrator'),
        ('OQITUVCHI', "O'qituvchi"),
        ('OTA_ONA', 'Ota-ona'),
    )
    
    roli = models.CharField(max_length=10, choices=ROL_TANLOVI, default='OQITUVCHI')
    telefon = models.CharField(max_length=13, unique=True, null=True, blank=True)
    telegram_chat_id = models.CharField(max_length=100, null=True, blank=True)
    tasdiqlangan = models.BooleanField(default=False)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'foydalanuvchilar'
    
    def __str__(self):
        return f"{self.username} - {self.get_roli_display()}"

class Oqituvchi(models.Model):
    foydalanuvchi = models.OneToOneField(Foydalanuvchi, on_delete=models.CASCADE, related_name='oqituvchi_profili')
    xodim_id = models.CharField(max_length=20, unique=True)
    mutaxassislik = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'oqituvchilar'
    
    def __str__(self):
        return self.foydalanuvchi.get_full_name()

class OtaOna(models.Model):
    foydalanuvchi = models.OneToOneField(Foydalanuvchi, on_delete=models.CASCADE, related_name='ota_ona_profili')
    manzil = models.TextField(blank=True)
    telegram_xabar = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'ota_onalar'
    
    def __str__(self):
        return self.foydalanuvchi.get_full_name()