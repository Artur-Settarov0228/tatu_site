"""
Umumiy modellar - barcha modellar uchun asosiy klasslar
"""

from django.db import models
from django.utils import timezone

class AsosiyModel(models.Model):
    """
    Barcha modellar uchun asosiy klass
    Bu klass barcha modellarda takrorlanadigan maydonlarni o'z ichiga oladi
    """
    
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    yangilangan_vaqt = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    aktiv = models.BooleanField(default=True, verbose_name="Aktiv")
    
    class Meta:
        abstract = True  # Bu klass ma'lumotlar bazasida jadval yaratmaydi
    
    def aktivlashtir(self):
        """Ob'ektni aktivlashtirish"""
        self.aktiv = True
        self.save(update_fields=['aktiv', 'yangilangan_vaqt'])
    
    def aktivlashtirmaslik(self):
        """Ob'ektni aktiv emas qilish"""
        self.aktiv = False
        self.save(update_fields=['aktiv', 'yangilangan_vaqt'])


class VaqtBelgiliModel(models.Model):
    """
    Faqat vaqt belgilari bo'lgan model
    Soft delete uchun o'chirilgan_vaqt maydoni qo'shilgan
    """
    
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    yangilangan_vaqt = models.DateTimeField(auto_now=True, verbose_name="Yangilangan vaqt")
    ochirilgan_vaqt = models.DateTimeField(null=True, blank=True, verbose_name="O'chirilgan vaqt")
    
    class Meta:
        abstract = True
    
    def yumshoq_ochir(self):
        """Ob'ektni yumshoq o'chirish (soft delete)"""
        self.ochirilgan_vaqt = timezone.now()
        self.save(update_fields=['ochirilgan_vaqt', 'yangilangan_vaqt'])
    
    def tiklash(self):
        """Yumshoq o'chirilgan ob'ektni tiklash"""
        self.ochirilgan_vaqt = None
        self.save(update_fields=['ochirilgan_vaqt', 'yangilangan_vaqt'])
    
    @property
    def ochirilganmi(self):
        """Ob'ekt o'chirilganligini tekshirish"""
        return self.ochirilgan_vaqt is not None


class TanlovModel(models.Model):
    """
    Tanlov (dropdown) uchun asosiy model
    Masalan: kurslar, yo'nalishlar va boshqalar
    """
    
    nomi = models.CharField(max_length=255, verbose_name="Nomi")
    tartib = models.IntegerField(default=0, verbose_name="Tartib")
    aktiv = models.BooleanField(default=True, verbose_name="Aktiv")
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqt")
    
    class Meta:
        abstract = True
        ordering = ['tartib', 'nomi']
    
    def __str__(self):
        return self.nomi