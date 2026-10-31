"""Müfredat (02) ve soru bankası (04) dokümanlarını kaynak verilerden üretir."""
import json, os, re
from collections import Counter, defaultdict
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
js = open(os.path.join(ROOT, "src", "lessons.js"), encoding="utf-8").read()
blocks = re.split(r"\n  \{\n    id: ", js)[1:]
LV = ["", "Başlangıç", "Kolay", "Orta", "Zor", "İleri"]
def arr(b, key):
    m = re.search(key + r': (\[.*?\]),\n', b, re.S)
    return json.loads(m.group(1)) if m else []
def s(b, key):
    m = re.search(key + r': "(.*?)",', b)
    return m.group(1) if m else ""
lessons = []
for b in blocks:
    lessons.append(dict(id=re.match(r'"(\w+)"', b).group(1), area=s(b, "area"), phase=re.search(r"phase: (\d)", b).group(1),
                        title=s(b, "title"), group=s(b, "group"), subs=arr(b, "subs"), kaz=arr(b, "kaz")))
qs = json.load(open(os.path.join(ROOT, "data", "questions.json"), encoding="utf-8"))["questions"]
bt = defaultdict(list)
for q in qs: bt[q["topic"]].append(q)
L = ["# ALES Akademi — Aşama 2: Eğitim Mimarisi ve Müfredat", "", "Bu doküman `src/lessons.js` dosyasından otomatik üretilmiştir. Her konu uygulamada 14 bölümlü yapıda sunulur:",
     "tanım · temel kavramlar · konunun mantığı · ayrıntılı anlatım · formüller · çözümlü örnekler · ALES tarzı uygulamalar · pratik yöntemler · sık hatalar · kolay/orta/zor testler · konu sonu değerlendirmesi · kısa tekrar notları.", "",
     "Konu grupları, kullanıcı tarafından verilen müfredatı esas alır; Sayısal 23–43 bloğu (ortak bilgi grupları) için ayrı bir 'Tablo ve Grafik Yorumlama' konusu, Sözel 13–18 blokları için ayrı bir 'Paragraf Yapısı' konusu, araştırmadaki blok yapısına göre eklenmiştir.", ""]
for area, name in (("say", "Sayısal Yetenek"), ("soz", "Sözel Yetenek")):
    L += [f"## {name}", ""]
    for l in [x for x in lessons if x["area"] == area]:
        n = len(bt[l["id"]]); lv = Counter(q["level"] for q in bt[l["id"]])
        L += [f"### {l['title']}  ({l['group']} · {l['phase']}. aşama)", "", "**Alt başlıklar:** " + ", ".join(l["subs"]), "", "**Kazanımlar:**"] + [f"- {k}" for k in l["kaz"]] + \
             ["", f"**Soru bankası:** {n} soru — " + ", ".join(f"{LV[k]} {v}" for k, v in sorted(lv.items())), ""]
open(os.path.join(ROOT, "docs", "02-mufredat.md"), "w", encoding="utf-8").write("\n".join(L))
title = {l["id"]: l["title"] for l in lessons}
M = ["# ALES Akademi — Aşama 4: Soru Bankası", "", f"Toplam **{len(qs)}** özgün soru. Veri dosyası: `data/questions.json` (uygulamaya `index.html` içinde gömülüdür).", "",
     "## Özgünlük ve doğrulama politikası", "",
     "- Hiçbir ÖSYM sorusu kopyalanmamıştır. ÖSYM örnek kitapçıkları yalnızca soru **tipini** ve blok yapısını anlamak için incelenmiştir.",
     "- **Sayısal sorular** (`tools/qgen_say.py`) parametrik şablonlardan üretilir; cevap Python ile hesaplanır (çoğunda tüm durumlar kaba kuvvetle denenir), seçenekler ÖSYM düzeninde küçükten büyüğe sıralanır. Derleyici her soruda anahtarlanan seçeneğin çözüm metninde geçtiğini ve beş seçeneğin birbirinden farklı olduğunu denetler.",
     "- **Sözel mantık** (`tools/qgen_logic.py`) kısıtlardan üretilir; her sorunun tek doğru cevabı tüm olası çözümler üzerinde kaba kuvvetle doğrulanır.",
     "- **Sözcük, cümle, paragraf yapısı ve paragraf** soruları (`tools/soz_manual.py`) elle yazılmıştır; her birinde doğru cevabın gerekçesi ve çeldiricilerin neden yanlış olduğu çözümde açıklanır.",
     "- Sabit tohum (`SEED`) kullanıldığı için banka her derlemede aynı üretilir.", "",
     "## Soru şeması", "", "| Alan | Açıklama |", "|---|---|",
     "| `id` | Benzersiz kimlik, ör. `SAY-PRB-012` |", "| `area` | `say` / `soz` |", "| `topic`, `sub` | Konu ve alt konu |", "| `level` | 1 Başlangıç · 2 Kolay · 3 Orta · 4 Zor · 5 İleri |",
     "| `q`, `opts`, `a` | Soru (HTML), beş seçenek, doğru seçenek indeksi |", "| `sol` | Adım adım çözüm |", "| `kaz` | Ölçülen kazanım |", "| `sure` | Önerilen çözüm süresi (sn) |", "| `src` | Kaynak: `Özgün – ALES Akademi` |", "| `group` | (varsa) ortak bilgi: `{id, info}` |", "",
     "## Dağılım", "", "| Konu | Soru | " + " | ".join(LV[1:]) + " |", "|---|---:|" + "---:|" * 5]
for t, lst in bt.items():
    c = Counter(q["level"] for q in lst)
    M.append(f"| {title[t]} | {len(lst)} | " + " | ".join(str(c.get(i, 0)) for i in range(1, 6)) + " |")
c = Counter(q["level"] for q in qs); a = Counter("ABCDE"[q["a"]] for q in qs)
M += [f"| **Toplam** | **{len(qs)}** | " + " | ".join(str(c.get(i, 0)) for i in range(1, 6)) + " |", "",
      "Cevap anahtarı dağılımı: " + ", ".join(f"{k}: {v}" for k, v in sorted(a.items())), "",
      "## Bilinen sınırlar", "",
      "- Hedef 'her ana konu için en az 30 soru' idi; 18 konunun tamamı bu hedefi karşılar (en az: sözcükte anlam 30, sözel 1.1 sürümünde cümle, paragraf yapısı ve paragraf 32'ye çıkarıldı).",
      "- Zor (4) ve İleri (5) seviyedeki soru sayısı azdır; konu testlerinde 'Zor seviye' havuzu yetersizse yakın seviyeyle tamamlanır ve bu durum arayüzde yazılır.",
      "- Sözel havuz, birbirini tekrar etmeyen yaklaşık iki tam denemeye yeter; sonrasında denemeler daha önce görülen soruları da kullanır.",
      "- Geometri soruları şekilsiz, metinle tanımlanmıştır.", "",
      "## Genişletme", "", "Yeni soru eklemek için `tools/soz_manual.py` içine `M(...)` öğesi ya da `tools/qgen_say.py` içine yeni bir şablon ekleyip `python3 tools/build_questions.py && python3 tools/build.py` çalıştırın. Şema, binlerce soruya ve ileride bir veritabanı tablosuna doğrudan taşınabilir."]
open(os.path.join(ROOT, "docs", "04-soru-bankasi.md"), "w", encoding="utf-8").write("\n".join(M))
print("ok", len(lessons))
