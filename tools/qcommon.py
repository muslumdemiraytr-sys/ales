"""Soru üretimi için ortak yardımcılar.

Her soru sözlüğü şu alanlara sahiptir:
  id, area (say|soz), topic, sub, level (1-5), q (HTML), opts (5), a (0-4),
  sol (adım listesi), kaz (kazanım), sure (sn), src, [group]
"""
from fractions import Fraction as F

SRC = "Özgün – ALES Akademi"
LETTERS = "ABCDE"


def frs(x):
    """Kesri uygulamanın ⟦a/b⟧ belirtecine çevirir (uygulama alt alta kesir çizer)."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    sign = "−" if x < 0 else ""
    return f"{sign}⟦{abs(x.numerator)}/{x.denominator}⟧"


def dec(x, nd=None):
    """Ondalık sayıyı Türkçe virgülle yazar."""
    if isinstance(x, F):
        if x.denominator == 1:
            return str(x.numerator)
        x = float(x)
    s = f"{x:.{nd}f}" if nd is not None else repr(round(x, 6))
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",").replace("-", "−")


def num(x):
    if isinstance(x, F):
        return frs(x)
    if isinstance(x, int):
        return str(x).replace("-", "−")
    return dec(x)


def num_opts(ans, rng, step=1, fmt=num, minv=None, extra=(), maxv=None):
    """ÖSYM düzeninde (küçükten büyüğe) beş sayısal seçenek üretir."""
    extra = [e for e in extra if e != ans]
    pool = set(extra)
    for k in range(1, 8):
        pool.add(ans + k * step)
        pool.add(ans - k * step)
    if minv is not None:
        pool = {v for v in pool if v >= minv}
    if maxv is not None:
        pool = {v for v in pool if v <= maxv}
    pool.discard(ans)
    below = [v for v in pool if v < ans]
    above = [v for v in pool if v > ans]

    def pick(lst, n):
        ex = [v for v in lst if v in extra]
        rest = sorted([v for v in lst if v not in extra], key=lambda v: abs(v - ans))[: max(n + 2, 4)]
        rng.shuffle(ex)
        rng.shuffle(rest)
        out = []
        for v in ex + rest:
            if v not in out:
                out.append(v)
        return out[:n]

    p = rng.randint(0, 4)
    p = min(p, len(below))
    if 4 - p > len(above):
        p = 4 - len(above)
    chosen = pick(below, p) + pick(above, 4 - p)
    vals = sorted(chosen + [ans])
    shown = [fmt(v) for v in vals]
    assert len(vals) == 5 and len(set(shown)) == 5, (ans, vals)
    return shown, vals.index(ans)


def text_opts(correct, wrongs, rng):
    wrongs = [w for w in wrongs if w != correct]
    assert len(set(wrongs)) >= 4, (correct, wrongs)
    seen = []
    for w in wrongs:
        if w not in seen:
            seen.append(w)
    opts = seen[:4] + [correct]
    rng.shuffle(opts)
    return opts, opts.index(correct)


_UNITS = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
_TENS = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]
_HARD = "fstkçşhp"


def _last_word(n):
    n = abs(int(n))
    if n == 0:
        return "sıfır"
    if n % 10:
        return _UNITS[n % 10]
    if n % 100:
        return _TENS[n % 100 // 10]
    if n % 1000:
        return "yüz"
    if n % 1000000:
        return "bin"
    return "milyon"


def nsuf(n, kind):
    """Sayılara Türkçe ek: nsuf(9,'dat') → 9'a, nsuf(30,'cop') → 30'dur, nsuf(5,'gen') → 5'in."""
    w = _last_word(n)
    lv = [ch for ch in w if ch in "aeıioöuü"][-1]
    two = "a" if lv in "aıou" else "e"
    four = {"a": "ı", "ı": "ı", "o": "u", "u": "u", "e": "i", "i": "i", "ö": "ü", "ü": "ü"}[lv]
    vow_end = w[-1] in "aeıioöuü"
    hard = w[-1] in _HARD
    s = str(n).replace("-", "−")
    if kind == "dat":
        return f"{s}'{'y' if vow_end else ''}{two}"
    if kind == "cop":
        return f"{s}'{'t' if hard else 'd'}{four}r"
    if kind == "abl":
        return f"{s}'{'t' if hard else 'd'}{two}n"
    if kind == "loc":
        return f"{s}'{'t' if hard else 'd'}{two}"
    if kind == "gen":
        return f"{s}'{'n' if vow_end else ''}{four}n"
    if kind == "er":   # üleştirme: 3'er, 6'şar
        return f"{s}'{'ş' if vow_end else ''}{two}r"
    raise ValueError(kind)


def _fix_minus(s):
    """Etiket dışındaki metinde sayı önündeki '-' işaretini '−' yapar ve '− -' gibi çift işaretleri düzeltir."""
    import re
    parts = re.split(r"(<[^>]+>)", s)
    for i, p in enumerate(parts):
        if p.startswith("<"):
            continue
        p = re.sub(r"(?<![\w])-(?=\d)", "−", p)
        p = p.replace("− −", "+ ").replace("+ −", "− ").replace("(+ ", "(")
        parts[i] = p
    return "".join(parts)


def Q(topic, sub, level, q, opts, a, sol, kaz, sure, area="say", group=None):
    assert len(opts) == 5 and 0 <= a < 5
    assert len(set(opts)) == 5, opts
    q = _fix_minus(q)
    opts = [_fix_minus(o) for o in opts]
    sol = [_fix_minus(x) for x in sol]
    d = dict(area=area, topic=topic, sub=sub, level=level, q=q, opts=opts, a=a,
             sol=sol, kaz=kaz, sure=sure, src=SRC)
    if group:
        d["group"] = group
    return d
