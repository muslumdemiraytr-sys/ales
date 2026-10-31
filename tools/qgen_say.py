"""Sayısal Testi için parametrik, doğrulanmış özgün soru şablonları.

Her şablon cevabı Python ile hesaplar (çoğu durumda kaba kuvvetle kontrol eder);
çözüm adımları aynı hesaplamadan üretilir.
"""
import itertools
import math
from fractions import Fraction as F

from qcommon import Q, num, num_opts, text_opts, frs, dec, nsuf

PRIMES = [p for p in range(2, 200) if all(p % d for d in range(2, int(p ** .5) + 1))]
NAMES = ["Ali", "Banu", "Cem", "Deniz", "Ece", "Fatih", "Gül", "Hakan", "İpek", "Kaan", "Leyla", "Mert", "Nil", "Onur", "Pelin", "Selin", "Tuna", "Umut", "Yasemin", "Zeynep"]
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

# ---------------------------------------------------------------- TEMEL KAVRAMLAR

PAR_CONDS = [
    ("a·b tek", lambda a, b, c: a * b % 2 == 1),
    ("a + b çift", lambda a, b, c: (a + b) % 2 == 0),
    ("a + b tek", lambda a, b, c: (a + b) % 2 == 1),
    ("b + c tek", lambda a, b, c: (b + c) % 2 == 1),
    ("b·c çift", lambda a, b, c: b * c % 2 == 0),
    ("a + c çift", lambda a, b, c: (a + c) % 2 == 0),
    ("a·c tek", lambda a, b, c: a * c % 2 == 1),
    ("a·b + c tek", lambda a, b, c: (a * b + c) % 2 == 1),
    ("a + b·c çift", lambda a, b, c: (a + b * c) % 2 == 0),
]
PAR_EXPR = [
    ("a + b", lambda a, b, c: a + b), ("a + c", lambda a, b, c: a + c), ("b + c", lambda a, b, c: b + c),
    ("a·c", lambda a, b, c: a * c), ("b·c", lambda a, b, c: b * c), ("a·b", lambda a, b, c: a * b),
    ("a + b + c", lambda a, b, c: a + b + c), ("a² + c", lambda a, b, c: a * a + c),
    ("a·b + c", lambda a, b, c: a * b + c), ("(a + 1)·c", lambda a, b, c: (a + 1) * c),
    ("b² + a·c", lambda a, b, c: b * b + a * c), ("c² + b", lambda a, b, c: c * c + b),
    ("a·b·c + 1", lambda a, b, c: a * b * c + 1), ("2a + c", lambda a, b, c: 2 * a + c),
]


def t_parity(rng):
    conds = rng.sample(PAR_CONDS, 2)
    states = [s for s in itertools.product([0, 1], repeat=3) if all(f(*s) for _, f in conds)]
    if len(states) < 2:
        return None
    want = rng.choice([1, 0])
    word = "tek" if want else "çift"
    always = [e for e in PAR_EXPR if all(e[1](*s) % 2 == want for s in states)]
    notalw = [e for e in PAR_EXPR if not all(e[1](*s) % 2 == want for s in states)]
    if not always or len(notalw) < 4:
        return None
    c = rng.choice(always)
    ws = rng.sample(notalw, 4)
    opts, a = text_opts(c[0], [w[0] for w in ws], rng)
    sts = ", ".join("(" + ", ".join("T" if v else "Ç" for v in s) + ")" for s in states)
    q = (f"a, b ve c birer tam sayı olmak üzere <b>{conds[0][0]}</b> ve <b>{conds[1][0]}</b> olduğu bilinmektedir."
         f"<br>Buna göre aşağıdakilerden hangisi <b>kesinlikle {word}</b> sayıdır?")
    sol = [f"Koşulları sağlayan (a, b, c) tek/çift durumları: {sts} (T: tek, Ç: çift).",
           f"Bu durumların hepsinde yalnızca <b>{c[0]}</b> ifadesi {word} çıkar.",
           "Diğer seçeneklerin her biri en az bir durumda farklı sonuç verir; bu yüzden 'kesinlikle' sağlanmaz."]
    return Q("temel", "Tek ve çift sayılar", 3, q, opts, a, sol, "Tek-çift sayıların işlem özelliklerini kullanarak kesin yargıya ulaşır.", 75)


def t_consec(rng):
    n = rng.choice([4, 5, 6, 7])
    kind = rng.choice(["çift", "tek", "doğal"])
    stp = 1 if kind == "doğal" else 2
    start = rng.randint(5, 40)
    if kind == "çift" and start % 2:
        start += 1
    if kind == "tek" and start % 2 == 0:
        start += 1
    seq = [start + stp * i for i in range(n)]
    S = sum(seq)
    ask = rng.choice(["en büyüğü", "en küçüğü"])
    ans = seq[-1] if ask == "en büyüğü" else seq[0]
    mid = F(S, n)
    q = f"Ardışık {n} {kind} sayının toplamı {nsuf(S, 'cop')}.<br>Buna göre bu sayıların {ask} kaçtır?"
    sol = [f"Ardışık sayılarda ortalama = ortanca: {S} ÷ {n} = {num(mid)}.",
           f"Sayılar {stp} artışla dizilir: {', '.join(map(str, seq))}.",
           f"İstenen {ask}: <b>{ans}</b>."]
    opts, a = num_opts(ans, rng, step=stp, extra=[seq[0] if ans == seq[-1] else seq[-1]], minv=0)
    return Q("temel", "Ardışık sayılar", 2, q, opts, a, sol, "Ardışık sayı dizilerinde ortalama–terim ilişkisini kullanır.", 60)


def t_digits_ab(rng):
    v = rng.choice(["katı", "toplam"])
    if v == "katı":
        k = rng.choice([3, 4, 6, 7, 8])
        sols = [10 * a + b for a in range(1, 10) for b in range(10) if 10 * a + b == k * (a + b)]
        if not sols:
            return None
        q = f"İki basamaklı AB doğal sayısı, rakamları toplamının {k} katına eşittir.<br>Bu koşulu sağlayan AB sayılarının toplamı kaçtır?"
        ans = sum(sols)
        sol = [f"10A + B = {k}(A + B) ⇒ {10 - k}A = {k - 1}B.",
               f"Rakam koşullarını (A ≥ 1, 0 ≤ B ≤ 9) sağlayan sayılar: {', '.join(map(str, sols))}.",
               f"Toplam = <b>{ans}</b>."]
        opts, a = num_opts(ans, rng, step=rng.choice([3, 9, 11]), minv=10, extra=[sols[0]] if len(sols) > 1 else [])
        return Q("temel", "Sayı basamakları", 3, q, opts, a, sol, "Basamak çözümlemesi ile denklem kurar.", 90)
    S = rng.choice([88, 99, 110, 121, 132, 143])
    sols = [10 * a + b for a in range(1, 10) for b in range(1, 10) if a > b and (10 * a + b) + (10 * b + a) == S]
    if not sols:
        return None
    ans = len(sols)
    q = f"Rakamları sıfırdan farklı iki basamaklı AB ve BA sayıları için A &gt; B ve AB + BA = {S} olduğuna göre kaç farklı AB sayısı yazılabilir?"
    sol = [f"AB + BA = 11(A + B) = {S} ⇒ A + B = {S // 11}.",
           f"A &gt; B ve rakamlar 1–9 arasında: {', '.join(map(str, sols))}.",
           f"Toplam <b>{ans}</b> sayı."]
    opts, a = num_opts(ans, rng, minv=1)
    return Q("temel", "Sayı basamakları", 2, q, opts, a, sol, "AB + BA = 11(A + B) özdeşliğini kullanır.", 60)


def t_build_number(rng):
    p, q2 = rng.sample([6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17], 2)
    mode = rng.choice(["en büyük", "en küçük"])
    cand = []
    for n in range(100, 1000):
        A, B, C = n // 100, n // 10 % 10, n % 10
        if len({A, B, C}) < 3:
            continue
        if (10 * A + B) % p == 0 and B != 0 and (10 * B + C) % q2 == 0:
            cand.append(n)
    if len(cand) < 2:
        return None
    n = max(cand) if mode == "en büyük" else min(cand)
    ans = sum(map(int, str(n)))
    q = (f"Rakamları birbirinden farklı üç basamaklı ABC doğal sayısında<br>• iki basamaklı AB sayısı {nsuf(p, 'dat')},<br>"
         f"• iki basamaklı BC sayısı {nsuf(q2, 'dat')}<br>tam bölünebilmektedir.<br>Buna göre {mode} ABC sayısının rakamları toplamı kaçtır?")
    sol = [f"AB, {nsuf(p, 'gen')} iki basamaklı katlarından; BC, {nsuf(q2, 'gen')} iki basamaklı katlarından olmalıdır (B ortak rakam).",
           f"{'Büyükten' if mode == 'en büyük' else 'Küçükten'} başlayarak denendiğinde rakamları farklı ilk uygun sayı <b>{n}</b> bulunur.",
           f"Rakamlar toplamı: {' + '.join(str(n))} = <b>{ans}</b>."]
    opts, a = num_opts(ans, rng, minv=1)
    return Q("temel", "Sayı basamakları", 4, q, opts, a, sol, "Bölünebilme koşullarını birlikte değerlendirerek sayı kurar.", 120)


def t_primes(rng):
    k1, k2 = rng.sample([2, 3, 5, 7], 2)
    N = rng.randint(30, 90)
    sols = [(a, b) for a in PRIMES for b in PRIMES if k1 * a + k2 * b == N]
    if not 1 <= len(sols) <= 3:
        return None
    vals = sorted({a + b for a, b in sols})
    ans = sum(vals)
    q = f"a ve b asal sayılar olmak üzere {k1}a + {k2}b = {N} eşitliği sağlanmaktadır.<br>Buna göre a + b toplamının alabileceği değerlerin toplamı kaçtır?"
    sol = ["Asal sayılardan yalnızca 2 çifttir; eşitliğin tek/çift durumu hangi değişkenin 2 olabileceğini sınırlar.",
           "Uygun (a, b) ikilileri: " + ", ".join(f"({a}, {b})" for a, b in sols) + ".",
           f"a + b değerleri: {', '.join(map(str, vals))} ⇒ toplam <b>{ans}</b>."]
    opts, a = num_opts(ans, rng, minv=2)
    return Q("temel", "Asal sayılar", 3, q, opts, a, sol, "Asal sayıların özelliklerini ve tek-çift analizini kullanır.", 90)


SIGN_CONDS = [
    ("a·b &lt; 0", lambda a, b, c: a * b < 0), ("b·c &gt; 0", lambda a, b, c: b * c > 0),
    ("a &lt; b", lambda a, b, c: a < b), ("a·c &gt; 0", lambda a, b, c: a * c > 0),
    ("c &lt; 0", lambda a, b, c: c < 0), ("a &gt; 0", lambda a, b, c: a > 0),
    ("b − a &gt; 0", lambda a, b, c: b - a > 0), ("a²·b &lt; 0", lambda a, b, c: a * a * b < 0),
]
SIGN_EXPR = [
    ("a·c", lambda a, b, c: a * c), ("b − c", lambda a, b, c: b - c), ("a − b", lambda a, b, c: a - b),
    ("a·b·c", lambda a, b, c: a * b * c), ("c − a", lambda a, b, c: c - a), ("b²·c", lambda a, b, c: b * b * c),
    ("a + b", lambda a, b, c: a + b), ("a·c − b", lambda a, b, c: a * c - b), ("c² − a", lambda a, b, c: c * c - a),
    ("b·c − a", lambda a, b, c: b * c - a), ("a³·c", lambda a, b, c: a ** 3 * c),
]


def t_signs(rng):
    conds = rng.sample(SIGN_CONDS, 3)
    vals = [v for v in range(-6, 7) if v]
    states = [s for s in itertools.product(vals, repeat=3) if all(f(*s) for _, f in conds)]
    if len(states) < 5:
        return None
    want = rng.choice(["pozitif", "negatif"])
    ok = (lambda v: v > 0) if want == "pozitif" else (lambda v: v < 0)
    alw = [e for e in SIGN_EXPR if all(ok(e[1](*s)) for s in states)]
    nal = [e for e in SIGN_EXPR if not all(ok(e[1](*s)) for s in states)]
    if not alw or len(nal) < 4:
        return None
    c = rng.choice(alw)
    signs = set(tuple("+" if x > 0 else "−" for x in s) for s in states)
    opts, a = text_opts(c[0], [w[0] for w in rng.sample(nal, 4)], rng)
    q = (f"a, b ve c sıfırdan farklı tam sayılar olmak üzere<br>{conds[0][0]}, &nbsp; {conds[1][0]}, &nbsp; {conds[2][0]}"
         f"<br>olduğuna göre aşağıdakilerden hangisi <b>kesinlikle {want}tir</b>?")
    sol = ["Koşullardan işaret tablosu çıkarılır. Olası (a, b, c) işaretleri: " + ", ".join("(" + ", ".join(s) + ")" for s in sorted(signs)) + ".",
           f"Her durumda {want} olan ifade <b>{c[0]}</b>'dir.",
           "Diğer ifadeler için koşulları sağlayan ama farklı işaret veren örnek değerler bulunabilir."]
    return Q("temel", "Pozitif ve negatif sayılar", 3, q, opts, a, sol, "Sayıların işaretlerini koşullardan belirler.", 75)


# ---------------------------------------------------------------- BÖLÜNEBİLME / FAKTÖRİYEL

