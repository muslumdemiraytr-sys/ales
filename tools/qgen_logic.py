"""Sözel mantık grupları: kısıtlardan üretilir, her sorunun tek doğru cevabı
tüm olası çözümler üzerinde kaba kuvvetle doğrulanır."""
import itertools

from qcommon import Q, text_opts

PEOPLE = ["Ahmet", "Burcu", "Can", "Derya", "Emre", "Funda", "Gökhan", "Hale", "İlker", "Jale", "Kemal", "Lale", "Murat", "Nesrin", "Oğuz", "Pınar", "Rıza", "Seda", "Tarık", "Ülkü"]
WEEK = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
CITIES = ["Ankara", "Bursa", "Edirne", "İzmir", "Konya", "Mardin", "Rize", "Sivas", "Trabzon", "Van"]
COLORS = ["kırmızı", "mavi", "yeşil", "sarı", "mor"]

def _lv(n):
    return [c for c in n.lower() if c in "aeıioöuü"][-1]


def dat(n):
    """Yönelme hâli: İzmir'e, Konya'ya."""
    v = "e" if _lv(n) in "eiöü" else "a"
    return f"{n}'{'y' if n[-1].lower() in 'aeıioöuü' else ''}{v}"


def abl(n):
    """Ayrılma hâli: Can'dan, Ahmet'ten, Emre'den."""
    v = "a" if _lv(n) in "aıou" else "e"
    d = "t" if n[-1].lower() in "fstkçşhp" else "d"
    return f"{n}'{d}{v}n"


def gen(n):
    """İlgi hâli: Can'ın, Emre'nin, Burcu'nun."""
    v = {"a": "ı", "ı": "ı", "o": "u", "u": "u", "e": "i", "i": "i", "ö": "ü", "ü": "ü"}[_lv(n)]
    return f"{n}'{'n' if n[-1].lower() in 'aeıioöuü' else ''}{v}n"


# ------------------------------------------------------------ SIRALAMA

def order_clues(names, n):
    cl = []
    for a, b in itertools.permutations(names, 2):
        cl.append((f"{a}, {abl(b)} hemen önce sunum yapacaktır.", lambda p, a=a, b=b: p[b] == p[a] + 1, ("adj", a, b)))
        cl.append((f"{a}, {abl(b)} önceki bir günde sunum yapacaktır.", lambda p, a=a, b=b: p[a] < p[b], ("before", a, b)))
    for a, b in itertools.combinations(names, 2):
        cl.append((f"{a} ile {b} ardışık günlerde sunum yapmayacaktır.", lambda p, a=a, b=b: abs(p[a] - p[b]) != 1, ("nadj", a, b)))
        cl.append((f"{a} ile {gen(b)} sunumları arasında tam bir gün vardır.", lambda p, a=a, b=b: abs(p[a] - p[b]) == 2, ("gap", a, b)))
    for a in names:
        for k in range(n):
            cl.append((f"{a}, {WEEK[k]} günü sunum yapmayacaktır.", lambda p, a=a, k=k: p[a] != k, ("not", a, k)))
        cl.append((f"{a}, haftanın ilk ya da son iş gününde sunum yapacaktır.", lambda p, a=a: p[a] in (0, n - 1), ("end", a)))
    return cl


def statements(names, n):
    st = []
    for a in names:
        for k in range(n):
            st.append((f"{a}, {WEEK[k]} günü sunum yapar.", lambda p, a=a, k=k: p[a] == k))
    for a, b in itertools.permutations(names, 2):
        st.append((f"{a}, {abl(b)} önce sunum yapar.", lambda p, a=a, b=b: p[a] < p[b]))
    return st


def solve(names, n, clues):
    sols = []
    for perm in itertools.permutations(range(n), len(names)):
        p = dict(zip(names, perm))
        if all(f(p) for _, f, _ in clues):
            sols.append(p)
    return sols


