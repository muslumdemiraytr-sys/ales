/* ALES Akademi — soru çözme oturumu ve sınav motoru (deneme, konu testi, zamanlı test). */
"use strict";

/* ================================================================ soru seçimi */
function usedIds() {
  const u = new Set(Object.keys(S().att));
  S().exams.forEach(e => e.qs.forEach(id => u.add(id)));
  return u;
}
function pickSingles(pool, n, used) {
  const fresh = shuffle(pool.filter(q => !used.has(q.id))), old = shuffle(pool.filter(q => used.has(q.id)));
  return fresh.concat(old).slice(0, n);
}
function pickGroups(pool, n, used) {
  const groups = {};
  pool.filter(q => q.group).forEach(q => (groups[q.group.id] = groups[q.group.id] || []).push(q));
  let gl = Object.values(groups);
  gl = shuffle(gl).sort((a, b) => a.filter(q => used.has(q.id)).length / a.length - b.filter(q => used.has(q.id)).length / b.length);
  const out = [];
  for (const g of gl) { if (out.length >= n) break; out.push(...g.slice(0, n - out.length)); }
  if (out.length < n) out.push(...pickSingles(pool.filter(q => !q.group && !out.includes(q)), n - out.length, used));
  return out;
}
const byTopic = (t, sub) => QB.filter(q => q.topic === t && (!sub || sub.includes(q.sub)));

function buildDeneme(kind) {
  const used = usedIds(), taken = new Set();
  const take = arr => { arr.forEach(q => taken.add(q.id)); return arr.map(q => q.id); };
  const avail = arr => arr.filter(q => !taken.has(q.id));
  const full = kind === "tam";
  const k = full ? 1 : 0.4;
  const sayDist = full ? { temel: 3, bolunebilme: 2, rasyonel: 2, esitsizlik: 2, uslu: 2, cebir: 2, oran: 2, problem: 4, islem: 2, sayma: 1 }
    : { temel: 1, bolunebilme: 1, rasyonel: 1, esitsizlik: 1, uslu: 1, cebir: 1, oran: 1, problem: 2, islem: 1 };
  let say = [];
  for (const [t, n] of Object.entries(sayDist)) say.push(...take(pickSingles(avail(byTopic(t)).filter(q => !q.group), n, used)));
  say.push(...take(pickGroups(avail(QB.filter(q => q.area === "say" && (q.topic === "veri" || q.topic === "saymantik"))), full ? 21 : 8, used)));
  say.push(...take(pickSingles(avail(byTopic("geometri")), full ? 7 : 3, used)));
  let soz = [];
  const sp = (pool, n) => soz.push(...take(pickSingles(avail(pool).filter(q => !q.group), n, used)));
  sp(byTopic("sozcuk", ["Boşluk doldurma"]), Math.round(5 * k));
  sp(byTopic("cumle", ["Kesin çıkarım"]), full ? 3 : 1);
  sp(QB.filter(q => (q.topic === "cumle" && q.sub !== "Kesin çıkarım") || (q.topic === "yapi" && q.sub === "Söz dizimi / sıralama") || (q.topic === "sozcuk" && q.sub !== "Boşluk doldurma")), full ? 4 : 2);
  sp(byTopic("yapi", ["Cümle yer değiştirme"]), full ? 3 : 1);
  sp(byTopic("yapi", ["Anlam bütünlüğünü bozan cümle"]), full ? 3 : 1);
  sp(QB.filter(q => q.topic === "paragraf" || (q.topic === "yapi" && q.sub === "Paragraf tamamlama")), full ? 19 : 8);
  soz.push(...take(pickGroups(avail(byTopic("paragraf")), full ? 5 : 2, used)));
  soz.push(...take(pickGroups(avail(byTopic("sozmantik")), full ? 8 : 4, used)));
  return { say: say.slice(0, full ? 50 : 20), soz: soz.slice(0, full ? 50 : 20) };
}

