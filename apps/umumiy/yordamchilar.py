"""
Yordamchi funksiyalar
"""

import re
from datetime import datetime, date
from django.utils import timezone

def telefon_formatla(telefon):
    """
    Telefon raqamni formatlash
    +998901234567 -> +998 90 123 45 67
    """
    telefon = re.sub(r'\D', '', str(telefon))
    
    if len(telefon) == 12 and telefon.startswith('998'):
        return f"+{telefon[:3]} {telefon[3:5]} {telefon[5:8]} {telefon[8:10]} {telefon[10:12]}"
    elif len(telefon) == 9:
        return f"{telefon[:2]} {telefon[2:5]} {telefon[5:7]} {telefon[7:9]}"
    
    return telefon


def telefon_tasdiqla(telefon):
    """
    Telefon raqamni tekshirish
    +998901234567 yoki 901234567 formatida bo'lishi kerak
    """
    telefon = re.sub(r'\D', '', str(telefon))
    
    if len(telefon) == 12 and telefon.startswith('998'):
        return True
    elif len(telefon) == 9:
        return True
    
    return False


def sana_formatla(sana, format="%d.%m.%Y"):
    """Sanani formatlash"""
    if isinstance(sana, str):
        sana = datetime.strptime(sana, '%Y-%m-%d').date()
    
    return sana.strftime(format)


def hafta_kunini_ol(sana):
    """Hafta kunini olish (Dushanba, Seshanba...)"""
    hafta_kunlari = {
        0: 'Dushanba', 1: 'Seshanba', 2: 'Chorshanba',
        3: 'Payshanba', 4: 'Juma', 5: 'Shanba', 6: 'Yakshanba'
    }
    
    if isinstance(sana, str):
        sana = datetime.strptime(sana, '%Y-%m-%d').date()
    
    return hafta_kunlari.get(sana.weekday(), 'Noma\'lum')


def unikal_id_generator(prefix='', uzunlik=8):
    """Unikal ID generatsiya qilish"""
    import random
    import string
    
    harflar = string.ascii_uppercase + string.digits
    tasodifiy_qism = ''.join(random.choices(harflar, k=uzunlik))
    
    if prefix:
        return f"{prefix}_{tasodifiy_qism}"
    return tasodifiy_qism


def vaqt_oraligi(vaqt1, vaqt2):
    """Ikki vaqt orasidagi farqni soat va daqiqada hisoblash"""
    if isinstance(vaqt1, str):
        vaqt1 = datetime.strptime(vaqt1, '%H:%M:%S').time()
    if isinstance(vaqt2, str):
        vaqt2 = datetime.strptime(vaqt2, '%H:%M:%S').time()
    
    from datetime import datetime, timedelta
    dt1 = datetime.combine(date.today(), vaqt1)
    dt2 = datetime.combine(date.today(), vaqt2)
    
    farq = dt2 - dt1 if dt2 > dt1 else dt1 - dt2
    
    soat = farq.seconds // 3600
    daqiqa = (farq.seconds % 3600) // 60
    
    return {'soat': soat, 'daqiqa': daqiqa, 'jami_daqiqa': farq.seconds // 60}


class MalumotQaytaruvchi:
    """API javoblarini standart formatda qaytarish uchun klass"""
    
    @staticmethod
    def muvaffaqiyatli(malumot=None, xabar="Muvaffaqiyatli", kod=200):
        return {
            'holat': 'success',
            'kod': kod,
            'xabar': xabar,
            'malumot': malumot
        }
    
    @staticmethod
    def xato(xabar="Xatolik yuz berdi", kod=400, malumot=None):
        return {
            'holat': 'error',
            'kod': kod,
            'xabar': xabar,
            'malumot': malumot
        }
    
    @staticmethod
    def ogohlantirish(xabar="Ogohlantirish", kod=200, malumot=None):
        return {
            'holat': 'warning',
            'kod': kod,
            'xabar': xabar,
            'malumot': malumot
        }