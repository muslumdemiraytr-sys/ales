/* ALES Akademi — Mantık Atölyesi: tablo kurma bulmacası, örüntüler, zamanlı test. */
"use strict";
const LG_NAMES = ["Arda", "Begüm", "Cenk", "Dila", "Eren", "Figen", "Gizem", "Halil", "Irmak", "Kaya", "Melis", "Nazlı", "Ozan", "Serra", "Taylan", "Yağmur"];
const LG_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"];
const LG_CITIES = ["Ankara", "Bursa", "İzmir", "Konya", "Rize", "Van", "Sivas", "Muğla"];
const lv_ = n => [...n.toLowerCase()].filter(c => "aeıioöuü".includes(c)).pop();
const sDat = n => `${n}'${"aeıioöuü".includes(n.slice(-1).toLowerCase()) ? "y" : ""}${"eiöü".includes(lv_(n)) ? "e" : "a"}`;
const sAbl = n => `${n}'${"fstkçşhp".includes(n.slice(-1).toLowerCase()) ? "t" : "d"}${"aıou".includes(lv_(n)) ? "a" : "e"}n`;

function perms(n) { const out = [], a = [...Array(n).keys()]; const rec = k => { if (k === n) { out.push(a.slice()); return; } for (let i = k; i < n; i++) { [a[k], a[i]] = [a[i], a[k]]; rec(k + 1); [a[k], a[i]] = [a[i], a[k]]; } }; rec(0); return out; }

