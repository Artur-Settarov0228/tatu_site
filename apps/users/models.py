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
    
    telefon_validator = RegexValidator(
        regex=r'^\+998\d{9}$',
        message="Telefon +998XXXXXXXXX formatida bo'lishi kerak"
    )
    telefon = models.CharField(
        validators=[telefon_validator], 
        max_length=13, 
        unique=True, 
        null=True, 
        blank=True
    )
    telegram_chat_id = models.CharField(max_length=100, null=True, blank=True)
    tasdiqlangan = models.BooleanField(default=False)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'foydalanuvchilar'
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_roli_display()}"

# Oqituvchi va OtaOna modellari yuqoridagi kabi qoladi...