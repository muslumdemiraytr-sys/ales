# ALES Akademi — Aşama 3: Çalışma Programları

Programlar uygulamada (`src/program.js`) kullanıcının seçimlerine göre üretilir: **süre** (30 / 60 / 90 / 120 gün), **başlangıç seviyesi** (Başlangıç / Orta / İleri), **hedef puan türü** (SAY / SÖZ / EA), **günlük dakika** ve **başlangıç tarihi**.

## Üç aşama

| Aşama | Sayısal | Sözel | Hedef |
|---|---|---|---|
| 1. Temel Oluşturma | Temel kavramlar, bölünebilme ve faktöriyel, rasyonel sayılar, eşitsizlik ve mutlak değer, üslü-köklü, çarpanlara ayırma ve denklemler, oran-orantı | Sözcükte anlam, cümlede anlam, paragrafta anlam, paragraf yapısı | Temel konuları öğrenmek, düzenli soru çözme alışkanlığı |
| 2. Gelişim | Problemler, işlem ve modüler aritmetik, permütasyon-kombinasyon-olasılık, tablo-grafik, sayısal mantık, geometri | İleri paragraf, paragraf yapısı, sözel mantık | Orta ve zor soruları çözebilmek |
| 3. Sınav Simülasyonu | Haftada 2–3 tam deneme, karma soru, zayıf konu tekrarı, hız, yanlış analizi, ileri mantık | | Sınav performansı |

## Aşama süreleri (gün)

Oranlar seviyeye göre değişir: Başlangıç 40/35/25, Orta 33/34/33, İleri 25/35/40. 30 günlük yoğun programda simülasyon aşaması en az %30'dur.

| Program | Başlangıç seviyesi | Orta | İleri |
|---|---|---|---|
| 30 gün (yoğun) | 11 / 10 / 9 | 10 / 10 / 10 | 8 / 11 / 11 |
| 60 gün | 24 / 21 / 15 | 20 / 20 / 20 | 15 / 21 / 24 |
| 90 gün | 36 / 31 / 23 | 30 / 31 / 29 | 23 / 31 / 36 |
| 120 gün | 48 / 42 / 30 | 40 / 41 / 39 | 30 / 42 / 48 |

Simülasyon aşamasında haftalık tam deneme sayısı: 60 ve 90 günlük programlarda 3, 30 ve 120 günlük programlarda 2.

## Günlük plan

Örnek 3 saatlik (180 dk) gün: 60 dk sayısal konu + soru · 45 dk sözel konu + soru · 35 dk mantık ve problem · 20 dk yanlış analizi · 20 dk tekrar. Günlük süre değiştirildiğinde aynı oranlar 5 dakikaya yuvarlanarak ölçeklenir. Hedef SAY ise sayısal pay +10, sözel −10 oran puanı; SÖZ ise tersi; EA'da eşit kalır.

Her 7. gün (1. ve 2. aşamada) **tekrar günüdür**: haftalık tekrar, yanlış analizi ve mini deneme.

## Görev mantığı

- Program varsa günün görevleri, o güne ilk girildiğinde programdan oluşturulur ve işaretlenebilir.
- Tamamlanmayan görevler ertesi güne tek tek ("Yarına") ya da toplu olarak ("Bugüne aktar") taşınabilir; taşınan görev, nereden geldiğini gösteren bir etiket taşır.
- Kullanıcı kendi görevlerini ekleyebilir; program düzenlendiğinde yalnızca henüz başlanmamış gelecek günler yeniden oluşturulur.