function makePuzzle(mode, level) {
  const n = level === 1 ? 4 : 5;
  const ent = shuffle(LG_NAMES).slice(0, n);
  const slots = mode === "sira" ? LG_DAYS.slice(0, n) : shuffle(LG_CITIES).slice(0, n);
  const all = perms(n); // p[i] = kişinin slot indeksi
  const truth = all[Math.floor(Math.random() * all.length)];
  const pool = [];
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) {
    if (truth[i] !== j) pool.push({ t: mode === "sira" ? `${ent[i]}, ${slots[j]} günü sunum yapmayacaktır.` : `${ent[i]} ${sDat(slots[j])} gitmemiştir.`, f: p => p[i] !== j, w: 1 });
    else if (level < 3) pool.push({ t: mode === "sira" ? `${ent[i]}, ${slots[j]} günü sunum yapacaktır.` : `${ent[i]} ${sDat(slots[j])} gitmiştir.`, f: p => p[i] === j, w: 3 });
  }
  for (let i = 0; i < n; i++) for (let k = 0; k < n; k++) if (i !== k) {
    if (mode === "sira") {
      if (truth[k] === truth[i] + 1) pool.push({ t: `${ent[i]}, ${sAbl(ent[k])} hemen önce sunum yapacaktır.`, f: p => p[k] === p[i] + 1, w: 2 });
      if (truth[i] < truth[k]) pool.push({ t: `${ent[i]}, ${sAbl(ent[k])} önce sunum yapacaktır.`, f: p => p[i] < p[k], w: 1 });
      if (i < k && Math.abs(truth[i] - truth[k]) !== 1) pool.push({ t: `${ent[i]} ile ${ent[k]} ardışık günlerde sunum yapmayacaktır.`, f: p => Math.abs(p[i] - p[k]) !== 1, w: 1 });
    } else {
      const a = truth[i], b = truth[k];
      pool.push({ t: `${ent[i]} ${sDat(slots[a])} gittiyse ${ent[k]} ${sDat(slots[b])} gitmiştir.`, f: p => p[i] !== a || p[k] === b, w: 1 });
    }
  }
  const sh = shuffle(pool), clues = [];
  let cur = all;
  for (const c of sh) {
    const nx = cur.filter(c.f);
    if (nx.length < cur.length) { clues.push(c); cur = nx; }
    if (cur.length === 1) break;
  }
  if (cur.length !== 1 || clues.length > (level === 3 ? 9 : 8)) return makePuzzle(mode, level);
  return { mode, level, n, ent, slots, truth, clues, grid: Array.from({ length: n }, () => Array(n).fill(0)), steps: [], revealed: false, start: Date.now() };
}
let PZ = null;
function consistent(pz, useClues) {
  return perms(pz.n).filter(p => pz.grid.every((row, i) => row.every((v, j) => v === 0 || (v === 1 ? p[i] === j : p[i] !== j))) && (!useClues || useClues.every(c => c.f(p))));
}
function puzzleHint(pz) {
  for (let i = 0; i < pz.n; i++) for (let j = 0; j < pz.n; j++) {
    const v = pz.grid[i][j];
    if ((v === 1 && pz.truth[i] !== j) || (v === 2 && pz.truth[i] === j)) return { err: true, i, j, text: `Bir işaretiniz hatalı: <b>${pz.ent[i]} – ${pz.slots[j]}</b> hücresini yeniden düşünün.` };
  }
  const P0 = consistent(pz);
  const unknown = [];
  for (let i = 0; i < pz.n; i++) for (let j = 0; j < pz.n; j++) if (pz.grid[i][j] === 0) unknown.push([i, j]);
  if (!unknown.length) return null;
  let best = null;
  for (const c of pz.clues) {
    const P1 = P0.filter(c.f); if (!P1.length) continue;
    const forced = unknown.filter(([i, j]) => P1.every(p => p[i] === j) || P1.every(p => p[i] !== j)).map(([i, j]) => [i, j, P1[0][i] === j ? 1 : 2]);
    const prev = unknown.filter(([i, j]) => P0.every(p => p[i] === j) || P0.every(p => p[i] !== j));
    const gain = forced.length - prev.length;
    if (forced.length && (!best || gain > best.gain || (gain === best.gain && forced.length < best.forced.length))) best = { c, forced, gain };
  }
  if (!best) { // ipuçları tek başına yetmiyorsa satır/sütun kuralı
    const P = P0; const forced = unknown.filter(([i, j]) => P.every(p => p[i] === j) || P.every(p => p[i] !== j)).map(([i, j]) => [i, j, P[0][i] === j ? 1 : 2]);
    return forced.length ? { text: "Her satırda ve her sütunda yalnızca bir ✓ olabilir. Dolu satır ve sütunlardan kalan hücreleri belirleyin.", forced } : null;
  }
  return { text: `Şu bilgiye odaklanın: <b>“${best.c.t}”</b>`, forced: best.forced };
}
function fdesc(pz, f) { return f.slice(0, 4).map(([i, j, v]) => `${pz.ent[i]} – ${pz.slots[j]}: ${v === 1 ? "✓" : "✗"}`).join(", ") + (f.length > 4 ? " …" : ""); }