/* ================================================================ sınav motoru */
function startExam(cfg) {
  const d = S();
  d.active = { id: uid(), kind: cfg.kind, title: cfg.title, ref: cfg.ref || null, sections: cfg.sections, ans: {}, mark: {}, time: {},
    cur: [0, 0], start: Date.now(), end: Date.now() + cfg.minutes * 60000, minutes: cfg.minutes, last: Date.now() };
  Store.save(); location.hash = "#/sinav";
}
function startDeneme(kind) {
  const set = buildDeneme(kind);
  const full = kind === "tam";
  startExam({ kind, title: full ? "Tam Deneme (50 Sayısal + 50 Sözel)" : "Mini Deneme (20 Sayısal + 20 Sözel)", minutes: full ? 150 : 60,
    sections: [{ key: "say", label: "Sayısal Testi", ids: set.say }, { key: "soz", label: "Sözel Testi", ids: set.soz }] });
}
function startTopicTest(topic, kind) {
  const L = LMAP[topic], pool = byTopic(topic);
  const lv = { kolay: [1, 2], orta: [3], zor: [4, 5], final: [1, 2, 3, 4, 5] }[kind];
  let qs = pool.filter(q => lv.includes(q.level));
  const want = kind === "final" ? 12 : 8;
  if (qs.length < want) { // zorluk aralığında yeterli soru yoksa bir alt/üst seviyeyle tamamla
    const near = kind === "zor" ? pool.filter(q => q.level === 3) : kind === "kolay" ? pool.filter(q => q.level === 3) : pool.filter(q => q.level !== 3);
    qs = qs.concat(shuffle(near).slice(0, want - qs.length));
  }
  const pick = pool.some(q => q.group) ? pickGroups(qs, want, usedIds()) : pickSingles(qs, want, usedIds());
  const ids = pick.map(q => q.id);
  const min = Math.max(5, Math.ceil(pick.reduce((s, q) => s + q.sure, 0) / 60 * 1.15));
  const names = { kolay: "Kolay seviye test", orta: "Orta seviye test", zor: "Zor seviye test", final: "Konu sonu değerlendirmesi" };
  startExam({ kind: "konu", title: `${L.title} — ${names[kind]}`, ref: { topic, kind }, minutes: min, sections: [{ key: L.area, label: L.title, ids }] });
}
function curQ(a = S().active) { const [s, i] = a.cur; return QMAP[a.sections[s].ids[i]]; }
function tickTime(a) { const now = Date.now(); const q = curQ(a); if (q) a.time[q.id] = (a.time[q.id] || 0) + (now - a.last); a.last = now; }
function examGo(s, i) { const a = S().active; tickTime(a); a.cur = [s, i]; Store.save(); renderExam(); window.scrollTo(0, 0); }

