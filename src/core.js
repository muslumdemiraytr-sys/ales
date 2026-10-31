/* ALES Akademi — çekirdek: veri katmanı, yardımcılar, soru gösterimi, grafikler. */
"use strict";
const APP = { version: "1.0.0" };
const QB = window.QBANK.questions;
const QMAP = Object.fromEntries(QB.map(q => [q.id, q]));
const LMAP = Object.fromEntries(window.LESSONS.map(l => [l.id, l]));
const LEVELS = ["", "Başlangıç", "Kolay", "Orta", "Zor", "İleri"];
const AREA = { say: "Sayısal", soz: "Sözel" };
const DAY = 86400000;

/* ------------------------------------------------------------------ yardımcılar */
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const pct = (a, b) => b ? Math.round(a * 100 / b) : 0;
const fmt1 = x => (Math.round(x * 100) / 100).toLocaleString("tr-TR");
const todayStr = (d = new Date()) => { const z = new Date(d.getTime() - d.getTimezoneOffset() * 60000); return z.toISOString().slice(0, 10); };
const addDays = (s, n) => todayStr(new Date(new Date(s + "T12:00:00").getTime() + n * DAY));
const dayDiff = (a, b) => Math.round((new Date(b + "T12:00:00") - new Date(a + "T12:00:00")) / DAY);
const trDate = (s, opt = { day: "numeric", month: "long" }) => new Date((s.length === 10 ? s + "T12:00:00" : s)).toLocaleDateString("tr-TR", opt);
const shuffle = (a, r = Math.random) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const uid = () => Math.random().toString(36).slice(2, 9);
const mmss = ms => { ms = Math.max(0, ms); const s = Math.floor(ms / 1000); const h = Math.floor(s / 3600), m = Math.floor(s % 3600 / 60), ss = s % 60; return (h ? h + ":" + String(m).padStart(2, "0") : m) + ":" + String(ss).padStart(2, "0"); };
const net = (d, y) => d - y / 4;

/* Soru metnindeki ⟦a/b⟧ belirtecini alt alta kesir olarak çizer. */
function rich(s) {
  return String(s).replace(/⟦([^⟧/]+)\/([^⟧]+)⟧/g, '<span class="fr"><span>$1</span><span>$2</span></span>');
}
const plain = s => String(s).replace(/⟦([^⟧/]+)\/([^⟧]+)⟧/g, "$1/$2").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();

/* ------------------------------------------------------------------ veri katmanı
 * Tüm kullanıcı verisi tek bir localStorage anahtarında tutulur. Yapı, ileride
 * bir sunucu API'sine (kullanıcı başına belge) birebir taşınabilecek biçimdedir. */
const KEY = "alesakademi.v1";
const DEFAULT = () => ({
  v: 1, theme: null, profile: null,
  att: {}, wrong: {}, fav: {}, mark: {}, lessons: {}, tasks: {}, exams: [], active: null, days: {}, xp: { logic: 0 }, plan: null
});
const Store = {
  d: null, ok: true,
  load() {
    try { const raw = localStorage.getItem(KEY); this.d = raw ? Object.assign(DEFAULT(), JSON.parse(raw)) : DEFAULT(); }
    catch (e) { this.d = DEFAULT(); this.ok = false; }
    return this.d;
  },
  save() { try { localStorage.setItem(KEY, JSON.stringify(this.d)); this.ok = true; } catch (e) { this.ok = false; } },
  reset() { this.d = DEFAULT(); this.save(); }
};
const S = () => Store.d;

/* Bir sorunun cevaplanmasını kaydeder; yanlışlar ve akıllı tekrar kutusu burada güncellenir. */
const BOX_DAYS = [1, 3, 7, 14];
function recordAnswer(qid, choice, ms, src = "banka") {
  const d = S(), q = QMAP[qid]; if (!q) return null;
  const ok = choice === q.a ? 1 : 0, now = Date.now();
  (d.att[qid] = d.att[qid] || []).push([now, choice, ok, Math.round(ms || 0), src]);
  const day = todayStr(); const dd = d.days[day] = d.days[day] || { q: 0, ok: 0, ms: 0 };
  dd.q++; dd.ok += ok; dd.ms += Math.min(ms || 0, 600000);
  const w = d.wrong[qid];
  if (!ok) d.wrong[qid] = { d: now, c: choice, box: 0, due: now + BOX_DAYS[0] * DAY, fixed: 0, n: (w ? w.n : 0) + 1 };
  else if (w && !w.fixed) { w.box++; w.last = now; if (w.box >= 3) { w.fixed = now; } else w.due = now + BOX_DAYS[w.box] * DAY; }
  return ok;
}