def g_order(rng, gid):
    n = 5
    names = rng.sample(PEOPLE, 5)
    truth = dict(zip(names, rng.sample(range(n), n)))
    pool = [c for c in order_clues(names, n) if c[1](truth)]
    rng.shuffle(pool)
    clues = []
    for c in pool:
        trial = clues + [c]
        s = solve(names, n, trial)
        if len(s) < len(solve(names, n, clues)) if clues else True:
            clues = trial
        if 2 <= len(s) <= 4 and len(clues) >= 4:
            break
    sols = solve(names, n, clues)
    if not 2 <= len(sols) <= 4 or len(clues) > 6:
        return None
    info = ("Bir şirkette " + ", ".join(names[:-1]) + f" ve {names[-1]} adlı beş çalışan, Pazartesi'den Cuma'ya kadar her gün yalnızca bir kişi olmak üzere birer sunum yapacaktır. "
            "Sunumlarla ilgili şunlar bilinmektedir:<ul>" + "".join(f"<li>{c[0]}</li>" for c in clues) + "</ul>")
    group = {"id": gid, "info": info}
    st = statements(names, n)
    out = []
    # 1) kesinlikle doğru
    alw = [s for s in st if all(s[1](p) for p in sols)]
    some = [s for s in st if any(s[1](p) for p in sols) and not all(s[1](p) for p in sols)]
    never = [s for s in st if not any(s[1](p) for p in sols)]
    if alw and len(some) + len(never) >= 4:
        c = rng.choice(alw)
        wr = rng.sample(some, min(3, len(some))) + rng.sample(never, 4 - min(3, len(some)))
        opts, i = text_opts(c[0], [w[0] for w in wr], rng)
        out.append(Q("sozmantik", "Sıralama", 3, "Bu bilgilere göre aşağıdakilerden hangisi <b>kesinlikle doğrudur</b>?", opts, i,
                     [f"Koşulları sağlayan {len(sols)} farklı sıralama vardır:"] + [" – ".join(f"{WEEK[k]}: {[a for a in names if p[a] == k][0]}" for k in range(n)) for p in sols] +
                     [f"Her sıralamada doğru olan yargı: <b>{c[0]}</b>"], "Tüm olası durumları tablo hâlinde kurup kesin yargıyı belirler.", 120, area="soz", group=group))
    # 2) olamaz
    if never and len(some) + len(alw) >= 4:
        c = rng.choice(never)
        wr = rng.sample(some + alw, 4)
        opts, i = text_opts(c[0], [w[0] for w in wr], rng)
        out.append(Q("sozmantik", "Sıralama", 3, "Bu bilgilere göre aşağıdakilerden hangisi <b>olamaz</b>?", opts, i,
                     ["Olası sıralamalar (yukarıdaki bilgilere göre) tek tek denenir.", f"<b>{c[0]}</b> yargısı hiçbir olası sıralamada gerçekleşmez; diğer seçeneklerin her biri en az bir sıralamada mümkündür."],
                     "Olası durumlar içinde imkânsız olanı bulur.", 100, area="soz", group=group))
    # 3) koşullu soru
    for cond in rng.sample(some, len(some)):
        sub = [p for p in sols if cond[1](p)]
        if not sub:
            continue
        who = [a for a in names if a not in cond[0] and len({p[a] for p in sub}) == 1 and len({p[a] for p in sols}) > 1]
        if not who:
            continue
        a = rng.choice(who)
        day = WEEK[sub[0][a]]
        wr = [d for d in WEEK if d != day]
        opts, i = text_opts(day, wr, rng)
        out.append(Q("sozmantik", "Koşullu çıkarım", 4, f"{cond[0][:-1].replace(' yapar', ' yaparsa')}, {a} hangi gün sunum yapar?".replace("yaparsa,", "yaparsa,"), opts, i,
                     [f"Ek koşulla olası sıralama sayısı {len(sub)}'e iner:"] + [" – ".join(f"{WEEK[k]}: {[x for x in names if p[x] == k][0]}" for k in range(n)) for p in sub] +
                     [f"Bu sıralamada {a} <b>{day}</b> günü sunum yapar."], "Ek bir koşulla çözüm kümesini daraltır.", 120, area="soz", group=group))
        break
    # 4) kaç farklı sıralama
    cnt = len(sols)
    wr = [str(x) for x in range(1, 7) if x != cnt][:4]
    opts = sorted([str(cnt)] + wr, key=int)
    out.append(Q("sozmantik", "Sıralama", 3, "Bu bilgilere göre sunum sırası kaç farklı biçimde oluşturulabilir?", opts, opts.index(str(cnt)),
                 ["Kesin bilgiler yerleştirilip kalan kişiler için tüm seçenekler denenir.", f"Tüm koşulları sağlayan sıralama sayısı: <b>{cnt}</b>."], "Olası tüm durumları sistematik biçimde sayar.", 120, area="soz", group=group))
    return out if len(out) >= 3 else None