let EXAM_TIMER = null;
function renderExam() {
  const a = S().active, root = $("#view");
  if (!a) { location.hash = "#/deneme"; return; }
  if (Date.now() >= a.end) { finishExam(true); return; }
  const [si, qi] = a.cur, sec = a.sections[si], q = curQ(a);
  const total = a.sections.reduce((s, x) => s + x.ids.length, 0), answered = Object.keys(a.ans).length;
  const grid = a.sections.map((s, sIdx) => `<div style="margin-top:10px"><div class="small muted" style="margin-bottom:6px;font-weight:600">${esc(s.label)}</div><div class="navgrid">${s.ids.map((id, i) =>
    `<button data-go="${sIdx},${i}" class="${a.ans[id] != null ? "ans" : ""} ${a.mark[id] ? "mk" : ""} ${sIdx === si && i === qi ? "cur" : ""}" aria-label="Soru ${i + 1}">${i + 1}</button>`).join("")}</div></div>`).join("");
  const isLast = si === a.sections.length - 1 && qi === sec.ids.length - 1, isFirst = si === 0 && qi === 0;
  root.innerHTML = `<div class="exam-bar"><div><div class="small muted">${esc(a.title)}</div><b>${esc(sec.label)} · Soru ${qi + 1}/${sec.ids.length}</b></div>
    <div class="row"><span class="clock" id="clock" aria-live="off">${mmss(a.end - Date.now())}</span><button class="btn primary" id="xfinish">${ic("flag")}Sınavı bitir</button></div></div>
  <div class="qwrap"><div class="card qcard">${questionHTML(q, { sel: a.ans[q.id] ?? null, num: qi + 1 })}
    <div class="row between" style="margin-top:18px"><button class="btn" id="xprev" ${isFirst ? "disabled" : ""}>${ic("left")}Önceki</button>
      <div class="row"><button class="btn ${a.mark[q.id] ? "on" : ""}" id="xmark">${ic("flag")}${a.mark[q.id] ? "İşaretli" : "İşaretle"}</button><button class="btn ghost" id="xclear" ${a.ans[q.id] == null ? "disabled" : ""}>Cevabı sil</button></div>
      <button class="btn ${isLast ? "" : "primary"}" id="xnext" ${isLast ? "disabled" : ""}>Sonraki${ic("right")}</button></div>
    <p class="tiny muted" style="margin-top:12px">Sınav sırasında doğru cevap ve çözüm gösterilmez. Klavye: A–E seçer, ← → gezinir.</p></div>
  <div class="qside stack"><div class="card"><div class="row between"><b>Soru haritası</b><span class="small muted">${answered}/${total} cevaplı</span></div>${grid}
    <div class="legend" style="margin-top:12px"><span><i style="background:var(--accent)"></i>Cevaplı</span><span><i></i>Boş</span><span><i style="background:var(--warn);border-radius:50%"></i>İşaretli</span></div></div></div></div>`;
  $$(".opt", root).forEach(b => b.onclick = () => { const v = +b.dataset.opt; if (a.ans[q.id] === v) delete a.ans[q.id]; else a.ans[q.id] = v; tickTime(a); Store.save(); renderExam(); });
  $$("[data-go]", root).forEach(b => b.onclick = () => { const [s, i] = b.dataset.go.split(",").map(Number); examGo(s, i); });
  $("#xprev").onclick = () => qi > 0 ? examGo(si, qi - 1) : examGo(si - 1, a.sections[si - 1].ids.length - 1);
  $("#xnext").onclick = () => qi < sec.ids.length - 1 ? examGo(si, qi + 1) : examGo(si + 1, 0);
  $("#xmark").onclick = () => { if (a.mark[q.id]) delete a.mark[q.id]; else a.mark[q.id] = 1; Store.save(); renderExam(); };
  $("#xclear").onclick = () => { delete a.ans[q.id]; Store.save(); renderExam(); };
  $("#xfinish").onclick = () => {
    const blank = total - answered, mk = Object.keys(a.mark).length;
    confirmBox("Sınavı bitirmek istiyor musunuz?", `${answered} soru cevaplandı, <b>${blank}</b> soru boş${mk ? `, ${mk} soru işaretli` : ""}. Bitirdikten sonra cevaplar değiştirilemez.`, "Evet, bitir", () => finishExam(false));
  };
  clearInterval(EXAM_TIMER);
  EXAM_TIMER = setInterval(() => {
    const c = $("#clock"); if (!c || !S().active) { clearInterval(EXAM_TIMER); return; }
    const left = S().active.end - Date.now(); c.textContent = mmss(left); c.classList.toggle("low", left < 5 * 60000);
    if (left <= 0) { clearInterval(EXAM_TIMER); finishExam(true); }
  }, 1000);
}
function examKeys(e) {
  if (!location.hash.startsWith("#/sinav") || !S().active || document.querySelector(".modal-bg")) return;
  if (e.target.matches && e.target.matches("input,textarea,select")) return;
  const k = e.key.toUpperCase();
  if ("ABCDE".includes(k) && k.length === 1) { const b = $(`.opt[data-opt="${"ABCDE".indexOf(k)}"]`); b && b.click(); }
  if (e.key === "ArrowRight") { const b = $("#xnext"); b && !b.disabled && b.click(); }
  if (e.key === "ArrowLeft") { const b = $("#xprev"); b && !b.disabled && b.click(); }
}
function finishExam(auto) {
  clearInterval(EXAM_TIMER);
  const d = S(), a = d.active; if (!a) return;
  tickTime(a);
  const res = { id: a.id, ts: Date.now(), kind: a.kind, title: a.title, ref: a.ref, minutes: a.minutes, used: Math.min(a.minutes * 60000, Date.now() - a.start), auto: !!auto, secs: [], topics: {}, qs: [], ans: {}, time: a.time };
  for (const sec of a.sections) {
    let dd = 0, y = 0, b = 0;
    for (const id of sec.ids) {
      const q = QMAP[id], c = a.ans[id]; res.qs.push(id);
      const t = res.topics[q.topic] = res.topics[q.topic] || [0, 0, 0];
      if (c == null) { b++; t[2]++; continue; }
      res.ans[id] = c;
      const ok = recordAnswer(id, c, a.time[id] || 0, a.kind === "konu" ? "test" : "deneme");
      if (ok) { dd++; t[0]++; } else { y++; t[1]++; }
    }
    res.secs.push({ key: sec.key, label: sec.label, n: sec.ids.length, d: dd, y, b, net: net(dd, y) });
  }
  if (a.kind === "konu" && a.ref) {
    const s = res.secs[0], L = d.lessons[a.ref.topic] = d.lessons[a.ref.topic] || {};
    (L.tests = L.tests || {})[a.ref.kind] = { d: s.d, y: s.y, b: s.b, n: s.n, p: pct(s.d, s.n), ts: res.ts };
  }
  if (a.kind === "mantik") d.xp.logic += res.secs[0].d * 10;
  d.exams.push(res); d.active = null; Store.save();
  if (auto) toast("Süre doldu — sınav otomatik olarak teslim edildi.");
  location.hash = "#/sonuc/" + res.id;
}