def t_crt(rng):
    m, n = rng.sample([4, 5, 6, 7, 8, 9, 10, 12], 2)
    if math.gcd(m, n) > 2:
        return None
    r1, r2 = rng.randrange(m), rng.randrange(n)
    mode = rng.choice(["en küçük", "en küçük üç basamaklı", "en büyük iki basamaklı"])
    cand = [x for x in range(1, 2000) if x % m == r1 and x % n == r2]
    if mode == "en küçük üç basamaklı":
        cand = [x for x in cand if x >= 100]
    if mode == "en büyük iki basamaklı":
        cand = [x for x in cand if 10 <= x <= 99]
        if not cand:
            return None
        ans = max(cand)
    else:
        if not cand:
            return None
        ans = cand[0]
    L = m * n // math.gcd(m, n)
    q = f"Bir x pozitif tam sayısının {m} ile bölümünden kalan {r1}, {n} ile bölümünden kalan {nsuf(r2, 'cop')}.<br>Buna göre x'in alabileceği {mode} değer kaçtır?"
    base = [x for x in range(1, L + 1) if x % m == r1 and x % n == r2][0]
    sol = [f"Her iki koşulu sağlayan en küçük pozitif sayı denenerek bulunur: {base}.",
           f"Koşulları sağlayan sayılar EKOK({m}, {n}) = {L} aralıklarla tekrar eder: {base}, {base + L}, {base + 2 * L}, …",
           f"İstenen {mode} değer: <b>{ans}</b>."]
    opts, a = num_opts(ans, rng, step=rng.choice([1, 2, L // 2 or 1]), minv=1)
    return Q("bolunebilme", "Bölme ve kalan", 3, q, opts, a, sol, "Kalan koşullarını EKOK yardımıyla birleştirir.", 90)


def t_remainder_expr(rng):
    m = rng.choice([8, 9, 10, 12, 14, 15, 18])
    r = rng.randrange(1, m)
    d = rng.choice([x for x in range(3, m) if m % x == 0] or [m])
    if d == m:
        return None
    k, c = rng.randint(2, 7), rng.randint(1, 9)
    res = {(k * A + c) % d for A in range(r, 500, m)}
    assert len(res) == 1
    ans = res.pop()
    q = f"Bir A doğal sayısının {m} ile bölümünden kalan {nsuf(r, 'cop')}.<br>Buna göre {k}A + {c} sayısının {d} ile bölümünden kalan kaçtır?"
    sol = [f"A = {m}t + {r} ve {d}, {nsuf(m, 'gen')} böleni olduğundan A'nın {d} ile bölümünden kalan {nsuf(r % d, 'cop')}.",
           f"{k}·{r % d} + {c} = {k * (r % d) + c}; bunun {d} ile bölümünden kalan <b>{ans}</b>."]
    opts, a = num_opts(ans, rng, minv=0, maxv=d - 1 if d >= 5 else None)
    return Q("bolunebilme", "Bölme ve kalan", 2, q, opts, a, sol, "Kalan aritmetiğini ifadelere uygular.", 60)


def t_div_digits(rng):
    D = rng.choice([12, 15, 18, 24, 36, 45, 72])
    d1, d3 = rng.randint(1, 9), rng.randint(0, 9)
    ask = rng.choice(["a'nın alabileceği değerlerin toplamı", "a + b toplamının en büyük değeri", "kaç farklı (a, b) ikilisi"])
    tail = "vardır?" if ask.startswith("kaç") else "kaçtır?"
    pairs = [(a, b) for a in range(10) for b in range(10) if int(f"{d1}{a}{d3}{b}") % D == 0]
    if len(pairs) < 1:
        return None
    if ask.startswith("a'nın"):
        ans = sum(sorted({a for a, _ in pairs}))
    elif ask.startswith("a + b"):
        ans = max(a + b for a, b in pairs)
    else:
        ans = len(pairs)
    if ans == 0:
        return None
    fac = {12: "3 ve 4", 15: "3 ve 5", 18: "2 ve 9", 24: "3 ve 8", 36: "4 ve 9", 45: "5 ve 9", 72: "8 ve 9"}[D]
    q = f"Dört basamaklı {d1}a{d3}b sayısı {D} ile tam bölünebilmektedir.<br>Buna göre {ask} {tail}"
    sol = [f"{D} ile bölünebilme için sayı {fac} ile aralarında asal çarpanlarının her birine bölünmelidir.",
           "Uygun (a, b) ikilileri: " + ", ".join(f"({a}, {b})" for a, b in pairs) + ".",
           f"Buna göre istenen değer <b>{ans}</b>."]
    opts, a = num_opts(ans, rng, minv=0)
    return Q("bolunebilme", "Bölünebilme kuralları", 3, q, opts, a, sol, "Bileşik sayılarla bölünebilmeyi aralarında asal çarpanlara ayırarak uygular.", 90)


def t_fact_zeros(rng):
    v = rng.choice(["zero", "legendre", "ratio"])
    if v == "zero":
        n = rng.randint(30, 140)
        ans = sum(n // 5 ** i for i in range(1, 5))
        q = f"{n}! sayısının sondan kaç basamağı sıfırdır?"
        sol = [f"Sondaki sıfır sayısı = 10 = 2·5 çarpanlarının sayısı; 5 çarpanı daha az olduğundan belirleyicidir.",
               " + ".join(f"⌊{n}/{5 ** i}⌋" for i in range(1, 5) if n // 5 ** i) + f" = <b>{ans}</b>."]
        opts, a = num_opts(ans, rng, minv=1, extra=[n // 5])
        return Q("bolunebilme", "Faktöriyel", 2, q, opts, a, sol, "Faktöriyelde asal çarpan sayısını hesaplar.", 45)
    if v == "legendre":
        n = rng.randint(15, 40)
        p = rng.choice([2, 3, 7])
        ans = sum(n // p ** i for i in range(1, 7))
        q = f"{n}! sayısı {p}<sup>k</sup> ile tam bölünebildiğine göre k en çok kaçtır?"
        sol = [f"{n}! içindeki {p} çarpanları: " + " + ".join(f"⌊{n}/{p ** i}⌋" for i in range(1, 7) if n // p ** i) + f" = <b>{ans}</b>."]
        opts, a = num_opts(ans, rng, minv=1, extra=[n // p])
        return Q("bolunebilme", "Faktöriyel", 3, q, opts, a, sol, "Legendre yöntemiyle asal çarpan üssü bulur.", 60)
    n = rng.randint(5, 12)
    k = rng.choice([1, 2])
    num_ = math.factorial(n + k) + math.factorial(n + k - 1)
    den = math.factorial(n + k - 1) - math.factorial(n + k - 2) if k == 2 else math.factorial(n)
    ans = F(num_, den)
    if ans.denominator != 1:
        return None
    ans = int(ans)
    if k == 1:
        q = f"({n + 1}! + {n}!) ÷ {n}! işleminin sonucu kaçtır?"
        sol = [f"{n + 1}! = {n + 1}·{n}! olduğundan pay {n}!·({n + 1} + 1) olur.", f"Sonuç: {n + 2} = <b>{ans}</b>."]
    else:
        q = f"({n + 2}! + {n + 1}!) ÷ ({n + 1}! − {n}!) işleminin sonucu kaçtır?"
        sol = [f"Pay: {n + 1}!·({n + 2} + 1) = {n + 1}!·{n + 3}; payda: {n}!·({n + 1} − 1) = {n}!·{n}.",
               f"Sadeleşince ({n + 1}·{n + 3}) ÷ {n} = <b>{ans}</b>."]
        if (n + 1) * (n + 3) % n:
            return None
    opts, a = num_opts(ans, rng, minv=1)
    return Q("bolunebilme", "Faktöriyel", 2, q, opts, a, sol, "Faktöriyel ifadeleri ortak çarpan parantezine alarak sadeleştirir.", 45)


def t_gcd_lcm(rng):
    v = rng.choice(["tile", "bell", "divisors"])
    if v == "tile":
        g = rng.choice([6, 8, 12, 15, 18, 20, 24])
        x, y = rng.sample([2, 3, 5, 7, 4, 9], 2)
        if math.gcd(x, y) != 1:
            return None
        W, H = g * x, g * y
        ans = x * y
        q = f"Boyutları {W} m ve {H} m olan dikdörtgen biçimindeki bir alan, kenar uzunlukları tam sayı olan eş kare karolarla boşluksuz döşenecektir.<br>Bu iş için en az kaç karo gerekir?"
        sol = [f"En az karo için karonun kenarı en büyük olmalı: EBOB({W}, {H}) = {g} m.",
               f"Karo sayısı: ({W} ÷ {g})·({H} ÷ {g}) = {x}·{y} = <b>{ans}</b>."]
        opts, a = num_opts(ans, rng, step=rng.choice([1, 2, 3]), minv=1, extra=[x + y])
        return Q("bolunebilme", "EBOB ve EKOK", 2, q, opts, a, sol, "EBOB'u gerçek yaşam problemine uygular.", 60)
    if v == "bell":
        ps = rng.sample([6, 8, 9, 10, 12, 15, 18, 20, 24, 30], 3)
        L = math.lcm(*ps)
        if L > 360:
            return None
        start_h = rng.randint(8, 10)
        tot = start_h * 60 + L
        ans_t = f"{tot // 60:02d}.{tot % 60:02d}"
        wrong = set()
        for d in [-30, -15, 15, 30, -60, 60, L // 2, -L // 2]:
            t = tot + d
            if t > start_h * 60:
                wrong.add(f"{t // 60:02d}.{t % 60:02d}")
        wrong.discard(ans_t)
        wl = sorted(wrong)
        rng.shuffle(wl)
        opts_raw = wl[:4] + [ans_t]
        opts_raw.sort()
        q = f"Üç alarm sırasıyla {ps[0]}, {ps[1]} ve {ps[2]} dakikada bir çalmaktadır. Üçü birlikte saat {start_h:02d}.00'da çaldığına göre, üçü birlikte ilk kez saat kaçta yeniden çalar?"
        sol = [f"Birlikte çalma aralığı EKOK({ps[0]}, {ps[1]}, {ps[2]}) = {L} dakikadır.",
               f"{start_h:02d}.00 + {L} dakika = <b>{ans_t}</b>."]
        return Q("bolunebilme", "EBOB ve EKOK", 2, q, opts_raw, opts_raw.index(ans_t), sol, "EKOK'u periyodik olaylara uygular.", 60)
    a_, b_, c_ = rng.randint(1, 4), rng.randint(1, 3), rng.randint(0, 2)
    N = 2 ** a_ * 3 ** b_ * 5 ** c_
    ask = rng.choice(["pozitif bölenlerinin sayısı", "çift pozitif bölenlerinin sayısı", "tek pozitif bölenlerinin sayısı"])
    divs = [d for d in range(1, N + 1) if N % d == 0]
    if ask.startswith("çift"):
        ans = sum(1 for d in divs if d % 2 == 0)
    elif ask.startswith("tek"):
        ans = sum(1 for d in divs if d % 2)
    else:
        ans = len(divs)
    fact = " · ".join(s for s in [f"2<sup>{a_}</sup>", f"3<sup>{b_}</sup>" if b_ else "", f"5<sup>{c_}</sup>" if c_ else ""] if s)
    q = f"{N} sayısının {ask} kaçtır?"
    sol = [f"{N} = {fact}.",
           "Toplam bölen sayısı üslerin bir fazlalarının çarpımıdır" + (": " + "·".join(str(e + 1) for e in [a_, b_, c_] if e) + f" = {len(divs)}." if True else ""),
           ("Tek bölenler 2 çarpanı içermez; çift bölenler = toplam − tek bölenler. " if not ask.startswith("pozitif") else "") + f"Sonuç: <b>{ans}</b>."]
    opts, a = num_opts(ans, rng, minv=1)
    return Q("bolunebilme", "Asal çarpanlar ve bölenler", 3, q, opts, a, sol, "Asal çarpanlara ayırarak bölen sayısını bulur.", 60)


# ---------------------------------------------------------------- RASYONEL SAYILAR

def t_frac_expr(rng):
    def rf():
        d = rng.choice([2, 3, 4, 5, 6, 8, 9, 10, 12])
        n = rng.randint(1, d - 1)
        return F(n, d)
    x, y, z, w = rf(), rf(), rf(), rf()
    form = rng.choice(["(x+y)/(z-w)", "(x-y)*z/w", "x/(y+z)+w", "(1-x)/(1+y)"])
    try:
        val = eval(form, {}, dict(x=x, y=y, z=z, w=w))
    except ZeroDivisionError:
        return None
    if val.denominator > 30 or abs(val.numerator) > 60 or val <= 0:
        return None
    disp = form.replace("*", " · ").replace("/", " ÷ ").replace("+", " + ").replace("-", " − ")
    disp = disp.replace("x", frs(x)).replace("y", frs(y)).replace("z", frs(z)).replace("w", frs(w))
    q = f"{disp}<br>işleminin sonucu kaçtır?"
    sol = ["Önce parantez içleri payda eşitlenerek hesaplanır.", "Bölme işlemi, ikinci kesrin ters çevrilip çarpılmasıyla yapılır.",
           f"Sonuç: <b>{frs(val)}</b>."]
    extra = [val + 1, val * 2, F(1, 1) / val if val != 1 else val + 2, val - F(1, 2)]
    opts, a = num_opts(val, rng, step=F(1, val.denominator) if val.denominator > 1 else F(1, 2), minv=F(1, 100), extra=[e for e in extra if e > 0])
    return Q("rasyonel", "Basit ve bileşik kesirler", 2, q, opts, a, sol, "Kesirlerle dört işlemi işlem önceliğine uygun yapar.", 60)


def t_decimal(rng):
    a = F(rng.randint(1, 9), 10)
    b = F(rng.randint(2, 9), 100)
    c = F(rng.randint(1, 30), 1000)
    d = F(rng.choice([2, 3, 4, 5, 6, 8]), 1000)
    val = (a * b + c) / d
    if val.denominator != 1:
        return None
    val = int(val)
    q = f"({dec(a)} · {dec(b)} + {dec(c)}) ÷ {dec(d)}<br>işleminin sonucu kaçtır?"
    sol = [f"{dec(a)} · {dec(b)} = {dec(a * b)}; {dec(a * b)} + {dec(c)} = {dec(a * b + c)}.",
           f"Virgülden kurtulmak için pay ve payda 1000 ile çarpılır: {int((a * b + c) * 1000)} ÷ {int(d * 1000)} = <b>{val}</b>."]
    opts, a_ = num_opts(val, rng, step=max(1, val // 10), minv=1, extra=[val * 10, val // 10 if val >= 10 else val + 3])
    return Q("rasyonel", "Ondalık sayılar", 2, q, opts, a_, sol, "Ondalık sayılarla işlemde virgül kaydırmayı doğru uygular.", 50)


def t_frac_order(rng):
    fr = set()
    while len(fr) < 3:
        d = rng.randint(5, 15)
        n = rng.randint(2, d - 1)
        f = F(n, d)
        if f.denominator == d:
            fr.add(f)
    fr = list(fr)
    if len({float(x) for x in fr}) < 3 or max(fr) - min(fr) > F(1, 3):
        return None
    names = ["a", "b", "c"]
    order = sorted(range(3), key=lambda i: fr[i])
    correct = " &lt; ".join(names[i] for i in order)
    perms = [" &lt; ".join(names[i] for i in p) for p in itertools.permutations(range(3))]
    opts, a = text_opts(correct, rng.sample([p for p in perms if p != correct], 4), rng)
    q = f"a = {frs(fr[0])}, &nbsp; b = {frs(fr[1])}, &nbsp; c = {frs(fr[2])}<br>sayılarının küçükten büyüğe doğru sıralanışı aşağıdakilerden hangisidir?"
    sol = ["Kesirleri karşılaştırmak için ondalık yaklaşımlar ya da payda eşitleme kullanılır: " +
           ", ".join(f"{names[i]} ≈ {dec(round(float(fr[i]), 3))}" for i in range(3)) + ".", f"Sıralama: <b>{correct}</b>."]
    return Q("rasyonel", "Rasyonel sayılarda sıralama", 2, q, opts, a, sol, "Rasyonel sayıları karşılaştırır.", 60)


def t_repeating(rng):
    a = rng.randint(1, 8)
    b = rng.randint(10, 98)
    x = F(a, 9)
    y = F(b, 99)
    val = x + y
    q = f"0,<span class='ov'>{a}</span> + 0,<span class='ov'>{b:02d}</span> toplamı kaçtır?"
    sol = [f"0,<span class='ov'>{a}</span> = {frs(x)}, &nbsp; 0,<span class='ov'>{b:02d}</span> = {frs(y)} (devreden kısım ÷ 9…9).",
           f"Toplam: {frs(x)} + {frs(y)} = <b>{frs(val)}</b>."]
    extra = [F(a, 10) + F(b, 100), F(a + b, 99), val + F(1, 9)]
    opts, i = num_opts(val, rng, step=F(1, 99), minv=0, extra=extra)
    return Q("rasyonel", "Devirli ondalık sayılar", 3, q, opts, i, sol, "Devirli ondalık sayıları kesre çevirir.", 60)


def t_frac_problem(rng):
    p1 = F(rng.randint(1, 3), rng.choice([4, 5, 6]))
    p2 = F(rng.randint(1, 3), rng.choice([4, 5, 7]))
    if p1 >= 1 or p2 >= 1:
        return None
    rest = (1 - p1) * (1 - p2)
    left = rng.choice([60, 72, 84, 90, 120, 144, 180, 240])
    total = F(left) / rest
    if total.denominator != 1:
        return None
    total = int(total)
    item = rng.choice(["kitap", "kırtasiye malzemesi", "yemek kartı"])
    q = (f"Bir öğrenci harçlığının {frs(p1)}'ini {item} için, kalan paranın {frs(p2)}'ini ulaşım için harcamıştır. Geriye {left} TL kaldığına göre öğrencinin harçlığı kaç TL'dir?")
    sol = [f"İlk harcamadan sonra kalan: 1 − {frs(p1)} = {frs(1 - p1)}.",
           f"İkinci harcamadan sonra kalan: {frs(1 - p1)} · (1 − {frs(p2)}) = {frs(rest)}.",
           f"{frs(rest)}·x = {left} ⇒ x = <b>{total}</b> TL."]
    opts, a = num_opts(total, rng, step=rng.choice([20, 30, 40]), minv=left + 1)
    return Q("rasyonel", "Kesir problemleri", 3, q, opts, a, sol, "Kalanın kesri ile 'bütünün kesri' ayrımını yapar.", 90)


# ---------------------------------------------------------------- EŞİTSİZLİK / MUTLAK DEĞER

def t_range_expr(rng):
    a, b = sorted(rng.sample(range(-6, 8), 2))
    c, d = sorted(rng.sample(range(-5, 7), 2))
    p, q2 = rng.choice([1, 2, 3]), rng.choice([1, 2, 3])
    sgn = rng.choice([1, -1])
    lo = p * a + (sgn * q2 * c if sgn > 0 else -q2 * d)
    hi = p * b + (sgn * q2 * d if sgn > 0 else -q2 * c)
    ans = hi - lo - 1
    if ans < 3:
        return None
    op = "+" if sgn > 0 else "−"
    pt = "" if p == 1 else str(p)
    qt = "" if q2 == 1 else str(q2)
    q = f"x ve y gerçel sayılar olmak üzere<br>{a} &lt; x &lt; {b} &nbsp; ve &nbsp; {c} &lt; y &lt; {d}<br>olduğuna göre {pt}x {op} {qt}y ifadesinin alabileceği kaç farklı tam sayı değeri vardır?".replace("−", "−")
    sol = [f"{pt}x aralığı: ({p * a}, {p * b}); {op}{qt}y aralığı: " + (f"({q2 * c}, {q2 * d})" if sgn > 0 else f"({-q2 * d}, {-q2 * c})") + ".",
           f"Uç değerler toplanır (çıkarmada önce −1 ile çarpılıp sıralama ters çevrilir): ({lo}, {hi}).",
           f"Açık aralıktaki tam sayılar {lo + 1}, …, {hi - 1} ⇒ <b>{ans}</b> tane."]
    opts, i = num_opts(ans, rng, minv=1, extra=[ans + 2, ans + 1])
    return Q("esitsizlik", "Eşitsizlikler", 3, q, opts, i, sol, "Eşitsizlikleri taraf tarafa işleme sokar.", 75)


def t_abs_count(rng):
    k = rng.choice([1, 2, 3])
    a = rng.randint(-6, 9)
    b = rng.randint(3, 15)
    rel = rng.choice(["≤", "&lt;"])
    sols = [x for x in range(-60, 60) if (abs(k * x - a) <= b if rel == "≤" else abs(k * x - a) < b)]
    if not sols:
        return None
    ask = rng.choice(["kaç farklı tam sayı değeri", "tam sayı değerlerinin toplamı"])
    ans = len(sols) if ask.startswith("kaç") else sum(sols)
    kt = "" if k == 1 else str(k)
    q = f"|{kt}x − {a}| {rel} {b}".replace("− -", "+ ") + (f"<br>eşitsizliğini sağlayan kaç farklı x tam sayısı vardır?" if ask.startswith("kaç") else f"<br>eşitsizliğini sağlayan x tam sayılarının toplamı kaçtır?")
    sol = [f"−{b} {rel} {kt}x − {a} {rel} {b}".replace("− -", "+ ") + f" ⇒ {a - b} {rel} {kt}x {rel} {a + b}.",
           f"Tam sayı çözümler: {sols[0]}, …, {sols[-1]}.", f"İstenen: <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=1 if ask.startswith("kaç") else rng.choice([1, 2, 3]), minv=1 if ask.startswith("kaç") else None)
    return Q("esitsizlik", "Mutlak değer", 2, q, opts, i, sol, "Mutlak değerli eşitsizliği çift taraflı eşitsizliğe çevirir.", 60)


def t_abs_equation(rng):
    a = rng.randint(-5, 8)
    b = rng.randint(1, 4)
    c = rng.randint(-10, 10)
    sols = set()
    for x2 in range(-200, 201):
        x = F(x2, 2)
        if abs(x - a) == b * x + c:
            sols.add(x)
    if not sols or any(s.denominator != 1 for s in sols):
        return None
    ans = sum(sols)
    q = f"|x − {a}| = {b}x {'+' if c >= 0 else '−'} {abs(c)}".replace("− -", "+ ") + "<br>denklemini sağlayan x değerlerinin toplamı kaçtır?"
    lhs = f"x {'−' if a >= 0 else '+'} {abs(a)}"
    rhs = f"{b}x {'+' if c >= 0 else '−'} {abs(c)}"
    sol = [f"1. durum: {lhs} = {rhs}; 2. durum: {lhs} = −({rhs}).",
           f"Her durumda bulunan kök, sağ tarafın negatif olmamasını (|…| ≥ 0) sağlamalıdır.",
           f"Geçerli kök(ler): {', '.join(num(s) for s in sorted(sols))} ⇒ toplam <b>{num(ans)}</b>."]
    opts, i = num_opts(ans, rng, step=1, extra=[ans + 1, ans - 1])
    return Q("esitsizlik", "Mutlak değer", 4, q, opts, i, sol, "Mutlak değerli denklemde kök kontrolü yapar.", 90)


ORDER_ST = [
    ("a·b &gt; 0", lambda a, b, c: a * b > 0), ("a² &gt; b²", lambda a, b, c: a * a > b * b),
    ("a·c &lt; b·c", lambda a, b, c: a * c < b * c), ("a + c &lt; b", lambda a, b, c: a + c < b),
    ("b·c &gt; a", lambda a, b, c: b * c > a), ("a − b &gt; 0", lambda a, b, c: a - b > 0),
    ("c − a &gt; c − b", lambda a, b, c: c - a > c - b), ("a + b &gt; c", lambda a, b, c: a + b > c),
    ("b² &gt; c", lambda a, b, c: b * b > c), ("a·b·c &lt; 0", lambda a, b, c: a * b * c < 0),
    ("⟦1/a⟧ &gt; ⟦1/b⟧", lambda a, b, c: F(1, 1) / a > F(1, 1) / b), ("|a| &lt; |b|", lambda a, b, c: abs(a) < abs(b)),
]


def t_order_truth(rng):
    vals = [F(n, 2) for n in range(-16, 17) if n]
    cfg = rng.choice(["a &lt; b &lt; 0 &lt; c", "0 &lt; a &lt; b &lt; c", "a &lt; 0 &lt; b &lt; c", "a &lt; b &lt; c &lt; 0"])
    chk = {
        "a &lt; b &lt; 0 &lt; c": lambda a, b, c: a < b < 0 < c,
        "0 &lt; a &lt; b &lt; c": lambda a, b, c: 0 < a < b < c,
        "a &lt; 0 &lt; b &lt; c": lambda a, b, c: a < 0 < b < c,
        "a &lt; b &lt; c &lt; 0": lambda a, b, c: a < b < c < 0,
    }[cfg]
    states = [(a, b, c) for a in vals for b in vals for c in vals if chk(a, b, c)]
    alw = [s for s in ORDER_ST if all(s[1](*t) for t in states)]
    nal = [s for s in ORDER_ST if not all(s[1](*t) for t in states)]
    if not alw or len(nal) < 4:
        return None
    c = rng.choice(alw)
    opts, i = text_opts(c[0], [s[0] for s in rng.sample(nal, 4)], rng)
    q = f"a, b ve c gerçel sayıları için {cfg} olduğuna göre aşağıdakilerden hangisi <b>kesinlikle doğrudur</b>?"
    sol = [f"Sıralamadan işaretler ve büyüklükler belirlenir ({cfg}).",
           f"<b>{c[0]}</b> ifadesi verilen sıralamadaki her değer için sağlanır.",
           "Diğer seçenekler için koşulu sağlayan karşı örnekler bulunabilir (örneğin kesirli ya da mutlak değerce farklı değerler)."]
    return Q("esitsizlik", "Sıralama ve eşitsizlik", 3, q, opts, i, sol, "Eşitsizliklerde çarpma/bölme işaret kurallarını uygular.", 75)


def t_minmax(rng):
    a, b = sorted(rng.sample(range(-6, 6), 2))
    c, d = sorted(rng.sample(range(-4, 7), 2))
    form, f = rng.choice([("x² − 2y", lambda x, y: x * x - 2 * y), ("x·y", lambda x, y: x * y),
                          ("x² + y²", lambda x, y: x * x + y * y), ("2x − y²", lambda x, y: 2 * x - y * y)])
    ask = rng.choice(["en küçük", "en büyük"])
    vals = [f(x, y) for x in range(a, b + 1) for y in range(c, d + 1)]
    ans = min(vals) if ask == "en küçük" else max(vals)
    q = f"x ve y tam sayılar olmak üzere {a} ≤ x ≤ {b} ve {c} ≤ y ≤ {d} olduğuna göre {form} ifadesinin alabileceği {ask} değer kaçtır?"
    xs = [(x, y) for x in range(a, b + 1) for y in range(c, d + 1) if f(x, y) == ans][0]
    sol = ["Kare alan ifadelerde mutlak değerce en büyük/en küçük değer, çarpımda ise işaret dikkate alınır.",
           f"{ask.capitalize()} değer x = {xs[0]}, y = {xs[1]} için elde edilir: <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=rng.choice([1, 2]))
    return Q("esitsizlik", "Eşitsizlikler", 3, q, opts, i, sol, "Tam sayı aralıklarında ifadenin uç değerini bulur.", 75)


# ---------------------------------------------------------------- ÜSLÜ / KÖKLÜ

def t_exp_simplify(rng):
    base = rng.choice([2, 3])
    b2, b3 = base ** 2, base ** 3
    x, y, z = rng.randint(1, 6), rng.randint(1, 5), rng.randint(1, 4)
    k = x + 2 * y - 3 * z
    q = f"({base}<sup>{x}</sup> · {b2}<sup>{y}</sup>) ÷ {b3}<sup>{z}</sup> = {base}<sup>k</sup><br>olduğuna göre k kaçtır?"
    sol = [f"{b2}<sup>{y}</sup> = {base}<sup>{2 * y}</sup>, &nbsp; {b3}<sup>{z}</sup> = {base}<sup>{3 * z}</sup>.",
           f"k = {x} + {2 * y} − {3 * z} = <b>{k}</b>."]
    opts, i = num_opts(k, rng, extra=[x + y - z, k + 2])
    return Q("uslu", "Üslü sayılar", 2, q, opts, i, sol, "Tabanları eşitleyerek üslü ifadeleri sadeleştirir.", 45)


def t_exp_equation(rng):
    b = rng.choice([2, 3, 5])
    s = rng.choice([1, 2, 3])
    x = rng.randint(1, 4)
    sg = rng.choice([1, -1])
    R = b ** x * (b ** s + sg)
    if R > 2000:
        return None
    op = "+" if sg > 0 else "−"
    q = f"{b}<sup>x + {s}</sup> {op} {b}<sup>x</sup> = {R}<br>olduğuna göre x kaçtır?"
    sol = [f"{b}<sup>x</sup> parantezine alınır: {b}<sup>x</sup>·({b ** s} {op} 1) = {R}.",
           f"{b}<sup>x</sup> = {R} ÷ {b ** s + sg} = {b ** x} ⇒ x = <b>{x}</b>."]
    opts, i = num_opts(x, rng, minv=0)
    return Q("uslu", "Üslü denklemler", 2, q, opts, i, sol, "Ortak çarpan parantezine alarak üslü denklem çözer.", 50)


def t_roots(rng):
    k = rng.choice([2, 3, 5, 6, 7])
    p, q2, r = rng.sample(range(1, 7), 3)
    m = p + q2 - r
    if m <= 0:
        return None
    ex = f"√{p * p * k} + √{q2 * q2 * k} − √{r * r * k}"
    q = f"{ex} = m√{k}<br>olduğuna göre m kaçtır?"
    sol = [f"√{p * p * k} = {p}√{k}, &nbsp; √{q2 * q2 * k} = {q2}√{k}, &nbsp; √{r * r * k} = {r}√{k}.",
           f"m = {p} + {q2} − {r} = <b>{m}</b>."]
    opts, i = num_opts(m, rng, minv=1)
    return Q("uslu", "Köklü sayılar", 2, q, opts, i, sol, "Kök içini tam kare çarpanlara ayırarak sadeleştirir.", 45)


def t_neg_exp(rng):
    a = rng.choice([F(1, 2), F(1, 3), F(1, 5), F(2, 3), F(1, 4)])
    b = rng.choice([F(1, 2), F(1, 3), F(2, 5), F(3, 4)])
    m, n = rng.randint(1, 3), rng.randint(1, 3)
    val = (1 / a) ** m + (1 / b) ** n
    if val.denominator > 30:
        return None
    da = dec(a) if a.denominator in (2, 4, 5) else frs(a)
    db = dec(b) if b.denominator in (2, 4, 5) else frs(b)
    da = f"({da})" if "⟦" not in da else f"({da})"
    db = f"({db})" if "⟦" not in db else f"({db})"
    q = f"{da}<sup>−{m}</sup> + {db}<sup>−{n}</sup><br>işleminin sonucu kaçtır?"
    sol = [f"Negatif üs, tabanı ters çevirir: {frs(1 / a)}<sup>{m}</sup> = {frs((1 / a) ** m)}, &nbsp; {frs(1 / b)}<sup>{n}</sup> = {frs((1 / b) ** n)}.",
           f"Toplam: <b>{frs(val)}</b>."]
    opts, i = num_opts(val, rng, step=F(1, val.denominator) if val.denominator > 1 else 1, minv=0, extra=[a ** m + b ** n])
    return Q("uslu", "Üslü sayılar", 2, q, opts, i, sol, "Negatif ve kesirli tabanlı üsleri hesaplar.", 50)


def t_exp_compare(rng):
    g = rng.choice([5, 10])
    trio = rng.choice([(2, 3, 5), (2, 3, 7), (3, 5, 11), (2, 5, 6), (4, 5, 7)])
    e = rng.sample([3, 2, 1, 4], 3)
    xs = [trio[i] ** (e[i] * g) for i in range(3)]
    if len(set(xs)) < 3:
        return None
    names = "abc"
    lab = [f"{names[i]} = {trio[i]}<sup>{e[i] * g}</sup>" for i in range(3)]
    order = sorted(range(3), key=lambda i: xs[i])
    correct = " &lt; ".join(names[i] for i in order)
    perms = [" &lt; ".join(names[i] for i in p) for p in itertools.permutations(range(3))]
    opts, i = text_opts(correct, rng.sample([p for p in perms if p != correct], 4), rng)
    q = ", &nbsp; ".join(lab) + "<br>sayılarının doğru sıralanışı aşağıdakilerden hangisidir?"
    sol = [f"Üslerin ortak böleni {g} ile ifadeler ({trio[0] ** e[0]})<sup>{g}</sup>, ({trio[1] ** e[1]})<sup>{g}</sup>, ({trio[2] ** e[2]})<sup>{g}</sup> biçimine getirilir.",
           f"Tabanlar karşılaştırılır: {trio[0] ** e[0]}, {trio[1] ** e[1]}, {trio[2] ** e[2]} ⇒ <b>{correct}</b>."]
    return Q("uslu", "Üslü sayılarda sıralama", 3, q, opts, i, sol, "Üsleri eşitleyerek büyüklük karşılaştırması yapar.", 60)


def t_rationalize(rng):
    a = rng.choice([2, 3, 5, 6, 7])
    b = rng.choice([1, 2, 3])
    if a == b * b:
        return None
    den = a - b * b
    num_ = rng.choice([den * k for k in (1, 2, 3)])
    k = num_ // den
    q = f"⟦{num_}/√{a} − {b}⟧ ifadesinin eşiti aşağıdakilerden hangisidir?"
    correct = f"{'' if k == 1 else k}(√{a} + {b})" if k != 1 else f"√{a} + {b}"
    wr = [f"{'' if k == 1 else k}(√{a} − {b})" if k != 1 else f"√{a} − {b}", f"√{a} + {b * k}", f"{k * 2}(√{a} + {b})",
          f"{k}√{a} − {b}", f"√{a} + {b + 1}"]
    opts, i = text_opts(correct, wr, rng)
    sol = [f"Pay ve payda eşleniği (√{a} + {b}) ile çarpılır.", f"Payda: {a} − {b * b} = {den}.",
           f"Sonuç: {num_} ÷ {den} · (√{a} + {b}) = <b>{correct}</b>."]
    if den <= 0:
        return None
    return Q("uslu", "Köklü sayılar", 3, q, opts, i, sol, "Paydayı eşlenikle çarparak rasyonel yapar.", 60)


# ---------------------------------------------------------------- ÇARPANLARA AYIRMA / DENKLEMLER

def t_identity(rng):
    v = rng.choice(["xy", "recip", "cube"])
    if v == "xy":
        a, b = rng.randint(1, 9), rng.randint(2, 20)
        sg = rng.choice(["−", "+"])
        ans = a * a + 2 * b if sg == "−" else a * a - 2 * b
        if ans <= 0:
            return None
        q = f"x {sg} y = {a} ve x·y = {b}<br>olduğuna göre x² + y² kaçtır?"
        sol = [f"(x {sg} y)² = x² + y² {sg} 2xy.", f"{a * a} = x² + y² {sg} {2 * b} ⇒ x² + y² = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=2, extra=[a * a + b, a * a])
        return Q("cebir", "Özdeşlikler", 2, q, opts, i, sol, "Tam kare özdeşliklerini kullanır.", 45)
    if v == "recip":
        a = rng.randint(3, 9)
        ans = a * a - 2
        q = f"x + ⟦1/x⟧ = {a}<br>olduğuna göre x² + ⟦1/x²⟧ kaçtır?"
        sol = [f"Her iki tarafın karesi alınır: x² + 2 + ⟦1/x²⟧ = {a * a}.", f"x² + ⟦1/x²⟧ = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, extra=[a * a, a * a + 2])
        return Q("cebir", "Özdeşlikler", 2, q, opts, i, sol, "Ters terimli ifadelerde kare alma tekniğini uygular.", 45)
    N = rng.choice([1001, 998, 1003, 497, 503, 2005, 105])
    d = rng.choice([1, 2, 3])
    ans = (N + d) ** 2 - (N - d) ** 2
    q = f"{N + d}² − {N - d}² işleminin sonucu kaçtır?"
    sol = [f"İki kare farkı: a² − b² = (a − b)(a + b).", f"({N + d} − {N - d})·({N + d} + {N - d}) = {2 * d}·{2 * N} = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=N, minv=1, extra=[2 * d * N])
    return Q("cebir", "Çarpanlara ayırma", 1, q, opts, i, sol, "İki kare farkı ile hızlı işlem yapar.", 30)


def t_factor_poly(rng):
    p, q2 = rng.sample([x for x in range(-7, 8) if x], 2)
    s, pr = p + q2, p * q2
    def lin(r):
        return f"x {'−' if r > 0 else '+'} {abs(r)}"
    poly = f"x² {'−' if s > 0 else '+'} {abs(s)}x {'+' if pr > 0 else '−'} {abs(pr)}" if s else f"x² {'+' if pr > 0 else '−'} {abs(pr)}"
    correct = lin(p)
    wr = [lin(-p), lin(-q2), lin(p + 1), lin(q2 - 1) if q2 - 1 not in (p,) and q2 - 1 else lin(q2 + 2), lin(s) if s not in (p, q2) and s else lin(pr)]
    wr = [w for w in wr if w not in (lin(p), lin(q2))]
    if len(set(wr)) < 4:
        return None
    opts, i = text_opts(correct, wr, rng)
    q = f"{poly} ifadesinin çarpanlarından biri aşağıdakilerden hangisidir?"
    sol = [f"Çarpımı {pr}, toplamı {-s} olan iki sayı aranır: {-p} ve {-q2}.", f"{poly} = ({lin(p)})({lin(q2)}). Seçeneklerde bulunan: <b>{correct}</b>."]
    return Q("cebir", "Çarpanlara ayırma", 2, q, opts, i, sol, "İkinci dereceden üç terimliyi çarpanlarına ayırır.", 45)


def t_lin_eq(rng):
    x = rng.randint(-6, 12)
    b, d = rng.sample([2, 3, 4, 5, 6], 2)
    a, c = rng.randint(-5, 9), rng.randint(-5, 9)
    e = F(x - a, b) + F(x + c, d)
    if e.denominator != 1:
        return None
    e = int(e)
    q = f"⟦x − {a}/{b}⟧ + ⟦x + {c}/{d}⟧ = {e}".replace("− -", "+ ").replace("+ -", "− ") + "<br>denklemini sağlayan x değeri kaçtır?"
    L = b * d // math.gcd(b, d)
    sol = [f"Payda {nsuf(L, 'loc')} eşitlenir: {L // b}(x − {a}) + {L // d}(x + {c}) = {L * e}.".replace("− -", "+ ").replace("+ -", "− "),
           f"{L // b + L // d}x = {L * e + L // b * a - L // d * c} ⇒ x = <b>{x}</b>."]
    opts, i = num_opts(x, rng)
    return Q("cebir", "Birinci dereceden denklemler", 2, q, opts, i, sol, "Kesirli denklemde payda eşitleyerek çözüm bulur.", 60)


def t_system(rng):
    x, y = rng.randint(1, 12), rng.randint(1, 12)
    a1, b1, a2, b2 = rng.randint(1, 5), rng.randint(1, 5), rng.randint(1, 5), rng.randint(-4, 4)
    if a1 * b2 - a2 * b1 == 0 or b2 == 0:
        return None
    c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
    ask = rng.choice(["x·y", "x + y", "x − y"])
    ans = {"x·y": x * y, "x + y": x + y, "x − y": x - y}[ask]
    def t(a, b):
        return f"{'' if a == 1 else a}x {'+' if b > 0 else '−'} {'' if abs(b) == 1 else abs(b)}y"
    q = f"{t(a1, b1)} = {c1}<br>{t(a2, b2)} = {c2}<br>olduğuna göre {ask} kaçtır?"
    sol = ["Denklemlerden biri uygun bir sayıyla çarpılıp diğerine eklenerek bir bilinmeyen yok edilir.", f"Çözüm: x = {x}, y = {y}.", f"{ask} = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=rng.choice([1, 2]))
    return Q("cebir", "Denklem sistemleri", 2, q, opts, i, sol, "İki bilinmeyenli doğrusal denklem sistemini çözer.", 60)


def t_word_eq(rng):
    n = rng.randint(4, 15)
    p1, p2 = rng.choice([(20, 35), (15, 25), (30, 45), (12, 20), (40, 55)])
    big = rng.randint(1, n - 1)
    total = big * p2 + (n - big) * p1
    q = (f"Bir kırtasiyeden tanesi {p1} TL olan defterlerden ve tanesi {p2} TL olan kitaplardan toplam {n} ürün alınmış ve {total} TL ödenmiştir.<br>Buna göre kaç kitap alınmıştır?")
    sol = [f"Kitap sayısı k ise defter sayısı {n} − k olur.", f"{p2}k + {p1}({n} − k) = {total} ⇒ {p2 - p1}k = {total - p1 * n}.", f"k = <b>{big}</b>."]
    opts, i = num_opts(big, rng, minv=0, maxv=n, extra=[n - big])
    return Q("cebir", "Birinci dereceden denklemler", 2, q, opts, i, sol, "Sözel ifadeyi denkleme dönüştürür.", 60)


# ---------------------------------------------------------------- ORAN ORANTI

def t_chain_ratio(rng):
    p, q2, r, s = [rng.randint(1, 7) for _ in range(4)]
    if math.gcd(p, q2) != 1 or math.gcd(r, s) != 1 or p == q2 or r == s:
        return None
    A, B, C = p * r, q2 * r, q2 * s
    g = math.gcd(math.gcd(A, B), C)
    A, B, C = A // g, B // g, C // g
    k = rng.randint(2, 6)
    T = (A + B + C) * k
    ask = rng.choice(["a", "b", "c"])
    ans = {"a": A, "b": B, "c": C}[ask] * k
    q = f"⟦a/b⟧ = ⟦{p}/{q2}⟧ ve ⟦b/c⟧ = ⟦{r}/{s}⟧ olmak üzere a + b + c = {T} olduğuna göre {ask} kaçtır?"
    sol = [f"b'yi ortak yapmak için oranlar genişletilir: a : b : c = {A} : {B} : {C}.",
           f"{A}t + {B}t + {C}t = {T} ⇒ t = {k}.", f"{ask} = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=k, minv=1)
    return Q("oran", "Oran ve orantı", 2, q, opts, i, sol, "Zincir oranları ortak terimde birleştirir.", 60)


def t_share(rng):
    ages = sorted(rng.sample(range(3, 15), 3))
    k = rng.choice([20, 25, 40, 50, 60, 100])
    total = sum(ages) * k
    kind = rng.choice(["doğru", "ters"])
    names = rng.sample(NAMES, 3)
    if kind == "doğru":
        ans = ages[2] * k
        q = f"{total} TL, yaşları {ages[0]}, {ages[1]} ve {ages[2]} olan {names[0]}, {names[1]} ve {names[2]} arasında yaşlarıyla doğru orantılı olarak paylaştırılıyor.<br>En büyük çocuk kaç TL alır?"
        sol = [f"Paylar {ages[0]}k, {ages[1]}k, {ages[2]}k ⇒ {sum(ages)}k = {total} ⇒ k = {k}.", f"En büyük pay: {ages[2]}·{k} = <b>{ans}</b> TL."]
        opts, i = num_opts(ans, rng, step=k, minv=1, extra=[ages[0] * k])
        return Q("oran", "Orantılı paylaştırma", 2, q, opts, i, sol, "Doğru orantılı paylaştırma yapar.", 50)
    L = math.lcm(*ages)
    parts = [L // a for a in ages]
    if total % sum(parts):
        total = sum(parts) * k
    t = total // sum(parts)
    ans = parts[0] * t
    q = f"{total} TL, yaşları {ages[0]}, {ages[1]} ve {ages[2]} olan üç kardeş arasında yaşlarıyla <b>ters orantılı</b> olarak paylaştırılıyor.<br>En küçük kardeş kaç TL alır?"
    sol = [f"Ters orantıda paylar ⟦1/{ages[0]}⟧ : ⟦1/{ages[1]}⟧ : ⟦1/{ages[2]}⟧; {L} ile genişletilince {parts[0]} : {parts[1]} : {parts[2]}.",
           f"Bir pay = {total} ÷ {sum(parts)} = {t}.", f"En küçük kardeşin payı: {parts[0]}·{t} = <b>{ans}</b> TL."]
    opts, i = num_opts(ans, rng, step=t, minv=1, extra=[parts[2] * t])
    return Q("oran", "Orantılı paylaştırma", 3, q, opts, i, sol, "Ters orantılı paylaştırma yapar.", 75)


def t_inverse(rng):
    w1, d1 = rng.choice([(6, 10), (8, 15), (12, 20), (5, 24), (9, 16), (10, 18)])
    w2 = rng.choice([x for x in range(3, 31) if (w1 * d1) % x == 0 and x != w1])
    ans = w1 * d1 // w2
    q = f"{w1} işçinin {d1} günde bitirdiği bir işi, aynı hızda çalışan {w2} işçi kaç günde bitirir?"
    sol = ["İşçi sayısı ile süre ters orantılıdır: işçi × gün sabittir.", f"{w1}·{d1} = {w2}·g ⇒ g = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, minv=1, extra=[w2 * d1 // w1 if w2 * d1 % w1 == 0 else ans + 3])
    return Q("oran", "Ters orantı", 1, q, opts, i, sol, "Ters orantıyı tanır ve uygular.", 40)


def t_scale(rng):
    scale = rng.choice([50000, 100000, 200000, 250000, 500000])
    cm = rng.choice([2, 3, 4, 5, 6, 8, 12, F(5, 2), F(7, 2)])
    km = F(cm) * scale / 100000
    if km.denominator != 1:
        return None
    km = int(km)
    q = f"1 : {scale} ölçekli bir haritada {dec(F(cm))} cm olarak gösterilen iki nokta arasındaki gerçek uzaklık kaç km'dir?"
    sol = [f"Gerçek uzaklık = {dec(F(cm))} · {scale} cm = {int(F(cm) * scale)} cm.", f"1 km = 100 000 cm ⇒ <b>{km}</b> km."]
    opts, i = num_opts(km, rng, step=max(1, km // 4), minv=1, extra=[km * 10, km // 10 if km >= 10 else km * 100])
    return Q("oran", "Ölçek", 1, q, opts, i, sol, "Ölçek ve birim dönüşümü yapar.", 40)


def t_equal_ratio(rng):
    p, q2, r = sorted(rng.sample(range(2, 10), 3))
    c1, c2, c3 = rng.randint(1, 3), rng.randint(-2, 3), rng.randint(-2, 2)
    k = rng.randint(1, 5)
    lhs = (c1 * p + c2 * q2 + c3 * r)
    if lhs == 0 or c2 == 0 or c3 == 0:
        return None
    val = lhs * k
    if val <= 0:
        return None
    ans = (p + q2 + r) * k
    def term(c, v):
        return f"{'+' if c > 0 else '−'} {'' if abs(c) == 1 else abs(c)}{v}"
    expr = f"{'' if c1 == 1 else c1}a {term(c2, 'b')} {term(c3, 'c')}"
    q = f"⟦a/{p}⟧ = ⟦b/{q2}⟧ = ⟦c/{r}⟧ ve {expr} = {val}<br>olduğuna göre a + b + c kaçtır?"
    sol = [f"Oranlar k'ye eşitlenir: a = {p}k, b = {q2}k, c = {r}k.", f"{expr} = {lhs}k = {val} ⇒ k = {k}.", f"a + b + c = {p + q2 + r}k = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=k, minv=1)
    return Q("oran", "Oran ve orantı", 2, q, opts, i, sol, "Eşit oranları ortak katsayı ile ifade eder.", 50)


# ---------------------------------------------------------------- PROBLEMLER

def t_age(rng):
    for _ in range(200):
        d = rng.randint(4, 16)
        k = rng.randint(3, 6)
        t = rng.randint(2, 20)
        m_num = k * d + t
        if m_num % (d + t) == 0:
            m = m_num // (d + t)
            if 1 < m < k:
                break
    else:
        return None
    adult, adult_g, child_g = rng.choice([("anne", "annenin", "kızının"), ("baba", "babanın", "oğlunun"), ("dede", "dedenin", "torununun")])
    q = (f"Bir {adult_g} bugünkü yaşı {child_g} bugünkü yaşının {k} katıdır. {t} yıl sonra {adult_g} yaşı {child_g} yaşının {m} katı olacaktır.<br>"
         f"Buna göre {adult_g} bugünkü yaşı kaçtır?")
    ans = k * d
    sol = [f"Çocuğun yaşı x ise yetişkinin yaşı {k}x olur.", f"{t} yıl sonra: {k}x + {t} = {m}(x + {t}) ⇒ {k - m}x = {m * t - t} ⇒ x = {d}.", f"Yetişkinin bugünkü yaşı: {k}·{d} = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=rng.choice([2, 3, 4]), minv=d + 15, extra=[d])
    return Q("problem", "Yaş problemleri", 2, q, opts, i, sol, "Yaş farkının sabitliğini kullanarak denklem kurar.", 75)


def t_age_sum(rng):
    kids = [rng.randint(2, 15) for _ in range(rng.choice([2, 3]))]
    mom = rng.randint(28, 45)
    dad = mom + rng.randint(1, 6)
    diff = dad - mom
    S = mom + dad + sum(kids)
    t = rng.randint(2, 8)
    Ks = sum(kids) + t * len(kids)
    q = (f"{len(kids)} çocuklu bir ailede babanın yaşı annenin yaşından {diff} fazladır. Anne, baba ve çocukların bugünkü yaşları toplamı {nsuf(S, 'cop')}; "
         f"{t} yıl sonra çocukların yaşları toplamı {Ks} olacaktır.<br>Buna göre annenin bugünkü yaşı kaçtır?")
    sol = [f"Çocukların bugünkü yaş toplamı: {Ks} − {len(kids)}·{t} = {sum(kids)}.", f"Anne + baba = {S} − {sum(kids)} = {mom + dad}.",
           f"Anne x ise 2x + {diff} = {mom + dad} ⇒ x = <b>{mom}</b>."]
    opts, i = num_opts(mom, rng, minv=20, extra=[dad])
    return Q("problem", "Yaş problemleri", 3, q, opts, i, sol, "Birden çok kişinin yaş toplamlarını zamanla ilişkilendirir.", 75)


WORK_PAIRS = [(3, 6), (6, 12), (10, 15), (12, 24), (20, 30), (4, 12), (12, 36), (15, 30), (6, 30), (8, 24), (12, 60), (18, 36), (20, 60)]


def t_work(rng):
    a, b = rng.choice(WORK_PAIRS)
    v = rng.choice(["together", "after", "pool"])
    if v == "together":
        ans = F(a * b, a + b)
        q = f"Bir işi A tek başına {a} günde, B tek başına {b} günde bitirebilmektedir.<br>İkisi birlikte bu işi kaç günde bitirir?"
        sol = [f"Bir günde yapılan işler: A ⟦1/{a}⟧, B ⟦1/{b}⟧.", f"Birlikte: ⟦1/{a}⟧ + ⟦1/{b}⟧ = {frs(F(1, a) + F(1, b))}.", f"Süre: <b>{frs(ans)}</b> gün."]
        opts, i = num_opts(ans, rng, minv=1, extra=[F(a + b, 2)])
        return Q("problem", "İşçi ve havuz problemleri", 2, q, opts, i, sol, "İş hızlarını toplayarak ortak süreyi bulur.", 50)
    if v == "after":
        x = rng.randint(1, a - 1)
        rem = 1 - F(x, a)
        t = rem / (F(1, a) + F(1, b))
        if t.denominator != 1:
            return None
        q = f"Bir işi A tek başına {a} saatte, B tek başına {b} saatte bitirebilmektedir. A işe tek başına başlayıp {x} saat çalıştıktan sonra B de ona katılıyor.<br>İş, B katıldıktan kaç saat sonra biter?"
        sol = [f"A'nın {x} saatte yaptığı iş: ⟦{x}/{a}⟧; kalan iş {frs(rem)}.", f"Birlikte saatlik iş: {frs(F(1, a) + F(1, b))}.", f"Süre: {frs(rem)} ÷ {frs(F(1, a) + F(1, b))} = <b>{int(t)}</b> saat."]
        opts, i = num_opts(int(t), rng, minv=1)
        return Q("problem", "İşçi ve havuz problemleri", 3, q, opts, i, sol, "Kısmi iş ve kalan iş hesabı yapar.", 75)
    if b == a:
        return None
    ans = F(a * b, b - a)
    if ans.denominator != 1:
        return None
    q = f"Boş bir havuzu bir musluk {a} saatte doldurmakta, havuzun dibindeki bir delik ise dolu havuzu {b} saatte boşaltmaktadır.<br>Havuz boşken musluk ve delik birlikte açılırsa havuz kaç saatte dolar?"
    sol = [f"Saatlik net dolum: ⟦1/{a}⟧ − ⟦1/{b}⟧ = {frs(F(1, a) - F(1, b))}.", f"Süre: <b>{int(ans)}</b> saat."]
    opts, i = num_opts(int(ans), rng, step=rng.choice([1, 2, 3]), minv=1, extra=[a + b])
    return Q("problem", "İşçi ve havuz problemleri", 2, q, opts, i, sol, "Dolduran ve boşaltan hızları farkla birleştirir.", 50)


def t_motion(rng):
    v = rng.choice(["meet", "catch", "avg"])
    if v == "meet":
        v1, v2 = rng.choice([(60, 80), (70, 90), (50, 70), (65, 85), (75, 95), (40, 60)])
        t = rng.choice([2, 3, F(3, 2), F(5, 2), 4])
        D = int((v1 + v2) * F(t))
        ask = rng.choice(["kaç saat sonra", "A'dan kaç km uzakta"])
        ans = F(t) if ask == "kaç saat sonra" else F(v1) * F(t)
        q = f"Aralarında {D} km bulunan A ve B kentlerinden iki araç aynı anda birbirine doğru hareket ediyor. A'dan çıkan aracın hızı saatte {v1} km, B'den çıkanınki saatte {v2} km'dir.<br>Araçlar {ask} karşılaşır?"
        sol = [f"Yaklaşma hızı: {v1} + {v2} = {v1 + v2} km/sa.", f"Karşılaşma süresi: {D} ÷ {v1 + v2} = {frs(F(t))} saat."]
        if ask != "kaç saat sonra":
            sol.append(f"A'dan uzaklık: {v1}·{frs(F(t))} = <b>{num(ans)}</b> km.")
        else:
            sol[-1] = sol[-1].replace(f"{frs(F(t))} saat", f"<b>{frs(F(t))}</b> saat")
        ans = int(ans) if ans.denominator == 1 else ans
        opts, i = num_opts(ans, rng, step=F(1, 2) if ask == "kaç saat sonra" else 10, minv=F(1, 2))
        return Q("problem", "Hareket problemleri", 2, q, opts, i, sol, "Karşılıklı harekette hızları toplar.", 60)
    if v == "catch":
        v1, v2 = rng.choice([(60, 80), (50, 75), (40, 60), (70, 90), (45, 60)])
        h = rng.choice([1, 2, 3])
        ans = F(v1 * h, v2 - v1)
        if ans.denominator != 1:
            return None
        q = f"Saatte {v1} km hızla giden bir araç yola çıktıktan {h} saat sonra, aynı noktadan aynı yöne saatte {v2} km hızla ikinci bir araç hareket ediyor.<br>İkinci araç birinciye kaç saat sonra yetişir?"
        sol = [f"Aradaki mesafe: {v1}·{h} = {v1 * h} km.", f"Yaklaşma hızı: {v2} − {v1} = {v2 - v1} km/sa.", f"Süre: {v1 * h} ÷ {v2 - v1} = <b>{int(ans)}</b> saat."]
        opts, i = num_opts(int(ans), rng, minv=1)
        return Q("problem", "Hareket problemleri", 2, q, opts, i, sol, "Aynı yönlü harekette hız farkını kullanır.", 60)
    a, b = rng.choice([(40, 60), (60, 90), (30, 60), (45, 90), (60, 120), (20, 30)])
    ans = F(2 * a * b, a + b)
    if ans.denominator != 1:
        return None
    q = f"Bir araç A'dan B'ye saatte {a} km, B'den A'ya ise aynı yoldan saatte {b} km hızla gitmiştir.<br>Gidiş-dönüş boyunca aracın ortalama hızı saatte kaç km'dir?"
    sol = ["Ortalama hız = toplam yol ÷ toplam süre (hızların aritmetik ortalaması DEĞİL).", f"Yol x ise: 2x ÷ (⟦x/{a}⟧ + ⟦x/{b}⟧) = 2·{a}·{b} ÷ ({a} + {b}) = <b>{int(ans)}</b>."]
    opts, i = num_opts(int(ans), rng, step=2, minv=1, extra=[(a + b) // 2])
    return Q("problem", "Hareket problemleri", 3, q, opts, i, sol, "Ortalama hızı doğru tanımla hesaplar.", 60)


def t_percent(rng):
    v = rng.choice(["profit", "discount", "change"])
    if v == "profit":
        for _ in range(100):
            p = rng.choice([20, 25, 30, 40, 50, 60, 75, 80, 100])
            d = rng.choice([10, 15, 20, 25, 30, 40])
            r = (100 + p) * (100 - d) / 100 - 100
            if r == int(r) and r != 0:
                break
        else:
            return None
        r = int(r)
        word = "kâr" if r > 0 else "zarar"
        q = f"Bir mağaza bir ürünü maliyetinin %{p} fazlasına etiketlemiş, daha sonra etiket fiyatı üzerinden %{d} indirim yaparak satmıştır.<br>Mağaza bu satıştan yüzde kaç {word} etmiştir?"
        sol = [f"Maliyet 100 birim alınır. Etiket: {100 + p}.", f"İndirimli satış: {100 + p}·⟦{100 - d}/100⟧ = {100 + r}.", f"Maliyete göre {word}: %<b>{abs(r)}</b>."]
        opts, i = num_opts(abs(r), rng, step=rng.choice([1, 2, 5]), minv=1, extra=[abs(p - d)])
        opts = ["%" + o for o in opts]
        return Q("problem", "Kâr-zarar ve yüzde", 3, q, opts, i, sol, "Ardışık yüzde değişimlerini birleştirir.", 75)
    if v == "discount":
        price = rng.choice([200, 240, 320, 400, 480, 600, 800, 1200])
        d1, d2 = rng.choice([10, 20, 25]), rng.choice([10, 20, 25, 50])
        final = F(price) * (100 - d1) / 100 * (100 - d2) / 100
        if final.denominator != 1:
            return None
        q = f"Etiket fiyatı {price} TL olan bir ürüne önce %{d1}, ardından indirimli fiyat üzerinden %{d2} indirim uygulanıyor.<br>Ürünün son fiyatı kaç TL'dir?"
        sol = [f"İlk indirim sonrası: {price}·⟦{100 - d1}/100⟧ = {num(F(price) * (100 - d1) / 100)} TL.", f"İkinci indirim sonrası: <b>{int(final)}</b> TL."]
        opts, i = num_opts(int(final), rng, step=rng.choice([4, 8, 12]), minv=1, extra=[int(price * (100 - d1 - d2) / 100)])
        return Q("problem", "Kâr-zarar ve yüzde", 2, q, opts, i, sol, "Ardışık indirimi doğru tabana uygular.", 50)
    a = rng.choice([20, 25, 40, 50])
    b = rng.choice([20, 25, 40, 50])
    ch = (100 + a) * (100 - b) / 100 - 100
    if ch != int(ch) or ch == 0:
        return None
    ch = int(ch)
    q = f"Bir dikdörtgenin uzun kenarı %{a} artırılır, kısa kenarı %{b} azaltılırsa alanı yüzde kaç değişir?"
    word = "artar" if ch > 0 else "azalır"
    sol = [f"Kenarlar 10 ve 10 birim düşünülür (alan 100).", f"Yeni alan: {(100 + a) / 10:g}·{(100 - b) / 10:g} = {100 + ch}.", f"Alan %{abs(ch)} {word}."]
    correct = f"%{abs(ch)} {word}"
    wr = [f"%{abs(ch)} {'azalır' if ch > 0 else 'artar'}", f"%{abs(a - b) if a != b else abs(ch) + 5} {word}", f"%{abs(ch) + 5} {word}", f"%{abs(ch) + 10} {word}", "Değişmez"]
    opts, i = text_opts(correct, wr, rng)
    return Q("problem", "Kâr-zarar ve yüzde", 3, q, opts, i, sol, "Yüzde değişimlerin çarpımsal etkisini hesaplar.", 60)


def t_mixture(rng):
    v = rng.choice(["mix", "dilute"])
    if v == "mix":
        for _ in range(100):
            p1, p2 = rng.sample([10, 15, 20, 25, 30, 40, 50], 2)
            m1, m2 = rng.choice([100, 200, 300, 400]), rng.choice([100, 200, 300, 600])
            r = F(p1 * m1 + p2 * m2, m1 + m2)
            if r.denominator == 1:
                break
        else:
            return None
        q = f"Tuz oranı %{p1} olan {m1} gram tuzlu su ile tuz oranı %{p2} olan {m2} gram tuzlu su karıştırılıyor.<br>Elde edilen karışımın tuz oranı yüzde kaçtır?"
        sol = [f"Tuz miktarları: {m1}·⟦{p1}/100⟧ = {p1 * m1 // 100} g ve {m2}·⟦{p2}/100⟧ = {p2 * m2 // 100} g.",
               f"Oran: ({p1 * m1 // 100} + {p2 * m2 // 100}) ÷ {m1 + m2} = %<b>{int(r)}</b>."]
        opts, i = num_opts(int(r), rng, minv=1, extra=[(p1 + p2) // 2])
        return Q("problem", "Karışım problemleri", 3, q, [f"%{o}" for o in opts], i, sol, "Karışımda madde miktarını korur.", 75)
    p = rng.choice([20, 25, 30, 40, 50])
    m = rng.choice([200, 300, 400, 600])
    t = rng.choice([x for x in [10, 12, 15, 20, 25] if x < p])
    w = F(p * m, t) - m
    if w.denominator != 1:
        return None
    q = f"Şeker oranı %{p} olan {m} gram şekerli suya kaç gram saf su eklenirse şeker oranı %{t} olur?"
    sol = [f"Şeker miktarı değişmez: {m}·⟦{p}/100⟧ = {p * m // 100} g.", f"{p * m // 100} ÷ ({m} + x) = ⟦{t}/100⟧ ⇒ x = <b>{int(w)}</b>."]
    opts, i = num_opts(int(w), rng, step=rng.choice([20, 25, 50]), minv=10)
    return Q("problem", "Karışım problemleri", 3, q, opts, i, sol, "Seyreltmede çözünen miktarının sabitliğini kullanır.", 75)


def t_interest(rng):
    A = rng.choice([10000, 20000, 25000, 40000, 50000, 60000])
    r = rng.choice([12, 18, 24, 30, 36, 40])
    n = rng.choice([3, 4, 6, 8, 9, 10])
    I = F(A * r * n, 1200)
    if I.denominator != 1:
        return None
    ask = rng.choice(["faiz", "toplam"])
    ans = int(I) if ask == "faiz" else A + int(I)
    q = f"{A} TL, yıllık %{r} basit faiz oranıyla {n} aylığına bankaya yatırılıyor.<br>Süre sonunda " + ("elde edilen faiz kaç TL'dir?" if ask == "faiz" else "hesapta toplam kaç TL olur?")
    sol = [f"Basit faiz: F = A·r·t / 1200 (t ay).", f"F = {A}·{r}·{n} / 1200 = {int(I)} TL."] + ([f"Toplam: {A} + {int(I)} = <b>{ans}</b> TL."] if ask == "toplam" else [f"Faiz: <b>{ans}</b> TL."])
    opts, i = num_opts(ans, rng, step=rng.choice([500, 1000, 200]), minv=1, extra=[ans + int(I)])
    return Q("problem", "Faiz problemleri", 2, q, opts, i, sol, "Basit faiz formülünü ay cinsinden uygular.", 50)


def t_number_problem(rng):
    v = rng.choice(["three", "tickets"])
    if v == "three":
        x = rng.randint(5, 30)
        d = rng.randint(2, 9)
        k = rng.choice([2, 3])
        nums = [x, x + d, k * x]
        S = sum(nums)
        q = f"Üç sayıdan ikincisi birincisinden {d} fazla, üçüncüsü birincisinin {k} katıdır. Bu üç sayının toplamı {S} olduğuna göre en büyük sayı kaçtır?"
        ans = max(nums)
        sol = [f"Birinci sayı x: x + (x + {d}) + {k}x = {S}.", f"{k + 2}x = {S - d} ⇒ x = {x}.", f"Sayılar {nums[0]}, {nums[1]}, {nums[2]}; en büyüğü <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, minv=1, extra=[x, x + d])
        return Q("problem", "Sayı problemleri", 2, q, opts, i, sol, "Sözel ifadeyi denkleme çevirir.", 60)
    a, b = rng.choice([(30, 45), (40, 60), (25, 40), (50, 80), (60, 90)])
    n = rng.randint(10, 40)
    s = rng.randint(1, n - 1)
    T = s * a + (n - s) * b
    q = f"Bir tiyatroda öğrenci bileti {a} TL, tam bilet {b} TL'dir. Bir gösteri için satılan {n} biletten toplam {T} TL gelir elde edilmiştir.<br>Kaç öğrenci bileti satılmıştır?"
    sol = [f"Hepsi tam bilet olsaydı gelir {n * b} TL olurdu.", f"Fark: {n * b} − {T} = {n * b - T}; her öğrenci bileti farkı {b - a} TL azaltır.", f"Öğrenci bileti: {n * b - T} ÷ {b - a} = <b>{s}</b>."]
    opts, i = num_opts(s, rng, minv=0, maxv=n, extra=[n - s])
    return Q("problem", "Sayı problemleri", 2, q, opts, i, sol, "Varsayım yöntemiyle hızlı çözüm üretir.", 60)


# ---------------------------------------------------------------- İŞLEM / MODÜLER / FONKSİYON

def t_defined_op(rng):
    p, q2, r = rng.randint(1, 3), rng.randint(-3, 3), rng.randint(-2, 3)
    if q2 == 0:
        return None
    def op(a, b):
        return p * a * b + q2 * a + r * b
    def tt(c, v):
        if c == 0:
            return ""
        return f" {'+' if c > 0 else '−'} {'' if abs(c) == 1 else abs(c)}{v}"
    defn = f"{'' if p == 1 else p}a·b{tt(q2, 'a')}{tt(r, 'b')}"
    x, y, z = rng.randint(-2, 4), rng.randint(-2, 4), rng.randint(-2, 3)
    inner = op(x, y)
    ans = op(inner, z)
    q = f"Gerçel sayılar kümesi üzerinde ∗ işlemi<br>a ∗ b = {defn}<br>biçiminde tanımlanıyor.<br>Buna göre ({x} ∗ {y}) ∗ {z} işleminin sonucu kaçtır?".replace("(-", "(−").replace(" -", " −")
    sol = [f"Önce parantez: {x} ∗ {y} = {inner}.", f"Sonra {inner} ∗ {z} = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=rng.choice([1, 2, 3]), extra=[op(x, op(y, z))])
    return Q("islem", "Tanımlı işlemler", 2, q, opts, i, sol, "Yeni tanımlanan işlemi kurala uygun uygular.", 50)


def t_piecewise_op(rng):
    a_, b_ = rng.randint(2, 4), rng.randint(1, 5)
    def op(x, y):
        return x - y if x >= y else a_ * y - x + b_
    x, y, z = [rng.randint(1, 12) for _ in range(3)]
    ans = op(op(x, y), z)
    q = f"x ve y doğal sayılar olmak üzere Δ işlemi<br>x ≥ y ise x Δ y = x − y,<br>x &lt; y ise x Δ y = {a_}y − x + {b_}<br>olarak tanımlanıyor.<br>Buna göre ({x} Δ {y}) Δ {z} kaçtır?"
    sol = [f"{x} {'≥' if x >= y else '&lt;'} {y} olduğundan {x} Δ {y} = {op(x, y)}.",
           f"{op(x, y)} {'≥' if op(x, y) >= z else '&lt;'} {z} olduğundan sonuç <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, minv=0)
    return Q("islem", "Tanımlı işlemler", 3, q, opts, i, sol, "Koşullu tanımlı işlemde doğru kuralı seçer.", 60)


def t_days(rng):
    start = rng.randrange(7)
    n = rng.randint(40, 400)
    end = (start + n) % 7
    q = f"Bugün günlerden {DAYS[start]} olduğuna göre bugünden {n} gün sonra hangi gündür?"
    sol = [f"Haftanın günleri 7'lik döngüdür: {n} = 7·{n // 7} + {n % 7}.", f"{DAYS[start]} gününden {n % 7} gün sonra: <b>{DAYS[end]}</b>."]
    wr = [DAYS[(end + k) % 7] for k in (1, -1, 2, -2, 3)]
    opts, i = text_opts(DAYS[end], wr, rng)
    return Q("islem", "Modüler aritmetik", 1, q, opts, i, sol, "Periyodik durumlarda mod 7 hesabı yapar.", 40)


def t_last_digit(rng):
    b = rng.choice([2, 3, 7, 8, 9, 4, 13, 17])
    n = rng.randint(20, 300)
    m = rng.choice([10, 5])
    ans = pow(b, n, m)
    cyc = []
    v = 1
    for _ in range(8):
        v = v * b % m
        if v in cyc:
            break
        cyc.append(v)
    q = f"{b}<sup>{n}</sup> sayısının {'birler basamağındaki rakam' if m == 10 else '5 ile bölümünden kalan'} kaçtır?"
    sol = [f"{nsuf(b, 'gen')} kuvvetlerinin {'birler basamağı' if m == 10 else '5 ile kalanı'} döngüsü: {', '.join(map(str, cyc))} (uzunluk {len(cyc)}).",
           f"{n} ≡ {n % len(cyc) or len(cyc)} (mod {len(cyc)}) ⇒ sonuç <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, minv=0, maxv=9 if m == 10 else 4)
    return Q("islem", "Modüler aritmetik", 3, q, opts, i, sol, "Kuvvetlerde kalan döngüsünü kullanır.", 60)


def t_mod_count(rng):
    m = rng.randint(4, 13)
    r = rng.randrange(m)
    lo, hi = rng.choice([(10, 99), (100, 999), (50, 150), (100, 300)])
    ans = sum(1 for x in range(lo, hi + 1) if x % m == r)
    rng_txt = {(10, 99): "iki basamaklı", (100, 999): "üç basamaklı"}.get((lo, hi), f"{lo} ile {hi} arasındaki (sınırlar dahil)")
    q = f"{m} ile bölümünden kalan {r} olan {rng_txt} kaç doğal sayı vardır?"
    first = next(x for x in range(lo, hi + 1) if x % m == r)
    last = max(x for x in range(lo, hi + 1) if x % m == r)
    sol = [f"İlk sayı {first}, son sayı {last}; sayılar {nsuf(m, 'er')} artar.", f"Terim sayısı: ({last} − {first}) ÷ {m} + 1 = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, minv=1)
    return Q("islem", "Modüler aritmetik", 2, q, opts, i, sol, "Belirli kalanı veren sayıları sayar.", 50)


def t_function(rng):
    v = rng.choice(["lin", "comp"])
    if v == "lin":
        a, b = rng.randint(2, 5), rng.randint(-4, 6)
        c, d = rng.randint(-5, 7), rng.randint(1, 4)
        k = rng.randint(-3, 9)
        # f(cx + d) = a x + b ; f(k) = ?
        x = F(k - d, c) if c else None
        if c == 0 or x.denominator != 1:
            return None
        ans = a * int(x) + b
        q = f"f(" + (f"{c}x" if c != 1 else "x") + f" + {d}) = {a}x {'+' if b >= 0 else '−'} {abs(b)}<br>olduğuna göre f({k}) kaçtır?"
        q = q.replace("f(-", "f(−").replace("(−1x", "(−x")
        sol = [f"İç ifade {nsuf(k, 'dat')} eşitlenir: {c}x + {d} = {k} ⇒ x = {int(x)}.", f"f({k}) = {a}·({int(x)}) {'+' if b >= 0 else '−'} {abs(b)} = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=rng.choice([1, 2]), extra=[a * k + b])
        return Q("islem", "Fonksiyonlar", 2, q, opts, i, sol, "Fonksiyonda iç ifadeyi eşitleyerek değer bulur.", 50)
    a, b, c, d = rng.randint(1, 4), rng.randint(-3, 5), rng.randint(1, 3), rng.randint(-4, 4)
    k = rng.randint(-2, 4)
    ans = a * (c * k + d) + b
    q = f"f(x) = {a}x {'+' if b >= 0 else '−'} {abs(b)} ve g(x) = {c}x {'+' if d >= 0 else '−'} {abs(d)}<br>olduğuna göre (f ∘ g)({k}) kaçtır?".replace("= 1x", "= x")
    sol = [f"Önce g({k}) = {c * k + d}.", f"Sonra f({c * k + d}) = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, extra=[c * (a * k + b) + d])
    return Q("islem", "Fonksiyonlar", 2, q, opts, i, sol, "Bileşke fonksiyonu içten dışa hesaplar.", 45)


def t_clock(rng):
    h = rng.randint(6, 11)
    mins = rng.randint(200, 1500)
    tot = (h * 60 + mins) % (24 * 60)
    ans = f"{tot // 60:02d}.{tot % 60:02d}"
    q = f"Saat {h:02d}.00'da başlayan bir çalışma {mins} dakika sürmüştür.<br>Çalışma saat kaçta bitmiştir?"
    sol = [f"{mins} dakika = {mins // 60} saat {mins % 60} dakika.", f"{h:02d}.00 + {mins // 60} sa {mins % 60} dk = <b>{ans}</b> (24 saat düzeni)."]
    wr = set()
    for d in (-60, 60, -10, 10, 120, -120, 30):
        t2 = (tot + d) % 1440
        wr.add(f"{t2 // 60:02d}.{t2 % 60:02d}")
    wr.discard(ans)
    lst = sorted(wr)
    rng.shuffle(lst)
    opts = sorted(lst[:4] + [ans])
    return Q("islem", "Modüler aritmetik", 1, q, opts, opts.index(ans), sol, "Zaman hesabında 60 ve 24'lük döngüleri kullanır.", 40)


# ---------------------------------------------------------------- SAYMA / OLASILIK

WORDS = ["KALEM", "DEFTER", "KİTAP", "ÇANTA", "OKUL", "BULUT", "SINAV", "MASA", "ROMAN", "HARİTA"]
VOWELS = set("AEIİOÖUÜ")


def t_perm_word(rng):
    w = rng.choice(WORDS)
    letters = list(w)
    cond = rng.choice(["none", "vowels_together", "start_consonant", "ends_vowel"])
    perms = set(itertools.permutations(letters))
    def ok(p):
        if cond == "vowels_together":
            idx = [i for i, ch in enumerate(p) if ch in VOWELS]
            return max(idx) - min(idx) == len(idx) - 1
        if cond == "start_consonant":
            return p[0] not in VOWELS
        if cond == "ends_vowel":
            return p[-1] in VOWELS
        return True
    ans = sum(1 for p in perms if ok(p))
    ctext = {"none": "", "vowels_together": " ve sesli harflerin hepsi yan yana bulunan", "start_consonant": " ve sessiz harfle başlayan", "ends_vowel": " ve sesli harfle biten"}[cond]
    q = f"{w} kelimesinin harflerinin tümü kullanılarak yazılabilecek{ctext} {len(letters)} harfli anlamlı ya da anlamsız kaç farklı kelime vardır?"
    rep = len(letters) != len(set(letters))
    sol = [f"Harfler: {', '.join(letters)}" + (" (tekrar eden harf var; tekrar sayısının faktöriyeline bölünür)." if rep else "."),
           {"none": "Tüm sıralamalar sayılır.", "vowels_together": "Sesli harfler tek blok kabul edilir, blok ve kalan harfler sıralanır; blok içi de sıralanır.",
            "start_consonant": "İlk harf sessizlerden seçilir, kalanlar sıralanır.", "ends_vowel": "Son harf seslilerden seçilir, kalanlar sıralanır."}[cond],
           f"Sonuç: <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=max(1, ans // 6), minv=1, extra=[math.factorial(len(letters))])
    return Q("sayma", "Permütasyon", 2 if cond == "none" else 3, q, opts, i, sol, "Koşullu sıralamaları sayar.", 75)


def t_committee(rng):
    m, f = rng.randint(4, 8), rng.randint(3, 6)
    k = rng.randint(3, 5)
    if k > m + f - 1:
        return None
    least = rng.randint(1, min(f, k) - 0)
    ans = sum(math.comb(f, j) * math.comb(m, k - j) for j in range(least, min(f, k) + 1))
    q = f"{m} erkek ve {f} kadın arasından en az {least} kadının bulunduğu {k} kişilik bir ekip kaç farklı biçimde seçilebilir?"
    terms = [f"C({f},{j})·C({m},{k - j})" for j in range(least, min(f, k) + 1) if k - j <= m]
    sol = ["'En az' koşulu durumlara ayrılarak (ya da tümünden istenmeyen çıkarılarak) sayılır.", " + ".join(terms) + f" = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=max(1, ans // 8), minv=1, extra=[math.comb(m + f, k)])
    return Q("sayma", "Kombinasyon", 3, q, opts, i, sol, "Koşullu seçimlerde durumlara ayırır.", 75)


def t_digits_count(rng):
    digs = sorted(rng.sample(range(0, 10), rng.choice([5, 6])))
    n = 3
    cond = rng.choice(["çift", "tek", "5 ile bölünebilen", "400'den büyük"])
    cnt = 0
    for p in itertools.permutations(digs, n):
        if p[0] == 0:
            continue
        v = int("".join(map(str, p)))
        if cond == "çift" and v % 2:
            continue
        if cond == "tek" and v % 2 == 0:
            continue
        if cond == "5 ile bölünebilen" and v % 5:
            continue
        if cond == "400'den büyük" and v <= 400:
            continue
        cnt += 1
    if cnt == 0:
        return None
    q = f"{{{', '.join(map(str, digs))}}} kümesinin elemanları kullanılarak rakamları birbirinden farklı üç basamaklı kaç {cond} sayı yazılabilir?".replace("kaç 400'den büyük sayı", "kaç tane 400'den büyük sayı")
    sol = ["Önce kısıtlı basamaklar (birler basamağı / yüzler basamağı, 0'ın başta olamaması) yerleştirilir.", "Gerekirse 0'ın birler basamağında olup olmadığına göre durumlara ayrılır.", f"Sonuç: <b>{cnt}</b>."]
    opts, i = num_opts(cnt, rng, step=rng.choice([2, 3, 4]), minv=1)
    return Q("sayma", "Sayma yöntemleri", 3, q, opts, i, sol, "Çarpma ilkesini kısıtlarla uygular.", 75)


def t_prob_balls(rng):
    r, b = rng.randint(2, 7), rng.randint(2, 7)
    g = rng.choice([0, 0, 2, 3])
    tot = r + b + g
    ev = rng.choice(["aynı renk", "farklı renk", "ikisi de kırmızı", "en az biri mavi"])
    pairs = math.comb(tot, 2)
    if ev == "aynı renk":
        fav = math.comb(r, 2) + math.comb(b, 2) + math.comb(g, 2)
    elif ev == "farklı renk":
        fav = pairs - (math.comb(r, 2) + math.comb(b, 2) + math.comb(g, 2))
    elif ev == "ikisi de kırmızı":
        fav = math.comb(r, 2)
    else:
        fav = pairs - math.comb(tot - b, 2)
    P = F(fav, pairs)
    gtxt = f", {g} yeşil" if g else ""
    q = f"Bir torbada {r} kırmızı, {b} mavi{gtxt} top vardır. Torbadan rastgele aynı anda iki top çekiliyor.<br>Çekilen topların <b>{ev}</b> olma olasılığı kaçtır?"
    sol = [f"Tüm durumlar: C({tot},2) = {pairs}.", f"İstenen durumlar: {fav}.", f"Olasılık: ⟦{fav}/{pairs}⟧ = <b>{frs(P)}</b>."]
    opts, i = num_opts(P, rng, step=F(1, P.denominator), minv=F(1, 100), maxv=F(99, 100))
    return Q("sayma", "Olasılık", 3, q, opts, i, sol, "Kombinasyonla olasılık hesaplar.", 75)


def t_prob_dice(rng):
    v = rng.choice(["sum", "ge", "prod_even", "diff"])
    outs = [(a, b) for a in range(1, 7) for b in range(1, 7)]
    if v == "sum":
        s = rng.randint(4, 10)
        fav = [o for o in outs if sum(o) == s]
        ev = f"üst yüzlerindeki sayıların toplamının {s} olma"
    elif v == "ge":
        s = rng.randint(8, 10)
        fav = [o for o in outs if sum(o) >= s]
        ev = f"üst yüzlerindeki sayıların toplamının en az {s} olma"
    elif v == "prod_even":
        fav = [o for o in outs if o[0] * o[1] % 2 == 0]
        ev = "üst yüzlerindeki sayıların çarpımının çift olma"
    else:
        d = rng.randint(1, 3)
        fav = [o for o in outs if abs(o[0] - o[1]) == d]
        ev = f"üst yüzlerindeki sayılar arasındaki farkın {d} olma"
    P = F(len(fav), 36)
    q = f"İki hilesiz zar birlikte atılıyor.<br>Zarların {ev} olasılığı kaçtır?"
    sol = ["Tüm durumlar: 6·6 = 36.", f"Uygun durum sayısı: {len(fav)}.", f"Olasılık: ⟦{len(fav)}/36⟧ = <b>{frs(P)}</b>."]
    opts, i = num_opts(P, rng, step=F(1, 36), minv=F(1, 36), maxv=F(35, 36))
    return Q("sayma", "Olasılık", 2, q, opts, i, sol, "Örnek uzayı listeleyerek olasılık bulur.", 60)


def t_count_misc(rng):
    v = rng.choice(["hand", "circle", "grid"])
    if v == "hand":
        n = rng.randint(6, 20)
        ans = math.comb(n, 2)
        q = f"Bir toplantıdaki {n} kişinin her biri diğerleriyle birer kez tokalaşıyor.<br>Toplam kaç tokalaşma olur?"
        sol = ["Her tokalaşma iki kişilik bir seçimdir.", f"C({n},2) = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=n // 2, minv=1, extra=[n * (n - 1)])
        return Q("sayma", "Kombinasyon", 1, q, opts, i, sol, "Eşleşme sayısını kombinasyonla bulur.", 40)
    if v == "circle":
        n = rng.randint(4, 7)
        tog = rng.choice([True, False])
        ans = math.factorial(n - 2) * 2 if tog else math.factorial(n - 1)
        q = f"{n} kişi yuvarlak bir masa etrafına " + ("belirli iki kişi yan yana oturmak koşuluyla " if tog else "") + "kaç farklı biçimde oturabilir?"
        sol = (["Yan yana olacak iki kişi tek kişi gibi düşünülür: {} birim dairesel sıralanır: ({} − 1)!.".format(n - 1, n - 1), f"Kendi aralarında 2! ⇒ {math.factorial(n - 2)}·2 = <b>{ans}</b>."] if tog
               else ["Dairesel sıralamada biri sabitlenir: (n − 1)!.", f"({n} − 1)! = <b>{ans}</b>."])
        opts, i = num_opts(ans, rng, step=max(1, ans // 4), minv=1, extra=[math.factorial(n)])
        return Q("sayma", "Permütasyon", 2, q, opts, i, sol, "Dairesel permütasyon uygular.", 50)
    a, b = rng.randint(2, 5), rng.randint(2, 5)
    ans = math.comb(a + b, a)
    q = f"{a} birim doğuya ve {b} birim kuzeye gidilmesi gereken kareli bir şehir planında, yalnızca doğu ve kuzey yönünde hareket ederek en kısa yoldan kaç farklı biçimde gidilebilir?"
    sol = [f"Toplam {a + b} adımın {a} tanesi doğu olacaktır.", f"C({a + b},{a}) = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=max(1, ans // 6), minv=1, extra=[a * b, (a + b) * 2])
    return Q("sayma", "Sayma yöntemleri", 2, q, opts, i, sol, "En kısa yol sayısını kombinasyonla bulur.", 50)


# ---------------------------------------------------------------- SAYISAL MANTIK

def t_sequence(rng):
    v = rng.choice(["arith2", "geo", "diff2", "interleave", "fib", "mulAdd"])
    if v == "arith2":
        a, d = rng.randint(1, 20), rng.randint(2, 9)
        seq = [a + d * i for i in range(6)]
        rule = f"Her terim bir öncekinden {d} fazladır."
    elif v == "geo":
        a, r = rng.randint(1, 5), rng.choice([2, 3])
        seq = [a * r ** i for i in range(6)]
        rule = f"Her terim bir öncekinin {r} katıdır."
    elif v == "diff2":
        a, d, e = rng.randint(1, 10), rng.randint(1, 4), rng.randint(1, 3)
        seq = [a]
        for i in range(5):
            seq.append(seq[-1] + d + e * i)
        rule = f"Ardışık farklar {d}, {d + e}, {d + 2 * e}, … biçiminde {nsuf(e, 'er')} artar."
    elif v == "interleave":
        a, d, b, f = rng.randint(1, 10), rng.randint(2, 5), rng.randint(20, 40), rng.randint(1, 4)
        seq = []
        for i in range(3):
            seq += [a + d * i, b - f * i]
        rule = f"Tek sıradaki terimler {nsuf(d, 'er')} artar, çift sıradakiler {nsuf(f, 'er')} azalır (iç içe iki dizi)."
    elif v == "fib":
        a, b = rng.randint(1, 5), rng.randint(2, 7)
        seq = [a, b]
        for _ in range(4):
            seq.append(seq[-1] + seq[-2])
        rule = "Her terim kendinden önceki iki terimin toplamıdır."
    else:
        m, c = rng.choice([2, 3]), rng.choice([-1, 1, 2, -2])
        seq = [rng.randint(1, 4)]
        for _ in range(5):
            seq.append(seq[-1] * m + c)
        rule = f"Her terim bir öncekinin {m} katının {abs(c)} {'fazlasıdır' if c > 0 else 'eksiğidir'}."
    pos = rng.choice([4, 5])
    ans = seq[pos]
    shown = [str(x) if i != pos else "?" for i, x in enumerate(seq[:pos + 1])]
    if pos == 4:
        shown.append(str(seq[5]))
    q = "Aşağıdaki sayı dizisinde ? yerine gelmesi gereken sayı kaçtır?<br><span class='seq'>" + ", ".join(shown) + "</span>"
    sol = [rule, f"Buna göre ? = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=rng.choice([1, 2, 3]))
    return Q("saymantik", "Sayı dizileri", 2 if v in ("arith2", "geo") else 3, q, opts, i, sol, "Dizideki örüntüyü bulur.", 50)


def t_machine(rng):
    rules = [
        ("çift ise yarısını, tek ise 3 katının 1 fazlasını", lambda n: n // 2 if n % 2 == 0 else 3 * n + 1),
        ("3'e bölünüyorsa 3'e bölümünü, bölünmüyorsa 2 fazlasını", lambda n: n // 3 if n % 3 == 0 else n + 2),
        ("10'dan büyükse rakamları toplamını, değilse 4 katını", lambda n: sum(map(int, str(n))) if n > 10 else 4 * n),
        ("çift ise 1 eksiğini, tek ise 2 katını", lambda n: n - 1 if n % 2 == 0 else 2 * n),
    ]
    txt, f = rng.choice(rules)
    x = rng.randint(3, 30)
    k = rng.randint(3, 6)
    vals = [x]
    for _ in range(k):
        vals.append(f(vals[-1]))
    ans = vals[-1]
    q = f"Bir makineye girilen sayı {txt} çıktı olarak vermektedir. Her çıktı yeniden makineye giriliyor.<br>Makineye ilk olarak {x} girildiğine göre {k}. çıktı kaçtır?"
    sol = ["Kural adım adım uygulanır: " + " → ".join(map(str, vals)) + ".", f"{k}. çıktı: <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, extra=[vals[-2]] if vals[-2] != ans else [], minv=0)
    return Q("saymantik", "Koşullu işlemler", 2, q, opts, i, sol, "Koşullu kuralı ardışık uygular.", 60)


TR_ALPHA = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"


def t_cipher(rng):
    k = rng.randint(2, 5)
    w = rng.choice(["KALEM", "SINAV", "ROMAN", "BULUT", "DENİZ", "GÜNEŞ", "ÇİÇEK", "KÖPRÜ", "ORMAN", "YILDIZ"])
    def enc(word, s):
        return "".join(TR_ALPHA[(TR_ALPHA.index(c) + s) % 29] for c in word)
    ans = enc(w, k)
    wr = [enc(w, k + 1), enc(w, k - 1), enc(w, -k), enc(w[::-1], k), enc(w, k)[:-1] + enc(w, k + 1)[-1]]
    opts, i = text_opts(ans, wr, rng)
    q = f"Bir şifreleme sisteminde, Türk alfabesindeki (29 harf) her harf, alfabede kendisinden {k} sonra gelen harfle değiştirilmektedir (Z'den sonra A'ya dönülür).<br>Buna göre <b>{w}</b> kelimesinin şifrelenmiş hâli aşağıdakilerden hangisidir?"
    sol = ["Alfabe: " + " ".join(TR_ALPHA) + ".", f"Her harf {k} sağa kaydırılır: " + ", ".join(f"{c}→{enc(c, k)}" for c in w) + ".", f"Sonuç: <b>{ans}</b>."]
    return Q("saymantik", "Şifreleme", 2, q, opts, i, sol, "Kurala dayalı kodlama yapar.", 60)


def g_parking(rng, gid):
    first = rng.choice([30, 40, 50])
    step_min = rng.choice([30, 60])
    step_fee = rng.choice([10, 15, 20])
    cap = rng.choice([150, 180, 200, 240])
    def fee(minutes):
        if minutes <= 60:
            return first
        extra = math.ceil((minutes - 60) / step_min)
        return min(cap, first + extra * step_fee)
    info = (f"Bir otoparkın ücret tarifesi şöyledir:<ul><li>İlk 1 saat (ve daha kısa süreler) için {first} TL alınır.</li>"
            f"<li>1 saatten sonraki her {'yarım saat' if step_min == 30 else 'saat'} ya da bu sürenin bir kısmı için {step_fee} TL eklenir.</li>"
            f"<li>Bir aracın günlük ödeyeceği ücret {cap} TL'yi geçemez.</li></ul>")
    group = {"id": gid, "info": info}
    out = []
    m1 = rng.choice([150, 170, 200, 225, 250])
    a1 = fee(m1)
    out.append(Q("saymantik", "Kural tabanlı ortak bilgi", 2, f"Otoparkta {m1 // 60} saat {m1 % 60} dakika kalan bir araç kaç TL öder?", *num_opts(a1, rng, step=step_fee, minv=first),
                 [f"İlk saat {first} TL; kalan {m1 - 60} dakika {math.ceil((m1 - 60) / step_min)} adet {step_min} dakikalık dilim eder.", f"{first} + {math.ceil((m1 - 60) / step_min)}·{step_fee} = <b>{a1}</b> TL (tavan {cap} TL aşılmıyor)."],
                 "Kademeli ücret kuralını uygular.", 60, group=group))
    k = next(m for m in range(60, 3000) if fee(m) == cap)
    hrs = F(k, 60)
    out.append(Q("saymantik", "Kural tabanlı ortak bilgi", 3, "Bir aracın ödediği ücretin günlük üst sınıra ilk kez ulaşması için otoparkta en az kaç dakikadan fazla kalması gerekir?",
                 *num_opts(k - 1, rng, step=step_min, minv=60),
                 [f"Üst sınır için gereken ek dilim sayısı: ⌈({cap} − {first}) ÷ {step_fee}⌉ = {math.ceil((cap - first) / step_fee)}.",
                  f"Bu dilim, {60 + (math.ceil((cap - first) / step_fee) - 1) * step_min} dakikadan fazla kalındığında başlar; yani <b>{k - 1}</b> dakikadan fazla kalmak gerekir."],
                 "Kuraldan eşik değeri çıkarır.", 90, group=group))
    a, b = rng.choice([(45, 130), (90, 200), (61, 121), (100, 320)])
    tot = fee(a) + fee(b)
    out.append(Q("saymantik", "Kural tabanlı ortak bilgi", 3, f"Biri {a} dakika, diğeri {b} dakika park eden iki aracın ödediği toplam ücret kaç TL'dir?",
                 *num_opts(tot, rng, step=step_fee, minv=first * 2),
                 [f"{a} dk ⇒ {fee(a)} TL; {b} dk ⇒ {fee(b)} TL.", f"Toplam: <b>{tot}</b> TL."], "Kuralı farklı durumlara uygular.", 60, group=group))
    return out


def g_tournament(rng, gid):
    teams = rng.sample(["Kartal", "Aslan", "Kurt", "Şahin", "Kaplan", "Yunus"], 4)
    w, d = 3, 1
    games = list(itertools.combinations(range(4), 2))
    while True:
        res = [rng.choice(["1", "X", "2"]) for _ in games]
        pts = [0] * 4
        wins = [0] * 4
        for (i, j), r in zip(games, res):
            if r == "1":
                pts[i] += 3; wins[i] += 1
            elif r == "2":
                pts[j] += 3; wins[j] += 1
            else:
                pts[i] += 1; pts[j] += 1
        if len(set(pts)) == 4:
            break
    rows = "".join(f"<tr><td>{teams[i]}</td><td>{teams[j]}</td><td>{'Galibiyet: ' + teams[i] if r == '1' else ('Galibiyet: ' + teams[j] if r == '2' else 'Beraberlik')}</td></tr>" for (i, j), r in zip(games, res))
    info = (f"Dört takımın katıldığı bir turnuvada her takım diğerleriyle birer maç yapmıştır. Galibiyete 3, beraberliğe 1, yenilgiye 0 puan verilmektedir. Maç sonuçları tabloda verilmiştir."
            f"<table class='qt'><tr><th>Ev</th><th>Konuk</th><th>Sonuç</th></tr>{rows}</table>")
    group = {"id": gid, "info": info}
    order = sorted(range(4), key=lambda i: -pts[i])
    out = []
    wr = [t for t in teams if t != teams[order[0]]] + ["Belirlenemez"]
    opts, i = text_opts(teams[order[0]], wr, rng)
    out.append(Q("saymantik", "Tablo yorumlama", 2, "Turnuvayı en yüksek puanla tamamlayan takım hangisidir?", opts, i,
                 ["Puanlar: " + ", ".join(f"{teams[k]} {pts[k]}" for k in range(4)) + ".", f"En yüksek puan: <b>{teams[order[0]]}</b>."], "Tablodan puan hesaplar.", 60, group=group))
    tot = sum(pts)
    draws = res.count("X")
    out.append(Q("saymantik", "Tablo yorumlama", 2, "Turnuvada tüm takımların topladığı puanların toplamı kaçtır?", *num_opts(tot, rng, minv=1, extra=[18]),
                 [f"Galibiyetli her maç 3, berabere biten her maç 2 puan dağıtır.", f"{6 - draws}·3 + {draws}·2 = <b>{tot}</b>."], "Toplam puanı maç türlerinden hesaplar.", 45, group=group))
    diff = pts[order[0]] - pts[order[3]]
    out.append(Q("saymantik", "Tablo yorumlama", 2, "Birinci ile sonuncu takım arasındaki puan farkı kaçtır?", *num_opts(diff, rng, minv=0),
                 [f"Birinci {teams[order[0]]}: {pts[order[0]]}; sonuncu {teams[order[3]]}: {pts[order[3]]}.", f"Fark: <b>{diff}</b>."], "Sıralama ve fark hesabı yapar.", 45, group=group))
    return out


# ---------------------------------------------------------------- VERİ / TABLO / GRAFİK (ortak bilgi grupları)

def svg_bar(labels, values, unit):
    W, H, pad = 340, 200, 30
    mx = max(values) * 1.15
    bw = (W - 2 * pad) / len(values)
    bars = []
    for k, (lab, v) in enumerate(zip(labels, values)):
        h = (H - 2 * pad) * v / mx
        x = pad + k * bw + bw * 0.18
        y = H - pad - h
        bars.append(f"<rect x='{x:.1f}' y='{y:.1f}' width='{bw * 0.64:.1f}' height='{h:.1f}' rx='3' class='bar'/>"
                    f"<text x='{x + bw * 0.32:.1f}' y='{y - 4:.1f}' class='bv'>{v}</text>"
                    f"<text x='{x + bw * 0.32:.1f}' y='{H - pad + 14:.1f}' class='bl'>{lab}</text>")
    return (f"<svg viewBox='0 0 {W} {H}' class='qchart' role='img' aria-label='Sütun grafiği'>"
            f"<line x1='{pad}' y1='{H - pad}' x2='{W - pad}' y2='{H - pad}' class='ax'/>{''.join(bars)}"
            f"<text x='{pad}' y='14' class='bl' text-anchor='start'>({unit})</text></svg>")


def g_table_sales(rng, gid):
    branches = rng.sample(["Merkez", "Kuzey", "Güney", "Doğu", "Batı", "Sahil"], 4)
    months = ["Ocak", "Şubat", "Mart"]
    item = rng.choice([("kitap", "adet"), ("bilet", "adet"), ("abonelik", "adet")])
    while True:
        data = [[rng.randrange(40, 200, 10) for _ in months] for _ in branches]
        totals = [sum(r) for r in data]
        febsum = sum(r[1] for r in data)
        if len(set(totals)) == 4 and febsum % 20 == 0:
            break
    rows = "".join(f"<tr><td>{b}</td>" + "".join(f"<td>{v}</td>" for v in r) + "</tr>" for b, r in zip(branches, data))
    info = (f"Tabloda bir şirketin dört şubesinde üç ayda satılan {item[0]} sayıları ({item[1]}) verilmiştir."
            f"<table class='qt'><tr><th>Şube</th>{''.join(f'<th>{m}</th>' for m in months)}</tr>{rows}</table>")
    group = {"id": gid, "info": info}
    out = []
    best = branches[totals.index(max(totals))]
    opts, i = text_opts(best, [b for b in branches if b != best] + ["Hepsi eşit"], rng)
    out.append(Q("veri", "Tablo yorumlama", 1, "Üç aylık toplam satışı en fazla olan şube hangisidir?", opts, i,
                 ["Toplamlar: " + ", ".join(f"{b} {t}" for b, t in zip(branches, totals)) + ".", f"En fazla: <b>{best}</b>."], "Tablodan toplam karşılaştırır.", 45, group=group))
    k = rng.randrange(4)
    share = F(data[k][1] * 100, febsum)
    if share.denominator == 1:
        o, i = num_opts(int(share), rng, step=rng.choice([2, 5]), minv=1)
        out.append(Q("veri", "Tablo yorumlama", 2, f"Şubat ayında {branches[k]} şubesinin satışı, o ayki toplam satışın yüzde kaçıdır?", ["%" + x for x in o], i,
                     [f"Şubat toplamı: {febsum}.", f"{data[k][1]} ÷ {febsum} · 100 = %<b>{int(share)}</b>."], "Parça–bütün yüzdesini hesaplar.", 60, group=group))
    else:
        avg = F(sum(data[k]), 3)
        val = avg if avg.denominator == 1 else F(sum(data[k]))
        txt = f"{branches[k]} şubesinin aylık ortalama satışı kaçtır?" if avg.denominator == 1 else f"{branches[k]} şubesinin üç aylık toplam satışı kaçtır?"
        out.append(Q("veri", "Tablo yorumlama", 1, txt, *num_opts(int(val), rng, step=10, minv=1), [f"{' + '.join(map(str, data[k]))} = " + (f"{sum(data[k])}; ÷ 3 = <b>{int(val)}</b>." if avg.denominator == 1 else f"<b>{sum(data[k])}</b>.")], "Tablodan ortalama/toplam bulur.", 45, group=group))
    incs = [F(r[2] - r[0], r[0]) for r in data]
    if len(set(incs)) == 4:
        bi = incs.index(max(incs))
        opts, i = text_opts(branches[bi], [b for b in branches if b != bi and b != branches[bi]] + ["Belirlenemez"], rng)
        out.append(Q("veri", "Tablo yorumlama", 3, "Mart ayı satışının Ocak ayı satışına göre <b>artış oranı</b> en yüksek olan şube hangisidir?", opts, i,
                     ["Artış oranı = (Mart − Ocak) ÷ Ocak: " + ", ".join(f"{b} {dec(round(float(x), 2))}" for b, x in zip(branches, incs)) + ".",
                      f"En yüksek oran: <b>{branches[bi]}</b>. (Mutlak artış ile oransal artış karıştırılmamalıdır.)"], "Mutlak ve oransal değişimi ayırt eder.", 75, group=group))
    return out


def g_bar_visitors(rng, gid):
    labels = rng.sample(["A", "B", "C", "D", "E", "F"], 5)
    labels.sort()
    while True:
        vals = [rng.randrange(12, 60, 2) for _ in labels]
        if len(set(vals)) == 5 and sum(vals) % 5 == 0:
            break
    unit = rng.choice(["bin kişi", "bin ziyaretçi"])
    info = f"Grafikte bir ilçedeki beş kütüphanenin bir yıllık ziyaretçi sayıları ({unit}) gösterilmiştir.<div class='chartwrap'>{svg_bar(labels, vals, unit)}</div>"
    group = {"id": gid, "info": info}
    out = []
    avg = sum(vals) // 5
    out.append(Q("veri", "Grafik yorumlama", 1, f"Kütüphanelerin ortalama yıllık ziyaretçi sayısı kaç {unit}dir?", *num_opts(avg, rng, step=2, minv=1),
                 [f"Toplam: {' + '.join(map(str, vals))} = {sum(vals)}.", f"Ortalama: {sum(vals)} ÷ 5 = <b>{avg}</b>."], "Grafikten ortalama hesaplar.", 45, group=group))
    hi, lo = max(vals), min(vals)
    r = F(hi, lo)
    out.append(Q("veri", "Grafik yorumlama", 2, "En çok ziyaret edilen kütüphanenin ziyaretçi sayısı, en az ziyaret edilenin kaç katıdır?", *num_opts(r, rng, step=F(1, r.denominator) if r.denominator > 1 else F(1, 2), minv=1),
                 [f"En çok: {hi}, en az: {lo}.", f"Oran: ⟦{hi}/{lo}⟧ = <b>{frs(r)}</b>."], "Grafikten oran kurar.", 45, group=group))
    k = rng.randrange(5)
    p = rng.choice([10, 20, 25, 50])
    newv = F(vals[k]) * (100 + p) / 100
    newtot = sum(vals) - vals[k] + newv
    if newtot.denominator == 1:
        out.append(Q("veri", "Grafik yorumlama", 3, f"{labels[k]} kütüphanesinin ziyaretçi sayısı ertesi yıl %{p} artar, diğerleri değişmezse beş kütüphanenin toplam ziyaretçi sayısı kaç {unit} olur?",
                     *num_opts(int(newtot), rng, step=rng.choice([1, 2, 3]), minv=1),
                     [f"{labels[k]}: {vals[k]} → {num(newv)}.", f"Yeni toplam: {sum(vals)} − {vals[k]} + {num(newv)} = <b>{int(newtot)}</b>."], "Grafikteki veriyi senaryoya göre günceller.", 60, group=group))
    return out


def g_budget(rng, gid):
    cats = ["Kira", "Gıda", "Ulaşım", "Eğitim", "Diğer"]
    while True:
        pct = [rng.randrange(10, 45, 5) for _ in range(4)]
        if sum(pct) < 95:
            pct.append(100 - sum(pct))
            if pct[-1] >= 5 and len(set(pct)) == 5:
                break
    income = rng.choice([24000, 30000, 36000, 40000, 48000])
    rows = "".join(f"<tr><td>{c}</td><td>%{p}</td></tr>" for c, p in zip(cats, pct))
    info = f"Bir ailenin aylık geliri {income} TL'dir. Tabloda gelirin harcama kalemlerine yüzde dağılımı verilmiştir.<table class='qt'><tr><th>Kalem</th><th>Pay</th></tr>{rows}</table>"
    group = {"id": gid, "info": info}
    out = []
    k = rng.randrange(5)
    amt = income * pct[k] // 100
    out.append(Q("veri", "Tablo yorumlama", 1, f"Ailenin aylık {cats[k].lower()} harcaması kaç TL'dir?", *num_opts(amt, rng, step=income // 50, minv=1),
                 [f"{income}·⟦{pct[k]}/100⟧ = <b>{amt}</b> TL."], "Yüzdeyi tutara çevirir.", 40, group=group))
    a, b = rng.sample(range(5), 2)
    diff = abs(pct[a] - pct[b]) * income // 100
    out.append(Q("veri", "Tablo yorumlama", 2, f"{cats[a]} ile {cats[b]} harcamaları arasındaki fark kaç TL'dir?", *num_opts(diff, rng, step=income // 100, minv=0),
                 [f"Fark payı: |%{pct[a]} − %{pct[b]}| = %{abs(pct[a] - pct[b])}.", f"Tutar: <b>{diff}</b> TL."], "Yüzde farkını tutara çevirir.", 45, group=group))
    if pct[0] > 0:
        newinc = income * rng.choice([F(5, 4), F(6, 5), F(11, 10)])
        if newinc.denominator == 1:
            newinc = int(newinc)
            rent = income * pct[0] // 100
            np_ = F(rent * 100, newinc)
            if np_.denominator == 1:
                out.append(Q("veri", "Tablo yorumlama", 3, f"Ailenin geliri {newinc} TL'ye yükselir ve kira tutarı değişmezse kiranın gelir içindeki payı yüzde kaç olur?",
                             *(lambda o: (["%" + s for s in o[0]], o[1]))(num_opts(int(np_), rng, step=rng.choice([1, 2]), minv=1, extra=[pct[0]])),
                             [f"Kira: {rent} TL (sabit).", f"Yeni pay: {rent} ÷ {newinc} · 100 = %<b>{int(np_)}</b>."], "Değişen bütüne göre payı yeniden hesaplar.", 60, group=group))
    return out


# ---------------------------------------------------------------- GEOMETRİ

TRIPLES = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (6, 8, 10), (9, 12, 15), (7, 24, 25), (12, 16, 20)]


def t_triangle_angle(rng):
    v = rng.choice(["expr", "ext", "iso", "bisector"])
    if v == "expr":
        while True:
            p, q2, r = rng.randint(1, 4), rng.randint(1, 4), rng.randint(1, 4)
            c1, c2 = rng.randrange(-20, 31, 5), rng.randrange(-20, 31, 5)
            x = F(180 - c1 - c2, p + q2 + r)
            if x.denominator == 1 and 0 < p * x + c1 < 180 and 0 < q2 * x + c2 < 180 and 0 < r * x < 180:
                break
        x = int(x)
        q = f"ABC üçgeninde m(Â) = {p}x {'+' if c1 >= 0 else '−'} {abs(c1)}°, m(B̂) = {q2}x {'+' if c2 >= 0 else '−'} {abs(c2)}° ve m(Ĉ) = {r}x olduğuna göre x kaç derecedir?".replace(" 1x", " x").replace("= 1x", "= x")
        sol = ["Üçgenin iç açıları toplamı 180°'dir.", f"{p + q2 + r}x + {c1 + c2} = 180 ⇒ x = <b>{x}</b>."]
        opts, i = num_opts(x, rng, step=5, minv=1)
        return Q("geometri", "Üçgende açılar", 1, q, opts, i, sol, "İç açılar toplamını kullanır.", 45)
    if v == "ext":
        a, b = rng.randrange(30, 80, 5), rng.randrange(30, 80, 5)
        ext = a + b
        q = f"ABC üçgeninde m(Â) = {a}° ve m(B̂) = {b}°'dir. C köşesindeki dış açının ölçüsü kaç derecedir?"
        sol = ["Bir dış açı, kendisine komşu olmayan iki iç açının toplamına eşittir.", f"{a} + {b} = <b>{ext}</b>°."]
        opts, i = num_opts(ext, rng, step=5, minv=1, extra=[180 - ext])
        return Q("geometri", "Üçgende açılar", 1, q, opts, i, sol, "Dış açı özelliğini uygular.", 40)
    if v == "iso":
        top = rng.randrange(20, 140, 4)
        base = (180 - top) // 2
        q = f"ABC üçgeninde |AB| = |AC| ve m(Â) = {top}° olduğuna göre m(B̂) kaç derecedir?"
        sol = ["İkizkenar üçgende taban açıları eşittir.", f"2·m(B̂) = 180 − {top} ⇒ m(B̂) = <b>{base}</b>°."]
        opts, i = num_opts(base, rng, step=2, minv=1, extra=[180 - top])
        return Q("geometri", "Özel üçgenler", 1, q, opts, i, sol, "İkizkenar üçgen özelliğini kullanır.", 40)
    a = rng.randrange(30, 120, 2)
    ans = 90 + a // 2
    q = f"ABC üçgeninde B ve C köşelerindeki iç açıortaylar I noktasında kesişmektedir. m(Â) = {a}° olduğuna göre m(BÎC) kaç derecedir?"
    sol = ["m(B̂) + m(Ĉ) = 180 − m(Â); açıortaylar bu açıların yarısını alır.", f"m(BÎC) = 180 − (180 − {a})/2 = 90 + {a}/2 = <b>{ans}</b>°."]
    opts, i = num_opts(ans, rng, step=rng.choice([2, 5]), minv=1, extra=[180 - a, 90 + a])
    return Q("geometri", "Üçgende açılar", 3, q, opts, i, sol, "İç açıortay kesişim açısını bulur.", 60)


def t_pyth(rng):
    a, b, c = rng.choice(TRIPLES)
    k = rng.choice([1, 2, 3])
    a, b, c = a * k, b * k, c * k
    v = rng.choice(["hyp", "leg", "area", "perim", "height"])
    if v == "hyp":
        ans = c
        q = f"Dik kenar uzunlukları {a} cm ve {b} cm olan dik üçgenin hipotenüsü kaç cm'dir?"
        sol = ["Pisagor bağıntısı: c² = a² + b².", f"c² = {a * a} + {b * b} = {c * c} ⇒ c = <b>{c}</b>."]
    elif v == "leg":
        ans = b
        q = f"Hipotenüsü {c} cm ve bir dik kenarı {a} cm olan dik üçgenin diğer dik kenarı kaç cm'dir?"
        sol = ["Pisagor bağıntısı: b² = c² − a².", f"b² = {c * c} − {a * a} = {b * b} ⇒ b = <b>{b}</b>."]
    elif v == "area":
        ans = a * b // 2
        q = f"Hipotenüsü {c} cm ve bir dik kenarı {a} cm olan dik üçgenin alanı kaç cm²'dir?"
        sol = [f"Diğer dik kenar: √({c * c} − {a * a}) = {b}.", f"Alan: {a}·{b}/2 = <b>{ans}</b>."]
    elif v == "perim":
        ans = a + b + c
        q = f"Dik kenarlarından biri {a} cm, hipotenüsü {c} cm olan dik üçgenin çevresi kaç cm'dir?"
        sol = [f"Diğer dik kenar: {b}.", f"Çevre: {a} + {b} + {c} = <b>{ans}</b>."]
    else:
        h = F(a * b, c)
        if h.denominator != 1:
            return None
        ans = int(h)
        q = f"Dik kenar uzunlukları {a} cm ve {b} cm olan dik üçgende hipotenüse ait yükseklik kaç cm'dir?"
        sol = [f"Hipotenüs: {c}.", f"Alan iki yoldan yazılır: {a}·{b} = {c}·h ⇒ h = <b>{ans}</b>."]
        return Q("geometri", "Dik üçgen", 3, q, *num_opts(ans, rng, minv=1), sol, "Alan eşitliğinden yükseklik bulur.", 60)
    opts, i = num_opts(ans, rng, step=rng.choice([1, 2]), minv=1)
    return Q("geometri", "Dik üçgen", 2, q, opts, i, sol, "Pisagor bağıntısını uygular.", 45)


def t_quad(rng):
    v = rng.choice(["rect", "trap", "square", "para"])
    if v == "rect":
        x, y = rng.randint(2, 6), rng.randint(2, 6)
        if x == y:
            return None
        k = rng.randint(2, 5)
        P = 2 * (x + y) * k
        A = x * y * k * k
        q = f"Kenar uzunlukları oranı {x}/{y} olan bir dikdörtgenin çevresi {P} cm'dir. Bu dikdörtgenin alanı kaç cm²'dir?".replace(f"{x}/{y}", f"⟦{x}/{y}⟧")
        sol = [f"Kenarlar {x}k ve {y}k: 2({x}k + {y}k) = {P} ⇒ k = {k}.", f"Alan: {x * k}·{y * k} = <b>{A}</b>."]
        opts, i = num_opts(A, rng, step=k * k, minv=1)
        return Q("geometri", "Dikdörtgen", 2, q, opts, i, sol, "Oran ve çevreden alan bulur.", 60)
    if v == "trap":
        a, b, h = rng.randint(4, 14), rng.randint(6, 20), rng.randint(3, 10)
        if a == b or (a + b) * h % 2:
            return None
        A = (a + b) * h // 2
        q = f"Paralel kenarlarının uzunlukları {a} cm ve {b} cm, yüksekliği {h} cm olan yamuğun alanı kaç cm²'dir?"
        sol = ["Yamuk alanı = (taban toplamı)·yükseklik / 2.", f"({a} + {b})·{h}/2 = <b>{A}</b>."]
        opts, i = num_opts(A, rng, step=rng.choice([2, 4, 5]), minv=1, extra=[(a + b) * h])
        return Q("geometri", "Yamuk", 1, q, opts, i, sol, "Yamuk alan formülünü uygular.", 40)
    if v == "square":
        d = rng.choice([4, 6, 8, 10, 12])
        A = d * d // 2
        q = f"Köşegen uzunluğu {d} cm olan karenin alanı kaç cm²'dir?"
        sol = ["Karede alan = köşegen² / 2.", f"{d}²/2 = <b>{A}</b>."]
        opts, i = num_opts(A, rng, step=rng.choice([2, 4]), minv=1, extra=[d * d])
        return Q("geometri", "Kare", 2, q, opts, i, sol, "Kare alanını köşegenden hesaplar.", 40)
    a, h = rng.randint(5, 16), rng.randint(3, 10)
    s = rng.randint(h + 1, h + 6)
    A = a * h
    q = f"Bir paralelkenarın bir kenarı {a} cm, bu kenara ait yüksekliği {h} cm, diğer kenarı {s} cm'dir. Diğer kenara ait yükseklik kaç cm'dir?"
    h2 = F(A, s)
    sol = [f"Alan: {a}·{h} = {A}.", f"{s}·h₂ = {A} ⇒ h₂ = <b>{frs(h2)}</b>."]
    opts, i = num_opts(h2, rng, step=F(1, h2.denominator) if h2.denominator > 1 else 1, minv=F(1, 2))
    return Q("geometri", "Paralelkenar", 3, q, opts, i, sol, "Alanın iki farklı yüksekliğe göre eşitliğini kullanır.", 60)


def t_circle(rng):
    v = rng.choice(["area", "circ", "ring", "sector"])
    r = rng.randint(2, 10)
    if v == "area":
        ans = 3 * r * r
        q = f"Yarıçapı {r} cm olan dairenin alanı kaç cm²'dir? (π = 3 alınız.)"
        sol = ["Daire alanı = πr².", f"3·{r}² = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=3, minv=1, extra=[6 * r])
    elif v == "circ":
        ans = 6 * r
        q = f"Yarıçapı {r} cm olan çemberin çevresi kaç cm'dir? (π = 3 alınız.)"
        sol = ["Çember çevresi = 2πr.", f"2·3·{r} = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=3, minv=1, extra=[3 * r * r])
    elif v == "ring":
        R = r + rng.randint(1, 5)
        ans = 3 * (R * R - r * r)
        q = f"Aynı merkezli, yarıçapları {r} cm ve {R} cm olan iki daire arasında kalan halka biçimli bölgenin alanı kaç cm²'dir? (π = 3 alınız.)"
        sol = ["Halka alanı = π(R² − r²).", f"3·({R * R} − {r * r}) = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=3, minv=1, extra=[3 * (R - r) ** 2])
    else:
        ang = rng.choice([30, 45, 60, 90, 120, 150])
        A = F(3 * r * r * ang, 360)
        if A.denominator != 1:
            return None
        ans = int(A)
        q = f"Yarıçapı {r} cm, merkez açısı {ang}° olan daire diliminin alanı kaç cm²'dir? (π = 3 alınız.)"
        sol = ["Dilim alanı = πr²·(α/360).", f"3·{r * r}·⟦{ang}/360⟧ = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=rng.choice([1, 3]), minv=1)
    return Q("geometri", "Çember ve daire", 1 if v in ("area", "circ") else 2, q, opts, i, sol, "Daire ve çember formüllerini uygular.", 45)


def t_polygon(rng):
    v = rng.choice(["int", "sum", "n_from"])
    n = rng.choice([5, 6, 8, 9, 10, 12, 15, 18, 20])
    if v == "int":
        ans = F(180 * (n - 2), n)
        if ans.denominator != 1:
            return None
        q = f"Düzgün {n}genin bir iç açısı kaç derecedir?"
        sol = ["İç açılar toplamı (n − 2)·180°.", f"({n} − 2)·180 ÷ {n} = <b>{int(ans)}</b>°."]
        opts, i = num_opts(int(ans), rng, step=rng.choice([2, 4, 6]), minv=1, extra=[360 // n])
        return Q("geometri", "Çokgenler", 2, q, opts, i, sol, "Düzgün çokgende iç açıyı hesaplar.", 45)
    if v == "sum":
        ans = 180 * (n - 2)
        q = f"Bir {n}genin iç açılarının ölçüleri toplamı kaç derecedir?"
        sol = [f"({n} − 2)·180 = <b>{ans}</b>°."]
        opts, i = num_opts(ans, rng, step=180, minv=180)
        return Q("geometri", "Çokgenler", 1, q, opts, i, sol, "Çokgen iç açılar toplamını bilir.", 30)
    ext = 360 // n
    if 360 % n:
        return None
    q = f"Bir dış açısı {ext}° olan düzgün çokgenin kaç kenarı vardır?"
    sol = ["Dış açılar toplamı 360°'dir.", f"360 ÷ {ext} = <b>{n}</b>."]
    opts, i = num_opts(n, rng, minv=3)
    return Q("geometri", "Çokgenler", 2, q, opts, i, sol, "Dış açıdan kenar sayısını bulur.", 40)


def t_similar(rng):
    a, b = rng.randint(2, 8), rng.randint(1, 8)
    c = rng.randint(2, 9) * a
    BC = F(c * (a + b), a)
    if BC.denominator != 1:
        return None
    v = rng.choice(["side", "area"])
    if v == "side":
        q = f"ABC üçgeninde D ∈ [AB], E ∈ [AC] ve [DE] ∥ [BC]'dir. |AD| = {a} cm, |DB| = {b} cm ve |DE| = {c} cm olduğuna göre |BC| kaç cm'dir?"
        sol = ["DE ∥ BC olduğundan ADE ve ABC üçgenleri benzerdir.", f"⟦{a}/{a + b}⟧ = ⟦{c}/|BC|⟧ ⇒ |BC| = <b>{int(BC)}</b>."]
        opts, i = num_opts(int(BC), rng, step=rng.choice([1, 2, 3]), minv=1, extra=[c * b // a if c * b % a == 0 else c + b])
        return Q("geometri", "Eşlik ve benzerlik", 2, q, opts, i, sol, "Temel orantı teoremini uygular.", 60)
    S = rng.choice([4, 6, 8, 9, 12])
    big = F(S * (a + b) ** 2, a * a)
    trap = big - S
    if trap.denominator != 1:
        return None
    q = f"ABC üçgeninde D ∈ [AB], E ∈ [AC] ve [DE] ∥ [BC]'dir. |AD| = {a} cm, |DB| = {b} cm ve A(ADE) = {S} cm² olduğuna göre DBCE dörtgeninin alanı kaç cm²'dir?"
    sol = [f"Benzerlik oranı ⟦{a}/{a + b}⟧; alanlar oranı bunun karesi: ⟦{a * a}/{(a + b) ** 2}⟧.", f"A(ABC) = {num(big)} ⇒ A(DBCE) = {num(big)} − {S} = <b>{int(trap)}</b>."]
    opts, i = num_opts(int(trap), rng, step=rng.choice([2, 3, 4]), minv=1, extra=[int(big)])
    return Q("geometri", "Eşlik ve benzerlik", 4, q, opts, i, sol, "Benzer üçgenlerde alan oranını kenar oranının karesi olarak kullanır.", 90)


def t_volume(rng):
    v = rng.choice(["box", "cube_fit", "cyl"])
    if v == "box":
        a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 9)
        ask = rng.choice(["hacmi", "yüzey alanı"])
        ans = a * b * c if ask == "hacmi" else 2 * (a * b + a * c + b * c)
        q = f"Ayrıt uzunlukları {a} cm, {b} cm ve {c} cm olan dikdörtgenler prizmasının {ask} kaç cm{'³' if ask == 'hacmi' else '²'}'tür?"
        sol = (["Hacim = a·b·c.", f"{a}·{b}·{c} = <b>{ans}</b>."] if ask == "hacmi" else ["Yüzey alanı = 2(ab + ac + bc).", f"2({a * b} + {a * c} + {b * c}) = <b>{ans}</b>."])
        opts, i = num_opts(ans, rng, step=rng.choice([2, 4, 6]), minv=1)
        return Q("geometri", "Hacim ve katı cisimler", 1, q, opts, i, sol, "Prizma hacim ve alanını hesaplar.", 45)
    if v == "cube_fit":
        e = rng.choice([2, 3, 4, 5])
        a, b, c = [e * rng.randint(2, 5) for _ in range(3)]
        ans = (a // e) * (b // e) * (c // e)
        q = f"İç ölçüleri {a} cm, {b} cm ve {c} cm olan dikdörtgenler prizması biçimindeki bir kutuya ayrıtı {e} cm olan küplerden en çok kaç tane yerleştirilebilir?"
        sol = [f"Her boyuta sığan küp sayısı: {a // e}, {b // e}, {c // e}.", f"Toplam: <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, step=rng.choice([2, 4, 6]), minv=1)
        return Q("geometri", "Hacim ve katı cisimler", 2, q, opts, i, sol, "Hacim içinde birim küp sayısını bulur.", 45)
    r, h = rng.randint(1, 6), rng.randint(2, 12)
    ans = 3 * r * r * h
    q = f"Taban yarıçapı {r} cm ve yüksekliği {h} cm olan dik dairesel silindirin hacmi kaç cm³'tür? (π = 3 alınız.)"
    sol = ["Silindir hacmi = πr²h.", f"3·{r * r}·{h} = <b>{ans}</b>."]
    opts, i = num_opts(ans, rng, step=rng.choice([3, 6, 9]), minv=1, extra=[6 * r * h])
    return Q("geometri", "Hacim ve katı cisimler", 2, q, opts, i, sol, "Silindir hacmini hesaplar.", 45)


def t_analytic(rng):
    v = rng.choice(["dist", "mid", "area", "slope"])
    if v == "dist":
        a, b, c = rng.choice(TRIPLES[:4])
        x1, y1 = rng.randint(-5, 5), rng.randint(-5, 5)
        x2, y2 = x1 + a * rng.choice([1, -1]), y1 + b * rng.choice([1, -1])
        q = f"Analitik düzlemde A({x1}, {y1}) ve B({x2}, {y2}) noktaları arasındaki uzaklık kaç birimdir?".replace("(-", "(−").replace(", -", ", −")
        sol = [f"|AB| = √[(Δx)² + (Δy)²] = √({a * a} + {b * b}).", f"|AB| = <b>{c}</b>."]
        opts, i = num_opts(c, rng, minv=1, extra=[a + b])
        return Q("geometri", "Analitik geometri", 2, q, opts, i, sol, "İki nokta arası uzaklığı hesaplar.", 45)
    if v == "mid":
        x1, y1, mx, my = [rng.randint(-6, 8) for _ in range(4)]
        x2, y2 = 2 * mx - x1, 2 * my - y1
        ans = x2 + y2
        q = f"Analitik düzlemde A({x1}, {y1}) noktası ile B(a, b) noktasını birleştiren doğru parçasının orta noktası M({mx}, {my}) olduğuna göre a + b kaçtır?".replace("(-", "(−").replace(", -", ", −")
        sol = [f"a = 2·{mx} − {x1} = {x2}, b = 2·{my} − {y1} = {y2}.".replace("− -", "+ "), f"a + b = <b>{ans}</b>."]
        opts, i = num_opts(ans, rng, extra=[mx + my])
        return Q("geometri", "Analitik geometri", 2, q, opts, i, sol, "Orta nokta formülünü tersten kullanır.", 45)
    if v == "area":
        a, b = rng.randint(2, 12), rng.randint(2, 12)
        ans = F(a * b, 2)
        q = f"Analitik düzlemde x/{a} + y/{b} = 1 doğrusu ile koordinat eksenleri arasında kalan üçgensel bölgenin alanı kaç birimkaredir?".replace(f"x/{a}", f"⟦x/{a}⟧").replace(f"y/{b}", f"⟦y/{b}⟧")
        sol = [f"Doğru eksenleri ({a}, 0) ve (0, {b}) noktalarında keser.", f"Alan: {a}·{b}/2 = <b>{num(ans)}</b>."]
        ans = int(ans) if ans.denominator == 1 else ans
        opts, i = num_opts(ans, rng, step=rng.choice([1, 2]) if isinstance(ans, int) else F(1, 2), minv=1, extra=[a * b])
        return Q("geometri", "Analitik geometri", 2, q, opts, i, sol, "Eksen kesim noktalarından alan bulur.", 45)
    x1, y1 = rng.randint(-4, 4), rng.randint(-4, 4)
    m = rng.choice([F(1, 2), F(2, 3), 2, 3, F(-1, 2), -2, F(3, 4)])
    dx = rng.choice([2, 4, 6]) if F(m).denominator in (1, 2) else rng.choice([3, 6])
    if F(m).denominator == 4:
        dx = 4
    y2 = y1 + F(m) * dx
    q = f"A({x1}, {y1}) ve B({x1 + dx}, k) noktalarından geçen doğrunun eğimi {frs(F(m))} olduğuna göre k kaçtır?".replace("(-", "(−").replace(", -", ", −")
    sol = [f"Eğim = (k − {y1}) ÷ {dx} = {frs(F(m))}.".replace("− -", "+ "), f"k = {y1} + {frs(F(m))}·{dx} = <b>{num(y2)}</b>."]
    y2v = int(y2) if y2.denominator == 1 else y2
    opts, i = num_opts(y2v, rng)
    return Q("geometri", "Analitik geometri", 2, q, opts, i, sol, "Eğim tanımını kullanır.", 45)


TEMPLATES = {
    "temel": [t_parity, t_consec, t_digits_ab, t_build_number, t_primes, t_signs],
    "bolunebilme": [t_crt, t_remainder_expr, t_div_digits, t_fact_zeros, t_gcd_lcm],
    "rasyonel": [t_frac_expr, t_decimal, t_frac_order, t_repeating, t_frac_problem],
    "esitsizlik": [t_range_expr, t_abs_count, t_abs_equation, t_order_truth, t_minmax],
    "uslu": [t_exp_simplify, t_exp_equation, t_roots, t_neg_exp, t_exp_compare, t_rationalize],
    "cebir": [t_identity, t_factor_poly, t_lin_eq, t_system, t_word_eq],
    "oran": [t_chain_ratio, t_share, t_inverse, t_scale, t_equal_ratio],
    "problem": [t_age, t_age_sum, t_work, t_motion, t_percent, t_mixture, t_interest, t_number_problem],
    "islem": [t_defined_op, t_piecewise_op, t_days, t_last_digit, t_mod_count, t_function, t_clock],
    "sayma": [t_perm_word, t_committee, t_digits_count, t_prob_balls, t_prob_dice, t_count_misc],
    "saymantik": [t_sequence, t_machine, t_cipher],
    "geometri": [t_triangle_angle, t_pyth, t_quad, t_circle, t_polygon, t_similar, t_volume, t_analytic],
}
GROUPS = {"veri": [g_table_sales, g_bar_visitors, g_budget], "saymantik": [g_parking, g_tournament]}