# ------------------------------------------------------------ EŞLEŞTİRME

def g_match(rng, gid):
    names = rng.sample(PEOPLE, 4)
    cities = rng.sample(CITIES, 4)
    truth = dict(zip(names, rng.sample(cities, 4)))
    pool = []
    for a in names:
        for c in cities:
            if truth[a] != c:
                pool.append((f"{a} {dat(c)} gitmemiştir.", lambda p, a=a, c=c: p[a] != c))
    for c in cities:
        for a, b in itertools.combinations(names, 2):
            if truth[a] == c or truth[b] == c:
                pool.append((f"{dat(c)} {a} ya da {b} gitmiştir.", lambda p, a=a, b=b, c=c: p[a] == c or p[b] == c))
    for a, b in itertools.permutations(names, 2):
        for c1, c2 in itertools.permutations(cities, 2):
            if (truth[a] == c1) == (truth[b] == c2):
                pool.append((f"{a} {dat(c1)} gittiyse {b} {dat(c2)} gitmiştir.", lambda p, a=a, b=b, c1=c1, c2=c2: p[a] != c1 or p[b] == c2))
    rng.shuffle(pool)
    clues = []
    def sols_of(cl):
        out = []
        for perm in itertools.permutations(cities):
            p = dict(zip(names, perm))
            if all(f(p) for _, f in cl):
                out.append(p)
        return out
    cur = sols_of(clues)
    for c in pool:
        s = sols_of(clues + [c])
        if len(s) < len(cur):
            clues.append(c)
            cur = s
        if 2 <= len(cur) <= 3 and len(clues) >= 3:
            break
    if not 2 <= len(cur) <= 3 or len(clues) > 6:
        return None
    sols = cur
    info = (", ".join(names[:-1]) + f" ve {names[-1]}, bir araştırma projesi kapsamında " + ", ".join(cities[:-1]) + f" ve {cities[-1]} illerinden birer tanesine gitmiş; her ile yalnızca bir kişi gitmiştir. "
            "Bu kişilerle ilgili şunlar bilinmektedir:<ul>" + "".join(f"<li>{c[0]}</li>" for c in clues) + "</ul>")
    group = {"id": gid, "info": info}
    st = [(f"{a} {dat(c)} gitmiştir.", lambda p, a=a, c=c: p[a] == c) for a in names for c in cities]
    alw = [s for s in st if all(s[1](p) for p in sols)]
    some = [s for s in st if any(s[1](p) for p in sols) and not all(s[1](p) for p in sols)]
    never = [s for s in st if not any(s[1](p) for p in sols)]
    out = []
    table = lambda p: ", ".join(f"{a}–{p[a]}" for a in names)
    if alw:
        c = rng.choice(alw)
        wr = rng.sample(some, min(2, len(some))) + rng.sample(never, 4 - min(2, len(some)))
        opts, i = text_opts(c[0], [w[0] for w in wr], rng)
        out.append(Q("sozmantik", "Eşleştirme", 3, "Bu bilgilere göre aşağıdakilerden hangisi <b>kesinlikle doğrudur</b>?", opts, i,
                     ["Kişi–il tablosu kurulur ve koşullar uygulanır. Olası eşleştirmeler:"] + [table(p) for p in sols] + [f"Hepsinde doğru olan: <b>{c[0]}</b>"],
                     "Eşleştirme tablosu kurarak kesin bilgiyi bulur.", 110, area="soz", group=group))
    for a in rng.sample(names, 4):
        poss = sorted({p[a] for p in sols})
        if len(poss) >= 2:
            imp = [c for c in cities if c not in poss]
            if len(poss) >= 1 and imp:
                cor = f"{', '.join(dat(x) for x in poss[:-1])} ya da {dat(poss[-1])}" if len(poss) > 1 else dat(poss[0])
                corr = cor
                wr = []
                for x in itertools.combinations(cities, len(poss)):
                    t = f"{', '.join(dat(y) for y in x[:-1])} ya da {dat(x[-1])}"
                    if sorted(x) != poss:
                        wr.append(t)
                rng.shuffle(wr)
                opts, i = text_opts(corr, wr[:4], rng)
                out.append(Q("sozmantik", "Eşleştirme", 3, f"{a} hangi illere gitmiş olabilir?", opts, i,
                             ["Olası eşleştirmeler:"] + [table(p) for p in sols] + [f"{a} için mümkün olan iller: <b>{corr}</b>."], "Bir kişi için olası seçenekleri belirler.", 100, area="soz", group=group))
                break
    if some:
        cond = rng.choice(some)
        sub = [p for p in sols if cond[1](p)]
        if len(sub) == 1:
            p = sub[0]
            b = rng.choice([x for x in names if x not in cond[0]])
            opts, i = text_opts(f"{b} {dat(p[b])} gitmiştir.", [f"{b} {dat(c)} gitmiştir." for c in cities if c != p[b]] + [f"{b} hiçbir yere gitmemiştir."], rng)
            out.append(Q("sozmantik", "Koşullu çıkarım", 4, f"{cond[0][:-len(' gitmiştir.')]} gittiyse aşağıdakilerden hangisi kesinlikle doğrudur?", opts, i,
                         [f"Ek koşulla tek eşleştirme kalır: {table(p)}.", f"Buna göre <b>{b} {dat(p[b])}</b> gitmiştir."], "Ek koşulla tek çözüme ulaşır.", 110, area="soz", group=group))
    return out if len(out) >= 2 else None


