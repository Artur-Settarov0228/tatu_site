from django.db import models
from django.utils import timezone

class AsosiyModel(models.Model):
    """Barcha modellar uchun asosiy klass"""
    
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)
    aktiv = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
    
    def aktivlashtir(self):
        self.aktiv = True
        self.save(update_fields=['aktiv', 'yangilangan_vaqt'])
    
    def aktivlashtirma(self):
        self.aktiv = False
        self.save(update_fields=['aktiv', 'yangilangan_vaqt'])


class VaqtBelgiliModel(models.Model):
    """Soft delete uchun vaqt belgilari"""
    
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)
    ochirilgan_vaqt = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True
    
    def yumshoq_ochir(self):
        self.ochirilgan_vaqt = timezone.now()
        self.save(update_fields=['ochirilgan_vaqt', 'yangilangan_vaqt'])
    
    def tikla(self):
        self.ochirilgan_vaqt = None
        self.save(update_fields=['ochirilgan_vaqt', 'yangilangan_vaqt'])
    
    @property
    def ochirilganmi(self):
        return self.ochirilgan_vaqt is not None