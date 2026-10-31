# ALES Akademi

Tamamen Türkçe, çevrim dışı çalışan dijital ALES hazırlık platformu. `index.html` dosyasını tarayıcıda açmanız yeterlidir.

- `docs/01-arastirma-raporu.md` — ÖSYM kaynak araştırması ve soru yapısı analizi
- `docs/02-mufredat.md` — 18 konu, alt başlıklar ve kazanımlar
- `docs/03-calisma-programlari.md` — 30/60/90/120 günlük programların mantığı
- `docs/04-soru-bankasi.md` — 627 özgün soru, doğrulama yöntemi ve sınırlar
- `docs/05-teknik-aciklama.md` — mimari, veri yapısı, test raporu

Yeniden derleme: `python3 tools/build_questions.py && python3 tools/build_docs.py && python3 tools/build.py`
