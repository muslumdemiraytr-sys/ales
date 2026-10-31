/* ALES Akademi — sayfalar ve yönlendirme. */
"use strict";

const NAV = [
  ["Çalışma", [["", "Ana Sayfa", "home"], ["akademi", "ALES Akademi", "book"], ["sayisal", "Sayısal Yetenek", "calc"], ["sozel", "Sözel Yetenek", "text"], ["banka", "Soru Bankası", "bank"], ["mantik", "Mantık Atölyesi", "puzzle"], ["deneme", "Deneme Merkezi", "exam"]]],
  ["Takip", [["gorevler", "Günlük Görevler", "task"], ["yanlislar", "Yanlışlarım", "x"], ["favoriler", "Favorilerim", "star"], ["program", "Çalışma Programım", "cal"], ["performans", "Performans Analizi", "chart"]]],
  ["Bilgi", [["puan", "ALES Puan Hesaplama", "score"], ["rehber", "Sınav Rehberi", "guide"], ["kaynak", "Kaynakça ve ÖSYM Arşivi", "link"], ["ayarlar", "Profil ve Ayarlar", "user"]]]
];
function renderNav() {
  const cur = (location.hash.replace(/^#\/?/, "").split(/[/?]/)[0]) || "";
  const alias = { konu: "akademi", coz: "banka", sinav: "deneme", sonuc: "deneme" }[cur] || cur;
  const badge = { yanlislar: Object.values(S().wrong).filter(w => !w.fixed).length, favoriler: Object.keys(S().fav).length, gorevler: tasksFor(todayStr()).filter(t => !t.done).length };
  $("#nav").innerHTML = NAV.map(([sec, items]) => `<div class="nav-sec">${sec}</div>` + items.map(([k, l, i]) => `<a href="#/${k}" class="${alias === k ? "on" : ""}" ${alias === k ? 'aria-current="page"' : ""}>${ic(i)}<span>${l}</span>${badge[k] ? `<span class="badge">${badge[k]}</span>` : ""}</a>`).join("")).join("");
}

/* ================================================================ ANA SAYFA */
function renderHome() {
  const d = S(), st = stats(), root = $("#view"), p = d.profile;
  const tasks = tasksFor(todayStr()), tDone = tasks.filter(t => t.done).length;
  const doneMin = tasks.filter(t => t.done).reduce((s, t) => s + (+t.min || 0), 0), goal = p ? p.dailyMin : 0;
  const lastEx = d.exams.filter(e => e.kind === "tam" || e.kind === "mini").slice(-5).reverse();
  const blank = d.exams.reduce((s, e) => s + e.secs.reduce((a, x) => a + x.b, 0), 0);
  const sayN = net(st.ar.say.ok, st.ar.say.n - st.ar.say.ok), sozN = net(st.ar.soz.ok, st.ar.soz.n - st.ar.soz.ok);
  const done = window.LESSONS.reduce((s, l) => s + lessonProgress(l.id), 0) / window.LESSONS.length;
  const weak = weakTopics().slice(0, 4);
  const days = [...Array(7)].map((_, i) => addDays(todayStr(), i - 6));
  const wk = barChart(days.map(x => ({ label: trDate(x, { weekday: "long", day: "numeric" }), short: trDate(x, { weekday: "short" }), v: (d.days[x] || {}).q || 0, tip: (d.days[x] || {}).q ? `%${pct(d.days[x].ok, d.days[x].q)} doğru` : "" })), { unit: " soru", h: 170 });
  const rec = recommend()[0];
  const due = dueWrongs().length;
  const hello = p && p.name ? `Merhaba ${esc(p.name)}` : "Merhaba";
  root.innerHTML = `<div class="stack fade-in">
  <div class="card hero"><div class="row between" style="align-items:flex-start"><div style="max-width:560px;position:relative;z-index:1"><p style="margin:0 0 4px">${hello} · ${trDate(todayStr(), { weekday: "long", day: "numeric", month: "long" })}</p>
    <h1>${p ? `Programınızın ${Math.min(p.days, Math.max(1, dayDiff(p.start, todayStr()) + 1))}. günü` : "ALES'e sistemli hazırlanın"}</h1>
    <p>ÖĞREN → UYGULA → TEST ET → ANALİZ ET → TEKRAR ET → GELİŞ. ${p ? "Bugünkü görevleriniz hazır." : "Seviyenize ve hedefinize göre bir çalışma programı oluşturarak başlayın."}</p>
    <div class="row">${p ? `<a class="btn primary" href="#/gorevler">${ic("task")}Bugünün görevleri</a>` : `<a class="btn primary" href="#/program">${ic("cal")}Program oluştur</a>`}<a class="btn" href="#/deneme">${ic("exam")}Deneme çöz</a>${due ? `<a class="btn" href="#/yanlislar">${due} tekrar bekliyor</a>` : ""}</div></div>
    <div class="card" style="background:rgba(255,255,255,.12);border:0;box-shadow:none;min-width:220px;position:relative;z-index:1"><div class="stat"><span class="l" style="color:#fff;opacity:.8">Günlük hedef</span><span class="v" style="color:#fff">${doneMin}/${goal || "—"} dk</span><span class="s" style="color:#fff;opacity:.85">${tDone}/${tasks.length} görev tamamlandı</span></div><div class="progress" style="background:rgba(255,255,255,.25);margin-top:8px"><i style="width:${pct(doneMin, goal || 1)}%;background:#fff"></i></div>
    <div class="stat" style="margin-top:12px"><span class="l" style="color:#fff;opacity:.8">Çalışma serisi</span><span class="v" style="color:#fff">${streak()} gün</span></div></div></div></div>
  <div class="grid g4">
    <div class="card"><div class="stat"><span class="l">Çözülen soru</span><span class="v">${st.n}</span><span class="s">${st.ok} doğru · ${st.bad} yanlış · ${blank} boş*</span></div></div>
    <div class="card"><div class="stat"><span class="l">Genel başarı</span><span class="v">%${pct(st.ok, st.n)}</span><span class="s">ortalama ${st.n ? Math.round(st.ms / st.n / 1000) : 0} sn/soru</span></div></div>
    <div class="card"><div class="stat"><span class="l">Sayısal / Sözel net</span><span class="v">${fmt1(sayN)} / ${fmt1(sozN)}</span><span class="s">tüm çözümlerde D − Y/4</span></div></div>
    <div class="card"><div class="stat"><span class="l">Konu tamamlama</span><span class="v">%${Math.round(done)}</span>${progressBar(Math.round(done))}</div></div></div>
  <div class="grid g2">
    <div class="card"><div class="row between"><h3 style="margin:0">Son 7 gün: çözülen soru</h3><a class="small" href="#/performans">Ayrıntılı analiz →</a></div>${st.n ? wk : '<div class="empty"><b>Henüz soru çözülmedi</b>İlk soru çözümünüzden sonra grafik burada görünecek.</div>'}</div>
    <div class="card"><h3>Önerilen sonraki çalışma</h3>${rec ? `<div class="note ${rec.cls || ""}">${rec.html}</div>` : ""}
      <h3 style="margin-top:16px">En zayıf konular</h3>${weak.length ? `<div class="list">${weak.map(w => `<div class="it"><div style="flex:1"><b>${esc(LMAP[w.id].title)}</b><div class="tiny muted">${w.n} soru · %${Math.round(w.acc * 100)} doğru</div></div><button class="btn sm" data-wk="${w.id}">20 soru çöz</button></div>`).join("")}</div>` : '<p class="small muted">Bir konuyu en az 5 soruyla denedikten sonra zayıf konularınız burada listelenir. Veri yokken sonuç üretilmez.</p>'}</div></div>
  <div class="grid g2">
    <div class="card"><div class="row between"><h3 style="margin:0">Son deneme sonuçları</h3><a class="small" href="#/deneme">Tümü →</a></div>${lastEx.length ? `<div class="tbl-wrap"><table class="t"><tr><th>Tarih</th><th>Tür</th><th class="n">Sayısal</th><th class="n">Sözel</th></tr>${lastEx.map(e => `<tr><td><a href="#/sonuc/${e.id}">${trDate(new Date(e.ts).toISOString().slice(0, 10), { day: "numeric", month: "short" })}</a></td><td>${e.kind === "tam" ? "Tam" : "Mini"}</td><td class="n">${fmt1(e.secs[0].net)}</td><td class="n">${fmt1(e.secs[1].net)}</td></tr>`).join("")}</table></div>` : '<p class="small muted">Henüz deneme çözmediniz.</p>'}</div>
    <div class="card"><h3>Hedef</h3>${p ? `<dl class="kv"><dt>Hedef puan</dt><dd>${p.targetScore} (ALES ${{ SAY: "Sayısal", SOZ: "Sözel", EA: "Eşit Ağırlık" }[p.targetType]})</dd><dt>Program</dt><dd>${p.days} gün · günde ${p.dailyMin} dk</dd><dt>Seviye</dt><dd>${{ baslangic: "Başlangıç", orta: "Orta", ileri: "İleri" }[p.level]}</dd></dl>
      <p class="tiny muted" style="margin-top:10px">Not: Netlerden kesin ALES puanı hesaplanamaz; ÖSYM puanı oturumun aday istatistiklerine bağlıdır.</p>` : '<p class="small muted">Hedef puanınızı <a href="#/program">Çalışma Programım</a> bölümünden belirleyin.</p>'}</div></div>
  <p class="tiny muted">* Boş sayısı yalnızca deneme ve testlerde boş bırakılan soruları kapsar.</p></div>`;
  $$("[data-wk]").forEach(b => b.onclick = () => startPractice(shuffle(QB.filter(q => q.topic === b.dataset.wk)).slice(0, 20).map(q => q.id), LMAP[b.dataset.wk].title + " — tekrar", "#/"));
}
function recommend() {
  const out = [], d = S(), w = weakTopics(), st = stats();
  if (!st.n) out.push({ html: `<b>Başlangıç:</b> <a href="#/konu/temel">Temel Kavramlar ve Sayılar</a> ve <a href="#/konu/paragraf">Paragrafta Anlam</a> konularından başlayın; ilk sonuçlarınızdan sonra öneriler verilerinize göre üretilecek.` });
  const due = dueWrongs().length;
  if (due) out.push({ html: `<b>${due} yanlış soru</b> akıllı tekrar takvimine göre bugün tekrar edilmeyi bekliyor. <a href="#/yanlislar">Tekrar et →</a>`, cls: "warn" });
  w.filter(x => x.acc < .5).slice(0, 2).forEach(x => {
    const L = LMAP[x.id];
    const extra = x.id === "problem" ? " Problem türlerini ayrı ayrı çalışın: yaş, işçi-havuz, hareket, yüzde ve karışım." : (x.id === "saymantik" || x.id === "sozmantik") ? ' <a href="#/mantik">Mantık Atölyesi</a>\'nde tablo kurma bulmacalarıyla ek çalışma yapın.' : "";
    out.push({ html: `<b>${L.title}</b> başarınız %${Math.round(x.acc * 100)} (${x.n} soru). Önce konu anlatımını ve sık yapılan hataları tekrar edin, ardından kolay testten başlayın.${extra} <a href="#/konu/${x.id}">Konuya git →</a>`, cls: "bad" });
  });
  w.filter(x => x.acc >= .75 && x.n >= 10).slice(-1).forEach(x => out.push({ html: `<b>${LMAP[x.id].title}</b> başarınız yüksek (%${Math.round(x.acc * 100)}). Mevcut seviyeyi korumak için haftada bir karma tekrar yeterli; zor seviye teste geçebilirsiniz.`, cls: "good" }));
  if (st.n && !d.exams.some(e => e.kind === "tam" || e.kind === "mini")) out.push({ html: `Henüz deneme çözmediniz. Süre yönetimini görmek için bir <a href="#/deneme">mini deneme</a> çözün.` });
  if (!out.length) out.push({ html: `Dengeli ilerliyorsunuz. Bugün bir <a href="#/deneme">tam deneme</a> ile süre yönetiminizi sınayın.` });
  return out;
}

/* ================================================================ AKADEMİ */
function renderAcademy(area) {
  const root = $("#view"), list = window.LESSONS.filter(l => !area || l.area === area);
  const title = area ? (area === "say" ? "Sayısal Yetenek" : "Sözel Yetenek") : "ALES Akademi";
  const groups = {};
  list.forEach(l => (groups[(area ? "" : AREA[l.area] + " · ") + l.group] = groups[(area ? "" : AREA[l.area] + " · ") + l.group] || []).push(l));
  const cnt = id => QB.filter(q => q.topic === id).length;
  root.innerHTML = `<div class="page-head"><div><h1>${title}</h1><p>${area === "say" ? "Sayısal Testi: sayısal ve mantıksal akıl yürütme (50 soru)." : area === "soz" ? "Sözel Testi: sözel akıl yürütme (50 soru)." : "Her konu 14 bölümlü yapıdadır: tanım, kavramlar, mantık, ayrıntılı anlatım, formüller, çözümlü örnekler, ALES tarzı uygulamalar, pratik yöntemler, sık hatalar, üç seviye test, konu sonu değerlendirmesi ve kısa tekrar notları."}</p></div>
    ${area ? "" : `<div class="row"><a class="btn" href="#/sayisal">Sayısal</a><a class="btn" href="#/sozel">Sözel</a></div>`}</div>
  <div class="stack">${Object.entries(groups).map(([g, ls]) => `<div><h3 class="muted small" style="text-transform:uppercase;letter-spacing:.06em">${esc(g)}</h3><div class="grid g3">${ls.map(l => { const p = lessonProgress(l.id); return `<a class="card topic-card" href="#/konu/${l.id}"><div class="row between">${areaChip(l.area)}<span class="tiny muted">${l.phase}. aşama</span></div><b>${esc(l.title)}</b><span class="small muted">${l.subs.length} alt başlık · ${cnt(l.id)} özgün soru</span>${progressBar(p)}<span class="tiny muted">%${p} tamamlandı</span></a>`; }).join("")}</div></div>`).join("")}</div>`;
}
function renderLesson(id) {
  const L = LMAP[id], root = $("#view"); if (!L) { root.innerHTML = '<div class="empty"><b>Konu bulunamadı</b></div>'; return; }
  const d = S(), rec = d.lessons[id] = d.lessons[id] || {}, tests = rec.tests || {};
  const qs = QB.filter(q => q.topic === id), apps = shuffle(qs.filter(q => q.level <= 3)).slice(0, 3);
  const testCard = (k, label, lv) => { const t = tests[k], n = qs.filter(q => lv.includes(q.level)).length; return `<div class="card flat"><div class="row between"><b>${label}</b>${t ? `<span class="chip ${t.p >= 60 ? "good" : "bad"}">%${t.p}</span>` : ""}</div><p class="tiny muted" style="margin:6px 0">${k === "final" ? "12 soru, tüm seviyeler" : `8 soru · ${lv.map(x => LEVELS[x]).join("/")}`}${n < 8 && k !== "final" ? " · yakın seviyeyle tamamlanır" : ""}</p><button class="btn sm ${t ? "" : "primary"}" data-test="${k}">${t ? "Yeniden çöz" : "Teste başla"}</button></div>`; };
  const secs = [["tanim", "Konunun tanımı"], ["kavram", "Temel kavramlar"], ["mantik", "Konunun mantığı"], ["anlatim", "Ayrıntılı anlatım"], ["formul", "Formüller ve önemli bilgiler"], ["ornek", "Çözümlü örnekler"], ["uygulama", "ALES tarzı uygulamalar"], ["pratik", "Pratik çözüm yöntemleri"], ["hata", "Sık yapılan hatalar"], ["test", "Kolay, orta ve zor seviye testler"], ["final", "Konu sonu değerlendirmesi"], ["not", "Kısa tekrar notları"]];
  const S_ = (k, n, body) => `<section class="card lesson-sec" id="ls-${k}"><h2><span class="num">${n}</span>${secs.find(s => s[0] === k)[1]}</h2>${body}</section>`;
  root.innerHTML = `<div class="page-head"><div><div class="crumb"><a href="#/${L.area === "say" ? "sayisal" : "sozel"}">← ${AREA[L.area]} Yetenek</a> · ${esc(L.group)}</div><h1>${esc(L.title)}</h1><p>${L.subs.map(esc).join(" · ")}</p></div>
    <div class="row"><button class="btn ${rec.read ? "on" : ""}" id="lread">${ic("check")}${rec.read ? "Okundu olarak işaretli" : "Konuyu okudum"}</button><button class="btn primary" id="lprac">${ic("play")}${qs.length} soruyla çalış</button></div></div>
  <div class="lesson-layout" style="display:grid;grid-template-columns:200px minmax(0,1fr);gap:18px"><nav class="lesson-nav card flat" style="padding:10px">${secs.map((s, i) => `<a href="#/konu/${id}" data-jump="ls-${s[0]}">${i + 1}. ${s[1]}</a>`).join("")}</nav>
  <div class="stack">
  ${S_("tanim", 1, `<p>${esc(L.tanim)}</p><h3>Kazanımlar</h3><ul class="clean">${L.kaz.map(k => `<li>${esc(k)}</li>`).join("")}</ul>`)}
  ${S_("kavram", 2, `<dl class="kv">${L.kavramlar.map(([a, b]) => `<dt>${esc(a)}</dt><dd style="font-weight:400">${esc(b)}</dd>`).join("")}</dl>`)}
  ${S_("mantik", 3, `<p>${esc(L.mantik)}</p>`)}
  ${S_("anlatim", 4, L.anlatim.map(a => `<h3>${esc(a.h)}</h3><p>${esc(a.p)}</p>`).join(""))}
  ${S_("formul", 5, `<div class="grid g2">${L.formuller.map(f => `<div class="formula">${esc(f)}</div>`).join("")}</div>`)}
  ${S_("ornek", 6, `<div class="stack">${L.ornekler.map((o, i) => `<div class="example"><b>Örnek ${i + 1}.</b> ${esc(o.q)}<details style="margin-top:8px"><summary class="small" style="cursor:pointer;color:var(--accent);font-weight:600">Çözümü göster</summary><ol class="small">${o.steps.map(s => `<li>${esc(s)}</li>`).join("")}</ol><b>Cevap: ${esc(o.a)}</b></details></div>`).join("")}</div>`)}
  ${S_("uygulama", 7, `<p class="small muted">Soru bankasından bu konuya ait özgün ALES tarzı sorular. Seçeneğe tıklayın; cevap ve çözüm hemen görünür (bu sorular istatistiğinize kaydedilir).</p><div class="stack" id="apps">${apps.map(q => `<div class="card flat" data-app="${q.id}">${questionHTML(q)}</div>`).join("")}</div>`)}
  ${S_("pratik", 8, `<ul class="clean">${L.pratik.map(x => `<li>${esc(x)}</li>`).join("")}</ul>`)}
  ${S_("hata", 9, `<ul class="clean">${L.hatalar.map(x => `<li>${esc(x)}</li>`).join("")}</ul>`)}
  ${S_("test", 10, `<div class="grid g3">${testCard("kolay", "Kolay seviye test", [1, 2])}${testCard("orta", "Orta seviye test", [3])}${testCard("zor", "Zor seviye test", [4, 5])}</div><p class="tiny muted" style="margin-top:8px">Testler süreli ve çözümler test bitince gösterilir.</p>`)}
  ${S_("final", 11, `${testCard("final", "Konu sonu değerlendirmesi", [1, 2, 3, 4, 5])}<p class="small muted" style="margin-top:8px">%60 ve üzeri başarı konuyu 'tamamlandı' sayar.</p>`)}
  ${S_("not", 12, `<ul class="clean">${L.notlar.map(x => `<li><b>${esc(x)}</b></li>`).join("")}</ul>`)}
  </div></div>`;
  $("#lread").onclick = () => { rec.read = rec.read ? 0 : Date.now(); Store.save(); renderLesson(id); };
  $("#lprac").onclick = () => startPractice(shuffle(qs).map(q => q.id), L.title, `#/konu/${id}`);
  $$("[data-test]").forEach(b => b.onclick = () => startTopicTest(id, b.dataset.test));
  $$("[data-jump]").forEach(a => a.onclick = e => { e.preventDefault(); document.getElementById(a.dataset.jump).scrollIntoView({ behavior: "smooth" }); });
  $$("[data-app]").forEach(card => {
    const q = QMAP[card.dataset.app], t0 = Date.now();
    $$(".opt", card).forEach(b => b.onclick = () => { const c = +b.dataset.opt; recordAnswer(q.id, c, Date.now() - t0, "konu"); Store.save(); card.innerHTML = questionHTML(q, { sel: c, reveal: true, showSol: true }); });
  });
}

/* ================================================================ SORU BANKASI */
function renderBank() {
  const root = $("#view"), d = S(), f = window._bf = window._bf || { area: "", topic: "", sub: "", level: "", state: "", n: 20 };
  let list = QB.filter(q => (!f.area || q.area === f.area) && (!f.topic || q.topic === f.topic) && (!f.sub || q.sub === f.sub) && (!f.level || q.level === +f.level));
  const st = id => { const a = d.att[id]; return !a ? "yeni" : a[a.length - 1][2] ? "dogru" : "yanlis"; };
  if (f.state === "yeni") list = list.filter(q => !d.att[q.id]);
  if (f.state === "yanlis") list = list.filter(q => d.wrong[q.id] && !d.wrong[q.id].fixed);
  if (f.state === "isaretli") list = list.filter(q => d.mark[q.id]);
  if (f.state === "favori") list = list.filter(q => d.fav[q.id]);
  const topics = window.LESSONS.filter(l => !f.area || l.area === f.area);
  const subs = [...new Set(QB.filter(q => (!f.topic || q.topic === f.topic) && (!f.area || q.area === f.area)).map(q => q.sub))].sort((a, b) => a.localeCompare(b, "tr"));
  const page = window._bp || 0, per = 25, shown = list.slice(page * per, page * per + per);
  const cntL = [1, 2, 3, 4, 5].map(l => QB.filter(q => q.level === l).length);
  root.innerHTML = `<div class="page-head"><div><h1>Soru Bankası</h1><p>${QB.length} özgün soru · tamamı ALES Akademi tarafından hazırlanmıştır, ÖSYM sorusu içermez. Seviye dağılımı: ${cntL.map((n, i) => `${LEVELS[i + 1]} ${n}`).join(" · ")}</p></div></div>
  <div class="card"><div class="form">
    <label class="f">Test alanı<select id="bf-area"><option value="">Tümü</option><option value="say" ${f.area === "say" ? "selected" : ""}>Sayısal</option><option value="soz" ${f.area === "soz" ? "selected" : ""}>Sözel</option></select></label>
    <label class="f">Konu<select id="bf-topic"><option value="">Tümü</option>${topics.map(l => `<option value="${l.id}" ${f.topic === l.id ? "selected" : ""}>${esc(l.title)}</option>`).join("")}</select></label>
    <label class="f">Alt konu / soru türü<select id="bf-sub"><option value="">Tümü</option>${subs.map(s => `<option ${f.sub === s ? "selected" : ""}>${esc(s)}</option>`).join("")}</select></label>
    <label class="f">Zorluk<select id="bf-level"><option value="">Tümü</option>${[1, 2, 3, 4, 5].map(l => `<option value="${l}" ${+f.level === l ? "selected" : ""}>${LEVELS[l]}</option>`).join("")}</select></label>
    <label class="f">Durum<select id="bf-state">${[["", "Tümü"], ["yeni", "Çözülmemiş"], ["yanlis", "Yanlışlarım"], ["isaretli", "Daha sonra tekrar"], ["favori", "Favoriler"]].map(([v, l]) => `<option value="${v}" ${f.state === v ? "selected" : ""}>${l}</option>`).join("")}</select></label>
    <label class="f">Soru sayısı<select id="bf-n">${[10, 20, 30, 50].map(n => `<option ${+f.n === n ? "selected" : ""}>${n}</option>`).join("")}<option value="0" ${+f.n === 0 ? "selected" : ""}>Tümü</option></select></label></div>
    <div class="row between" style="margin-top:14px"><span class="small muted"><b>${list.length}</b> soru eşleşti</span><div class="row"><button class="btn" id="bf-reset">Filtreleri temizle</button><button class="btn primary" id="bf-go" ${list.length ? "" : "disabled"}>${ic("play")}Çözmeye başla</button></div></div></div>
  <div class="card" style="margin-top:16px"><div class="tbl-wrap"><table class="t"><tr><th>ID</th><th>Soru</th><th>Konu</th><th>Zorluk</th><th>Durum</th></tr>${shown.map(q => `<tr><td class="tiny muted">${q.id}</td><td><a href="#/banka" data-one="${q.id}">${esc(plain(q.group ? "[Ortak bilgi] " + q.q : q.q).slice(0, 80))}…</a></td><td class="small">${esc(LMAP[q.topic].title)}<div class="tiny muted">${esc(q.sub)}</div></td><td>${lvlBars(q.level)}</td><td>${{ yeni: '<span class="chip">Yeni</span>', dogru: '<span class="chip good">Doğru</span>', yanlis: '<span class="chip bad">Yanlış</span>' }[st(q.id)]}${d.fav[q.id] ? " ★" : ""}</td></tr>`).join("")}</table></div>
    ${list.length > per ? `<div class="row between" style="margin-top:12px"><button class="btn sm" id="bp-prev" ${page ? "" : "disabled"}>${ic("left")}Önceki</button><span class="small muted">Sayfa ${page + 1}/${Math.ceil(list.length / per)}</span><button class="btn sm" id="bp-next" ${(page + 1) * per < list.length ? "" : "disabled"}>Sonraki${ic("right")}</button></div>` : ""}</div>`;
  const upd = (k, v) => { f[k] = v; if (k === "area") { f.topic = ""; f.sub = ""; } if (k === "topic") f.sub = ""; window._bp = 0; renderBank(); };
  ["area", "topic", "sub", "level", "state", "n"].forEach(k => $("#bf-" + k).onchange = e => upd(k, e.target.value));
  $("#bf-reset").onclick = () => { window._bf = null; window._bp = 0; renderBank(); };
  const order = l => { const g = {}; const out = []; shuffle(l).forEach(q => { if (q.group) { if (!g[q.group.id]) { g[q.group.id] = 1; out.push(...l.filter(x => x.group && x.group.id === q.group.id)); } } else out.push(q); }); return out; };
  $("#bf-go").onclick = () => { const o = order(list); startPractice((+f.n ? o.slice(0, +f.n) : o).map(q => q.id), "Soru Bankası", "#/banka"); };
  $$("[data-one]").forEach(a => a.onclick = e => { e.preventDefault(); startPractice([a.dataset.one, ...list.map(q => q.id).filter(x => x !== a.dataset.one)], "Soru Bankası", "#/banka"); });
  const pp = $("#bp-prev"), pn = $("#bp-next");
  pp && (pp.onclick = () => { window._bp = page - 1; renderBank(); }); pn && (pn.onclick = () => { window._bp = page + 1; renderBank(); });
}

/* ================================================================ DENEME MERKEZİ */
function renderExamCenter() {
  const d = S(), root = $("#view"), a = d.active;
  const ex = d.exams.slice().reverse();
  const unusedSoz = QB.filter(q => q.area === "soz" && !usedIds().has(q.id)).length;
  root.innerHTML = `<div class="page-head"><div><h1>Deneme Merkezi</h1><p>Biçim, ÖSYM 2026-ALES Başvuru Kılavuzu'na göre: 50 Sayısal + 50 Sözel soru, 150 dakika. Soru sırası, incelenen 2025–2026 örnek kitapçıklarındaki blok düzenini izler.</p></div></div>
  <div class="stack">${a ? `<div class="note warn row between"><span>Devam eden bir sınavınız var: <b>${esc(a.title)}</b> · kalan süre ${mmss(a.end - Date.now())}</span><div class="row"><a class="btn sm primary" href="#/sinav">Devam et</a><button class="btn sm" id="xabandon">Sınavı teslim et</button></div></div>` : ""}
  <div class="grid g2">
    <div class="card"><h3>${ic("exam")}Tam deneme</h3><p class="small muted">50 Sayısal (1–22 tekil, 23–43 ortak bilgi grupları, 44–50 geometri) + 50 Sözel (1–5 boşluk, 6–8 kesin çıkarım, 9–18 cümle ve paragraf yapısı, 19–42 paragraf, 43–50 sözel mantık). 150 dakika, geri sayım, soru haritası, işaretleme, süre bitince otomatik teslim.</p><button class="btn primary" data-start="tam" ${a ? "disabled" : ""}>Tam denemeyi başlat</button></div>
    <div class="card"><h3>${ic("exam")}Mini deneme</h3><p class="small muted">20 Sayısal + 20 Sözel, 60 dakika. Aynı blok mantığıyla kısa sınav simülasyonu.</p><button class="btn" data-start="mini" ${a ? "disabled" : ""}>Mini denemeyi başlat</button></div></div>
  <div class="note small">Denemeler önce daha önce görmediğiniz soruları kullanır. Şu an daha önce görülmemiş ${unusedSoz} sözel soru var; sözel havuz bittiğinde sorular tekrar kullanılır. Sınav sırasında çözümler gösterilmez.</div>
  <div class="card"><h3>Geçmiş denemeler ve testler</h3>${ex.length ? `<div class="tbl-wrap"><table class="t"><tr><th>Tarih</th><th>Sınav</th><th class="n">D</th><th class="n">Y</th><th class="n">B</th><th class="n">Net</th><th class="n">Süre</th></tr>${ex.map(e => { const t = e.secs.reduce((s, x) => ({ d: s.d + x.d, y: s.y + x.y, b: s.b + x.b }), { d: 0, y: 0, b: 0 }); return `<tr><td class="small">${new Date(e.ts).toLocaleDateString("tr-TR")}</td><td><a href="#/sonuc/${e.id}">${esc(e.title)}</a></td><td class="n">${t.d}</td><td class="n">${t.y}</td><td class="n">${t.b}</td><td class="n"><b>${fmt1(net(t.d, t.y))}</b></td><td class="n small">${mmss(e.used)}</td></tr>`; }).join("")}</table></div>` : '<div class="empty"><b>Henüz deneme yok</b>İlk denemenizi çözerek başlangıç seviyenizi görün.</div>'}</div></div>`;
  $$("[data-start]").forEach(b => b.onclick = () => confirmBox(b.dataset.start === "tam" ? "Tam deneme başlasın mı?" : "Mini deneme başlasın mı?", b.dataset.start === "tam" ? "150 dakikalık süre hemen başlar. Sayfayı yenileseniz de sınav kaldığı yerden sürer; süre ise işlemeye devam eder." : "60 dakikalık süre hemen başlar.", "Başlat", () => startDeneme(b.dataset.start)));
  const ab = $("#xabandon"); ab && (ab.onclick = () => confirmBox("Sınav teslim edilsin mi?", "Cevaplanan sorular değerlendirilir, boşlar boş sayılır.", "Teslim et", () => finishExam(false)));
}

/* ================================================================ YANLIŞLARIM / FAVORİLER */
function renderWrongs() {
  const d = S(), root = $("#view"), tab = window._wt || "aktif";
  const all = Object.entries(d.wrong).filter(([id]) => QMAP[id]);
  const active = all.filter(([, w]) => !w.fixed).sort((a, b) => a[1].due - b[1].due), fixed = all.filter(([, w]) => w.fixed);
  const due = dueWrongs();
  const tl = window._wtp || "";
  const list = (tab === "aktif" ? active : fixed).filter(([id]) => !tl || QMAP[id].topic === tl);
  const byT = {}; active.forEach(([id]) => { const t = QMAP[id].topic; byT[t] = (byT[t] || 0) + 1; });
  root.innerHTML = `<div class="page-head"><div><h1>Yanlışlarım ve Akıllı Tekrar</h1><p>Yanlış cevapladığınız her soru buraya düşer ve 1 → 3 → 7 → 14 gün aralıklarla tekrar karşınıza çıkar. Arka arkaya 3 kez doğru çözülen soru 'düzeltildi' sayılır.</p></div>
    <div class="row"><button class="btn primary" id="wdue" ${due.length ? "" : "disabled"}>${ic("redo")}Bugünün tekrarı (${due.length})</button><button class="btn" id="wall" ${active.length ? "" : "disabled"}>Tüm aktif yanlışları çöz</button></div></div>
  <div class="stack">${Object.keys(byT).length ? `<div class="card"><h3>Zorlandığınız konular</h3><div class="row">${Object.entries(byT).sort((a, b) => b[1] - a[1]).map(([t, n]) => `<button class="chip" data-wtp="${t}" style="cursor:pointer;${tl === t ? "outline:2px solid var(--accent)" : ""}">${esc(LMAP[t].title)}: ${n}</button>`).join("")}${tl ? '<button class="btn sm ghost" data-wtp="">Filtreyi kaldır</button>' : ""}</div></div>` : ""}
  <div class="tabs" id="wtabs"><button data-t="aktif" class="${tab === "aktif" ? "on" : ""}">Aktif (${active.length})</button><button data-t="duz" class="${tab === "duz" ? "on" : ""}">Düzeltilenler (${fixed.length})</button></div>
  ${list.length ? list.map(([id, w]) => { const q = QMAP[id]; return `<details class="card flat"><summary style="cursor:pointer"><div class="row between"><span><b>${esc(LMAP[q.topic].title)}</b> · <span class="small muted">${esc(q.sub)}</span></span><span class="row small muted">${w.fixed ? '<span class="chip good">Düzeltildi</span>' : w.due <= Date.now() ? '<span class="chip warn">Bugün tekrar</span>' : `<span class="chip">Tekrar: ${new Date(w.due).toLocaleDateString("tr-TR")}</span>`}<span>Yanlış: ${new Date(w.d).toLocaleDateString("tr-TR")}</span></span></div>
      <div class="small" style="margin-top:6px">${esc(plain(q.q).slice(0, 140))}…</div><div class="tiny muted">Verdiğiniz cevap: <b>${"ABCDE"[w.c]}</b> · Doğru cevap: <b>${"ABCDE"[q.a]}</b> · yanlış sayısı ${w.n || 1} · tekrar kutusu ${w.box}/3</div></summary>
      <div style="margin-top:12px">${questionHTML(q, { sel: w.c, reveal: true, showSol: true })}<div class="row" style="margin-top:12px"><button class="btn primary sm" data-redo="${id}">${ic("redo")}Tekrar çöz</button>${w.fixed ? "" : `<button class="btn sm ghost" data-fix="${id}">Öğrendim, listeden çıkar</button>`}</div></div></details>`; }).join("") : `<div class="empty card"><b>${tab === "aktif" ? "Aktif yanlış yok" : "Henüz düzeltilen soru yok"}</b>${tab === "aktif" ? "Soru çözdükçe yanlışlarınız burada toplanır." : ""}</div>`}</div>`;
  $$("#wtabs button").forEach(b => b.onclick = () => { window._wt = b.dataset.t; renderWrongs(); });
  $$("[data-wtp]").forEach(b => b.onclick = () => { window._wtp = b.dataset.wtp; renderWrongs(); });
  $("#wdue").onclick = () => startPractice(due, "Akıllı tekrar", "#/yanlislar");
  $("#wall").onclick = () => startPractice(active.map(x => x[0]), "Yanlışlarım", "#/yanlislar");
  $$("[data-redo]").forEach(b => b.onclick = () => startPractice([b.dataset.redo], "Yanlışlarım", "#/yanlislar"));
  $$("[data-fix]").forEach(b => b.onclick = () => { d.wrong[b.dataset.fix].fixed = Date.now(); Store.save(); renderWrongs(); });
}
function renderFavs() {
  const d = S(), root = $("#view");
  const favs = Object.entries(d.fav).filter(([id]) => QMAP[id]).sort((a, b) => b[1] - a[1]), marks = Object.keys(d.mark).filter(id => QMAP[id]);
  root.innerHTML = `<div class="page-head"><div><h1>Favorilerim</h1><p>Favorilere eklediğiniz ve 'daha sonra tekrar çöz' olarak işaretlediğiniz sorular.</p></div><div class="row"><button class="btn primary" id="fgo" ${favs.length ? "" : "disabled"}>Favorileri çöz</button><button class="btn" id="mgo" ${marks.length ? "" : "disabled"}>İşaretlileri çöz (${marks.length})</button></div></div>
  <div class="card">${favs.length ? `<div class="list">${favs.map(([id, t]) => { const q = QMAP[id]; return `<div class="it"><div style="flex:1;min-width:0"><b class="small">${esc(LMAP[q.topic].title)}</b> <span class="tiny muted">· ${esc(q.sub)} · ${new Date(t).toLocaleDateString("tr-TR")}</span><div class="small">${esc(plain(q.q).slice(0, 120))}…</div></div><button class="btn sm" data-one="${id}">Çöz</button><button class="btn sm ghost icon" data-unfav="${id}" aria-label="Favoriden çıkar">${ic("trash")}</button></div>`; }).join("")}</div>` : '<div class="empty"><b>Favori soru yok</b>Soru çözerken ★ Favorilere ekle düğmesini kullanın.</div>'}</div>`;
  $("#fgo").onclick = () => startPractice(favs.map(x => x[0]), "Favorilerim", "#/favoriler");
  $("#mgo").onclick = () => startPractice(marks, "Daha sonra tekrar", "#/favoriler");
  $$("[data-one]").forEach(b => b.onclick = () => startPractice([b.dataset.one], "Favorilerim", "#/favoriler"));
  $$("[data-unfav]").forEach(b => b.onclick = () => { delete d.fav[b.dataset.unfav]; Store.save(); renderFavs(); });
}

/* ================================================================ PERFORMANS */
function renderPerf() {
  const d = S(), root = $("#view"), st = stats();
  if (!st.n) { root.innerHTML = `<div class="page-head"><div><h1>Performans ve Gelişim Merkezi</h1></div></div><div class="card empty"><b>Henüz analiz edilecek veri yok</b>Soru çözdükçe, deneme ve testlere girdikçe grafikler ve öneriler burada oluşur. Veri olmadan sonuç üretilmez.<div style="margin-top:12px"><a class="btn primary" href="#/banka">Soru çözmeye başla</a></div></div>`; return; }
  const days = [...Array(14)].map((_, i) => addDays(todayStr(), i - 13));
  const daily = barChart(days.map(x => ({ label: trDate(x, { day: "numeric", month: "long" }), short: trDate(x, { day: "numeric" }), v: (d.days[x] || {}).q || 0, tip: (d.days[x] || {}).q ? `%${pct(d.days[x].ok, d.days[x].q)} doğru` : "" })), { unit: " soru" });
  // haftalık: son 8 hafta, alan bazında net ve başarı
  const wkStart = i => addDays(todayStr(), -7 * (7 - i) - 6), weeks = [...Array(8)].map((_, i) => [wkStart(i), addDays(wkStart(i), 6)]);
  const wlab = weeks.map(([a]) => trDate(a, { day: "numeric", month: "short" }));
  const wstat = (area, a, b) => stats((at, q) => q.area === area && todayStr(new Date(at[0])) >= a && todayStr(new Date(at[0])) <= b).ar[area];
  const wNet = area => weeks.map(([a, b]) => { const s = wstat(area, a, b); return s.n ? net(s.ok, s.n - s.ok) : null; });
  const wAcc = area => weeks.map(([a, b]) => { const s = wstat(area, a, b); return s.n ? pct(s.ok, s.n) : null; });
  const netChart = lineChart([{ name: "Sayısal", cls: "s1", vals: wNet("say") }, { name: "Sözel", cls: "s2", vals: wNet("soz") }], wlab, { unit: " net" });
  const sayAcc = lineChart([{ name: "Sayısal", cls: "s1", vals: wAcc("say") }], wlab, { unit: "%", min: 0, max: 100 });
  const sozAcc = lineChart([{ name: "Sözel", cls: "s2", vals: wAcc("soz") }], wlab, { unit: "%", min: 0, max: 100 });
  const heat = window.LESSONS.map(l => { const v = st.by[l.id]; return `<div class="cell" ${v ? `data-tip="<b>${esc(l.title)}</b><br>${v.ok}/${v.n} doğru"` : ""}><div class="row between"><span>${esc(l.title)}</span>${v ? `<i style="width:14px;height:14px;border-radius:4px;background:${seqColor(v.ok / v.n)};display:inline-block;flex:none" aria-hidden="true"></i>` : ""}</div><b>${v ? "%" + pct(v.ok, v.n) : "—"}</b><span class="tiny muted">${v ? v.n + " soru" : "veri yok"}</span></div>`; }).join("");
  const lv = barChart([1, 2, 3, 4, 5].map(l => ({ label: LEVELS[l], v: st.lv[l] ? pct(st.lv[l].ok, st.lv[l].n) : 0, tip: st.lv[l] ? `${st.lv[l].n} soru` : "veri yok" })), { unit: "%", max: 100, h: 170 });
  const tm = Object.entries(st.by).map(([k, v]) => ({ label: LMAP[k].title, short: LMAP[k].title.split(" ")[0], v: Math.round(v.ms / v.n / 1000) })).sort((a, b) => b.v - a.v).slice(0, 10);
  const ex = d.exams.filter(e => e.kind === "tam" || e.kind === "mini");
  const exChart = ex.length ? lineChart([{ name: "Sayısal", cls: "s1", vals: ex.map(e => e.secs[0].net) }, { name: "Sözel", cls: "s2", vals: ex.map(e => e.secs[1].net) }], ex.map((e, i) => `${i + 1}. ${e.kind === "tam" ? "tam" : "mini"}`), { unit: " net" }) : "";
  const sk = [...Array(28)].map((_, i) => addDays(todayStr(), i - 27));
  const recs = recommend();
  root.innerHTML = `<div class="page-head"><div><h1>Performans ve Gelişim Merkezi</h1><p>Tüm grafikler bu cihazdaki gerçek çalışma verilerinizden hesaplanır.</p></div></div>
  <div class="stack"><div class="grid g4">
    <div class="card"><div class="stat"><span class="l">Toplam çözüm</span><span class="v">${st.n}</span><span class="s">${Object.keys(d.att).length} farklı soru</span></div></div>
    <div class="card"><div class="stat"><span class="l">Sayısal başarı</span><span class="v">%${pct(st.ar.say.ok, st.ar.say.n)}</span><span class="s">${st.ar.say.n} çözüm</span></div></div>
    <div class="card"><div class="stat"><span class="l">Sözel başarı</span><span class="v">%${pct(st.ar.soz.ok, st.ar.soz.n)}</span><span class="s">${st.ar.soz.n} çözüm</span></div></div>
    <div class="card"><div class="stat"><span class="l">Ortalama süre</span><span class="v">${Math.round(st.ms / st.n / 1000)} sn</span><span class="s">soru başına</span></div></div></div>
  <div class="card"><h3>Çalışma önerileri</h3><div class="stack" style="gap:8px">${recs.map(r => `<div class="note ${r.cls || ""}">${r.html}</div>`).join("")}</div></div>
  <div class="grid g2"><div class="card"><h3>Günlük soru çözümü (son 14 gün)</h3>${daily}</div><div class="card"><h3>Haftalık net</h3>${legend([["Sayısal", "series-1"], ["Sözel", "series-2"]])}${netChart}</div></div>
  <div class="grid g2"><div class="card"><h3>Sayısal başarı (haftalık %)</h3>${sayAcc}</div><div class="card"><h3>Sözel başarı (haftalık %)</h3>${sozAcc}</div></div>
  <div class="card"><div class="row between"><h3 style="margin:0">Konu bazlı başarı haritası</h3><div class="legend"><span>Düşük</span>${[0, .2, .4, .6, .8, 1].map(x => `<i style="background:${seqColor(x)};border:0"></i>`).join("")}<span>Yüksek</span></div></div><div class="heat" style="margin-top:12px">${heat}</div></div>
  <div class="grid g2"><div class="card"><h3>Zorluk seviyesine göre başarı (%)</h3>${lv}</div><div class="card"><h3>Soru başına ortalama süre (sn)</h3>${barChart(tm, { unit: " sn", cls: "s1" })}</div></div>
  <div class="grid g2"><div class="card"><h3>Denemeler arası gelişim</h3>${ex.length ? legend([["Sayısal", "series-1"], ["Sözel", "series-2"]]) + exChart : '<p class="small muted">Deneme çözdükçe gelişim çizgisi oluşur.</p>'}</div>
    <div class="card"><h3>Çalışma devamlılığı (son 4 hafta)</h3><div class="streak" style="grid-template-columns:repeat(7,1fr)">${sk.map(x => { const v = (d.days[x] || {}).q || 0; return `<i data-tip="${trDate(x)}: ${v} soru" style="background:${v ? seqColor(Math.min(1, v / 40)) : "var(--surface-3)"}"></i>`; }).join("")}</div><p class="small muted" style="margin-top:10px">Güncel seri: <b>${streak()} gün</b> · aktif gün: ${Object.values(d.days).filter(x => x.q).length}</p></div></div>
  <details class="card"><summary style="cursor:pointer"><b>Tablo görünümü</b> (konu bazında ham veri)</summary><div class="tbl-wrap" style="margin-top:10px"><table class="t"><tr><th>Konu</th><th class="n">Çözüm</th><th class="n">Doğru</th><th class="n">Başarı</th><th class="n">Ort. süre</th></tr>${Object.entries(st.by).map(([k, v]) => `<tr><td>${esc(LMAP[k].title)}</td><td class="n">${v.n}</td><td class="n">${v.ok}</td><td class="n">%${pct(v.ok, v.n)}</td><td class="n">${Math.round(v.ms / v.n / 1000)} sn</td></tr>`).join("")}</table></div></details></div>`;
}

/* ================================================================ PUAN HESAPLAMA */
function renderScore() {
  const root = $("#view"), v = window._sc = window._sc || { sd: 30, sy: 8, zd: 32, zy: 8, adv: false, ms: "", ss: "", mz: "", sz: "", tx: { SAY: ["", "", ""], SOZ: ["", "", ""], EA: ["", "", ""] } };
  root.innerHTML = `<div class="page-head"><div><h1>ALES Puan Hesaplama</h1><p>Net hesabı ÖSYM kılavuzuna göre kesindir. Puan ise yalnızca sizin gireceğiniz oturum istatistikleriyle <b>tahmini</b> olarak hesaplanır.</p></div></div>
  <div class="stack"><div class="grid g2"><div class="card"><h3>${areaChip("say")} Sayısal Testi (50 soru)</h3><div class="form"><label class="f">Doğru<input type="number" id="sc-sd" min="0" max="50" value="${v.sd}"></label><label class="f">Yanlış<input type="number" id="sc-sy" min="0" max="50" value="${v.sy}"></label></div></div>
    <div class="card"><h3>${areaChip("soz")} Sözel Testi (50 soru)</h3><div class="form"><label class="f">Doğru<input type="number" id="sc-zd" min="0" max="50" value="${v.zd}"></label><label class="f">Yanlış<input type="number" id="sc-zy" min="0" max="50" value="${v.zy}"></label></div></div></div>
  <div id="sc-out"></div>
  <div class="card"><h3>ÖSYM'nin puan hesaplama yöntemi</h3><ol class="small" style="padding-left:1.2em;margin:0"><li>Her testte <b>ham puan = doğru − yanlış ÷ 4</b>.</li><li>Ham puanlar, o oturumdaki tüm adayların ortalaması ve standart sapması kullanılarak <b>ortalaması 50, standart sapması 10</b> olan standart puana (SP) dönüştürülür.</li>
    <li>Ağırlıklı puan (AP): Sayısal = 0,75·SP<sub>say</sub> + 0,25·SP<sub>söz</sub>; Sözel = 0,25·SP<sub>say</sub> + 0,75·SP<sub>söz</sub>; Eşit Ağırlık = 0,50·SP<sub>say</sub> + 0,50·SP<sub>söz</sub>.</li><li>ALES puanı = 70 + 30·[2(AP − X) − S] / [2(B − X) − S]; X: ağırlıklı puanların ortalaması, S: standart sapması, B: en büyük ağırlıklı puan.</li></ol>
    <p class="tiny muted" style="margin-top:8px">Kaynak: 2026-ALES Başvuru Kılavuzu, md. 3.9, ÖSYM. Ortalama, standart sapma, X, S ve B değerleri her oturumda değişir ve bu araştırmada resmî kaynakta yayımlanmış hâlleri bulunamamıştır; bu nedenle platform hiçbir katsayıyı varsayılan olarak doldurmaz.</p></div>
  <div class="card"><div class="row between"><h3 style="margin:0">Tahmini puan (senaryo)</h3><button class="btn sm" id="sc-adv">${v.adv ? "Gizle" : "Senaryo değerlerini gir"}</button></div>
  ${v.adv ? `<div class="note warn small" style="margin-top:12px">Bu alana gireceğiniz değerler sizin varsayımlarınızdır. Sonuç resmî ÖSYM puanı değildir.</div>
    <h4 style="margin-top:14px">1. Standart puan için ham puan istatistikleri</h4><div class="form"><label class="f">Sayısal ham ortalama<input type="number" step="0.01" id="sc-ms" value="${v.ms}"></label><label class="f">Sayısal ham std. sapma<input type="number" step="0.01" id="sc-ss" value="${v.ss}"></label><label class="f">Sözel ham ortalama<input type="number" step="0.01" id="sc-mz" value="${v.mz}"></label><label class="f">Sözel ham std. sapma<input type="number" step="0.01" id="sc-sz" value="${v.sz}"></label></div>
    <h4 style="margin-top:14px">2. 100'lük ölçeğe dönüşüm (her puan türü için X, S, B)</h4><div class="tbl-wrap"><table class="t"><tr><th>Puan türü</th><th>X (ortalama AP)</th><th>S (std. sapma)</th><th>B (en büyük AP)</th></tr>${["SAY", "SOZ", "EA"].map(t => `<tr><td>${{ SAY: "Sayısal", SOZ: "Sözel", EA: "Eşit Ağırlık" }[t]}</td>${[0, 1, 2].map(k => `<td><input type="number" step="0.01" data-tx="${t},${k}" value="${v.tx[t][k]}" style="min-width:90px"></td>`).join("")}</tr>`).join("")}</table></div>` : ""}</div></div>`;
  const calc = () => {
    const num = id => { const el = $("#" + id); return el ? Math.max(0, Math.min(50, Math.floor(+el.value || 0))) : 0; };
    v.sd = num("sc-sd"); v.sy = num("sc-sy"); v.zd = num("sc-zd"); v.zy = num("sc-zy");
    const err = (v.sd + v.sy > 50 ? "Sayısal Testi'nde doğru + yanlış 50'yi geçemez. " : "") + (v.zd + v.zy > 50 ? "Sözel Testi'nde doğru + yanlış 50'yi geçemez." : "");
    const ns = net(v.sd, v.sy), nz = net(v.zd, v.zy);
    let est = "";
    if (v.adv) {
      ["ms", "ss", "mz", "sz"].forEach(k => v[k] = $("#sc-" + k).value);
      $$("[data-tx]").forEach(el => { const [t, k] = el.dataset.tx.split(","); v.tx[t][+k] = el.value; });
      const f = x => x === "" ? null : +x;
      if ([v.ms, v.ss, v.mz, v.sz].every(x => x !== "") && +v.ss > 0 && +v.sz > 0) {
        const sps = 50 + 10 * (ns - v.ms) / v.ss, spz = 50 + 10 * (nz - v.mz) / v.sz;
        const ap = { SAY: .75 * sps + .25 * spz, SOZ: .25 * sps + .75 * spz, EA: .5 * sps + .5 * spz };
        est = `<div class="card"><h3>Tahmini sonuç <span class="chip warn">varsayıma dayalı</span></h3><div class="grid g4"><div class="stat"><span class="l">SP Sayısal</span><span class="v">${fmt1(sps)}</span></div><div class="stat"><span class="l">SP Sözel</span><span class="v">${fmt1(spz)}</span></div></div>
          <div class="tbl-wrap" style="margin-top:12px"><table class="t"><tr><th>Puan türü</th><th class="n">Ağırlıklı puan</th><th class="n">Tahmini ALES puanı</th></tr>${["SAY", "SOZ", "EA"].map(t => { const [X, Sd, Bm] = v.tx[t].map(f); const ok = X != null && Sd != null && Bm != null && (2 * (Bm - X) - Sd) !== 0; const sc = ok ? 70 + 30 * (2 * (ap[t] - X) - Sd) / (2 * (Bm - X) - Sd) : null; return `<tr><td>${{ SAY: "ALES Sayısal", SOZ: "ALES Sözel", EA: "ALES Eşit Ağırlık" }[t]}</td><td class="n">${fmt1(ap[t])}</td><td class="n">${ok ? `<b>${fmt1(Math.min(100, sc))}</b>` : '<span class="muted">X, S, B girin</span>'}</td></tr>`; }).join("")}</table></div></div>`;
      } else est = `<div class="note small">Tahmin için dört ham puan istatistiğini girin.</div>`;
    }
    $("#sc-out").innerHTML = `${err ? `<div class="note bad">${err}</div>` : ""}<div class="grid g3"><div class="card"><div class="stat"><span class="l">Sayısal net (kesin)</span><span class="v">${fmt1(ns)}</span><span class="s">${v.sd} − ${v.sy}/4 · boş ${Math.max(0, 50 - v.sd - v.sy)}</span></div></div>
      <div class="card"><div class="stat"><span class="l">Sözel net (kesin)</span><span class="v">${fmt1(nz)}</span><span class="s">${v.zd} − ${v.zy}/4 · boş ${Math.max(0, 50 - v.zd - v.zy)}</span></div></div>
      <div class="card"><div class="stat"><span class="l">ALES SAY / SÖZ / EA</span><span class="v" style="font-size:1.1rem">Kesin hesaplanamaz</span><span class="s">Oturum istatistikleri gerekir · aşağıdaki senaryo bölümünü kullanın</span></div></div></div>${est}`;
  };
  $$("input", root).forEach(i => i.oninput = calc);
  $("#sc-adv").onclick = () => { v.adv = !v.adv; renderScore(); };
  calc();
}

/* ================================================================ REHBER ve KAYNAKÇA */
function renderGuide() {
  const root = $("#view");
  const sec = (t, b) => `<details class="card" ${t.startsWith("ALES nedir") ? "open" : ""}><summary style="cursor:pointer"><h3 style="display:inline">${t}</h3></summary><div style="margin-top:10px">${b}</div></details>`;
  const src = '<p class="tiny muted">Kaynak: 2026-ALES Başvuru Kılavuzu, ÖSYM (dokuman.osym.gov.tr, 25.03.2026). Başvuru öncesinde güncel kılavuzu mutlaka kontrol edin.</p>';
  root.innerHTML = `<div class="page-head"><div><h1>Sınav Rehberi</h1><p>Resmî bilgiler ÖSYM kılavuzundan, strateji önerileri ise ALES Akademi'nin pedagojik önerileridir; ikisi ayrı belirtilmiştir.</p></div></div><div class="stack">
  ${sec("ALES nedir?", `<p>Akademik Personel ve Lisansüstü Eğitimi Giriş Sınavı (ALES); lisansüstü eğitime girişte, yurt dışına lisansüstü eğitim için gönderilecek adayların seçiminde ve teknik öğretmenler için mühendislik tamamlama programlarında ilgili kurumların kullanacağı puanları veren sınavdır (Kılavuz md. 1.1).</p>
    <dl class="kv"><dt>Testler</dt><dd>Sayısal (50 soru) ve Sözel (50 soru)</dd><dt>Süre</dt><dd>150 dakika, başlangıç 10.15</dd><dt>Ölçülen beceri</dt><dd>Sayısal ve mantıksal akıl yürütme; sözel akıl yürütme. Belirli bir lisans programının bilgisini ölçmez.</dd><dt>Yanlışların etkisi</dt><dd>4 yanlış 1 doğruyu götürür (ham puan = D − Y/4)</dd><dt>Geçerlilik</dt><dd>Sonuçların açıklandığı tarihten itibaren 5 yıl</dd><dt>2026 oturumları</dt><dd>ALES/1 10 Mayıs · ALES/2 2 Ağustos (kılavuzda 26 Temmuz olarak yer almış, ÖSYM duyurularına göre 2 Ağustos'ta yapılmıştır) · ALES/3 29 Kasım 2026</dd></dl>${src}`)}
  ${sec("Kimler ALES'e girebilir?", `<p>Bir lisans programından mezun olabilecek durumda bulunanlar, lisans programını bitirenler ve denklik belgesi almış olmak kaydıyla yurt dışında lisans eğitimi görmüş olanlar başvurabilir (md. 1.2).</p>${src}`)}
  ${sec("ALES puan türleri", `<div class="tbl-wrap"><table class="t"><tr><th>Puan türü</th><th class="n">Sayısal SP</th><th class="n">Sözel SP</th></tr><tr><td>ALES Sayısal</td><td class="n">0,75</td><td class="n">0,25</td></tr><tr><td>ALES Sözel</td><td class="n">0,25</td><td class="n">0,75</td></tr><tr><td>ALES Eşit Ağırlık</td><td class="n">0,50</td><td class="n">0,50</td></tr></table></div><p class="small" style="margin-top:8px">Ayrıntılı yöntem için <a href="#/puan">ALES Puan Hesaplama</a>.</p>${src}`)}
  ${sec("ALES puanı nerelerde kullanılır? Lisansüstü başvurularda ALES", `<ul class="clean"><li>Öğretim görevlisi ve araştırma görevlisi kadroları için alanındaki puan türünde 100 üzerinden en az <b>70</b> (md. 1.6).</li><li>Tezli yüksek lisans başvurularında programın puan türünde en az <b>55</b>; lisans diplomasıyla doktora başvurusunda en az <b>80</b>. Senatolar daha yüksek taban belirleyebilir ve ALES'in değerlendirmedeki ağırlığı %50'den az olamaz (md. 1.7).</li><li>Tezsiz yüksek lisans programlarında ALES şartı aranıp aranmayacağı senatoya bırakılmıştır.</li></ul>${src}`)}
  ${sec("ALES'e nasıl hazırlanılır?", `<p><span class="chip orig">ALES Akademi önerisi</span> Önce iki testin blok yapısını tanıyın; ardından temel konuları sağlamlaştırın (1. aşama), problem–mantık–paragraf derinliğini artırın (2. aşama) ve son dönemde haftada 2–3 tam deneme ile süre yönetimine odaklanın (3. aşama). <a href="#/program">Çalışma programı oluşturun</a>.</p>`)}
  ${sec("Sınavda zaman yönetimi", `<p><span class="chip orig">Öneri</span> 150 dakika iki test için ortak süredir; soru başına ortalama 1,5 dakikaya denk gelir. Bir yol haritası: Sözel testte paragraf bloğuna ve sözel mantık gruplarına, sayısal testte 23–43 arasındaki ortak bilgi gruplarına yeterli süre ayırın. İlk turda 2 dakikayı aşan soruyu işaretleyip geçin; ikinci turda dönün. Kılavuza göre sınavın ilk 110 dakikası ve son 15 dakikası içinde salondan çıkılamaz.</p>`)}
  ${sec("Paragraf çözme teknikleri", `<ul class="clean"><li>Önce soru kökünü okuyun (ana düşünce mi, değinilmeyen mi, çıkarım mı?).</li><li>'Oysa, ancak, bu nedenle, asıl' sözcüklerinden sonra yazarın görüşünü arayın.</li><li>'Hepsi, asla, tek, kesinlikle' içeren seçenekleri iki kez denetleyin.</li><li>Uzun metinlerde her paragrafın işlevini (tanım, sorun, neden, çözüm) not edin.</li></ul>`)}
  ${sec("Problem çözme teknikleri", `<ul class="clean"><li>Sabit kalanı bulun: yaş farkı, çözünen madde, toplam iş.</li><li>Yüzde sorularında başlangıcı 100 alın.</li><li>Seçenekleri yerine koyma yöntemi, özellikle tam sayı cevaplı problemlerde hızlıdır.</li></ul>`)}
  ${sec("Sayısal mantık stratejileri", `<ul class="clean"><li>Dizilerde sırayla: fark, oran, ikinci fark, iç içe dizi.</li><li>Kural tabanlı gruplarda kuralı küçük bir tabloya çevirin; uç durumları (tavan, eşik) test edin.</li></ul>`)}
  ${sec("Sözel mantık stratejileri", `<ul class="clean"><li>Her grupta tablo kurun; önce kesin bilgiler, sonra 'hemen önce/yan yana' blokları.</li><li>Ek koşullu soruların koşulu yalnızca o soruya aittir.</li><li>'A ise B' önermesinden yalnızca 'B değilse A değil' çıkar. <a href="#/mantik">Mantık Atölyesi</a></li></ul>`)}
  ${sec("Sınav kaygısı yönetimi", `<ul class="clean"><li>Deneme sınavlarını gerçek sınav saatinde (10.15) çözerek alışkanlık kazanın.</li><li>Sınav sırasında takıldığınızda 4 saniye nefes al – 4 saniye tut – 6 saniye ver tekniğiyle kısa bir mola verin.</li><li>Tek bir sorunun tüm sınavı belirlemediğini hatırlayın; işaretleyip geçin.</li><li>Kaygı günlük yaşamı etkiliyorsa üniversitenizin psikolojik danışmanlık birimine başvurun.</li></ul>`)}
  ${sec("Son hafta çalışma önerileri", `<ul class="clean"><li>Yeni konu öğrenmek yerine kısa tekrar notlarını ve Yanlışlarım listesini çalışın.</li><li>En fazla 2 tam deneme çözün; aradaki günlerde analiz yapın.</li><li>Sınavdan önceki gün hafif tekrar ve düzenli uyku. Sınava giriş belgesini ais.osym.gov.tr'den edinin ve sınav binasını önceden görün.</li><li>Kimlik belgesi kurallarını kılavuzdan (md. 3.2) kontrol edin.</li></ul>`)}
  </div>`;
}
const SOURCES = [
  ["2026-ALES Başvuru Kılavuzu", "Kılavuz", "25.03.2026", "https://dokuman.osym.gov.tr/pdfdokuman/2026/ALES-1/kilavuz_b25032026.pdf", "Format, süre, değerlendirme, puan türleri ve geçerlilik bilgilerinin kaynağı."],
  ["ALES/1 duyuruları", "Duyuru listesi", "—", "https://osym.gov.tr/SinavGrubu/Menu/368", "2025 ve 2026 ALES/1 başvuru, kitapçık ve sonuç duyuruları."],
  ["ALES/2 duyuruları", "Duyuru listesi", "—", "https://osym.gov.tr/SinavGrubu/Menu/386", "2026-ALES/2'nin 2 Ağustos 2026'da yapıldığını gösteren duyurular."],
  ["ALES/3 duyuruları", "Duyuru listesi", "—", "https://osym.gov.tr/SinavGrubu/Menu/398", "ALES/3 (sonbahar) oturum duyuruları."],
  ["ALES hakkında", "Bilgi sayfası", "—", "https://osym.gov.tr/ales-hakkinda", "ÖSYM'nin ALES tanıtım sayfası."],
  ["Aday İşlemleri Sistemi", "Hizmet", "—", "https://ais.osym.gov.tr", "Başvuru, sınava giriş belgesi ve soru kitapçığının tamamına (adaylara 10 gün) erişim."],
  ["Sonuç sistemi", "Hizmet", "—", "https://sonuc.osym.gov.tr", "Sınav sonuçları."]
];
const ARCHIVE = [
  ["2026-ALES/2", "02.08.2026", "https://osym.gov.tr/2026-ales2-temel-soru-kitapcigi-ve-cevap-anahtari-yayimlandi", "https://dokuman.osym.gov.tr/web/2026/8/2025-ales2-temel-soru-kitapcigi-ve-cevap-anahtari-10-b22o51-02132535.pdf"],
  ["2026-ALES/1", "10.05.2026", "https://osym.gov.tr/2026ales1-temel-soru-kitapcigi-ve-cevap-anahtari-yayimlandi", "https://dokuman.osym.gov.tr/pdfdokuman/2026/ALES-1/tsk_als10052026.pdf"],
  ["2025-ALES/3", "23.11.2025", "https://osym.gov.tr/2025ales3-temel-soru-kitapcigi-ve-cevap-anahtari-yayimlandi", "https://dokuman.osym.gov.tr/pdfdokuman/2025/ALES-3/TSK/tsk_al3d23112025.pdf"],
  ["2025-ALES/1", "13.04.2025", "https://osym.gov.tr/2025ales1-temel-soru-kitapcigi-ve-cevap-anahtari-yayimlandi", "https://dokuman.osym.gov.tr/pdfdokuman/2025/ALES-1/tsk_13042025.pdf"]
];
function renderSources() {
  $("#view").innerHTML = `<div class="page-head"><div><h1>Kaynakça ve ÖSYM Arşivi</h1><p>Resmî kaynaklara bağlantılar. ÖSYM'nin telif hakkına sahip hiçbir materyali bu platformda çoğaltılmamış veya yüklenmemiştir.</p></div></div>
  <div class="stack"><div class="note"><b>Platformdaki soruların tamamı özgündür</b> ve "Özgün – ALES Akademi" etiketini taşır. ÖSYM soruları yalnızca aşağıdaki resmî bağlantılardan incelenebilir. Kılavuza göre sorular, ÖSYM'nin yazılı izni olmadan çoğaltılamaz ve yayımlanamaz.</div>
  <div class="card"><h3>Resmî kaynaklar</h3><div class="tbl-wrap"><table class="t"><tr><th>Kaynak</th><th>Tür</th><th>Yayım</th><th>Açıklama</th></tr>${SOURCES.map(s => `<tr><td><a href="${s[3]}" target="_blank" rel="noopener">${s[0]}</a></td><td class="small">${s[1]}</td><td class="small">${s[2]}</td><td class="small">${s[4]}</td></tr>`).join("")}</table></div><p class="tiny muted">Erişim tarihi: 31.10.2026.</p></div>
  <div class="card"><h3>Kamuya açık soru kitapçığı örnekleri (%10)</h3><p class="small muted">ÖSYM her oturumdan sonra Temel Soru Kitapçığı ve Cevap Anahtarı'nın yalnızca <b>%10'unu</b> kamuya açar; tamamı yalnızca sınava başvuran adaylara Aday İşlemleri Sistemi'nde 10 gün süreyle görüntülenebilir. ALES Akademi araştırmasında aşağıdaki dört oturumun kamuya açık bölümleri incelenmiştir; 2021–2024 ve 2025-ALES/2 incelenmemiştir.</p>
    <div class="tbl-wrap"><table class="t"><tr><th>Oturum</th><th>Sınav / yayım</th><th>Duyuru</th><th>Kitapçık (%10, PDF)</th></tr>${ARCHIVE.map(a => `<tr><td><b>${a[0]}</b></td><td class="small">${a[1]}</td><td><a href="${a[2]}" target="_blank" rel="noopener">ÖSYM duyurusu</a></td><td><a href="${a[3]}" target="_blank" rel="noopener">Resmî PDF</a></td></tr>`).join("")}</table></div></div>
  <div class="card"><h3>Araştırma bulguları (özet)</h3><ul class="clean small"><li>Dört oturumda da Sayısal Testi: 1–22 tekil sorular, 23–43 ortak bilgiye dayalı 2'li/3'lü gruplar (8 grup), 44–50 geometri.</li><li>Sözel Testi: 1–5 boşluk doldurma, 6–8 kesin çıkarım, 13–15 cümle yer değiştirme, 16–18 anlam bütünlüğünü bozan cümle, 29–42 parçaya bağlı paragraf grupları, 43–50 iki adet dörtlü sözel mantık grubu.</li><li>Konu bazında kesin soru dağılımı ÖSYM tarafından yayımlanmamıştır; yukarıdakiler yönerge başlıklarından çıkarılmış gözlemlerdir. Gelecek sınavlar hakkında tahmin yapılmaz.</li></ul></div></div>`;
}

/* ================================================================ AYARLAR */
function renderSettings() {
  const d = S(), root = $("#view");
  root.innerHTML = `<div class="page-head"><div><h1>Profil ve Ayarlar</h1><p>Verileriniz yalnızca bu tarayıcıda (localStorage) saklanır.</p></div></div>
  <div class="stack"><div class="card"><h3>Tema</h3><div class="tabs" id="thm">${[["", "Sistem"], ["light", "Açık"], ["dark", "Koyu"]].map(([v, l]) => `<button data-th="${v}" class="${(d.theme || "") === v ? "on" : ""}">${l}</button>`).join("")}</div></div>
  <div class="card"><h3>Profil ve program</h3>${d.profile ? `<dl class="kv"><dt>Ad</dt><dd>${esc(d.profile.name || "—")}</dd><dt>Hedef</dt><dd>${d.profile.targetScore} · ${d.profile.targetType}</dd><dt>Program</dt><dd>${d.profile.days} gün, ${trDate(d.profile.start)} başlangıç</dd></dl>` : '<p class="small muted">Profil oluşturulmadı.</p>'}<a class="btn" href="#/program" style="margin-top:10px">Programı düzenle</a></div>
  <div class="card"><h3>Yedekleme</h3><p class="small muted">İlerlemenizi bir JSON dosyasına aktarın ya da başka bir cihazda içe aktarın.</p><div class="row"><button class="btn" id="exp">Verileri dışa aktar</button><label class="btn">İçe aktar<input type="file" id="imp" accept="application/json" class="sr"></label><button class="btn danger" id="rst">Tüm verileri sıfırla</button></div></div>
  <div class="card"><h3>Hakkında</h3><p class="small">ALES Akademi v${APP.version} · ${QB.length} özgün soru · ${window.LESSONS.length} konu. Soru bankası sürümü ${esc(window.QBANK.meta.version)} (${esc(window.QBANK.meta.generated)}).</p>${Store.ok ? "" : '<div class="note bad small">Tarayıcı depolamasına yazılamıyor (gizli pencere ya da engellenmiş site verisi olabilir). İlerlemeniz bu oturum kapanınca kaybolabilir.</div>'}</div></div>`;
  $$("[data-th]").forEach(b => b.onclick = () => { d.theme = b.dataset.th || null; Store.save(); applyTheme(); renderSettings(); });
  $("#exp").onclick = () => { const blob = new Blob([JSON.stringify(d)], { type: "application/json" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `ales-akademi-yedek-${todayStr()}.json`; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); };
  $("#imp").onchange = e => { const f = e.target.files[0]; if (!f) return; f.text().then(t => { try { const j = JSON.parse(t); if (!j || j.v !== 1) throw 0; Store.d = Object.assign(DEFAULT(), j); Store.save(); toast("Veriler içe aktarıldı."); route(); } catch (x) { toast("Dosya okunamadı: geçerli bir ALES Akademi yedeği değil."); } }); };
  $("#rst").onclick = () => confirmBox("Tüm veriler silinsin mi?", "Çözülen sorular, yanlışlar, favoriler, görevler ve denemeler kalıcı olarak silinir.", "Evet, sıfırla", () => { Store.reset(); toast("Veriler sıfırlandı."); route(); });
}

/* ================================================================ yönlendirme */
function applyTheme() {
  const t = S().theme; if (t) document.documentElement.dataset.theme = t; else delete document.documentElement.dataset.theme;
  const dark = t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
  $$(".theme-btn").forEach(b => { b.innerHTML = ic(dark ? "sun" : "moon"); b.setAttribute("aria-label", dark ? "Açık temaya geç" : "Koyu temaya geç"); });
}
function route() {
  const h = location.hash.replace(/^#\/?/, ""), [path] = h.split("?"), parts = path.split("/");
  if (parts[0] !== "sinav") clearInterval(EXAM_TIMER);
  if (parts[0] !== "coz") clearInterval(window._qt);
  const map = {
    "": renderHome, akademi: () => renderAcademy(), sayisal: () => renderAcademy("say"), sozel: () => renderAcademy("soz"),
    konu: () => renderLesson(parts[1]), banka: renderBank, coz: renderPractice, mantik: () => renderLogic(parts[1] || ""),
    deneme: renderExamCenter, sinav: renderExam, sonuc: () => renderResult(parts[1]), gorevler: renderTasks, yanlislar: renderWrongs,
    favoriler: renderFavs, program: renderProgram, performans: renderPerf, puan: renderScore, rehber: renderGuide, kaynak: renderSources, ayarlar: renderSettings
  };
  const fn = map[parts[0]] || renderHome;
  try { fn(); } catch (e) { console.error(e); $("#view").innerHTML = `<div class="note bad">Sayfa yüklenirken bir hata oluştu: ${esc(e.message)}</div>`; }
  renderNav();
  $(".side").classList.remove("open"); $(".scrim").classList.remove("on");
  if (!["sinav", "coz"].includes(parts[0])) window.scrollTo(0, 0);
  document.title = (({ "": "Ana Sayfa", konu: (LMAP[parts[1]] || {}).title }[parts[0]]) || ($(".nav a.on span") || {}).textContent || "ALES Akademi") + " · ALES Akademi";
}
function boot() {
  Store.load(); applyTheme(); tipInit();
  const toggleTheme = () => { const dark = document.documentElement.dataset.theme ? document.documentElement.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; S().theme = dark ? "light" : "dark"; Store.save(); applyTheme(); };
  $$(".theme-btn").forEach(b => b.onclick = toggleTheme);
  $("#menu").onclick = () => { $(".side").classList.add("open"); $(".scrim").classList.add("on"); };
  $(".scrim").onclick = () => { $(".side").classList.remove("open"); $(".scrim").classList.remove("on"); };
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", applyTheme);
  addEventListener("hashchange", route);
  addEventListener("keydown", e => { examKeys(e); practiceKeys(e); });
  if (S().active && Date.now() >= S().active.end) finishExam(true);
  route();
}
document.addEventListener("DOMContentLoaded", boot);
