/* ALES Akademi — kişiselleştirilmiş çalışma programı ve günlük görevler. */
"use strict";

const PHASES = [
  { key: 1, name: "Temel Oluşturma", goal: "Temel konuları öğrenmek ve düzenli soru çözme alışkanlığı kazanmak.",
    say: ["temel", "bolunebilme", "rasyonel", "esitsizlik", "uslu", "cebir", "oran"], soz: ["sozcuk", "cumle", "paragraf", "yapi"] },
  { key: 2, name: "Gelişim", goal: "Orta ve zor seviyedeki soruları çözebilmek.",
    say: ["problem", "islem", "sayma", "veri", "saymantik", "geometri"], soz: ["paragraf", "yapi", "sozmantik"] },
  { key: 3, name: "Sınav Simülasyonu", goal: "Deneme, süre yönetimi ve zayıf konu tekrarıyla sınav performansını geliştirmek.", say: [], soz: [] }
];
/* Seviye ve süreye göre aşama oranları */
function phaseSplit(days, level) {
  const base = { baslangic: [.4, .35, .25], orta: [.33, .34, .33], ileri: [.25, .35, .4] }[level] || [.33, .34, .33];
  const r = days <= 30 ? base.map((x, i) => i === 2 ? Math.max(x, .3) : x) : base;
  const s = r.reduce((a, b) => a + b, 0);
  const p1 = Math.round(days * r[0] / s), p2 = Math.round(days * r[1] / s);
  return [p1, p2, days - p1 - p2];
}
/* Günlük dakikayı örnek 3 saatlik plana (60/45/35/20/20) oranlayarak böler; hedef puan türüne göre sayısal–sözel payı kaydırır. */
function minuteSplit(total, type) {
  const r = { say: 60, soz: 45, mantik: 35, yanlis: 20, tekrar: 20 };
  const shift = type === "SAY" ? 10 : type === "SOZ" ? -10 : 0;
  r.say += shift; r.soz -= shift;
  const sum = Object.values(r).reduce((a, b) => a + b, 0), out = {};
  for (const k in r) out[k] = Math.max(5, Math.round(total * r[k] / sum / 5) * 5);
  return out;
}
function buildPlan(p) {
  const [a, b, c] = phaseSplit(p.days, p.level), days = [];
  const sp = minuteSplit(p.dailyMin, p.targetType);
  const spread = (list, n) => Array.from({ length: n }, (_, i) => list[Math.min(list.length - 1, Math.floor(i * list.length / n))]);
  const s1 = spread(PHASES[0].say, a), z1 = spread(PHASES[0].soz, a), s2 = spread(PHASES[1].say, b), z2 = spread(PHASES[1].soz, b);
  const perWeek = p.days <= 30 ? 2 : p.days >= 120 ? 2 : 3;
  for (let i = 0; i < p.days; i++) {
    const date = addDays(p.start, i), ph = i < a ? 1 : i < a + b ? 2 : 3, tasks = [];
    const rest = (i + 1) % 7 === 0 && ph !== 3;
    if (rest) {
      tasks.push({ t: "Haftalık genel tekrar: bu haftanın konularının kısa tekrar notları", min: Math.round(p.dailyMin * .4), cat: "tekrar", go: "#/akademi" });
      tasks.push({ t: "Yanlışlarım: bugün tekrar edilecek soruları çöz", min: Math.round(p.dailyMin * .35), cat: "yanlis", go: "#/yanlislar" });
      tasks.push({ t: "Mini deneme (20 + 20 soru, 60 dk)", min: 60, cat: "deneme", go: "#/deneme" });
    } else if (ph < 3) {
      const st = ph === 1 ? s1[i] : s2[i - a], zt = ph === 1 ? z1[i] : z2[i - a];
      tasks.push({ t: `Sayısal: ${LMAP[st].title} — konu çalışması ve 15–20 soru`, min: sp.say, cat: "say", go: `#/konu/${st}` });
      tasks.push({ t: `Sözel: ${LMAP[zt].title} — konu çalışması ve 15 soru`, min: sp.soz, cat: "soz", go: `#/konu/${zt}` });
      tasks.push({ t: ph === 1 ? "Mantık ve problem: sayı örüntüleri + 5 problem sorusu" : "Mantık Atölyesi: tablo kurma bulmacası + zamanlı mantık testi", min: sp.mantik, cat: "mantik", go: "#/mantik" });
      tasks.push({ t: "Yanlış analizi: bugünkü yanlışların çözümlerini incele", min: sp.yanlis, cat: "yanlis", go: "#/yanlislar" });
      tasks.push({ t: "Tekrar: önceki günlerin kısa tekrar notları", min: sp.tekrar, cat: "tekrar", go: "#/akademi" });
    } else {
      const k = i - a - b, slot = perWeek === 3 ? [0, 2, 4] : [1, 4];
      if (slot.includes(k % 7)) {
        tasks.push({ t: "Tam deneme sınavı (50 + 50 soru, 150 dk)", min: 150, cat: "deneme", go: "#/deneme" });
        tasks.push({ t: "Deneme sonrası yanlış ve boş analizi", min: Math.max(20, p.dailyMin - 150), cat: "yanlis", go: "#/yanlislar" });
      } else {
        tasks.push({ t: "Zayıf konu tekrarı: Performans Analizi'nin önerdiği konu", min: Math.round(p.dailyMin * .4), cat: "tekrar", go: "#/performans" });
        tasks.push({ t: "Hız çalışması: karma 20 soru, soru başına önerilen süreye uy", min: Math.round(p.dailyMin * .3), cat: "say", go: "#/banka" });
        tasks.push({ t: "İleri seviye mantık: sözel mantık grupları", min: Math.round(p.dailyMin * .2), cat: "mantik", go: "#/mantik" });
        tasks.push({ t: "Yanlışlarım: akıllı tekrar", min: Math.round(p.dailyMin * .1), cat: "yanlis", go: "#/yanlislar" });
      }
    }
    days.push({ date, ph, rest, tasks });
  }
  return days;
}
function planDay(date) {
  const d = S(); if (!d.profile) return null;
  if (!d.plan || d.plan.sig !== planSig()) d.plan = { sig: planSig(), days: buildPlan(d.profile) };
  const i = dayDiff(d.profile.start, date);
  return i < 0 || i >= d.profile.days ? null : d.plan.days[i];
}
const planSig = () => { const p = S().profile; return [p.days, p.level, p.targetType, p.dailyMin, p.start].join("|"); };

