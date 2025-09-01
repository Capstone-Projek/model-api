
# REST API Model

Ini adalah repository pengembangan REST API untuk model machine learning klasifikasi 10 makanan khas daerah Bangka Belitung. Ini adalah project Capstone Program BEKUP Create dari Tim Capstone B25-PG003.
## Instalasi Project

Berikut adalah cara untuk melakukan instalasi dan menjalankan REST API model.

### Install library yang diperlukan
Install library yang diperlukan menggunakan Python via terminal atau command prompt
```bash
  pip install django djangorestframework tensorflow numpy Pillow
```

### Jalankan REST API
Jalankan kode di bawah untuk menjalankan server REST API. Endpoint untuk melakukan testing yaitu menggunakan POST request ke BASE_URL/api/classify/ dengan mengirimkan image di body request.
```bash
  cd model-api/
  python manage.py runserver
```