/* ------------------------------------------------------------------ istatistik */
function stats(filter = () => true) {
  const d = S(); let n = 0, ok = 0, ms = 0;
  const by = {}, lv = {}, ar = { say: { n: 0, ok: 0 }, soz: { n: 0, ok: 0 } };
  for (const [id, list] of Object.entries(d.att)) {
    const q = QMAP[id]; if (!q) continue;
    for (const a of list) {
      if (!filter(a, q)) continue;
      n++; ok += a[2]; ms += a[3];
      const t = by[q.topic] = by[q.topic] || { n: 0, ok: 0, ms: 0 }; t.n++; t.ok += a[2]; t.ms += a[3];
      const l = lv[q.level] = lv[q.level] || { n: 0, ok: 0 }; l.n++; l.ok += a[2];
      ar[q.area].n++; ar[q.area].ok += a[2];
    }
  }
  return { n, ok, bad: n - ok, ms, by, lv, ar };
}
function weakTopics(minN = 5) {
  const st = stats().by;
  return Object.entries(st).filter(([, v]) => v.n >= minN)
    .map(([k, v]) => ({ id: k, acc: v.ok / v.n, n: v.n, score: (v.ok + 1) / (v.n + 2) }))
    .sort((a, b) => a.score - b.score);
}
function streak() {
  const d = S().days; let s = 0, day = todayStr();
  if (!d[day]) day = addDays(day, -1);
  while (d[day] && d[day].q > 0) { s++; day = addDays(day, -1); }
  return s;
}
function lessonProgress(id) {
  const L = S().lessons[id] || {}; let p = 0;
  if (L.read) p += 40;
  const t = L.tests || {};
  ["kolay", "orta", "zor"].forEach(k => { if (t[k]) p += 12; });
  if (t.final && t.final.p >= 60) p += 24;
  return Math.min(100, p);
}
const dueWrongs = () => Object.entries(S().wrong).filter(([id, w]) => !w.fixed && w.due <= Date.now() && QMAP[id]).map(([id]) => id);

/* ------------------------------------------------------------------ ikonlar */
const ICON = {
  home: '<path d="M3 11l9-8 9 8"/><path d="M5 10v10h14V10"/>',
  book: '<path d="M4 4h10a4 4 0 014 4v12H8a4 4 0 01-4-4z"/><path d="M4 16a4 4 0 014-4h10"/>',
  calc: '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
  text: '<path d="M4 6h16M4 12h16M4 18h10"/>',
  bank: '<path d="M4 7h16v12H4z"/><path d="M8 7V4h8v3"/><path d="M9 12h6"/>',
  puzzle: '<path d="M10 3h4v3a2 2 0 104 0V3h3v7h-3a2 2 0 100 4h3v7h-7v-3a2 2 0 10-4 0v3H3v-7h3a2 2 0 100-4H3V3z"/>',
  exam: '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 2h6"/>',
  task: '<path d="M9 11l3 3 8-8"/><path d="M20 12v7a2 2 0 01-2 2H6a2 2 0 01-2-2V5a2 2 0 012-2h9"/>',
  x: '<circle cx="12" cy="12" r="9"/><path d="M9 9l6 6M15 9l-6 6"/>',
  star: '<path d="M12 3l2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9z"/>',
  cal: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
  chart: '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
  score: '<path d="M4 19h16M6 15l4-4 3 3 5-6"/>',
  guide: '<circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/>',
  link: '<path d="M10 14a5 5 0 007 0l3-3a5 5 0 00-7-7l-1 1"/><path d="M14 10a5 5 0 00-7 0l-3 3a5 5 0 007 7l1-1"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0116 0"/>',
  moon: '<path d="M21 13A9 9 0 1111 3a7 7 0 0010 10z"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
  flag: '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
  left: '<path d="M15 18l-6-6 6-6"/>', right: '<path d="M9 18l6-6-6-6"/>',
  play: '<path d="M7 5l12 7-12 7z"/>', check: '<path d="M5 12l5 5 9-10"/>', bulb: '<path d="M9 18h6M10 21h4M12 3a6 6 0 00-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0012 3z"/>',
  redo: '<path d="M20 11a8 8 0 10-2.3 5.7"/><path d="M20 4v7h-7"/>', plus: '<path d="M12 5v14M5 12h14"/>', trash: '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>'
};
const ic = (n, cls = "") => `<svg viewBox="0 0 24 24" class="${cls}" aria-hidden="true">${ICON[n] || ""}</svg>`;