/* ================================================================ sonuç ekranı */
function renderResult(id) {
  const e = S().exams.find(x => x.id === id), root = $("#view");
  if (!e) { root.innerHTML = `<div class="empty"><b>Sonuç bulunamadı</b><a href="#/deneme">Deneme merkezine dön</a></div>`; return; }
  const tot = e.secs.reduce((s, x) => ({ d: s.d + x.d, y: s.y + x.y, b: s.b + x.b, n: s.n + x.n }), { d: 0, y: 0, b: 0, n: 0 });
  const secCards = e.secs.map(s => `<div class="card"><div class="row between"><h3 style="margin:0">${esc(s.label)}</h3>${s.key === "say" || s.key === "soz" ? areaChip(s.key) : ""}</div>
    <div class="grid g4" style="margin-top:12px"><div class="stat"><span class="l">Doğru</span><span class="v" style="color:var(--good)">${s.d}</span></div><div class="stat"><span class="l">Yanlış</span><span class="v" style="color:var(--bad)">${s.y}</span></div><div class="stat"><span class="l">Boş</span><span class="v">${s.b}</span></div><div class="stat"><span class="l">Net</span><span class="v">${fmt1(s.net)}</span><span class="s">/ ${s.n}</span></div></div></div>`).join("");
  const rows = Object.entries(e.topics).map(([t, v]) => `<tr><td>${esc(LMAP[t].title)}</td><td class="n">${v[0] + v[1] + v[2]}</td><td class="n">${v[0]}</td><td class="n">${v[1]}</td><td class="n">${v[2]}</td><td class="n">${fmt1(net(v[0], v[1]))}</td><td class="n">%${pct(v[0], v[0] + v[1] + v[2])}</td></tr>`).join("");
  const filt = window._rf || "hepsi";
  const list = e.qs.filter(id => filt === "hepsi" || (filt === "yanlis" && e.ans[id] != null && e.ans[id] !== QMAP[id].a) || (filt === "bos" && e.ans[id] == null) || (filt === "dogru" && e.ans[id] === QMAP[id].a));
  const back = e.kind === "konu" && e.ref ? `#/konu/${e.ref.topic}` : e.kind === "mantik" ? "#/mantik" : "#/deneme";
  root.innerHTML = `<div class="page-head"><div><div class="crumb"><a href="${back}">← Geri</a></div><h1>${esc(e.title)}</h1><p>${new Date(e.ts).toLocaleString("tr-TR")} · Kullanılan süre ${mmss(e.used)} / ${e.minutes} dk${e.auto ? " · <b>süre dolduğu için otomatik teslim</b>" : ""}</p></div>
    <div class="row"><a class="btn" href="#/yanlislar">Yanlışlarım</a><a class="btn primary" href="${back}">Devam et</a></div></div>
    <div class="stack">${e.secs.length > 1 ? `<div class="card hero"><div class="row between"><div><p style="margin:0">Toplam</p><h1 style="margin:0">${fmt1(net(tot.d, tot.y))} net</h1><p style="margin:0">${tot.d} doğru · ${tot.y} yanlış · ${tot.b} boş — ${tot.n} soru</p></div>
      <p class="small" style="max-width:360px;margin:0">Net = Doğru − Yanlış ÷ 4 (ÖSYM 2026-ALES Kılavuzu, md. 3.9). ALES puanı standart puan ve oturum istatistiklerine bağlı olduğundan bu netten kesin puan hesaplanamaz; tahmin için <a href="#/puan" style="color:#fff;text-decoration:underline">Puan Hesaplama</a>.</p></div></div>` : ""}
    <div class="grid ${e.secs.length > 1 ? "g2" : ""}">${secCards}</div>
    <div class="card"><h3>Konu bazında analiz</h3><div class="tbl-wrap"><table class="t"><tr><th>Konu</th><th class="n">Soru</th><th class="n">D</th><th class="n">Y</th><th class="n">B</th><th class="n">Net</th><th class="n">Başarı</th></tr>${rows}</table></div></div>
    <div class="card"><div class="row between"><h3 style="margin:0">Ayrıntılı cevap analizi</h3><div class="tabs" id="rtabs">${[["hepsi", "Tümü"], ["yanlis", "Yanlışlar"], ["bos", "Boşlar"], ["dogru", "Doğrular"]].map(([k, l]) => `<button data-f="${k}" class="${filt === k ? "on" : ""}">${l}</button>`).join("")}</div></div>
    <div class="stack" style="margin-top:14px">${list.length ? list.map(id => { const q = QMAP[id], c = e.ans[id]; const st = c == null ? '<span class="chip">Boş</span>' : c === q.a ? '<span class="chip good">Doğru</span>' : '<span class="chip bad">Yanlış</span>';
      return `<details class="card flat"><summary class="row between" style="cursor:pointer"><span><b>${e.qs.indexOf(id) + 1}.</b> ${esc(plain(q.q).slice(0, 90))}…</span><span class="row">${st}<span class="tiny muted">${mmss(e.time[id] || 0)}</span></span></summary><div style="margin-top:12px">${questionHTML(q, { sel: c ?? null, reveal: true, showSol: true })}</div></details>`; }).join("") : '<div class="empty">Bu filtrede soru yok.</div>'}</div></div></div>`;
  $$("#rtabs button").forEach(b => b.onclick = () => { window._rf = b.dataset.f; renderResult(id); });
}

