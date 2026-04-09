from django.db import models
from apps.students.models import Talaba, Guruh
from apps.users.models import Oqituvchi

class Fan(models.Model):
    nomi = models.CharField(max_length=200)
    kodi = models.CharField(max_length=20, unique=True)
    
    class Meta:
        db_table = 'fanlar'
    
    def __str__(self):
        return self.nomi

class Jadval(models.Model):
    HAFTA_KUNLARI = ((1, 'Dushanba'), (2, 'Seshanba'), (3, 'Chorshanba'), (4, 'Payshanba'), (5, 'Juma'), (6, 'Shanba'))
    
    guruh = models.ForeignKey(Guruh, on_delete=models.CASCADE, related_name='jadval')
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    oqituvchi = models.ForeignKey(Oqituvchi, on_delete=models.CASCADE)
    hafta_kuni = models.IntegerField(choices=HAFTA_KUNLARI)
    boshlanish_vaqti = models.TimeField()
    tugash_vaqti = models.TimeField()
    xona = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'jadval'
    
    def __str__(self):
        return f"{self.guruh.nomi} - {self.fan.nomi}"

class Davomat(models.Model):
    HOLAT = (('KELDI', 'Qatnashdi'), ('KELMADI', 'Qatnashmadi'))
    SABAB = (('SABABSIZ', 'Sababsiz'), ('KASAL', 'Kasal'), ('RUXSAT', 'Ruxsat bilan'))
    
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE, related_name='davomatlar')
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    sana = models.DateField()
    holat = models.CharField(max_length=10, choices=HOLAT, default='KELDI')
    sabab = models.CharField(max_length=10, choices=SABAB, default='SABABSIZ')
    izoh = models.TextField(blank=True)
    kiritgan = models.ForeignKey(Oqituvchi, on_delete=models.SET_NULL, null=True)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'davomatlar'
        unique_together = [['talaba', 'fan', 'sana']]
    
    def __str__(self):
        return f"{self.talaba.toliq_ism} - {self.sana}"