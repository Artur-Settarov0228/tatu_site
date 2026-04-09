from django.db import models
from apps.users.models import Oqituvchi

class Kurs(models.Model):
    nomi = models.CharField(max_length=100)
    tartib = models.IntegerField(unique=True)
    
    class Meta:
        db_table = 'kurslar'
        ordering = ['tartib']
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
    
    def __str__(self):
        return self.nomi

class Yonalish(models.Model):
    nomi = models.CharField(max_length=200)
    kodi = models.CharField(max_length=20, unique=True)
    tavsif = models.TextField(blank=True)
    
    class Meta:
        db_table = 'yonalishlar'
        verbose_name = 'Yo\'nalish'
        verbose_name_plural = 'Yo\'nalishlar'
    
    def __str__(self):
        return self.nomi

class Guruh(models.Model):
    nomi = models.CharField(max_length=50, unique=True)
    yonalish = models.ForeignKey(Yonalish, on_delete=models.CASCADE, related_name='guruhlar')
    kurs = models.ForeignKey(Kurs, on_delete=models.CASCADE, related_name='guruhlar')
    oquv_yili = models.CharField(max_length=9)
    rahbar = models.ForeignKey(Oqituvchi, on_delete=models.SET_NULL, null=True, blank=True, related_name='rahbarlik_guruhlari')
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    aktiv = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'guruhlar'
        unique_together = [['nomi', 'oquv_yili']]
        verbose_name = 'Guruh'
        verbose_name_plural = 'Guruhlar'
    
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
    qabul_sana = models.DateField(auto_now_add=True)
    aktiv = models.BooleanField(default=True)
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)
    yangilangan_vaqt = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'talabalar'
        ordering = ['familiya', 'ism']
        verbose_name = 'Talaba'
        verbose_name_plural = 'Talabalar'
    
    @property
    def toliq_ism(self):
        return f"{self.familiya} {self.ism}"
    
    @property
    def nb_soni(self):
        from apps.attendance.models import Davomat
        return Davomat.objects.filter(talaba=self, holat='KELMADI').count()
    
    def ketma_ket_nb_olish(self):
        from apps.attendance.models import Davomat
        oxirgilar = Davomat.objects.filter(talaba=self).order_by('-sana')[:10]
        ketma_ket = 0
        for d in oxirgilar:
            if d.holat == 'KELMADI':
                ketma_ket += 1
            else:
                break
        return ketma_ket
    
    def __str__(self):
        return self.toliq_ism

class OtaOnaTalaba(models.Model):
    QARINDOSHLIK = (('OTA', 'Ota'), ('ONA', 'Ona'), ('VASIY', 'Vasiy'))
    
    ota_ona = models.ForeignKey('users.OtaOna', on_delete=models.CASCADE, related_name='bolalar')
    talaba = models.ForeignKey(Talaba, on_delete=models.CASCADE, related_name='ota_onalar')
    qarindoshlik = models.CharField(max_length=20, choices=QARINDOSHLIK)
    asosiy = models.BooleanField(default=True)
    xabar_olish_mumkin = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'ota_ona_talabalar'
        unique_together = [['ota_ona', 'talaba']]
        verbose_name = 'Ota-ona-Talaba'
        verbose_name_plural = 'Ota-ona-Talabalar'
    
    def __str__(self):
        return f"{self.ota_ona} -> {self.talaba.toliq_ism}"