# ------------------------------------------------------------ GRUPLANDIRMA

def g_group(rng, gid):
    names = rng.sample(PEOPLE, 6)
    teams = rng.sample(COLORS, 2)
    for _ in range(50):
        tA = set(rng.sample(names, 3))
        truth = {a: (teams[0] if a in tA else teams[1]) for a in names}
        pool = []
        for a, b in itertools.combinations(names, 2):
            if truth[a] == truth[b]:
                pool.append((f"{a} ile {b} aynı takımdadır.", lambda p, a=a, b=b: p[a] == p[b]))
            else:
                pool.append((f"{a} ile {b} farklı takımlardadır.", lambda p, a=a, b=b: p[a] != p[b]))
        for a in names:
            pool.append((f"{a} {truth[a]} takımdadır.", lambda p, a=a, t=truth[a]: p[a] == t))
        rng.shuffle(pool)
        def sols_of(cl):
            out = []
            for c in itertools.combinations(names, 3):
                p = {a: (teams[0] if a in c else teams[1]) for a in names}
                if all(f(p) for _, f in cl):
                    out.append(p)
            return out
        clues = []
        cur = sols_of([])
        for c in pool:
            s = sols_of(clues + [c])
            if len(s) < len(cur):
                clues.append(c)
                cur = s
            if 2 <= len(cur) <= 3 and len(clues) >= 3:
                break
        if 2 <= len(cur) <= 3 and len(clues) <= 5:
            break
    else:
        return None
    sols = cur
    info = (", ".join(names[:-1]) + f" ve {names[-1]} adlı altı öğrenci, üçer kişilik {teams[0]} ve {teams[1]} takımlara ayrılacaktır. "
            "Takımlarla ilgili şunlar bilinmektedir:<ul>" + "".join(f"<li>{c[0]}</li>" for c in clues) + "</ul>")
    group = {"id": gid, "info": info}
    st = [(f"{a} {t} takımdadır.", lambda p, a=a, t=t: p[a] == t) for a in names for t in teams]
    st += [(f"{a} ile {b} aynı takımdadır.", lambda p, a=a, b=b: p[a] == p[b]) for a, b in itertools.combinations(names, 2)]
    alw = [s for s in st if all(s[1](p) for p in sols)]
    some = [s for s in st if any(s[1](p) for p in sols) and not all(s[1](p) for p in sols)]
    never = [s for s in st if not any(s[1](p) for p in sols)]
    tbl = lambda p: f"{teams[0]}: " + ", ".join(a for a in names if p[a] == teams[0]) + f" | {teams[1]}: " + ", ".join(a for a in names if p[a] == teams[1])
    out = []
    clue_txt = {c[0] for c in clues}
    alw2 = [s for s in alw if s[0] not in clue_txt]
    if alw2 and len(some) + len(never) >= 4:
        c = rng.choice(alw2)
        wr = rng.sample(some, min(2, len(some))) + rng.sample(never, 4 - min(2, len(some)))
        opts, i = text_opts(c[0], [w[0] for w in wr], rng)
        out.append(Q("sozmantik", "Gruplandırma", 3, "Bu bilgilere göre aşağıdakilerden hangisi <b>kesinlikle doğrudur</b>?", opts, i,
                     ["Olası takım dağılımları:"] + [tbl(p) for p in sols] + [f"Hepsinde doğru olan: <b>{c[0]}</b>"], "Gruplama koşullarını birlikte değerlendirir.", 110, area="soz", group=group))
    if never and len(some) + len(alw2) >= 4:
        c = rng.choice(never)
        wr = rng.sample(some + alw2, 4)
        opts, i = text_opts(c[0], [w[0] for w in wr], rng)
        out.append(Q("sozmantik", "Gruplandırma", 3, "Bu bilgilere göre aşağıdakilerden hangisi <b>olamaz</b>?", opts, i,
                     ["Olası takım dağılımları:"] + [tbl(p) for p in sols] + [f"Hiçbir dağılımda gerçekleşmeyen: <b>{c[0]}</b>"], "Gruplamada imkânsız durumu belirler.", 100, area="soz", group=group))
    for cond in some:
        sub = [p for p in sols if cond[1](p)]
        if len(sub) == 1:
            p = sub[0]
            members = sorted(a for a in names if p[a] == teams[1])
            cor = ", ".join(members)
            wr = []
            for c in itertools.combinations(names, 3):
                if sorted(c) != members:
                    wr.append(", ".join(sorted(c)))
            rng.shuffle(wr)
            opts, i = text_opts(cor, wr[:4], rng)
            out.append(Q("sozmantik", "Koşullu çıkarım", 4, f"{cond[0][:-1].replace('takımdadır', 'takımdaysa')}, {teams[1]} takımdaki öğrenciler kimlerdir?", opts, i,
                         [f"Ek koşul olası dağılımı teke indirir: {tbl(p)}."], "Ek koşulla gruplamayı kesinleştirir.", 100, area="soz", group=group))
            break
    return out if len(out) >= 2 else None


GROUPS = [g_order, g_match, g_group]
