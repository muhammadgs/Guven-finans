# Güvən Finans statik ön üz

Bu repo daxilindəki əvvəlki Django + Tailwind şablonları tamamilə HTML, CSS və Vanilla JS ilə əvəz olundu. Bütün səhifələr `frontend/` qovluğunda yerləşir və birbaşa statik serverlə açılır.

## Strukturu
- `frontend/index.html`: Ana səhifə (hero, statistika, xidmətlər, layihə karuseli, partnyorlar, konsultasiya formu)
- `frontend/login.html`: Giriş formu və token yoxlama düymələri
- `frontend/register-choice.html`: Qeydiyyat növü seçimi
- `frontend/owner-register.html`, `frontend/worker-register.html`, `frontend/isci-form.html`: Şirkət sahibi/işçi qeydiyyatı formaları
- `frontend/owner-dashboard.html`, `frontend/worker-dashboard.html`: Qorunan panel səhifələri, `Auth.getMe()` cavabı ilə yüklənir
- `frontend/owner-thanks.html`, `frontend/worker-thanks.html`: Uğurlu müraciət ekranları
- `frontend/assets/styles.css`: Tailwind-siz stil faylı
- `frontend/assets/scripts/api.js`: `BASE_URL` və `API.request` sarmalayıcısı (placeholder)
- `frontend/assets/scripts/auth.js`: `login`, `logout`, `getMe` və token idarəetməsi (localStorage)
- `frontend/assets/scripts/main.js`: Header/footer enjeksiyası, loader, smooth scroll, karusel və form davranışları

## İşə salınması
Statik serverdən açmaq kifayətdir:

```bash
cd frontend
python -m http.server 8000
```

və ya VS Code “Live Server” kimi istənilən statik server pluginindən istifadə edin.

## API konfiqurasiyası
`frontend/assets/scripts/api.js` içindəki `BASE_URL` dəyişəni placeholder olaraq `https://api.example.com` dəyərinə sahibdir. Öz API ünvanınızı burada dəyişdirin.

## Autentifikasiya və qorunan səhifələr
- Token localStorage-da `access_token` açarı ilə saxlanılır və yalnız `auth.js` bu idarəni edir.
- Panel səhifələrində (`owner-dashboard.html`, `worker-dashboard.html`) səhifə yüklənən kimi `Auth.getMe()` çağırılır; uğursuz olduqda avtomatik `login.html` ünvanına yönləndirilir.

## Vacib qeydlər
- Django templating, Tailwind və digər framework izləri silinib.
- Heç bir binary fayl əlavə/dəyişdirilməyib; mövcud şəkillər `financeApp/staticfiles/images/` içindən istinad edilir.
- HTML fayllarında bütün daxili linklər statik `.html` ünvanlarına yenilənib.
