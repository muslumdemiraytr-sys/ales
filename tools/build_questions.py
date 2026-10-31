"""Soru bankasını üretir, doğrular ve data/questions.json dosyasına yazar.

Kullanım:  python3 tools/build_questions.py
Sabit tohum (SEED) kullanıldığından her çalıştırmada aynı banka üretilir.
"""
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
import qgen_say  # noqa: E402
import qgen_logic  # noqa: E402
import soz_manual  # noqa: E402
from qcommon import SRC  # noqa: E402

SEED = 20261031
TARGET = 36            # şablonlu konular için hedef soru sayısı
GROUP_TARGET = 33      # ortak bilgi grubu konuları için hedef
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PREFIX = {"temel": "TEM", "bolunebilme": "BOL", "rasyonel": "RAS", "esitsizlik": "ESI", "uslu": "USL", "cebir": "CEB",
          "oran": "ORN", "problem": "PRB", "islem": "ISL", "sayma": "SAY", "veri": "VER", "saymantik": "SML", "geometri": "GEO",
          "sozcuk": "SOZ", "cumle": "CUM", "yapi": "YAP", "paragraf": "PAR", "sozmantik": "SZM"}


def key(q):
    return re.sub(r"\s+", " ", (q.get("group") or {}).get("info", "")[:80] + q["q"])


def build():
    rng = random.Random(SEED)
    bank = defaultdict(list)
    seen = set()

    def add(q):
        k = key(q)
        if k in seen:
            return False
        seen.add(k)
        bank[q["topic"]].append(q)
        return True

    # 1) Tekil sayısal şablonlar (konu içinde şablonlar sırayla döner → çeşitlilik)
    for topic, temps in qgen_say.TEMPLATES.items():
        goal = 22 if topic == "saymantik" else TARGET
        tries = 0
        while len(bank[topic]) < goal and tries < 6000:
            t = temps[tries % len(temps)]
            tries += 1
            try:
                q = t(rng)
            except (ZeroDivisionError, AssertionError, IndexError, ValueError, StopIteration):
                q = None
            if q:
                add(q)
    # 2) Ortak bilgi grupları (sayısal)
    gidn = 0
    for topic, gens in qgen_say.GROUPS.items():
        goal = GROUP_TARGET if topic == "veri" else len(bank[topic]) + 14
        tries = 0
        while len(bank[topic]) < goal and tries < 400:
            g = gens[tries % len(gens)]
            tries += 1
            gidn += 1
            try:
                qs = g(rng, f"g{gidn}")
            except (ZeroDivisionError, AssertionError, IndexError, ValueError, StopIteration):
                qs = None
            if qs:
                for q in qs:
                    add(q)
    # 3) Sözel mantık grupları
    tries = 0
    while len(bank["sozmantik"]) < 36 and tries < 600:
        g = qgen_logic.GROUPS[tries % len(qgen_logic.GROUPS)]
        tries += 1
        gidn += 1
        try:
            qs = g(rng, f"g{gidn}")
        except (AssertionError, IndexError, ValueError):
            qs = None
        if qs:
            for q in qs:
                add(q)
    # 4) Elle yazılmış sözel sorular
    for it in soz_manual.ITEMS:
        opts = it["wrongs"] + [it["correct"]]
        rng.shuffle(opts)
        q = dict(area="soz", topic=it["topic"], sub=it["sub"], level=it["level"], q=it["q"], opts=opts, a=opts.index(it["correct"]),
                 sol=it["sol"], kaz=it["kaz"], sure=it["sure"], src=SRC)
        if it["group"]:
            q["group"] = it["group"]
        assert add(q), it["q"][:60]

    # Kimlik ver, doğrula
    out = []
    problems = []
    for topic, qs in bank.items():
        for n, q in enumerate(qs, 1):
            q["id"] = f"{q['area'].upper()}-{PREFIX[topic]}-{n:03d}"
            if q["sub"] == "Koşullu çıkarım" and q["area"] == "soz":
                q["level"] = 5  # ek koşullu sözel mantık: İleri
            if len(q["opts"]) != 5 or len(set(q["opts"])) != 5:
                problems.append((q["id"], "seçenekler"))
            if not 0 <= q["a"] < 5:
                problems.append((q["id"], "cevap indeksi"))
            if not q["sol"]:
                problems.append((q["id"], "çözüm yok"))
            # Çapraz kontrol: sayısal sorularda anahtarlanan seçenek çözümde geçmeli
            if q["area"] == "say":
                ans = re.sub(r"<[^>]+>", "", q["opts"][q["a"]]).replace("%", "").strip()
                soltxt = re.sub(r"<[^>]+>", "", " ".join(q["sol"])).replace("-", "−")
                if ans not in soltxt:
                    problems.append((q["id"], f"anahtar '{ans}' çözümde yok"))
            out.append(q)
    return out, problems


def main():
    qs, problems = build()
    for p in problems:
        print("SORUN:", *p)
    by_topic = Counter(q["topic"] for q in qs)
    by_level = Counter(q["level"] for q in qs)
    by_ans = Counter("ABCDE"[q["a"]] for q in qs)
    print("Toplam:", len(qs))
    print("Konu:", dict(by_topic))
    print("Seviye:", dict(sorted(by_level.items())))
    print("Cevap dağılımı:", dict(sorted(by_ans.items())))
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    meta = {"version": "1.0.0", "seed": SEED, "generated": "2026-10-31", "count": len(qs),
            "note": "Tüm sorular özgündür (ALES Akademi). ÖSYM sorusu içermez."}
    with open(os.path.join(ROOT, "data", "questions.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta, "questions": qs}, f, ensure_ascii=False, indent=1)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