/* Günün görevleri: program varsa ilk açılışta programdan oluşturulur. */
function tasksFor(date) {
  const d = S();
  if (!d.tasks[date]) {
    const pd = planDay(date);
    if (pd) { d.tasks[date] = pd.tasks.map(t => ({ id: uid(), ...t, done: false })); Store.save(); }
  }
  return d.tasks[date] || [];
}
function pendingPast(date = todayStr()) {
  const out = [];
  for (const [k, list] of Object.entries(S().tasks)) if (k < date) list.forEach(t => { if (!t.done && !t.moved) out.push([k, t]); });
  return out;
}
function carryOver(date = todayStr()) {
  const list = tasksFor(date); let n = 0;
  for (const [k, t] of pendingPast(date)) { t.moved = date; list.push({ ...t, id: uid(), from: k, moved: undefined, done: false }); n++; }
  S().tasks[date] = list; Store.save(); return n;
}
function moveTask(date, id, toDate) {
  const list = S().tasks[date], t = list.find(x => x.id === id); if (!t) return;
  S().tasks[date] = list.filter(x => x.id !== id);
  tasksFor(toDate); S().tasks[toDate].push({ ...t, id: uid(), from: date }); Store.save();
}

/* ------------------------------------------------------------------ görünümler */
function renderProgram() {
  const d = S(), root = $("#view"), p = d.profile;
  const form = (pp = {}) => `<div class="form">
    <label class="f">Adınız<input type="text" id="pf-name" value="${esc(pp.name || "")}" placeholder="İsteğe bağlı"></label>
    <label class="f">Başlangıç seviyesi<select id="pf-level">${[["baslangic", "Başlangıç"], ["orta", "Orta"], ["ileri", "İleri"]].map(([v, l]) => `<option value="${v}" ${pp.level === v ? "selected" : ""}>${l}</option>`).join("")}</select></label>
    <label class="f">Hedef puan türü<select id="pf-type">${[["SAY", "ALES Sayısal"], ["SOZ", "ALES Sözel"], ["EA", "ALES Eşit Ağırlık"]].map(([v, l]) => `<option value="${v}" ${pp.targetType === v ? "selected" : ""}>${l}</option>`).join("")}</select></label>
    <label class="f">Hedef puan (100 üzerinden)<input type="number" id="pf-score" min="55" max="100" value="${pp.targetScore || 75}"></label>
    <label class="f">Program süresi<select id="pf-days">${[30, 60, 90, 120].map(v => `<option value="${v}" ${(pp.days || 90) === v ? "selected" : ""}>${v} gün${v === 30 ? " (yoğun)" : ""}</option>`).join("")}</select></label>
    <label class="f">Günlük çalışma (dk)<input type="number" id="pf-min" min="30" max="480" step="15" value="${pp.dailyMin || 180}"></label>
    <label class="f">Başlangıç tarihi<input type="date" id="pf-start" value="${pp.start || todayStr()}"></label></div>`;
  if (!p) {
    root.innerHTML = `<div class="page-head"><div><h1>Çalışma Programım</h1><p>Seviyenize, hedefinize ve günlük sürenize göre 30, 60, 90 ya da 120 günlük program oluşturun.</p></div></div>
      <div class="card">${form()}<div class="row" style="margin-top:16px"><button class="btn primary" id="pf-save">${ic("cal")}Programımı oluştur</button></div></div>`;
    $("#pf-save").onclick = saveProfile; return;
  }
  const plan = (planDay(todayStr()), d.plan.days), today = todayStr(), idx = dayDiff(p.start, today);
  const [a, b, c] = phaseSplit(p.days, p.level);
  const ph = idx < 0 ? 0 : idx < a ? 1 : idx < a + b ? 2 : idx < p.days ? 3 : 4;
  const weeks = [];
  for (let i = 0; i < plan.length; i += 7) weeks.push(plan.slice(i, i + 7));
  const wsel = window._wk ?? Math.max(0, Math.min(weeks.length - 1, Math.floor(Math.max(0, idx) / 7)));
  const sp = minuteSplit(p.dailyMin, p.targetType);
  root.innerHTML = `<div class="page-head"><div><h1>Çalışma Programım</h1><p>${p.days} günlük program · ${trDate(p.start)} – ${trDate(addDays(p.start, p.days - 1))} · günde ${p.dailyMin} dk</p></div>
    <div class="row"><button class="btn" id="pf-edit">Programı düzenle</button><a class="btn primary" href="#/gorevler">Bugünün görevleri</a></div></div>
  <div class="stack"><div class="grid g3">${PHASES.map((P, i) => { const n = [a, b, c][i], st = [0, a, a + b][i]; return `<div class="card ${ph === P.key ? "" : "flat"}" style="${ph === P.key ? "border-color:var(--accent)" : ""}">
    <div class="row between"><b>${P.key}. Aşama: ${P.name}</b><span class="chip ${ph === P.key ? "orig" : ""}">${st + 1}–${st + n}. gün</span></div>
    <p class="small muted" style="margin:6px 0">${P.goal}</p>${P.key < 3 ? `<div class="small"><b>Sayısal:</b> ${P.say.map(t => LMAP[t].title).join(", ")}<br><b>Sözel:</b> ${P.soz.map(t => LMAP[t].title).join(", ")}</div>` : `<div class="small">Haftada ${p.days <= 30 || p.days >= 120 ? 2 : 3} tam deneme · karma soru · zayıf konu tekrarı · süre ve hız çalışması · yanlış analizi</div>`}</div>`; }).join("")}</div>
  <div class="card"><div class="row between"><h3 style="margin:0">Günlük dakika dağılımı</h3><span class="small muted">Örnek 3 saatlik plan oranlarıyla (60/45/35/20/20), hedef türüne göre ayarlandı</span></div>
    <div class="grid g4" style="margin-top:10px;grid-template-columns:repeat(5,minmax(0,1fr))">${[["Sayısal", sp.say], ["Sözel", sp.soz], ["Mantık / problem", sp.mantik], ["Yanlış analizi", sp.yanlis], ["Tekrar", sp.tekrar]].map(([l, v]) => `<div class="stat"><span class="l">${l}</span><span class="v">${v}</span><span class="s">dakika</span></div>`).join("")}</div></div>
  <div class="card"><div class="row between"><h3 style="margin:0">Hafta ${wsel + 1} / ${weeks.length}</h3><div class="row"><button class="btn sm" id="wprev" ${wsel === 0 ? "disabled" : ""}>${ic("left")}</button><button class="btn sm" id="wnow">Bu hafta</button><button class="btn sm" id="wnext" ${wsel === weeks.length - 1 ? "disabled" : ""}>${ic("right")}</button></div></div>
    <div class="week" style="margin-top:12px">${weeks[wsel].map(dd => `<div class="day ${dd.date === today ? "today" : dd.date < today ? "past" : ""}" data-day="${dd.date}" tabindex="0"><b>${trDate(dd.date, { day: "numeric", month: "short" })}</b><span class="ph">${dd.rest ? "Tekrar günü" : dd.ph + ". aşama"}</span><div style="margin-top:4px">${dd.tasks.slice(0, 2).map(t => esc(t.t.split(":")[0])).join("<br>")}</div></div>`).join("")}</div>
    <div id="daydetail" style="margin-top:14px"></div></div></div>`;
  const showDay = date => { const dd = plan.find(x => x.date === date); $("#daydetail").innerHTML = `<div class="card flat"><b>${trDate(date, { weekday: "long", day: "numeric", month: "long" })}</b><ul class="clean small" style="margin-top:8px">${dd.tasks.map(t => `<li>${esc(t.t)} <span class="muted">· ${t.min} dk</span></li>`).join("")}</ul></div>`; };
  $$("[data-day]").forEach(el => el.onclick = () => showDay(el.dataset.day));
  $("#wprev").onclick = () => { window._wk = wsel - 1; renderProgram(); };
  $("#wnext").onclick = () => { window._wk = wsel + 1; renderProgram(); };
  $("#wnow").onclick = () => { window._wk = undefined; renderProgram(); };
  $("#pf-edit").onclick = () => modal(`<h3>Programı düzenle</h3>${form(p)}<p class="tiny muted" style="margin-top:10px">Değişiklik, henüz oluşturulmamış günlerin görevlerini etkiler; tamamlanmış görevler korunur.</p><div class="row" style="justify-content:flex-end;margin-top:12px"><button class="btn" data-close>Vazgeç</button><button class="btn primary" id="pf-save">Kaydet</button></div>`,
    (bg, close) => { $("#pf-save", bg).onclick = () => { saveProfile(); close(); }; });
}
function saveProfile() {
  const d = S(), prev = d.profile || {};
  d.profile = { ...prev, name: $("#pf-name").value.trim(), level: $("#pf-level").value, targetType: $("#pf-type").value,
    targetScore: Math.min(100, Math.max(0, +$("#pf-score").value || 75)), days: +$("#pf-days").value,
    dailyMin: Math.min(480, Math.max(30, +$("#pf-min").value || 180)), start: $("#pf-start").value || todayStr(), created: prev.created || Date.now() };
  d.plan = null;
  for (const k of Object.keys(d.tasks)) if (k >= todayStr() && d.tasks[k].every(t => !t.done && !t.custom)) delete d.tasks[k];
  Store.save(); toast("Program kaydedildi."); route();
}

