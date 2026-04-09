from django.db import models

class AsosiyModel(models.Model):
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True