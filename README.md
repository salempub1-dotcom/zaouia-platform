# منصة الزاوية البلقائدية الهبرية

منصة Django موحدة للدروس والمحاضرات والصوتيات والمرئيات والكتب وPDF، بواجهة عربية RTL وREST API جاهزة لتطبيق Flutter مستقبلًا.

## تشغيل سريع

```bash
cp .env.example .env
docker compose up --build -d
docker compose exec web python manage.py createsuperuser
```

- الواجهة: http://localhost:8000/
- الإدارة: http://localhost:8000/admin/
- API: http://localhost:8000/api/v1/contents/
- التوثيق: http://localhost:8000/api/docs/

## التطوير بدون Docker

اترك `DATABASE_URL` غير معرّف لاستخدام SQLite للاختبار المحلي، وثبّت `requirements/dev.txt` ثم نفّذ:

```bash
python manage.py migrate
python manage.py runserver
```

الواجهة Mobile-first وتدعم البحث والفلاتر، صفحات التفاصيل، YouTube، الصوت والفيديو، مكتبة PDF، المشايخ، المفضلة، السجل، الإشعارات وPWA أساسي.
