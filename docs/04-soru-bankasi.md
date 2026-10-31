# ALES Akademi — Aşama 4: Soru Bankası

Toplam **627** özgün soru. Veri dosyası: `data/questions.json` (uygulamaya `index.html` içinde gömülüdür).

## Özgünlük ve doğrulama politikası

- Hiçbir ÖSYM sorusu kopyalanmamıştır. ÖSYM örnek kitapçıkları yalnızca soru **tipini** ve blok yapısını anlamak için incelenmiştir.
- **Sayısal sorular** (`tools/qgen_say.py`) parametrik şablonlardan üretilir; cevap Python ile hesaplanır (çoğunda tüm durumlar kaba kuvvetle denenir), seçenekler ÖSYM düzeninde küçükten büyüğe sıralanır. Derleyici her soruda anahtarlanan seçeneğin çözüm metninde geçtiğini ve beş seçeneğin birbirinden farklı olduğunu denetler.
- **Sözel mantık** (`tools/qgen_logic.py`) kısıtlardan üretilir; her sorunun tek doğru cevabı tüm olası çözümler üzerinde kaba kuvvetle doğrulanır.
- **Sözcük, cümle, paragraf yapısı ve paragraf** soruları (`tools/soz_manual.py`) elle yazılmıştır; her birinde doğru cevabın gerekçesi ve çeldiricilerin neden yanlış olduğu çözümde açıklanır.
- Sabit tohum (`SEED`) kullanıldığı için banka her derlemede aynı üretilir.

## Soru şeması

| Alan | Açıklama |
|---|---|
| `id` | Benzersiz kimlik, ör. `SAY-PRB-012` |
| `area` | `say` / `soz` |
| `topic`, `sub` | Konu ve alt konu |
| `level` | 1 Başlangıç · 2 Kolay · 3 Orta · 4 Zor · 5 İleri |
| `q`, `opts`, `a` | Soru (HTML), beş seçenek, doğru seçenek indeksi |
| `sol` | Adım adım çözüm |
| `kaz` | Ölçülen kazanım |
| `sure` | Önerilen çözüm süresi (sn) |
| `src` | Kaynak: `Özgün – ALES Akademi` |
| `group` | (varsa) ortak bilgi: `{id, info}` |

## Dağılım

| Konu | Soru | Başlangıç | Kolay | Orta | Zor | İleri |
|---|---:|---:|---:|---:|---:|---:|
| Temel Kavramlar ve Sayılar | 36 | 0 | 12 | 19 | 5 | 0 |
| Bölme, Bölünebilme ve Faktöriyel | 36 | 0 | 20 | 16 | 0 | 0 |
| Rasyonel ve Ondalık Sayılar | 36 | 0 | 17 | 19 | 0 | 0 |
| Eşitsizlikler ve Mutlak Değer | 36 | 0 | 9 | 22 | 5 | 0 |
| Üslü ve Köklü Sayılar | 36 | 0 | 26 | 10 | 0 | 0 |
| Çarpanlara Ayırma ve Denklemler | 36 | 1 | 35 | 0 | 0 | 0 |
| Oran ve Orantı | 36 | 18 | 10 | 8 | 0 | 0 |
| Problemler | 36 | 0 | 22 | 14 | 0 | 0 |
| İşlem, Fonksiyon ve Modüler Aritmetik | 36 | 11 | 13 | 12 | 0 | 0 |
| Permütasyon, Kombinasyon ve Olasılık | 36 | 3 | 8 | 25 | 0 | 0 |
| Sayısal Mantık | 35 | 0 | 26 | 9 | 0 | 0 |
| Geometri | 36 | 11 | 24 | 1 | 0 | 0 |
| Tablo ve Grafik Yorumlama | 33 | 16 | 9 | 8 | 0 | 0 |
| Sözel Mantık | 37 | 0 | 0 | 26 | 0 | 11 |
| Sözcükte Anlam ve Boşluk Doldurma | 30 | 3 | 18 | 8 | 1 | 0 |
| Cümlede Anlam ve Kesin Çıkarım | 32 | 9 | 12 | 9 | 2 | 0 |
| Paragraf Yapısı: Sıralama, Bütünlük, Tamamlama | 32 | 0 | 9 | 20 | 3 | 0 |
| Paragrafta Anlam | 32 | 0 | 16 | 13 | 3 | 0 |
| **Toplam** | **627** | 72 | 286 | 239 | 19 | 11 |

Cevap anahtarı dağılımı: A: 125, B: 130, C: 122, D: 127, E: 123

## Bilinen sınırlar

- Hedef 'her ana konu için en az 30 soru' idi; 18 konunun tamamı bu hedefi karşılar (en az: sözcükte anlam 30, sözel 1.1 sürümünde cümle, paragraf yapısı ve paragraf 32'ye çıkarıldı).
- Zor (4) ve İleri (5) seviyedeki soru sayısı azdır; konu testlerinde 'Zor seviye' havuzu yetersizse yakın seviyeyle tamamlanır ve bu durum arayüzde yazılır.
- Sözel havuz, birbirini tekrar etmeyen yaklaşık iki tam denemeye yeter; sonrasında denemeler daha önce görülen soruları da kullanır.
- Geometri soruları şekilsiz, metinle tanımlanmıştır.

## Genişletme

Yeni soru eklemek için `tools/soz_manual.py` içine `M(...)` öğesi ya da `tools/qgen_say.py` içine yeni bir şablon ekleyip `python3 tools/build_questions.py && python3 tools/build.py` çalıştırın. Şema, binlerce soruya ve ileride bir veritabanı tablosuna doğrudan taşınabilir.