/* ------------------------------------------------------------------ küçük bileşenler */
const lvlBars = l => `<span class="lvl" title="${LEVELS[l]}">${[1, 2, 3, 4, 5].map(i => `<i class="${i <= l ? "f" : ""}"></i>`).join("")}</span>`;
const areaChip = a => `<span class="chip ${a}">${AREA[a]}</span>`;
const progressBar = p => `<div class="progress" role="progressbar" aria-valuenow="${p}" aria-valuemin="0" aria-valuemax="100"><i style="width:${p}%"></i></div>`;
function toast(msg) {
  let t = $("#toast"); if (!t) { t = document.createElement("div"); t.id = "toast"; t.className = "toast"; t.setAttribute("role", "status"); document.body.appendChild(t); }
  t.textContent = msg; t.classList.add("on"); clearTimeout(t._h); t._h = setTimeout(() => t.classList.remove("on"), 2200);
}
function modal(html, onMount) {
  const bg = document.createElement("div"); bg.className = "modal-bg";
  bg.innerHTML = `<div class="modal" role="dialog" aria-modal="true">${html}</div>`;
  document.body.appendChild(bg);
  const close = () => bg.remove();
  bg.addEventListener("click", e => { if (e.target === bg || e.target.closest("[data-close]")) close(); });
  onMount && onMount(bg, close);
  const f = bg.querySelector("button,input"); f && f.focus();
  return close;
}
function confirmBox(title, body, okText, cb) {
  modal(`<h3>${title}</h3><p class="muted">${body}</p><div class="row" style="justify-content:flex-end;margin-top:14px"><button class="btn" data-close>Vazgeç</button><button class="btn primary" id="cfok">${okText}</button></div>`,
    (bg, close) => $("#cfok", bg).onclick = () => { close(); cb(); });
}

/* ------------------------------------------------------------------ soru gösterimi */
function questionHTML(q, o = {}) {
  const { sel = null, reveal = false, num = null, showSol = false, lock = false } = o;
  const L = LMAP[q.topic];
  const info = q.group ? `<div class="qinfo">${rich(q.group.info)}</div>` : "";
  const opts = q.opts.map((t, i) => {
    let c = "";
    if (reveal) { if (i === q.a) c = "ok"; else if (i === sel) c = "no"; }
    else if (i === sel) c = "sel";
    return `<button class="opt ${c}" data-opt="${i}" ${reveal || lock ? "disabled" : ""} aria-pressed="${i === sel}"><span class="k">${"ABCDE"[i]}</span><span class="ot">${rich(t)}</span></button>`;
  }).join("");
  const sol = showSol ? solutionHTML(q) : "";
  return `<div class="qmeta">${num ? `<b>Soru ${num}</b>` : ""}${areaChip(q.area)}<span class="chip">${esc(L ? L.title : q.topic)}</span><span class="chip">${esc(q.sub)}</span>${lvlBars(q.level)}<span class="chip orig" title="${esc(q.src)}">Özgün</span></div>
    ${info}<div class="qtext">${rich(q.q)}</div><div class="opts">${opts}</div>${sol}`;
}
function solutionHTML(q) {
  return `<div class="sol fade-in"><div class="row between"><b>Çözüm — Doğru cevap: ${"ABCDE"[q.a]}</b><span class="tiny muted">${esc(q.id)} · önerilen süre ${Math.round(q.sure)} sn</span></div>
    <ol>${q.sol.map(s => `<li>${rich(s)}</li>`).join("")}</ol>
    <div class="tiny muted"><b>Ölçülen kazanım:</b> ${esc(q.kaz)} · <b>Kaynak:</b> ${esc(q.src)}</div></div>`;
}

