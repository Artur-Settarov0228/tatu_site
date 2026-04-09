from django.db import models
from apps.users.models import Oqituvchi

class Kurs(models.Model):
    nomi = models.CharField(max_length=100)
    tartib = models.IntegerField(unique=True)
    
    class Meta:
        db_table = 'kurslar'
        ordering = ['tartib']
    
    def __str__(self):
        return self.nomi

class Yonalish(models.Model):
    nomi = models.CharField(max_length=200)
    kodi = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'yonalishlar'
    
    def __str__(self):
        return self.nomi

class Guruh(models.Model):
    nomi = models.CharField(max_length=50, unique=True)
    yonalish = models.ForeignKey(Yonalish, on_delete=models.CASCADE, related_name='guruhlar')
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='guruhlar')
    oquv_yili = models.CharField(max_length=9)
    rahbar = models.ForeignKey(Oqituvchi, on_delete=models.SET_NULL, null=True)
    aktiv = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'guruhlar'
    
    def __str__(self):
        return f"{self.nomi} - {self.yonalish.nomi}"

class Talaba(models.Model):
    ism = models.CharField(max_length=100)
    familiya = models.CharField(max_length=100)
    talaba_id = models.CharField(max_length=20, unique=True)
    guruh = models.ForeignKey(Guruh, on_delete=models.CASCADE, related_name='talabalar')
    telefon = models.CharField(max_length=13)
    ota_ona_telefon = models.CharField(max_length=13)
    manzil = models.TextField(blank=True)
    aktiv = models.BooleanField(default=True)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'talabalar'
    
    @property
    def toliq_ism(self):
        return f"{self.familiya} {self.ism}"
    
    def __str__(self):
        return self.toliq_ism

class OtaOnaTalaba(models.Model):
    QARINDOSHLIK = (('OTA', 'Ota'), ('ONA', 'Ona'), ('VASIY', 'Vasiy'))
    
    ota_ona = models.ForeignKey('users.OtaOna', on_delete=models.CASCADE)
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE)
    qarindoshlik = models.CharField(max_length=10, choices=QARINDOSHLIK)
    
    class Meta:
        db_table = 'ota_ona_talabalar'
        unique_together = [['ota_ona', 'talaba']]