/* ------------------------------------------------------------------ örüntüler */
function numberPattern(level) {
  const r = (a, b) => a + Math.floor(Math.random() * (b - a + 1));
  const L = Math.min(5, level), kinds = [["ar"], ["ar", "geo", "alt"], ["d2", "fib", "geo"], ["inter", "muladd", "d2"], ["sq", "muladd", "altop", "inter"]][L - 1];
  const k = kinds[r(0, kinds.length - 1)];
  let seq = [], rule = "";
  if (k === "ar") { const a = r(1, 30), d = r(2, 12) * (Math.random() < .25 ? -1 : 1); seq = [0, 1, 2, 3, 4, 5].map(i => a + d * i); rule = `Her terim öncekinden ${Math.abs(d)} ${d > 0 ? "fazla" : "eksik"}.`; }
  if (k === "geo") { const a = r(1, 6), q = r(2, 3); seq = [0, 1, 2, 3, 4, 5].map(i => a * q ** i); rule = `Her terim öncekinin ${q} katı.`; }
  if (k === "alt") { const a = r(2, 20), x = r(2, 9), y = r(1, 5); seq = [a]; for (let i = 1; i < 6; i++) seq.push(seq[i - 1] + (i % 2 ? x : -y)); rule = `Sırayla +${x} ve −${y} uygulanıyor.`; }
  if (k === "d2") { const a = r(1, 10), d = r(1, 5), e = r(1, 4); seq = [a]; for (let i = 0; i < 5; i++) seq.push(seq[i] + d + e * i); rule = `Ardışık farklar ${d}'den başlayıp ${e}'er artıyor.`; }
  if (k === "fib") { seq = [r(1, 5), r(2, 8)]; for (let i = 2; i < 6; i++) seq.push(seq[i - 1] + seq[i - 2]); rule = "Her terim önceki iki terimin toplamı."; }
  if (k === "inter") { const a = r(1, 9), d = r(2, 6), b = r(30, 60), f = r(2, 7); for (let i = 0; i < 3; i++) seq.push(a + d * i, b - f * i); rule = `Tek sıralar +${d}, çift sıralar −${f} ile ilerleyen iç içe iki dizi.`; }
  if (k === "muladd") { const m = r(2, 3), c = r(-3, 4) || 1; seq = [r(1, 5)]; for (let i = 1; i < 6; i++) seq.push(seq[i - 1] * m + c); rule = `Her terim öncekinin ${m} katının ${Math.abs(c)} ${c > 0 ? "fazlası" : "eksiği"}.`; }
  if (k === "sq") { const s = r(1, 4), c = r(-3, 5); seq = [0, 1, 2, 3, 4, 5].map(i => (s + i) ** 2 + c); rule = `Terimler ardışık tam karelerin ${c >= 0 ? c + " fazlası" : -c + " eksiği"}: (${s}+n)² ${c >= 0 ? "+" : "−"} ${Math.abs(c)}.`; }
  if (k === "altop") { seq = [r(2, 6)]; const x = r(2, 3), y = r(1, 6); for (let i = 1; i < 6; i++) seq.push(i % 2 ? seq[i - 1] * x : seq[i - 1] + y); rule = `Sırayla ×${x} ve +${y} uygulanıyor.`; }
  return { shown: seq.slice(0, 5), ans: seq[5], rule, level: L };
}
const FILLS = ["", "o", "h"];
function figSVG(f) {
  const pts = []; const R = 24;
  for (let i = 0; i < f.sides; i++) { const a = (Math.PI * 2 * i / f.sides) - Math.PI / 2 + f.rot * Math.PI / 180; pts.push((32 + R * Math.cos(a)).toFixed(1) + "," + (32 + R * Math.sin(a)).toFixed(1)); }
  const dots = Array.from({ length: f.dots }, (_, i) => `<circle cx="${20 + i * 8}" cy="60" r="2.4" fill="var(--text)"/>`).join("");
  return `<svg viewBox="0 0 64 64" aria-hidden="true"><defs><pattern id="hatch" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="0" y2="6" stroke="var(--series-1)" stroke-width="2.5"/></pattern></defs><polygon class="fig ${FILLS[f.fill]}" points="${pts.join(" ")}"/><line x1="32" y1="32" x2="${(32 + 16 * Math.cos((f.rot - 90) * Math.PI / 180)).toFixed(1)}" y2="${(32 + 16 * Math.sin((f.rot - 90) * Math.PI / 180)).toFixed(1)}" stroke="var(--text)" stroke-width="2.5" stroke-linecap="round"/>${dots}</svg>`;
}
function shapePattern(level) {
  const attrs = shuffle(["sides", "rot", "fill", "dots"]).slice(0, Math.min(3, level));
  const step = { sides: 1, rot: [45, 90][Math.floor(Math.random() * 2)], fill: 1, dots: 1 };
  const base = { sides: 3, rot: 0, fill: 0, dots: 0 };
  const at = i => { const f = { ...base }; attrs.forEach(a => { if (a === "sides") f.sides = 3 + i; if (a === "rot") f.rot = (i * step.rot) % 360; if (a === "fill") f.fill = i % 3; if (a === "dots") f.dots = i; }); if (!attrs.includes("sides")) f.sides = 4; return f; };
  const seq = [0, 1, 2, 3].map(at), ans = at(4);
  const wrongs = []; const key = f => JSON.stringify(f);
  const variants = [{ ...ans, rot: (ans.rot + 90) % 360 }, { ...ans, sides: ans.sides + 1 }, { ...ans, fill: (ans.fill + 1) % 3 }, { ...ans, dots: Math.max(0, ans.dots - 1) }, { ...ans, sides: Math.max(3, ans.sides - 1) }, { ...ans, rot: (ans.rot + 45) % 360 }, at(3), { ...ans, dots: ans.dots + 1 }];
  for (const v of shuffle(variants)) if (key(v) !== key(ans) && !wrongs.some(w => key(w) === key(v))) wrongs.push(v);
  const opts = shuffle([ans, ...wrongs.slice(0, 4)]);
  const desc = { sides: "kenar sayısı her adımda 1 artıyor", rot: `iç çizgi her adımda ${step.rot}° dönüyor`, fill: "dolgu sırayla dolu → boş → taralı değişiyor", dots: "alttaki nokta sayısı her adımda 1 artıyor" };
  return { seq, opts, a: opts.indexOf(ans), rule: attrs.map(a => desc[a]).join("; ") + "." };
}

