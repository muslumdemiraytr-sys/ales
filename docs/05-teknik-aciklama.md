# ALES Akademi — Teknik Açıklama ve Test Raporu

## Çalıştırma

`index.html` tek başına çalışır: çift tıklayarak açılabilir, internet ya da sunucu gerektirmez (harici kütüphane, yazı tipi veya CDN kullanılmaz).

Kaynaktan yeniden derlemek için:

```bash
python3 tools/build_questions.py && python3 tools/build_docs.py && python3 tools/build.py
```

## Dosya yapısı

| Yol | İçerik |
|---|---|
| `index.html` | Derlenmiş, bağımsız uygulama (~620 KB) |
| `src/style.css` | Tasarım: açık/koyu tema belirteçleri, mobil öncelikli düzen |
| `src/lessons.js` | 18 konunun anlatımları ve deneme blok şablonu |
| `src/core.js` | Veri katmanı (localStorage), istatistik, soru gösterimi, SVG grafikler |
| `src/engine.js` | Alıştırma oturumu ve sınav motoru (deneme, konu testi, zamanlı test) |
| `src/program.js` | Çalışma programı üretimi ve günlük görevler |
| `src/logic.js` | Mantık Atölyesi (tablo kurma bulmacası, sayı ve şekil örüntüleri) |
| `src/views.js` | Sayfalar ve hash tabanlı yönlendirme |
| `data/questions.json` | Soru bankası (JSON) |
| `tools/` | Soru üreticileri, doğrulayıcı ve derleyici |
| `docs/` | Araştırma raporu, müfredat, programlar, soru bankası, teknik açıklama |

## Veri katmanı

Tüm kullanıcı verisi `localStorage["alesakademi.v1"]` altında tek bir belgede tutulur: `profile`, `theme`, `att` (soru başına deneme kayıtları: zaman, seçim, doğru/yanlış, süre, kaynak), `wrong` (akıllı tekrar kutusu), `fav`, `mark`, `lessons`, `tasks`, `exams`, `active` (süren sınav), `days` (günlük etkinlik), `xp`. Yapı kullanıcı başına bir belge olduğu için ileride bir sunucu API'sine (`GET/PUT /users/:id/state`) ya da tablolara (`attempts`, `exams`, `tasks`) doğrudan taşınabilir. Ayarlar sayfasından JSON yedeği alınıp geri yüklenebilir.

**Akıllı tekrar:** Yanlış cevaplanan soru kutu 0'a girer ve 1 gün sonra tekrar edilmeye hazır olur; her doğru çözümde kutu ilerler (1 → 3 → 7 → 14 gün); 3 doğru sonrası "düzeltildi" sayılır. Zayıf konu sıralaması, en az 5 çözüm olan konularda (doğru+1)/(çözüm+2) puanına göre yapılır; veri yoksa öneri üretilmez.

**Sınav motoru:** Süren sınav her işlemde kaydedilir; sayfa yenilense de kaldığı yerden sürer, süre bitiş zamanına göre işler. Süre dolunca (sayfa açıkken ya da açıldığında) otomatik teslim edilir. Sınav sırasında çözüm gösterilmez.

## Test raporu (31.10.2026, uygulama içi tarayıcı)

| Kontrol | Sonuç |
|---|---|
| 23 sayfanın açılması, konsol hatası | Hepsi hatasız |
| Soru cevaplama, kontrol, çözüm, favori, yanlış kaydı | Doğru |
| Net hesabı (3D 2Y → 2,5 net), puan hesaplayıcı doğrulaması (D+Y>50 uyarısı) | Doğru |
| Tam deneme 50+50 benzersiz soru, blok sırası; mini deneme 20+20 | Doğru |
| Geri sayım, soru haritası, işaretleme, bitirme onayı | Doğru |
| Süre sonunda otomatik teslim (açık sayfada ve sayfa açılışında) | Doğru |
| Yenileme sonrası ilerleme ve süren sınavın korunması | Doğru |
| Konu testlerinin sonuçlarının konuya kaydı | Doğru |
| Mantık bulmacası: 6 tür/seviyede tek çözüm; ipucu zinciriyle tam çözüm | Doğru |
| Performans grafikleri (7 SVG grafik, ısı haritası, ipuçları) | Doğru |
| 375 px genişlikte 16 sayfada yatay taşma | Taşma yok |
| Açık/koyu tema | Çalışıyor |

Test edilmeyenler: gerçek cihazlarda (iOS Safari, Android Chrome) deneme; ekran okuyucu ile tam erişilebilirlik denetimi; çok büyük veri birikiminde (binlerce çözüm) performans.

## Sonraki geliştirme aşamaları

1. Üyelik ve sunucu tarafı veri saklama (veri katmanı tek belge olduğu için `Store.load/save` yerine API çağrısı yeterlidir).
2. Yönetim paneli: soru ekleme/düzenleme, soru başına istatistik (zorluk kalibrasyonu, çeldirici analizi).
3. Sözel soru havuzunun ve zor/ileri seviye soruların uzman yazarlarla genişletilmesi; geometri için şekilli sorular.
4. 2021–2024 ve 2025-ALES/2 örnek kitapçıklarının incelenmesiyle araştırma raporunun genişletilmesi.