function renderTasks() {
  const root = $("#view"), d = S(), date = window._td || todayStr(), list = tasksFor(date), past = pendingPast(todayStr());
  const doneMin = list.filter(t => t.done).reduce((s, t) => s + (+t.min || 0), 0), allMin = list.reduce((s, t) => s + (+t.min || 0), 0);
  const tgt = d.profile ? d.profile.dailyMin : allMin;
  const cat = { say: "say", soz: "soz", mantik: "orig", yanlis: "bad", tekrar: "", deneme: "warn" };
  root.innerHTML = `<div class="page-head"><div><h1>Günlük Görevler</h1><p>${trDate(date, { weekday: "long", day: "numeric", month: "long", year: "numeric" })}</p></div>
    <div class="row"><button class="btn sm" id="tprev">${ic("left")}</button><button class="btn sm" id="ttoday">Bugün</button><button class="btn sm" id="tnext">${ic("right")}</button></div></div>
  <div class="stack">${!d.profile ? `<div class="note">Henüz bir çalışma programınız yok. <a href="#/program">Program oluşturun</a>; görevleriniz her gün otomatik hazırlansın. Aşağıdan kendi görevlerinizi de ekleyebilirsiniz.</div>` : ""}
  ${past.length && date === todayStr() ? `<div class="note warn row between"><span><b>${past.length}</b> görev önceki günlerden tamamlanmadan kaldı.</span><button class="btn sm" id="tcarry">Bugüne aktar</button></div>` : ""}
  <div class="card"><div class="row between"><b>Günlük hedef</b><span class="small muted">${doneMin} / ${tgt} dk · ${list.filter(t => t.done).length}/${list.length} görev</span></div>${progressBar(pct(doneMin, tgt))}</div>
  <div class="stack" style="gap:10px">${list.length ? list.map(t => `<div class="task ${t.done ? "done" : ""}"><input type="checkbox" data-tk="${t.id}" ${t.done ? "checked" : ""} aria-label="Tamamlandı"><div style="flex:1;min-width:0"><div class="tt">${esc(t.t)}</div>
    <div class="row small muted" style="gap:6px;margin-top:4px"><span class="chip ${cat[t.cat] || ""}">${t.min} dk</span>${t.from ? `<span class="chip warn">${trDate(t.from, { day: "numeric", month: "short" })} tarihinden devreden</span>` : ""}${t.go ? `<a href="${t.go}">Göreve git →</a>` : ""}</div></div>
    <div class="row" style="gap:4px"><button class="btn sm ghost" data-mv="${t.id}" title="Yarına aktar">Yarına</button><button class="btn sm ghost icon" data-del="${t.id}" aria-label="Sil">${ic("trash")}</button></div></div>`).join("") : '<div class="empty card"><b>Bu gün için görev yok</b>Aşağıdan görev ekleyebilirsiniz.</div>'}</div>
  <div class="card"><b>Görev ekle</b><div class="row" style="margin-top:10px"><input type="text" id="tnew" placeholder="Örn. 20 paragraf sorusu çöz" style="flex:1;min-width:180px"><input type="number" id="tmin" value="30" min="5" step="5" style="width:90px" aria-label="Dakika"><button class="btn primary" id="tadd">${ic("plus")}Ekle</button></div></div></div>`;
  $$("[data-tk]").forEach(c => c.onchange = () => { const t = list.find(x => x.id === c.dataset.tk); t.done = c.checked; t.doneAt = c.checked ? Date.now() : null; Store.save(); renderTasks(); if (c.checked) toast("Görev tamamlandı ✔"); });
  $$("[data-mv]").forEach(b => b.onclick = () => { moveTask(date, b.dataset.mv, addDays(date, 1)); toast("Görev ertesi güne aktarıldı."); renderTasks(); });
  $$("[data-del]").forEach(b => b.onclick = () => { d.tasks[date] = list.filter(x => x.id !== b.dataset.del); Store.save(); renderTasks(); });
  $("#tadd").onclick = () => { const v = $("#tnew").value.trim(); if (!v) return; list.push({ id: uid(), t: v, min: +$("#tmin").value || 30, cat: "tekrar", done: false, custom: 1 }); d.tasks[date] = list; Store.save(); renderTasks(); };
  $("#tnew").onkeydown = e => { if (e.key === "Enter") $("#tadd").click(); };
  const c = $("#tcarry"); c && (c.onclick = () => { const n = carryOver(); toast(`${n} görev bugüne aktarıldı.`); renderTasks(); });
  $("#tprev").onclick = () => { window._td = addDays(date, -1); renderTasks(); };
  $("#tnext").onclick = () => { window._td = addDays(date, 1); renderTasks(); };
  $("#ttoday").onclick = () => { window._td = undefined; renderTasks(); };
}