/* ------------------------------------------------------------------ görünüm */
function renderLogic(sub) {
  const root = $("#view"), d = S(), xp = d.xp.logic || 0, lvl = 1 + Math.floor(xp / 150);
  const head = `<div class="page-head"><div><div class="crumb">${sub ? '<a href="#/mantik">← Mantık Atölyesi</a>' : "Mantık Atölyesi"}</div><h1>${{ "": "Mantık Atölyesi", tablo: "Tablo Kurma Bulmacası", sayi: "Sayı Örüntüleri", sekil: "Şekil Örüntüleri" }[sub || ""]}</h1>
    <p>Doğru cevabı görmekten çok, soruyu nasıl çözümleyeceğinizi öğrenin.</p></div><div class="card flat" style="padding:12px 16px;min-width:220px"><div class="row between"><b>Seviye ${lvl}</b><span class="small muted">${xp} XP</span></div>${progressBar(pct(xp % 150, 150))}</div></div>`;
  if (!sub) {
    const mods = [
      ["tablo", "Tablo kurma: sıralama", "Kişileri günlere yerleştirin; ipucu sistemi bir sonraki mantıksal adımı gösterir.", "puzzle", "#/mantik/tablo?m=sira"],
      ["tablo", "Tablo kurma: eşleştirme", "Kişi–il eşleştirmesi; koşullu önermelerle çıkarım yapın.", "puzzle", "#/mantik/tablo?m=esle"],
      ["sayi", "Sayı örüntüleri", "Beş seviyeli, sonsuz üretilen diziler. Arka arkaya 5 doğru seviye atlatır.", "chart", "#/mantik/sayi"],
      ["sekil", "Şekil örüntüleri", "Kenar, dönme, dolgu ve nokta değişimlerini birlikte izleyin.", "star", "#/mantik/sekil"]
    ];
    const cnt = sub => QB.filter(q => q.sub === sub).length;
    root.innerHTML = head + `<div class="grid g2">${mods.map(m => `<a class="card topic-card" href="${m[4]}"><div class="row">${ic(m[3])}<b>${m[1]}</b></div><p class="small muted" style="margin:0">${m[2]}</p></a>`).join("")}</div>
      <div class="grid g3" style="margin-top:16px">
        <div class="card"><h3>${ic("exam")}Zamanlı mantık testi</h3><p class="small muted">10 soru · 15 dakika · sayısal ve sözel mantık karışık. Doğru başına 10 XP.</p><button class="btn primary" id="lg-timed">Başlat</button></div>
        <div class="card"><h3>${ic("bulb")}Koşullu çıkarım</h3><p class="small muted">Ek koşulla çözüm kümesini daraltma alıştırmaları (${cnt("Koşullu çıkarım")} soru), anında çözümlü.</p><button class="btn" id="lg-cond">Alıştırmaya başla</button></div>
        <div class="card"><h3>${ic("puzzle")}Sözel ve sayısal mantık setleri</h3><p class="small muted">Sıralama, eşleştirme, gruplandırma ve kural tabanlı ortak bilgi grupları.</p><div class="row"><button class="btn" id="lg-soz">Sözel mantık</button><button class="btn" id="lg-say">Sayısal mantık</button></div></div></div>
      <div class="card" style="margin-top:16px"><h3>Tablo kurma yöntemi: adım adım</h3><ol class="small" style="margin:0;padding-left:1.2em"><li>Bilgileri okuyun ve kişiler × yerler tablosu çizin.</li><li>Kesin bilgileri (✓) ve doğrudan olanaksızlıkları (✗) işaretleyin.</li><li>'Hemen önce', 'yan yana' gibi blok bilgileri olası konumlara yerleştirin.</li><li>Her satırda ve sütunda tek ✓ olacağını kullanarak kalan hücreleri eleyin.</li><li>Koşullu önermelerde (A ise B) yalnızca karşıt tersin (B değilse A değil) geçerli olduğunu unutmayın.</li></ol></div>`;
    $("#lg-timed").onclick = () => {
      const used = usedIds();
      const ids = [...pickGroups(QB.filter(q => q.topic === "saymantik"), 5, used), ...pickGroups(QB.filter(q => q.topic === "sozmantik"), 5, used)].map(q => q.id);
      startExam({ kind: "mantik", title: "Zamanlı Mantık Testi", minutes: 15, sections: [{ key: "mantik", label: "Mantık", ids }] });
    };
    $("#lg-cond").onclick = () => startPractice(shuffle(QB.filter(q => q.sub === "Koşullu çıkarım")).map(q => q.id), "Koşullu çıkarım", "#/mantik");
    $("#lg-soz").onclick = () => startPractice(QB.filter(q => q.topic === "sozmantik").map(q => q.id), "Sözel mantık", "#/mantik");
    $("#lg-say").onclick = () => startPractice(QB.filter(q => q.topic === "saymantik").map(q => q.id), "Sayısal mantık", "#/mantik");
    return;
  }
  if (sub === "tablo") {
    const mode = (location.hash.split("m=")[1] || "sira").slice(0, 4) === "esle" ? "esle" : "sira";
    const lv = +(window._pzl || 1);
    if (!PZ || PZ.mode !== mode || PZ.level !== lv) PZ = makePuzzle(mode, lv);
    const pz = PZ;
    const cells = pz.ent.map((e, i) => `<tr><th style="text-align:right">${e}</th>${pz.slots.map((s, j) => `<td><button data-c="${i},${j}" class="${["", "y", "n"][pz.grid[i][j]]}" aria-label="${e} – ${s}">${["", "✓", "✗"][pz.grid[i][j]]}</button></td>`).join("")}</tr>`).join("");
    const intro = mode === "sira" ? `${pz.ent.join(", ")} adlı ${pz.n} kişi, ${pz.slots[0]}–${pz.slots[pz.n - 1]} günlerinde her gün bir kişi olmak üzere birer sunum yapacaktır.` : `${pz.ent.join(", ")} adlı ${pz.n} kişi ${pz.slots.join(", ")} illerinden birine gitmiş, her ile yalnızca bir kişi gitmiştir.`;
    root.innerHTML = head + `<div class="row" style="margin-bottom:12px"><div class="tabs" id="pzlv">${[1, 2, 3].map(l => `<button data-l="${l}" class="${lv === l ? "on" : ""}">${["", "Kolay", "Orta", "Zor"][l]}</button>`).join("")}</div><a class="btn sm" href="#/mantik/tablo?m=${mode === "sira" ? "esle" : "sira"}">${mode === "sira" ? "Eşleştirmeye geç" : "Sıralamaya geç"}</a><button class="btn sm" id="pznew">${ic("redo")}Yeni bulmaca</button></div>
    <div class="grid g2"><div class="card"><h3>Bilgiler</h3><p class="small">${intro}</p><ul class="clean small">${pz.clues.map(c => `<li>${c.t}</li>`).join("")}</ul>
      <p class="tiny muted">Hücreye tıklayın: boş → ✓ → ✗ → boş.</p></div>
    <div class="card"><div class="tbl-wrap"><table class="lgrid"><tr><th></th>${pz.slots.map(s => `<th>${mode === "sira" ? s.slice(0, 3) : s}</th>`).join("")}</tr>${cells}</table></div>
      <div class="row" style="margin-top:12px"><button class="btn primary" id="pzcheck">${ic("check")}Kontrol et</button><button class="btn" id="pzhint">${ic("bulb")}İpucu</button><button class="btn ghost" id="pzsolve">Adım adım çözüm</button></div>
      <div id="pzmsg" style="margin-top:12px"></div></div></div>`;
    $$("[data-c]").forEach(b => b.onclick = () => { const [i, j] = b.dataset.c.split(",").map(Number); pz.grid[i][j] = (pz.grid[i][j] + 1) % 3; renderLogic("tablo"); });
    $$("#pzlv button").forEach(b => b.onclick = () => { window._pzl = +b.dataset.l; PZ = null; renderLogic("tablo"); });
    $("#pznew").onclick = () => { PZ = null; renderLogic("tablo"); };
    $("#pzhint").onclick = () => { const h = puzzleHint(pz); $("#pzmsg").innerHTML = h ? `<div class="note ${h.err ? "bad" : ""}">${h.text}${h.forced ? `<br><span class="small">Bu adımla kesinleşenler: ${fdesc(pz, h.forced)}</span>` : ""}</div>` : '<div class="note good">Tablo dolu görünüyor; kontrol edin.</div>'; };
    $("#pzsolve").onclick = () => {
      const steps = []; let guard = 0;
      while (guard++ < 40) { const h = puzzleHint(pz); if (!h) break; if (h.err) { pz.grid[h.i][h.j] = 0; steps.push("Hatalı işaret kaldırıldı: " + pz.ent[h.i] + " – " + pz.slots[h.j]); continue; } h.forced.forEach(([i, j, v]) => pz.grid[i][j] = v); steps.push(h.text.replace(/<[^>]+>/g, "") + " → " + fdesc(pz, h.forced)); }
      pz.revealed = true; renderLogic("tablo");
      $("#pzmsg").innerHTML = `<div class="note"><b>Çözüm adımları</b><ol class="small" style="margin:.4em 0 0 1.2em;padding:0">${steps.map(s => `<li>${esc(s)}</li>`).join("")}</ol></div>`;
    };
    $("#pzcheck").onclick = () => {
      let wrong = 0, missing = 0;
      for (let i = 0; i < pz.n; i++) { if (pz.grid[i][pz.truth[i]] !== 1) missing++; for (let j = 0; j < pz.n; j++) if ((pz.grid[i][j] === 1 && pz.truth[i] !== j) || (pz.grid[i][j] === 2 && pz.truth[i] === j)) wrong++; }
      if (!wrong && !missing) {
        if (!pz.revealed && !pz.scored) { pz.scored = 1; d.xp.logic += 20 + pz.level * 10; Store.save(); }
        $("#pzmsg").innerHTML = `<div class="note good"><b>Tebrikler, bulmaca çözüldü!</b> ${pz.revealed ? "(Çözüm gösterildiği için XP verilmedi.)" : `+${20 + pz.level * 10} XP · ${mmss(Date.now() - pz.start)}`}</div>`;
      } else $("#pzmsg").innerHTML = `<div class="note ${wrong ? "bad" : "warn"}">${wrong ? `${wrong} hatalı işaret var. ` : ""}${missing ? `${missing} kişinin yeri henüz ✓ ile belirlenmedi.` : ""}</div>`;
    };
    return;
  }
  if (sub === "sayi") {
    const st = window._np = window._np || { level: 1, run: 0, cur: null, best: 0 };
    if (!st.cur) st.cur = numberPattern(st.level);
    const c = st.cur;
    root.innerHTML = head + `<div class="card" style="max-width:640px"><div class="row between"><span class="chip orig">Seviye ${st.level} / 5</span><span class="small muted">Arka arkaya doğru: ${st.run} · en iyi: ${st.best}</span></div>
      <p style="margin-top:14px">? yerine gelmesi gereken sayıyı yazın.</p><div class="seq" style="font-size:1.4rem;margin:8px 0 16px">${c.shown.join(", ")}, ?</div>
      <div class="row"><input type="number" id="npin" style="max-width:160px" aria-label="Cevap"><button class="btn primary" id="npok">Kontrol et</button><button class="btn ghost" id="npskip">Göster ve geç</button></div><div id="npmsg" style="margin-top:12px"></div></div>`;
    const next = () => { st.cur = null; renderLogic("sayi"); };
    $("#npin").focus();
    $("#npin").onkeydown = e => { if (e.key === "Enter") $("#npok").click(); };
    $("#npok").onclick = () => {
      const v = +$("#npin").value;
      if ($("#npin").value === "") return;
      if (v === c.ans) { st.run++; st.best = Math.max(st.best, st.run); d.xp.logic += 5 * st.level; Store.save(); let up = ""; if (st.run % 5 === 0 && st.level < 5) { st.level++; up = ` <b>Seviye ${st.level}'e yükseldiniz!</b>`; } $("#npmsg").innerHTML = `<div class="note good">Doğru! ${c.rule}${up}</div>`; setTimeout(next, 1300); }
      else { st.run = 0; $("#npmsg").innerHTML = `<div class="note bad">Yanlış. Doğru cevap <b>${c.ans}</b>. Kural: ${c.rule}</div><button class="btn sm" id="npn" style="margin-top:8px">Sonraki</button>`; $("#npn").onclick = next; }
    };
    $("#npskip").onclick = () => { st.run = 0; $("#npmsg").innerHTML = `<div class="note">Cevap <b>${c.ans}</b>. Kural: ${c.rule}</div><button class="btn sm" id="npn" style="margin-top:8px">Sonraki</button>`; $("#npn").onclick = next; };
    return;
  }
  if (sub === "sekil") {
    const st = window._sp = window._sp || { level: 1, run: 0, cur: null };
    if (!st.cur) st.cur = shapePattern(st.level);
    const c = st.cur;
    root.innerHTML = head + `<div class="card" style="max-width:720px"><div class="row between"><span class="chip orig">Seviye ${st.level} / 3 · ${st.level} özellik değişiyor</span><span class="small muted">Arka arkaya doğru: ${st.run}</span></div>
      <p style="margin-top:14px">Dizide ? yerine hangi şekil gelmelidir?</p><div class="shape-seq">${c.seq.map(figSVG).join("")}<div class="q">?</div></div>
      <div class="shape-opts" style="margin-top:16px">${c.opts.map((f, i) => `<button data-s="${i}" aria-label="Seçenek ${"ABCDE"[i]}"><div class="tiny muted">${"ABCDE"[i]}</div>${figSVG(f)}</button>`).join("")}</div><div id="spmsg" style="margin-top:12px"></div></div>`;
    $$("[data-s]").forEach(b => b.onclick = () => {
      if (c.done) return; c.done = 1; const i = +b.dataset.s;
      $$("[data-s]").forEach(x => { const k = +x.dataset.s; if (k === c.a) x.classList.add("ok"); else if (k === i) x.classList.add("no"); });
      if (i === c.a) { st.run++; d.xp.logic += 5 * st.level; Store.save(); if (st.run % 4 === 0 && st.level < 3) st.level++; }
      else st.run = 0;
      $("#spmsg").innerHTML = `<div class="note ${i === c.a ? "good" : "bad"}">${i === c.a ? "Doğru!" : "Yanlış."} Kural: ${c.rule}</div><button class="btn sm" id="spn" style="margin-top:8px">Sonraki</button>`;
      $("#spn").onclick = () => { st.cur = null; renderLogic("sekil"); };
    });
  }
}
