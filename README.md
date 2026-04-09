```
┌─────────────────────────────────────────────────────────────────┐
│                        1. OTA-ONA BOTGA KIRISH                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Telegramda @davomat_bot → /start                               │
│                              ↓                                    │
│   Bot: "Telefon raqamingizni yuboring"                           │
│                              ↓                                    │
│   Ota-ona: Telefon raqamni yuboradi (+998901234567)              │
│                              ↓                                    │
│   Bot: "✅ Telefon raqamingiz saqlandi!"                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        2. O'QITUVCHI DAVOMAT KIRITADI             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   O'qituvchi Admin panelga kirib:                                │
│   - Talabani tanlaydi                                            │
│   - "KELMADI" deb belgilaydi                                     │
│   - Sababini tanlaydi (Sababsiz/Kasal/Ruxsat bilan)              │
│                              ↓                                    │
│   Tizim NB sonini hisoblaydi                                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   3. NB SONI TEKSHIRILADI                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Agar NB soni ≥ 5 bo'lsa:                                       │
│                              ↓                                    │
│   "⚠️ Diqqat! Farzandingiz 5-marta dars qoldirdi!"               │
│                              ↓                                    │
│   Xabar Ota-onaning Telegramiga yuboriladi                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────┐
│                      FOYDALANUVCHI TIZIMI                     │
├─────────────────────────────────────────────────────────────┤
│  MaxsusFoydalanuvchi (AbstractUser)                          │
│  ├── roli: [ADMIN, OQITUVCHI, OTA_ONA]                      │
│  ├── telefon, telegram_chat_id, tasdiqlangan                 │
│  └── JWT + Session Autentifikatsiya                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐                    │
│  │ ADMIN   │  │ OQITUVCHI │  │ OTA-ONA │                    │
│  │ Panel   │  │ Panel     │  │ Panel   │                    │
│  │ To'liq  │  │ Cheklangan│  │ Faqat   │                    │
│  │ Kirish  │  │ Kirish    │  │ Ko'rish │                    │
│  └─────────┘  └──────────┘  └─────────┘                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      TALABALAR ASOSI                          │
├─────────────────────────────────────────────────────────────┤
│  Talaba ──────┬────── Guruh                                  │
│  ├── ism      │       ├── nomi                               │
│  ├── talaba_id│       ├── kurs ────┐                        │
│  ├── telefon  │       └── yo'nalish ─┤                       │
│  └── ota_ona_telefon                 │                        │
│       │                               │                        │
│       ▼                               ▼                        │
│  OtaOnaTalaba ◄──────────────────────┘                        │
│  ├── qarindoshlik                                             │
│  └── asosiy                                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DAVOMAT TIZIMI                             │
├─────────────────────────────────────────────────────────────┤
│  Davomat                                                     │
│  ├── talaba (FK)                                            │
│  ├── fan (FK)                                               │
│  ├── sana                                                   │
│  ├── holat: [KELDI, KELMADI]                               │
│  ├── sabab: [KASAL, SABABSIZ, RUXSAT BILAN]                │
│  └── kim_kiritdi (Oqituvchi)                                │
│                                                             │
│  Jadval                                                      │
│  ├── guruh, fan, oqituvchi                                  │
│  ├── hafta_kuni, boshlanish_vaqti, tugash_vaqti            │
│  └── xona                                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   XABARNOMA MOTORI                            │
├─────────────────────────────────────────────────────────────┤
│  ⚠️ Qoidalar:                                                │
│  • 2 NB → OGOHLANTIRISH                                      │
│  • 3 NB → XABAR (Ota-ona + Telegram)                        │
│  • Ketma-ket NB → Telegram Xabari                           │
│                                                             │
│  Xabarnoma                                                   │
│  ├── talaba, ota_ona                                        │
│  ├── turi, matn                                             │
│  ├── nb_soni, ketma_ket_nb                                 │
│  └── yuborildi, yuborilgan_vaqt                             │
│                                                             │
│  KuzatuvQaydi (barcha harakatlar)                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   YETKAZISH KANALLARI                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  VEB PANEL   │  │ TELEGRAM BOT │  │  EMAIL       │     │
│  │              │  │              │  │  (Ixtiyoriy) │     │
│  │ • Admin      │  │ • /start     │  │              │     │
│  │ • Oqituvchi  │  │ • Telefon    │  │              │     │
│  │ • Ota-ona    │  │ • Statistika │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
davomat_tizimi/
├── boshqar.py
│
├── sozlamalar/
│   ├── __init__.py
│   ├── asosiy.py              # Asosiy sozlamalar
│   ├── ishlab_chiqarish.py    # Ishchi muhit sozlamalari
│   └── sinov.py               # Sinov muhiti sozlamalari
│
├── ilovalar/
│   ├── __init__.py
│   │
│   ├── umumiy/
│   │   ├── __init__.py
│   │   ├── modellar.py        # AsosiyModel, VaqtBelgiliModel
│   │   ├── ruxsatlar.py       # RolAsosidaRuxsat
│   │   ├── dekoratorlar.py    # @rol_talab_qilinadi
│   │   ├── sahifalash.py      # Maxsus sahifalash
│   │   └── yordamchilar.py    # Yordamchi funksiyalar
│   │
│   ├── foydalanuvchilar/
│   │   ├── __init__.py
│   │   ├── modellar.py        # Foydalanuvchi, Oqituvchi, OtaOna
│   │   ├── seriyalashtiruvchilar.py   # FoydalanuvchiSeriyalashtiruvchi
│   │   ├── korinishlar/
│   │   │   ├── __init__.py
│   │   │   ├── kirish_korinishlari.py    # Kirish, Chiqish
│   │   │   ├── foydalanuvchi_korinishlari.py
│   │   │   └── ota_ona_korinishlari.py
│   │   ├── marshrutlar.py
│   │   ├── xizmatlar.py       # FoydalanuvchiXizmati
│   │   ├── tanlovchilar.py    # FoydalanuvchiTanlovchi
│   │   └── shablonlar/
│   │       └── foydalanuvchilar/
│   │           ├── ota_ona_bosh_sahifasi.html
│   │           └── farzand_tafsilotlari.html
│   │
│   ├── talabalar/
│   │   ├── __init__.py
│   │   ├── modellar.py        # Talaba, Guruh, Kurs, Yonalish
│   │   ├── seriyalashtiruvchilar.py
│   │   ├── korinishlar.py
│   │   ├── marshrutlar.py
│   │   ├── xizmatlar.py       # TalabaXizmati
│   │   ├── tanlovchilar.py    # TalabaTanlovchi
│   │   └── shablonlar/
│   │       └── talabalar/
│   │           ├── royxat.html
│   │           ├── yaratish.html
│   │           ├── tahrirlash.html
│   │           └── tafsilotlar.html
│   │
│   ├── davomat/
│   │   ├── __init__.py
│   │   ├── modellar.py        # Davomat, Fan, Jadval
│   │   ├── seriyalashtiruvchilar.py
│   │   ├── korinishlar.py
│   │   ├── marshrutlar.py
│   │   ├── xizmatlar.py       # DavomatXizmati
│   │   ├── tanlovchilar.py
│   │   └── shablonlar/
│   │       └── davomat/
│   │           ├── index.html
│   │           ├── kop_davomat.html
│   │           └── tarix.html
│   │
│   ├── xabarnomalar/
│   │   ├── __init__.py
│   │   ├── modellar.py        # Xabarnoma
│   │   ├── seriyalashtiruvchilar.py
│   │   ├── korinishlar.py
│   │   ├── marshrutlar.py
│   │   ├── xizmatlar.py       # XabarnomaXizmati
│   │   ├── vazifalar.py       # Celery vazifalari
│   │   ├── telegram_bot.py    # Bot boshqaruvchisi
│   │   └── shablonlar/
│   │       └── xabarnomalar/
│   │           └── sozlamalar.html
│   │
│   └── tahlillar/
│       ├── __init__.py
│       ├── modellar.py
│       ├── seriyalashtiruvchilar.py
│       ├── korinishlar.py
│       ├── marshrutlar.py
│       ├── xizmatlar.py       # TahlilXizmati
│       └── shablonlar/
│           └── tahlillar/
│               ├── bosh_sahifa.html
│               ├── xavf_hisoboti.html
│               └── guruh_statistikasi.html
│
├── shablonlar/
│   ├── asosiy/
│   │   ├── asosiy.html
│   │   ├── yon_panel.html
│   │   ├── bosh_menu.html
│   │   └── pastki_qism.html
│   ├── autentifikatsiya/
│   │   ├── kirish.html
│   │   └── royhatdan_otish.html
│   └── bosh_sahifalar/
│       ├── admin_bosh_sahifasi.html
│       ├── oqituvchi_bosh_sahifasi.html
│       └── ota_ona_bosh_sahifasi.html
│
├── statik/
│   ├── css/
│   │   ├── tailwind.css
│   │   ├── maxsus.css
│   │   └── qorongu_rejim.css
│   ├── js/
│   │   ├── asosiy.js
│   │   ├── davomat.js
│   │   └── grafiklar.js
│   └── rasmlar/
│
├── talablar/
│   ├── asosiy.txt
│   ├── ishlab_chiqarish.txt
│   └── sinov.txt
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── skriptlar/
│   ├── ozgartirish.sh
│   ├── migrate.sh
│   └── zaxiralash.sh
│
├── .env.misol
├── .gitignore
└── README.md