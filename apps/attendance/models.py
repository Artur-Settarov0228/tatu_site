from django.db import models
from apps.students.models import Talaba, Guruh
from apps.users.models import Oqituvchi

class Fan(models.Model):
    nomi = models.CharField(max_length=200)
    kodi = models.CharField(max_length=20, unique=True)
    qisqa_nomi = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'fanlar'
        verbose_name = 'Fan'
        verbose_name_plural = 'Fanlar'
    
    def __str__(self):
        return self.nomi

class Jadval(models.Model):
    HAFTA_KUNLARI = ((1, 'Dushanba'), (2, 'Seshanba'), (3, 'Chorshanba'), (4, 'Payshanba'), (5, 'Juma'), (6, 'Shanba'))
    
    guruh = models.ForeignKey(Guruh, on_delete=models.CASCADE, related_name='jadval')
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE, related_name='jadval')
    oqituvchi = models.ForeignKey(Oqituvchi, on_delete=models.CASCADE, related_name='jadval')
    hafta_kuni = models.IntegerField(choices=HAFTA_KUNLARI)
    boshlanish_vaqti = models.TimeField()
    tugash_vaqti = models.TimeField()
    xona = models.CharField(max_length=50)
    aktiv = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'jadval'
        unique_together = [['guruh', 'fan', 'hafta_kuni', 'boshlanish_vaqti']]
        verbose_name = 'Jadval'
        verbose_name_plural = 'Jadvallar'
    
    def __str__(self):
        return f"{self.guruh.nomi} - {self.fan.nomi}"

class Davomat(models.Model):
    HOLAT = (('KELDI', '✅ Qatnashdi'), ('KELMADI', '❌ Qatnashmadi'))
    SABAB = (('SABABSIZ', 'Sababsiz'), ('KASAL', 'Kasal'), ('RUXSAT', 'Ruxsat bilan'), ('KECHIKDI', 'Kechikish'))
    
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE, related_name='davomatlar')
    jadval = models.ForeignKey(Jadval, on_delete=models.CASCADE, null=True, blank=True)
    fan = models.ForeignKey(Fan, on_delete=models.CASCADE)
    sana = models.DateField()
    holat = models.CharField(max_length=10, choices=HOLAT, default='KELDI')
    sabab = models.CharField(max_length=20, choices=SABAB, default='SABABSIZ')
    izoh = models.TextField(blank=True)
    kiritgan = models.ForeignKey(Oqituvchi, on_delete=models.SET_NULL, null=True)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'davomatlar'
        ordering = ['-sana']
        unique_together = [['talaba', 'fan', 'sana']]
        verbose_name = 'Davomat'
        verbose_name_plural = 'Davomatlar'
    
    def __str__(self):
        return f"{self.talaba.toliq_ism} - {self.sana}"
    
    def save(self, *args, **kwargs):
        yangi = self.pk is None
        super().save(*args, **kwargs)
        if yangi and self.holat == 'KELMADI':
            from apps.notifications.services import nb_chegarasini_tekshir
            nb_chegarasini_tekshir(self.talaba)