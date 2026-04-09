import re
import random
import string
from datetime import datetime

def telefon_formatla(telefon):
    telefon = re.sub(r'\D', '', str(telefon))
    if len(telefon) == 12 and telefon.startswith('998'):
        return f"+{telefon[:3]} {telefon[3:5]} {telefon[5:8]} {telefon[8:10]} {telefon[10:12]}"
    return telefon

def unikal_id_yarat(prefix='', uzunlik=8):
    harflar = string.ascii_uppercase + string.digits
    tasodifiy = ''.join(random.choices(harflar, k=uzunlik))
    return f"{prefix}_{tasodifiy}" if prefix else tasodifiy

def standart_javob(holat, xabar, malumot=None, kod=200):
    return {
        'holat': holat,
        'kod': kod,
        'xabar': xabar,
        'malumot': malumot
    }