/* ================================================================ alıştırma oturumu (anında geri bildirim) */
let SESSION = null;
function startPractice(ids, title, back = "#/banka") {
  if (!ids.length) { toast("Bu filtreye uyan soru bulunamadı."); return; }
  SESSION = { ids, title, back, i: 0, sel: {}, checked: {}, shown: {}, t: {}, last: Date.now() };
  location.hash = "#/coz";
}
function renderPractice() {
  const root = $("#view"), s = SESSION;
  if (!s) { location.hash = "#/banka"; return; }
  const q = QMAP[s.ids[s.i]], d = S();
  const checked = s.checked[q.id] != null, sel = s.sel[q.id] ?? null;
  const done = Object.keys(s.checked).length, okN = Object.values(s.checked).filter(Boolean).length;
  s.last = Date.now();
  root.innerHTML = `<div class="page-head"><div><div class="crumb"><a href="${s.back}">← ${esc(s.title)}</a></div><h1>Soru ${s.i + 1} / ${s.ids.length}</h1></div>
    <div class="row"><span class="chip">${done} çözüldü · ${okN} doğru</span><button class="btn" id="pend">Oturumu bitir</button></div></div>
  <div class="qwrap"><div class="card qcard">${questionHTML(q, { sel, reveal: checked, showSol: checked || s.shown[q.id] })}
    <div class="row between" style="margin-top:18px"><button class="btn" id="pprev" ${s.i === 0 ? "disabled" : ""}>${ic("left")}Önceki</button>
      <div class="row">${checked ? "" : `<button class="btn primary" id="pcheck" ${sel == null ? "disabled" : ""}>${ic("check")}Cevabı kontrol et</button>`}
      ${checked || s.shown[q.id] ? "" : `<button class="btn ghost" id="psol">Çözümü göster</button>`}</div>
      <button class="btn ${checked ? "primary" : ""}" id="pnext" ${s.i === s.ids.length - 1 ? "disabled" : ""}>Sonraki${ic("right")}</button></div></div>
  <div class="qside stack"><div class="card"><div class="row between"><b>Bu soru</b><span class="qtimer" id="qt">${mmss(s.t[q.id] || 0)}</span></div>
    <p class="tiny muted" style="margin:6px 0 12px">Önerilen süre: ${q.sure} sn. Süre kontrol anına kadar ölçülür.</p>
    <div class="stack" style="gap:8px"><button class="btn ${d.fav[q.id] ? "on" : ""}" id="pfav">${ic("star")}${d.fav[q.id] ? "Favorilerde" : "Favorilere ekle"}</button>
    <button class="btn ${d.mark[q.id] ? "on" : ""}" id="pmark">${ic("flag")}${d.mark[q.id] ? "Daha sonra tekrar: işaretli" : "Daha sonra tekrar çöz"}</button>
    ${d.wrong[q.id] ? `<span class="chip bad">Yanlışlarım listesinde${d.wrong[q.id].fixed ? " · düzeltildi" : ""}</span>` : ""}</div></div>
    <div class="card"><b>Oturum</b>${progressBar(pct(done, s.ids.length))}<div class="navgrid" style="margin-top:10px">${s.ids.map((id, i) => `<button data-i="${i}" class="${s.checked[id] === 1 ? "ok" : s.checked[id] === 0 ? "no" : ""} ${i === s.i ? "cur" : ""}">${i + 1}</button>`).join("")}</div></div></div></div>`;
  const stop = () => { s.t[q.id] = (s.t[q.id] || 0) + (Date.now() - s.last); s.last = Date.now(); };
  if (!checked) $$(".opt", root).forEach(b => b.onclick = () => { s.sel[q.id] = +b.dataset.opt; stop(); renderPractice(); });
  const c = $("#pcheck"); c && (c.onclick = () => { stop(); const ok = recordAnswer(q.id, s.sel[q.id], s.t[q.id], "banka"); s.checked[q.id] = ok; Store.save(); renderPractice(); toast(ok ? "Doğru! 🎯" : "Yanlış — çözümü inceleyin, soru Yanlışlarım'a eklendi."); });
  const so = $("#psol"); so && (so.onclick = () => { s.shown[q.id] = 1; stop(); renderPractice(); });
  $("#pprev").onclick = () => { stop(); s.i--; renderPractice(); };
  $("#pnext").onclick = () => { stop(); s.i++; renderPractice(); };
  $$("[data-i]", root).forEach(b => b.onclick = () => { stop(); s.i = +b.dataset.i; renderPractice(); });
  $("#pfav").onclick = () => { if (d.fav[q.id]) delete d.fav[q.id]; else d.fav[q.id] = Date.now(); Store.save(); renderPractice(); };
  $("#pmark").onclick = () => { if (d.mark[q.id]) delete d.mark[q.id]; else d.mark[q.id] = Date.now(); Store.save(); renderPractice(); };
  $("#pend").onclick = () => {
    stop();
    modal(`<h3>Oturum özeti</h3><div class="grid g3" style="margin:12px 0"><div class="stat"><span class="l">Çözülen</span><span class="v">${done}</span></div><div class="stat"><span class="l">Doğru</span><span class="v" style="color:var(--good)">${okN}</span></div><div class="stat"><span class="l">Net</span><span class="v">${fmt1(net(okN, done - okN))}</span></div></div>
      <p class="small muted">Yanlış cevapladığınız sorular Yanlışlarım listesine kaydedildi.</p><div class="row" style="justify-content:flex-end"><button class="btn" data-close>Devam et</button><a class="btn primary" href="${s.back}" data-close>Bitir</a></div>`);
  };
  clearInterval(window._qt);
  window._qt = setInterval(() => { const el = $("#qt"); if (!el || !SESSION || checked) { clearInterval(window._qt); return; } el.textContent = mmss((s.t[q.id] || 0) + Date.now() - s.last); }, 1000);
}
function practiceKeys(e) {
  if (!location.hash.startsWith("#/coz") || document.querySelector(".modal-bg") || (e.target.matches && e.target.matches("input,textarea,select"))) return;
  const k = e.key.toUpperCase();
  if (k.length === 1 && "ABCDE".includes(k)) { const b = $(`.opt[data-opt="${"ABCDE".indexOf(k)}"]`); b && !b.disabled && b.click(); }
  if (e.key === "Enter") { const b = $("#pcheck"); b && !b.disabled && b.click(); }
  if (e.key === "ArrowRight") { const b = $("#pnext"); b && !b.disabled && b.click(); }
  if (e.key === "ArrowLeft") { const b = $("#pprev"); b && !b.disabled && b.click(); }
}
