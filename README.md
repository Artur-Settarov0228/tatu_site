# tatu_site
```
nb_monitoring/
├── manage.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── .env
├── config/                      # project config (settings)
│   ├── __init__.py
│   ├── asgi.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── celery.py
│   └── settings/
│       ├── __init__.py
│       ├── base.py
│       ├── dev.py
│       └── prod.py
│
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── managers.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   ├── permissions.py
│   │   └── admin.py
│   │
│   ├── students/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   └── admin.py
│   │
│   ├── attendance/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── services.py
│   │   ├── selectors.py
│   │   └── admin.py
│   │
│   ├── notifications/
│   │   ├── models.py
│   │   ├── services.py
│   │   ├── tasks.py
│   │   └── telegram.py
│   │
│   └── common/
│       ├── models.py
│       ├── utils.py
│       ├── constants.py
│       └── mixins.py
│
├── templates/
│   ├── base/
│   │   ├── base.html
│   │   ├── navbar.html
│   │   └── sidebar.html
│   │
│   ├── auth/
│   │   └── login.html
│   │
│   ├── dashboard/
│   │   └── dashboard.html
│   │
│   ├── students/
│   │   ├── list.html
│   │   ├── create.html
│   │   └── edit.html
│   │
│   └── attendance/
│       └── mark.html
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── bot/
│   ├── main.py
│   ├── handlers/
│   ├── keyboards/
│   ├── services/
│   └── states/
│
└── docker/
    ├── Dockerfile
    └── docker-compose.yml
# 🎯 VAZIFA

Men universitet talabalarining dars qoldirishini (NB) nazorat qiluvchi to‘liq tizim yaratmoqchiman.

Tizim quyidagilardan iborat bo‘lsin:

1. Django + Django REST Framework (backend)
2. PostgreSQL (database)
3. Telegram bot (faqat ota-onalar uchun)
4. Django Template asosida zamonaviy admin panel (frontend)
5. Celery + Redis (background tasks)
6. JWT + Session auth (web uchun)
7. Role-based access control (ADMIN, TEACHER, PARENT)

---

# 🔐 AUTH VA LOGIN SYSTEM

## Web uchun:

* Login sahifa:

  * username / phone
  * password
* Logout
* Session-based auth
* Admin va Teacher login qiladi

## UI:

* Zamonaviy dizayn (Bootstrap / Tailwind)
* Dark/light variant (optional)

---

# 🧑‍🎓 TALABALAR PANELI (ADMIN PANEL)

Login bo‘lgandan keyin:

## 📋 Student List Page

* Table ko‘rinish:

  * F.I.Sh
  * Guruh
  * Kurs
  * Yo‘nalish
  * NB soni
* Search
* Filter:

  * group
  * course

## ➕ Student Create

Forma:

* ism
* familya
* group
* kurs
* yo‘nalish
* telefon

## ✏️ Student Edit

* update qilish
* delete (soft delete)

---

# 📅 ATTENDANCE PANEL

## Sahifa:

* Student tanlash
* Sana
* Subject
* Status:

  * PRESENT
  * ABSENT
* Reason:

  * kasal
  * sababsiz
  * ruxsat bilan

## UI:

* tez belgilash (checkbox list)
* bulk submit

---

# 🔔 NOTIFICATION LOGIC

* 2 NB → warning
* 3 NB → parent alert
* ketma-ket NB → alert

Telegram orqali yuborilsin.

---

# 🤖 TELEGRAM BOT (FAKAT OTA-ONA UCHUN)

## Flow:

1. /start
2. telefon yuborish
3. tasdiqlash
4. farzandini tanlash

## Feature:

* 📊 NB statistikasi
* 📅 oxirgi darslar
* ⚠️ ogohlantirishlar

---

# 🧠 DATABASE MODELLAR

Quyidagilarni yoz:

* Custom User:

  * role (ADMIN, TEACHER, PARENT)

* Student

* Group

* Teacher

* Parent

* ParentStudent

* Attendance:

  * status
  * reason
  * date
  * subject

* Schedule

* AuditLog

Har biri uchun:

* fieldlar
* FK va M2M
* indexlar
* unique constraint
* best practice

---

# ⚙️ DJANGO STRUCTURE (CLEAN ARCHITECTURE)

Project structure:

* apps/

  * users/
  * students/
  * attendance/
  * notifications/
  * common/

Har bir app:

* models.py
* serializers.py
* views.py
* urls.py
* services.py
* selectors.py

---

# 🔌 API (DRF)

Yozib ber:

## Student

* CRUD
* pagination
* filtering

## Attendance

* create
* bulk create
* history

## Analytics

* top NB studentlar
* group stats

---

# 🎨 FRONTEND (DJANGO TEMPLATE)

Quyidagilarni to‘liq yoz:

## Layout

* sidebar
* navbar
* dashboard

## Pages:

1. Login page (chiroyli UI)
2. Dashboard
3. Student list
4. Student create/edit
5. Attendance page

## UX:

* responsive design
* table + pagination
* alert messages

---

# ⚡ CELERY + REDIS

Tasks:

* notification send
* report generate

Retry mechanism yoz

---

# 📊 ANALYTICS

* eng ko‘p NB qilganlar
* trend (hafta/oy)
* group kesimida

---

# 🧠 ADVANCED

* risk score:

  * NB soni
  * ketma-ket NB

* QR attendance (optional)

---

# 🚀 TALABLAR

* production-ready kod
* clean architecture
* service layer
* validation
* error handling
* logging

---

# 🧭 JAVOB FORMAT

Bosqichma-bosqich chiqar:

1. Database schema
2. Django models
3. DRF serializers
4. Views + API
5. Template (HTML + CSS)
6. Telegram bot
7. Celery setup

Har bir qismni alohida yoz va tushuntir.

---