/* ------------------------------------------------------------------ grafikler (SVG, kütüphanesiz) */
const TIP = { el: null };
function tipInit() {
  TIP.el = document.createElement("div"); TIP.el.className = "tip"; TIP.el.setAttribute("role", "tooltip"); document.body.appendChild(TIP.el);
  document.addEventListener("pointerover", e => { const t = e.target.closest("[data-tip]"); if (!t) return; TIP.el.innerHTML = t.dataset.tip; TIP.el.classList.add("on"); });
  document.addEventListener("pointermove", e => { if (!TIP.el.classList.contains("on")) return; const x = Math.min(e.clientX + 14, innerWidth - TIP.el.offsetWidth - 8); TIP.el.style.left = x + "px"; TIP.el.style.top = (e.clientY + 14) + "px"; });
  document.addEventListener("pointerout", e => { if (e.target.closest("[data-tip]")) TIP.el.classList.remove("on"); });
}
function niceMax(v) { if (v <= 0) return 1; const p = Math.pow(10, Math.floor(Math.log10(v))); const n = v / p; return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * p; }
/* Tek seri sütun grafiği */
function barChart(data, { h = 180, unit = "", cls = "s1", max = null } = {}) {
  if (!data.length) return "";
  const W = 560, H = h, pl = 34, pr = 8, pt = 14, pb = 26;
  const mx = max || niceMax(Math.max(...data.map(d => d.v), 1));
  const bw = (W - pl - pr) / data.length;
  const y = v => H - pb - (H - pt - pb) * v / mx;
  const ticks = [0, mx / 2, mx];
  let s = `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Sütun grafiği"><g class="grid">${ticks.map(t => `<line x1="${pl}" x2="${W - pr}" y1="${y(t)}" y2="${y(t)}"/>`).join("")}</g>`;
  s += ticks.map(t => `<text x="${pl - 6}" y="${y(t) + 4}" text-anchor="end">${fmt1(t)}</text>`).join("");
  data.forEach((d, i) => {
    const x = pl + i * bw, w = Math.max(4, bw * .58), bx = x + (bw - w) / 2, top = y(d.v), hh = H - pb - top;
    const r = Math.min(4, w / 2, hh);
    if (d.v > 0) s += `<path class="${cls}" d="M${bx},${H - pb} V${top + r} q0,-${r} ${r},-${r} H${bx + w - r} q${r},0 ${r},${r} V${H - pb} Z"/>`;
    s += `<rect class="hit" x="${x}" y="${pt}" width="${bw}" height="${H - pt - pb}" data-tip="<b>${esc(d.label)}</b><br>${fmt1(d.v)}${unit}${d.tip ? "<br>" + d.tip : ""}"/>`;
    if (data.length <= 16 || i % 2 === 0) s += `<text x="${x + bw / 2}" y="${H - 8}" text-anchor="middle">${esc(d.short || d.label)}</text>`;
  });
  return s + "</svg>";
}
/* Çok serili çizgi grafiği (tek eksen) */
function lineChart(series, labels, { h = 200, unit = "", min = null, max = null } = {}) {
  const pts = series.flatMap(s => s.vals.filter(v => v != null));
  if (!pts.length) return "";
  const W = 560, H = h, pl = 36, pr = 64, pt = 14, pb = 26;
  let lo = min != null ? min : Math.min(0, ...pts), hi = max != null ? max : niceMax(Math.max(...pts, 1));
  const n = labels.length, xs = i => pl + (n === 1 ? (W - pl - pr) / 2 : i * (W - pl - pr) / (n - 1));
  const y = v => H - pb - (H - pt - pb) * (v - lo) / (hi - lo || 1);
  const ticks = [lo, (lo + hi) / 2, hi];
  let s = `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="Çizgi grafiği"><g class="grid">${ticks.map(t => `<line x1="${pl}" x2="${W - pr}" y1="${y(t)}" y2="${y(t)}"/>`).join("")}</g>`;
  s += ticks.map(t => `<text x="${pl - 6}" y="${y(t) + 4}" text-anchor="end">${fmt1(t)}</text>`).join("");
  labels.forEach((l, i) => { if (n <= 10 || i % Math.ceil(n / 8) === 0 || i === n - 1) s += `<text x="${xs(i)}" y="${H - 8}" text-anchor="middle">${esc(l)}</text>`; });
  series.forEach(se => {
    let d = "", started = false;
    se.vals.forEach((v, i) => { if (v == null) { started = false; return; } d += (started ? "L" : "M") + xs(i) + "," + y(v); started = true; });
    s += `<path class="line ${se.cls}" style="fill:none" d="${d}"/>`;
    se.vals.forEach((v, i) => { if (v != null) s += `<circle class="${se.cls}" cx="${xs(i)}" cy="${y(v)}" r="4" stroke="var(--surface)" stroke-width="2"/>`; });
    const li = se.vals.map((v, i) => v != null ? i : -1).filter(i => i >= 0).pop();
    if (li != null && series.length > 1) s += `<text class="dl" x="${xs(li) + 8}" y="${y(se.vals[li]) + 4}">${esc(se.name)}</text>`;
  });
  labels.forEach((l, i) => {
    const tip = `<b>${esc(l)}</b>` + series.map(se => se.vals[i] != null ? `<br>${esc(se.name)}: ${fmt1(se.vals[i])}${unit}` : "").join("");
    const x0 = i === 0 ? pl : (xs(i - 1) + xs(i)) / 2, x1 = i === n - 1 ? W - pr : (xs(i) + xs(i + 1)) / 2;
    s += `<rect class="hit" x="${x0}" y="${pt}" width="${Math.max(2, x1 - x0)}" height="${H - pt - pb}" data-tip="${tip.replace(/"/g, "&quot;")}"/>`;
  });
  return s + "</svg>";
}
const legend = items => `<div class="legend">${items.map(([n, c]) => `<span><i style="background:var(--${c});border-color:transparent"></i>${esc(n)}</span>`).join("")}</div>`;
function seqColor(acc) { const i = Math.min(5, Math.max(0, Math.floor(acc * 6))); return [`var(--seq-1)`, `var(--seq-2)`, `var(--seq-3)`, `var(--seq-4)`, `var(--seq-5)`, `var(--seq-6)`][i]; }
