/* ALES Akademi — müfredat ve konu anlatımları.
 * Her konu 14 bölümlü yapıyı izler; 7 (ALES tarzı uygulama) ve 10–13 (testler)
 * soru bankasından konu ve zorluğa göre otomatik oluşturulur.
 */
window.LESSONS = [
  // ===================================================================== SAYISAL
  {
    id: "temel", area: "say", phase: 1, title: "Temel Kavramlar ve Sayılar", group: "A. Temel Matematik",
    subs: ["Doğal sayılar", "Tam sayılar", "Sayı kümeleri", "Tek ve çift sayılar", "Pozitif ve negatif sayılar", "Asal sayılar", "Ardışık sayılar", "Sayı basamakları"],
    kaz: ["Sayı kümelerini ve aralarındaki kapsama ilişkisini açıklar.", "Tek-çift ve işaret kurallarını kullanarak kesin yargıya ulaşır.", "Basamak çözümlemesiyle denklem kurar.", "Ardışık sayı dizilerinde terim-toplam ilişkisini kullanır."],
    tanim: "Temel kavramlar; sayı kümeleri, sayıların türleri (tek, çift, asal, ardışık) ve basamak yapısıyla ilgilidir. ALES Sayısal testinin ilk sorularında sıkça doğrudan, ilerleyen sorularda ise başka konuların içinde dolaylı olarak kullanılır.",
    kavramlar: [["Doğal sayılar (ℕ)", "0, 1, 2, 3, … biçiminde devam eden sayılar."], ["Tam sayılar (ℤ)", "…, −2, −1, 0, 1, 2, … ; sıfır ne pozitif ne negatiftir."], ["Rakam", "0–9 arasındaki 10 simge; sayı, rakamlarla yazılır."], ["Asal sayı", "1'den büyük, yalnızca 1'e ve kendisine bölünebilen doğal sayı. En küçük asal 2'dir ve tek çift asal da odur."], ["Ardışık sayılar", "Belirli bir kurala göre (genellikle eşit artışla) art arda gelen sayılar."]],
    mantik: "Bu konudaki soruların çoğu bir 'durum tablosu' kurmayı gerektirir: Tek-çift, pozitif-negatif ya da rakam olasılıkları tek tek listelenir ve 'kesinlikle' istenen yargı tüm durumlarda sınanır. Ezberden çok sistemli deneme yapılır.",
    anlatim: [
      { h: "Tek ve çift sayılar", p: "Çift ± çift = çift, tek ± tek = çift, tek ± çift = tek. Çarpımda tek bir çift çarpan sonucu çift yapar; çarpımın tek olması için bütün çarpanlar tek olmalıdır. Üs almak tek-çiftliği değiştirmez (pozitif tam sayı üslerde): aⁿ ile a aynı tek-çiftliktedir." },
      { h: "Pozitif ve negatif sayılar", p: "Çarpma ve bölmede işaretler çarpılır: (−)·(−) = (+), (−)·(+) = (−). Çift kuvvetler her zaman negatif olmayan sonuç verir; tek kuvvetler tabanın işaretini korur. 'a·b < 0' bilgisi a ile b'nin ters işaretli olduğunu söyler, hangisinin negatif olduğunu söylemez." },
      { h: "Asal sayılar", p: "100'e kadar 25 asal vardır. Bir sayının asal olup olmadığı, karekökünden küçük asallara bölünüp bölünmediğine bakılarak anlaşılır. 'a ve b asal, a + b tek' bilgisi asallardan birinin 2 olmasını zorunlu kılar." },
      { h: "Ardışık sayılar", p: "Ardışık sayılarda terim sayısı = (son − ilk) ÷ artış + 1; toplam = (ilk + son) · terim sayısı ÷ 2. Terim sayısı tek ise ortadaki terim ortalamaya eşittir." },
      { h: "Sayı basamakları", p: "AB = 10A + B, ABC = 100A + 10B + C. AB + BA = 11(A + B), AB − BA = 9(A − B). Rakamların farklı olması, ilk rakamın sıfır olamaması gibi koşullar en büyük/en küçük sayı sorularının anahtarıdır." }
    ],
    formuller: ["AB = 10A + B", "AB + BA = 11(A + B)", "AB − BA = 9(A − B)", "Terim sayısı = (son − ilk) / artış + 1", "Toplam = (ilk + son) · n / 2"],
    ornekler: [
      { q: "Ardışık 5 tek sayının toplamı 85'tir. En büyüğü kaçtır?", steps: ["Ortanca terim = 85 ÷ 5 = 17.", "Sayılar 13, 15, 17, 19, 21."], a: "21" },
      { q: "a ve b asal sayılar ve a + b = 25 ise a·b kaçtır?", steps: ["İki tek sayının toplamı çifttir; toplam tek olduğuna göre asallardan biri çift olmalıdır: 2.", "Diğeri 25 − 2 = 23 olur ve 23 asaldır.", "a·b = 2·23 = 46."], a: "46" },
      { q: "İki basamaklı AB sayısı, BA sayısından 36 fazladır. A + B = 10 ise AB kaçtır?", steps: ["AB − BA = 9(A − B) = 36 ⇒ A − B = 4.", "A + B = 10 ⇒ A = 7, B = 3."], a: "73" }
    ],
    pratik: ["'Kesinlikle' sorularında her seçenek için bir karşı örnek arayın; bulamadığınız seçenek doğrudur.", "Tek-çift sorularında sayılar yerine T/Ç sembolleriyle tablo kurun.", "En büyük sayı istenirken soldaki basamağa en büyük uygun rakamı yerleştirip sağa doğru ilerleyin."],
    hatalar: ["Sıfırı pozitif ya da negatif saymak.", "1'i asal saymak.", "'a·b < 0' bilgisinden a'nın negatif olduğunu varsaymak.", "AB yazımını A·B çarpımı sanmak."],
    notlar: ["2 tek çift asaldır.", "Çarpımın tek olması için tüm çarpanlar tek olmalı.", "AB + BA her zaman 11'in katıdır.", "Ardışık sayılarda ortalama = ortanca."]
  },
  {
    id: "bolunebilme", area: "say", phase: 1, title: "Bölme, Bölünebilme ve Faktöriyel", group: "A. Temel Matematik",
    subs: ["Bölme işlemi", "Bölünebilme kuralları", "Faktöriyel", "Asal çarpanlar ve bölen sayısı", "EBOB ve EKOK"],
    kaz: ["Bölme işleminde bölünen = bölen·bölüm + kalan bağıntısını kullanır.", "2, 3, 4, 5, 8, 9, 10, 11 ve bileşik sayılarla bölünebilmeyi uygular.", "Faktöriyelli ifadeleri sadeleştirir ve asal çarpan üssünü bulur.", "EBOB-EKOK'u gerçek yaşam problemlerine uygular."],
    tanim: "Bölme, bir sayının başka bir sayının içinde kaç kez bulunduğunu ve geriye ne kaldığını inceler. Bölünebilme kuralları, bölme yapmadan kalanı kestirmeyi sağlar.",
    kavramlar: [["Kalan", "0 ≤ kalan < bölen olmalıdır."], ["Faktöriyel", "n! = 1·2·3·…·n; 0! = 1."], ["EBOB", "Sayıları tam bölen en büyük ortak sayı."], ["EKOK", "Sayıların her birine tam bölünen en küçük ortak kat."], ["Aralarında asal", "EBOB'u 1 olan sayılar."]],
    mantik: "Kalan sorularında sayıyı 'bölen·t + kalan' biçiminde yazmak çoğu soruyu tek adıma indirir. Bileşik sayıyla bölünebilmede sayı, aralarında asal çarpanlarına ayrılır (36 = 4·9) ve her biri ayrı denetlenir.",
    anlatim: [
      { h: "Bölme bağıntısı", p: "A = B·Q + K ve 0 ≤ K < B. A'nın B ile kalanı K ise, B'nin bir böleni d için A'nın d ile kalanı K'nin d ile kalanına eşittir." },
      { h: "Bölünebilme kuralları", p: "2: son rakam çift. 3: rakamlar toplamı 3'ün katı. 4: son iki basamak 4'ün katı. 5: son rakam 0 ya da 5. 8: son üç basamak 8'in katı. 9: rakamlar toplamı 9'un katı. 10: son rakam 0. 11: sağdan başlayarak +, −, + … işaretleriyle toplanan rakamların sonucu 11'in katı." },
      { h: "Faktöriyel", p: "(n+1)! = (n+1)·n!. Ortak faktöriyel parantezine almak sadeleştirmenin anahtarıdır. n! içindeki p asal çarpanının üssü ⌊n/p⌋ + ⌊n/p²⌋ + ⌊n/p³⌋ + … ile bulunur; sondaki sıfır sayısı 5'lerin sayısıdır." },
      { h: "Bölen sayısı", p: "N = a^x · b^y · c^z (a, b, c farklı asallar) ise pozitif bölen sayısı (x+1)(y+1)(z+1)'dir. Tek bölen sayısı 2'nin üssü yok sayılarak bulunur." },
      { h: "EBOB-EKOK problemleri", p: "'En büyük parça, en az sayıda kare karo, eşit aralıkla dikim' → EBOB. 'Birlikte ilk kez, en az kaç gün sonra yeniden' → EKOK. İki sayı için EBOB·EKOK = sayıların çarpımı." }
    ],
    formuller: ["A = B·Q + K, 0 ≤ K < B", "Bölen sayısı = (x+1)(y+1)(z+1)", "EBOB(a,b)·EKOK(a,b) = a·b", "n! içinde p'nin üssü = Σ ⌊n/pᵏ⌋"],
    ornekler: [
      { q: "x'in 6 ile bölümünden kalan 4, 8 ile bölümünden kalan 6'dır. x'in en küçük pozitif değeri kaçtır?", steps: ["Her iki kalanda bölen − kalan = 2: x + 2 hem 6'nın hem 8'in katı.", "x + 2 = EKOK(6, 8) = 24 ⇒ x = 22."], a: "22" },
      { q: "50! sayısının sondan kaç basamağı sıfırdır?", steps: ["⌊50/5⌋ + ⌊50/25⌋ = 10 + 2 = 12."], a: "12" },
      { q: "72 sayısının kaç pozitif böleni vardır?", steps: ["72 = 2³·3².", "(3+1)(2+1) = 12."], a: "12" }
    ],
    pratik: ["'Bölen − kalan' tüm koşullarda eşitse x + (fark) ortak kattır.", "Basamakları bilinmeyen sayılarda önce son rakam koşulunu (2, 4, 5, 8) sonra rakam toplamını (3, 9) kullanın.", "Faktöriyelli kesirlerde en küçük faktöriyeli ortak parantez yapın."],
    hatalar: ["Kalanı bölenden büyük ya da eşit bırakmak.", "36'ya bölünebilmeyi 6 ve 6 ile denetlemek (aralarında asal değiller).", "0! değerini 0 almak.", "Sondaki sıfır sayısında yalnızca ⌊n/5⌋ almak, 25 ve 125'leri unutmak."],
    notlar: ["Bileşik bölünebilme: aralarında asal çarpanlara ayır.", "0! = 1! = 1.", "EKOK: 'birlikte yeniden'; EBOB: 'en büyük eş parça'."]
  },
  {
    id: "rasyonel", area: "say", phase: 1, title: "Rasyonel ve Ondalık Sayılar", group: "B. Sayılar ve Cebir",
    subs: ["Rasyonel sayılar", "Basit kesirler", "Bileşik kesirler", "Ondalık sayılar", "Devirli ondalık sayılar", "Kesir problemleri"],
    kaz: ["Kesirlerle dört işlemi işlem önceliğine uygun yapar.", "Rasyonel sayıları sıralar.", "Ondalık ve devirli ondalık sayıları kesre çevirir.", "'Kalanın kesri' ile 'bütünün kesri' ayrımını yapar."],
    tanim: "a/b (b ≠ 0, a ve b tam sayı) biçiminde yazılabilen sayılara rasyonel sayı denir. ALES'te özellikle ilk sorularda işlem becerisi, problemlerde ise kesir mantığı ölçülür.",
    kavramlar: [["Basit kesir", "Payı paydasından küçük kesir (3/5)."], ["Bileşik kesir", "Payı paydasından büyük ya da eşit kesir (7/4)."], ["Tam sayılı kesir", "2¾ = 11/4."], ["Devirli ondalık", "Virgülden sonra bir grup rakamın sonsuza dek tekrar ettiği sayı: 0,3̄."]],
    mantik: "Kesir işlemlerinde hız, payda eşitlemeyi gereksiz yere yapmamaktan gelir: çarpma ve bölmede sadeleştirme önce yapılır. Kesir problemlerinde 'kalanın' sözcüğü her adımda yeni bir bütün tanımlar.",
    anlatim: [
      { h: "İşlem önceliği", p: "Parantez → üs → çarpma/bölme (soldan sağa) → toplama/çıkarma (soldan sağa). Bölme, ikinci kesrin ters çevrilip çarpılmasıdır." },
      { h: "Sıralama", p: "Paydaları ya da payları eşitleyerek; ya da çapraz çarpımla karşılaştırma: a/b < c/d ⇔ a·d < b·c (b, d > 0). Bire yakınlık yöntemi: 1'den farkı küçük olan pozitif basit kesir daha büyüktür (6/7 > 5/6 çünkü 1/7 < 1/6)." },
      { h: "Ondalık sayılar", p: "Çarpmada virgülden sonraki basamak sayıları toplanır. Bölmede pay ve payda aynı 10'un kuvvetiyle çarpılarak virgülden kurtulunur." },
      { h: "Devirli ondalıklar", p: "0,a̅ = a/9; 0,a̅b̅ = ab/99; 0,ab̅ = (ab − a)/90. Genel kural: (sayının tamamı − devretmeyen kısım) / (devreden basamak kadar 9, devretmeyen basamak kadar 0)." },
      { h: "Kesir problemleri", p: "'Parasının 1/3'ünü harcadı, kalanın 2/5'ini harcadı' → kalan her seferinde (1 − kesir) ile çarpılır: 2/3 · 3/5 = 2/5 kalır." }
    ],
    formuller: ["a/b ÷ c/d = a/b · d/c", "0,a̅ = a/9", "0,a̅b̅ = ab/99", "0,ab̅ = (ab − a)/90"],
    ornekler: [
      { q: "(1/2 + 1/3) ÷ (1 − 1/6) kaçtır?", steps: ["Pay: 5/6. Payda: 5/6.", "Sonuç: 1."], a: "1" },
      { q: "Yalnızca 6 rakamının devrettiği 0,16̅ sayısı kesir olarak nedir?", steps: ["(16 − 1)/90 = 15/90 = 1/6."], a: "1/6" },
      { q: "Bir miktarın 1/4'ü, sonra kalanın 1/3'ü harcanınca 90 TL kalıyor. Başlangıç kaç TL?", steps: ["Kalan oran: 3/4 · 2/3 = 1/2.", "x/2 = 90 ⇒ x = 180."], a: "180" }
    ],
    pratik: ["Çarpma-bölmede önce çapraz sadeleştirin.", "Seçenekler kesirse sonucu ondalık yaklaşıkla sınayın.", "'Kalanın' sözcüğünü gördüğünüzde kalan oranları çarpın."],
    hatalar: ["Kesirleri toplarken payları ve paydaları ayrı ayrı toplamak.", "0,9̅'un 1'e eşit olduğunu unutmak.", "Kalanın kesrini bütünün kesri gibi hesaplamak."],
    notlar: ["Bölme = ters çevir, çarp.", "0,a̅ = a/9.", "Kalan oranları çarpılır."]
  },
  {
    id: "esitsizlik", area: "say", phase: 1, title: "Eşitsizlikler ve Mutlak Değer", group: "B. Sayılar ve Cebir",
    subs: ["Eşitsizlikler", "Aralıklar", "Mutlak değer", "Mutlak değerli denklem ve eşitsizlikler"],
    kaz: ["Eşitsizlikleri taraf tarafa toplar ve çarpar.", "Negatif sayıyla çarpmada yön değiştirir.", "Mutlak değerli denklemleri durumlara ayırarak çözer.", "Bir ifadenin alabileceği değer aralığını bulur."],
    tanim: "Eşitsizlik, iki ifade arasındaki büyüklük ilişkisidir. Mutlak değer ise bir sayının sayı doğrusunda sıfıra uzaklığıdır: |x| ≥ 0.",
    kavramlar: [["Açık aralık", "(a, b): uç noktalar dahil değil."], ["Kapalı aralık", "[a, b]: uç noktalar dahil."], ["|x|", "x ≥ 0 ise x; x < 0 ise −x."]],
    mantik: "Aralık sorularında ifadenin en küçük ve en büyük değeri uç noktalardan hesaplanır; kare alan ifadelerde sıfırın aralıkta olup olmadığı mutlaka denetlenir.",
    anlatim: [
      { h: "Temel kurallar", p: "Eşitsizliğin iki yanına aynı sayı eklenebilir. Pozitif sayıyla çarpma yönü korur; negatif sayıyla çarpma yönü ters çevirir. Aynı yönlü eşitsizlikler taraf tarafa toplanabilir; çıkarma doğrudan yapılmaz, önce −1 ile çarpılıp toplanır." },
      { h: "İfadenin aralığı", p: "a < x < b ve c < y < d ise x + y ∈ (a + c, b + d), x − y ∈ (a − d, b − c). x·y için dört uç çarpımın en küçüğü ve en büyüğü alınır. x² için aralık sıfırı içeriyorsa en küçük değer 0'dır." },
      { h: "Mutlak değer", p: "|x − a| = b (b ≥ 0) ⇒ x = a ± b. |x − a| < b ⇒ a − b < x < a + b. |x − a| > b ⇒ x < a − b ya da x > a + b. |x − a| + |x − b| ifadesinin en küçük değeri |a − b|'dir ve a ile b arasında alınır." },
      { h: "Kök kontrolü", p: "|f(x)| = g(x) denkleminde bulunan kökler g(x) ≥ 0 koşulunu sağlamalıdır; sağlamayan kök atılır." }
    ],
    formuller: ["|x − a| < b ⇔ a − b < x < a + b", "x − y ∈ (a − d, b − c)", "|a·b| = |a|·|b|", "|x| = |−x|"],
    ornekler: [
      { q: "−2 < x < 3 ise x² hangi aralıktadır?", steps: ["Aralık sıfırı içerir ⇒ en küçük 0.", "En büyük: max(4, 9) = 9 (uç dahil değil)."], a: "[0, 9)" },
      { q: "|2x − 3| ≤ 5 kaç tam sayıyla sağlanır?", steps: ["−5 ≤ 2x − 3 ≤ 5 ⇒ −1 ≤ x ≤ 4.", "−1, 0, 1, 2, 3, 4 ⇒ 6 tane."], a: "6" }
    ],
    pratik: ["Gerçel sayı mı tam sayı mı istendiğine dikkat edin.", "Kare içeren ifadelerde önce sıfırı denetleyin.", "Mutlak değerde kök bulunca sağ tarafın işaretini kontrol edin."],
    hatalar: ["Eşitsizlikleri taraf tarafa çıkarmak.", "Negatifle çarparken yönü çevirmeyi unutmak.", "Açık aralıkta uç değerleri saymak."],
    notlar: ["Çıkarma: −1 ile çarp, sonra topla.", "x² için sıfırı kontrol et.", "|f| = g ⇒ g ≥ 0 şartı."]
  },
  {
    id: "uslu", area: "say", phase: 1, title: "Üslü ve Köklü Sayılar", group: "B. Sayılar ve Cebir",
    subs: ["Üslü sayılar", "Üslü denklemler", "Köklü sayılar", "Paydayı rasyonel yapma", "Sıralama"],
    kaz: ["Tabanları eşitleyerek üslü ifadeleri sadeleştirir.", "Ortak çarpan parantezine alarak üslü denklem çözer.", "Kök içini tam kare çarpanlara ayırır.", "Üsleri eşitleyerek büyüklük karşılaştırır."],
    tanim: "aⁿ, a'nın n kez kendisiyle çarpımıdır. ⁿ√a ise n. kuvveti a olan sayıdır ve a^(1/n) olarak da yazılır.",
    kavramlar: [["Negatif üs", "a⁻ⁿ = 1/aⁿ (a ≠ 0)."], ["Sıfırıncı kuvvet", "a⁰ = 1 (a ≠ 0)."], ["Eşlenik", "√a − b'nin eşleniği √a + b'dir."]],
    mantik: "Her üslü soruda ilk hamle tabanları ortak asala indirmektir (4 = 2², 27 = 3³). Toplama içeren üslü denklemlerde en küçük kuvvet ortak parantezine alınır.",
    anlatim: [
      { h: "Üs kuralları", p: "aᵐ·aⁿ = aᵐ⁺ⁿ, aᵐ/aⁿ = aᵐ⁻ⁿ, (aᵐ)ⁿ = aᵐⁿ, (a·b)ⁿ = aⁿbⁿ. Toplamada üsler toplanmaz: 2³ + 2³ = 2·2³ = 2⁴." },
      { h: "Üslü denklemler", p: "3ˣ⁺² − 3ˣ = 72 ⇒ 3ˣ(9 − 1) = 72 ⇒ 3ˣ = 9 ⇒ x = 2. Tabanlar eşitse üsler eşittir (taban 0, 1, −1 değilse)." },
      { h: "Köklü sayılar", p: "√(a²b) = |a|√b. Toplama yalnızca kök içleri aynı olan terimler arasında yapılır: 2√3 + 5√3 = 7√3. √a·√b = √(ab) (a, b ≥ 0)." },
      { h: "Paydayı rasyonel yapma", p: "1/√a = √a/a. 1/(√a − b) = (√a + b)/(a − b²)." },
      { h: "Büyüklük karşılaştırma", p: "2³⁰, 3²⁰, 5¹⁰ gibi sayılarda üslerin ortak böleni (10) çıkarılır: (2³)¹⁰, (3²)¹⁰, 5¹⁰ ⇒ 8, 9, 5 karşılaştırılır." }
    ],
    formuller: ["aᵐ·aⁿ = aᵐ⁺ⁿ", "(aᵐ)ⁿ = aᵐⁿ", "a⁻ⁿ = 1/aⁿ", "√(a²b) = |a|√b", "(√a − √b)(√a + √b) = a − b"],
    ornekler: [
      { q: "8³ · 4² ÷ 2⁵ = 2ᵏ ise k kaçtır?", steps: ["2⁹ · 2⁴ ÷ 2⁵ = 2⁸."], a: "8" },
      { q: "√48 + √27 − √12 kaçtır?", steps: ["4√3 + 3√3 − 2√3 = 5√3."], a: "5√3" }
    ],
    pratik: ["Ondalık tabanları kesre çevirin: (0,25)⁻² = 4² = 16.", "Seçeneklerde kök varsa sonucu √ cinsinden bırakın.", "Toplama varsa ortak çarpan; çarpma varsa üs toplama."],
    hatalar: ["2ⁿ + 2ⁿ = 4ⁿ sanmak (doğrusu 2ⁿ⁺¹).", "−2² ile (−2)²'yi karıştırmak.", "√(a + b) = √a + √b sanmak."],
    notlar: ["Önce tabanları eşitle.", "aⁿ + aⁿ = 2aⁿ.", "Kökte yalnızca benzer terimler toplanır."]
  },
  {
    id: "cebir", area: "say", phase: 1, title: "Çarpanlara Ayırma ve Denklemler", group: "B. Sayılar ve Cebir",
    subs: ["Özdeşlikler", "Çarpanlara ayırma", "Birinci dereceden denklemler", "Denklem sistemleri"],
    kaz: ["Tam kare ve iki kare farkı özdeşliklerini uygular.", "İkinci dereceden üç terimliyi çarpanlarına ayırır.", "Kesirli birinci dereceden denklem çözer.", "İki bilinmeyenli doğrusal sistem çözer."],
    tanim: "Çarpanlara ayırma, bir ifadeyi çarpımlar biçiminde yazmaktır. Denklem ise bilinmeyen içeren ve belirli değerler için doğru olan eşitliktir.",
    kavramlar: [["Özdeşlik", "Bilinmeyenin her değeri için doğru olan eşitlik."], ["Kök", "Denklemi sağlayan değer."], ["Yok etme yöntemi", "Denklemleri uygun katsayılarla çarpıp toplayarak bir bilinmeyeni ortadan kaldırmak."]],
    mantik: "ALES'te özdeşlikler çoğunlukla 'x ve y'yi bulmadan' istenen ifadeyi hesaplatır. Önce istenen ifadenin hangi özdeşlikle verilenlere bağlandığı bulunur.",
    anlatim: [
      { h: "Özdeşlikler", p: "(a ± b)² = a² ± 2ab + b²; a² − b² = (a − b)(a + b); a³ ± b³ = (a ± b)(a² ∓ ab + b²); x + 1/x = k ⇒ x² + 1/x² = k² − 2." },
      { h: "Üç terimli ifadeler", p: "x² + bx + c ifadesinde çarpımı c, toplamı b olan iki sayı (m, n) bulunur: (x + m)(x + n)." },
      { h: "Denklemler", p: "Kesirli denklemde paydalar EKOK ile eşitlenir. Sözel problemlerde bilinmeyen en küçük ya da en çok tekrar eden niceliğe atanır." },
      { h: "Sistemler", p: "Yok etme ya da yerine koyma. Bazen x + y ve x − y doğrudan istenir; denklemleri toplamak/çıkarmak yeterli olabilir." }
    ],
    formuller: ["(a + b)² = a² + 2ab + b²", "a² − b² = (a − b)(a + b)", "x² + 1/x² = (x + 1/x)² − 2", "x³ + 1/x³ = (x + 1/x)³ − 3(x + 1/x)"],
    ornekler: [
      { q: "x − y = 3, xy = 10 ise x² + y² kaçtır?", steps: ["(x − y)² = x² + y² − 2xy ⇒ 9 = x² + y² − 20."], a: "29" },
      { q: "1004² − 996² kaçtır?", steps: ["(1004 − 996)(1004 + 996) = 8·2000."], a: "16000" }
    ],
    pratik: ["Büyük sayıların kare farklarında iki kare farkını kullanın.", "Sözel denklemde varsayım yöntemi (hepsi pahalı olsaydı…) çoğu zaman daha hızlıdır.", "Çarpan sorularında seçenekleri yerine koyarak kök denetimi yapın."],
    hatalar: ["(a + b)² = a² + b² sanmak.", "Denklemi bir sayıyla çarparken tüm terimleri çarpmamak.", "Payda eşitlerken işaretleri dağıtmayı unutmak."],
    notlar: ["İki kare farkı hız kazandırır.", "x + 1/x tipinde kare al.", "Çarpım c, toplam b."]
  },
  {
    id: "oran", area: "say", phase: 1, title: "Oran ve Orantı", group: "B. Sayılar ve Cebir",
    subs: ["Oran", "Doğru orantı", "Ters orantı", "Bileşik orantı", "Orantılı paylaştırma", "Ölçek"],
    kaz: ["Zincir oranları ortak terimde birleştirir.", "Doğru ve ters orantıyı ayırt eder.", "Orantılı paylaştırma yapar.", "Ölçek ve birim dönüşümü yapar."],
    tanim: "Oran, aynı birimli iki çokluğun bölümüdür. Orantı, iki ya da daha çok oranın eşitliğidir.",
    kavramlar: [["Doğru orantı", "Biri artarken diğeri aynı oranda artar: y = k·x."], ["Ters orantı", "Biri artarken diğeri aynı oranda azalır: x·y = k."], ["Ölçek", "Harita uzunluğu / gerçek uzunluk."]],
    mantik: "Oran sorularının neredeyse tamamı 'k sabiti' ile çözülür: a/3 = b/5 ⇒ a = 3k, b = 5k. Zincir oranlarda ortak terimin katsayıları EKOK'ta eşitlenir.",
    anlatim: [
      { h: "Zincir oranlar", p: "a/b = 2/3, b/c = 4/5 ⇒ b ortak: a : b : c = 8 : 12 : 15." },
      { h: "Doğru/ters orantı", p: "İşçi sayısı ile süre ters orantılıdır; işçi sayısı ile yapılan iş doğru orantılıdır. Bileşik orantıda: (işçi · gün · saat) / iş = sabit." },
      { h: "Paylaştırma", p: "Doğru orantılı paylaştırmada paylar 2k, 3k, 5k; ters orantılı paylaştırmada paylar 1/2, 1/3, 1/5 oranlarının EKOK ile genişletilmiş hâlidir (15k, 10k, 6k)." },
      { h: "Ölçek", p: "1 : 100 000 ölçekte 1 cm = 1 km. km ↔ cm dönüşümünde 100 000 çarpanı kullanılır." }
    ],
    formuller: ["a/x = b/y = c/z = k ⇒ a = kx, …", "(işçi·gün)/iş = sabit", "Gerçek = harita · ölçek paydası"],
    ornekler: [
      { q: "a/2 = b/3 = c/5 ve a + b + c = 50 ise c kaçtır?", steps: ["10k = 50 ⇒ k = 5."], a: "25" },
      { q: "8 işçi bir işi 12 günde bitiriyorsa 6 işçi kaç günde bitirir?", steps: ["8·12 = 6·g ⇒ g = 16."], a: "16" }
    ],
    pratik: ["Her oranı k ile ifade edin.", "Ters orantıda 'çarpım sabit' cümlesini yazın.", "Ölçekte birimleri en sona bırakın."],
    hatalar: ["Ters orantılı paylaştırmada doğrudan oranları kullanmak.", "Zincir oranda ortak terimi eşitlemeden birleştirmek."],
    notlar: ["Oran = k.", "Ters orantı: çarpım sabit.", "1 km = 100 000 cm."]
  },
  {
    id: "problem", area: "say", phase: 2, title: "Problemler", group: "C. Problemler",
    subs: ["Sayı problemleri", "Kesir problemleri", "Yaş problemleri", "İşçi ve havuz problemleri", "Hareket problemleri", "Yüzde problemleri", "Kâr ve zarar problemleri", "Faiz problemleri", "Karışım problemleri", "Günlük yaşam problemleri"],
    kaz: ["Sözel ifadeyi denkleme dönüştürür.", "Yaş farkının sabitliğini kullanır.", "İş ve hareket problemlerinde hızları birleştirir.", "Ardışık yüzde değişimlerini birleştirir.", "Karışımda madde miktarını korur."],
    tanim: "Problemler, gündelik durumların matematiksel modele dönüştürülmesini ölçer. İncelenen 2025–2026 örnek kitapçıklarında yaş problemleri birden fazla oturumda görülmüştür.",
    kavramlar: [["İş hızı", "Birim zamanda yapılan iş = 1 / süre."], ["Ortalama hız", "Toplam yol / toplam süre."], ["Yüzde değişim", "(yeni − eski) / eski · 100."], ["Basit faiz", "F = A·r·t / 100 (t yıl)."]],
    mantik: "Her problemde üç soru sorulur: Bilinmeyen ne? Sabit kalan ne (yaş farkı, madde miktarı, toplam iş)? Hangi büyüklükler toplanır (hızlar, iş oranları)?",
    anlatim: [
      { h: "Yaş problemleri", p: "İki kişinin yaş farkı hiçbir zaman değişmez. t yıl sonra herkesin yaşı t artar; n kişilik grubun yaş toplamı n·t artar." },
      { h: "İşçi-havuz", p: "A işi a günde, B b günde bitiriyorsa birlikte 1/(1/a + 1/b) = ab/(a + b) günde biter. Boşaltan musluk/delik çıkarılır." },
      { h: "Hareket", p: "Yol = hız · zaman. Karşılıklı harekette hızlar toplanır, aynı yönde farkı alınır. Gidiş-dönüşte ortalama hız 2v₁v₂/(v₁ + v₂)'dir; aritmetik ortalama değildir." },
      { h: "Yüzde ve kâr-zarar", p: "Kâr ve zarar her zaman maliyet üzerinden hesaplanır. %a artış sonra %b indirim: (1 + a/100)(1 − b/100). %20 artış ve %20 indirim fiyatı %4 düşürür." },
      { h: "Karışım", p: "Çözünen miktarı = toplam · oran. Su eklemek çözünen miktarını değiştirmez; buharlaştırmak da değiştirmez." },
      { h: "Faiz", p: "Basit faiz: F = A·r·t/100 (t yıl) ya da A·r·t/1200 (t ay)." }
    ],
    formuller: ["Birlikte süre = ab/(a + b)", "Ortalama hız = 2v₁v₂/(v₁ + v₂)", "F = A·r·t/1200 (ay)", "Oran = çözünen / karışım"],
    ornekler: [
      { q: "Annenin yaşı kızının yaşının 4 katıdır. 6 yıl sonra 2,5 katı olacaktır. Anne kaç yaşındadır?", steps: ["4x + 6 = 2,5(x + 6) ⇒ 1,5x = 9 ⇒ x = 6."], a: "24" },
      { q: "%30 tuzlu 200 g suya kaç g su eklenirse oran %20 olur?", steps: ["Tuz: 60 g. 60/(200 + x) = 0,2 ⇒ x = 100."], a: "100" }
    ],
    pratik: ["Yüzde sorularında başlangıç değerini 100 alın.", "İş problemlerinde toplam işi süreler EKOK'u kadar birim seçin (12 ve 18 gün → 36 birim iş).", "Seçeneklerden geriye doğru deneme, denklem kurmaktan hızlı olabilir."],
    hatalar: ["Ortalama hızı hızların ortalaması almak.", "İndirimi maliyet üzerinden hesaplamak.", "Yaş toplamında kişi sayısını unutmak."],
    notlar: ["Yaş farkı sabittir.", "İş hızları toplanır.", "Kâr maliyete göredir."]
  },
  {
    id: "islem", area: "say", phase: 2, title: "İşlem, Fonksiyon ve Modüler Aritmetik", group: "D. İleri Matematiksel İşlemler",
    subs: ["İşlem soruları", "Tanımlı işlemler", "Fonksiyonlar", "Modüler aritmetik", "Saat ve takvim problemleri"],
    kaz: ["Yeni tanımlanan işlemi kurala uygun uygular.", "Koşullu tanımlı işlemlerde doğru kuralı seçer.", "Fonksiyonda iç ifadeyi eşitleyerek değer bulur.", "Periyodik durumları mod ile çözer."],
    tanim: "Tanımlı işlem soruları, size verilen yeni bir kuralı doğru uygulayıp uygulamadığınızı ölçer. Modüler aritmetik ise döngüsel tekrar eden durumların (günler, saatler, son basamak) matematiğidir.",
    kavramlar: [["a ≡ b (mod m)", "a ile b'nin m ile bölümünden kalanlar eşittir."], ["Döngü", "Kuvvetlerin kalanları belirli uzunlukta tekrar eder."], ["Bileşke", "(f∘g)(x) = f(g(x))."]],
    mantik: "Tanımlı işlemlerde kural, sayılar yerine konarak mekanik olarak uygulanır; parantez önceliği ve koşullu kuralda hangi dalın seçildiği hata kaynağıdır. Modüler sorularda önce döngü uzunluğu bulunur.",
    anlatim: [
      { h: "Tanımlı işlemler", p: "a∗b = 2a + b − ab gibi bir tanımda a yerine ilk, b yerine ikinci sayı yazılır. (a∗b)∗c ile a∗(b∗c) genellikle farklıdır." },
      { h: "Fonksiyonlar", p: "f(2x + 1) = 4x + 3 ise f(5) için 2x + 1 = 5 ⇒ x = 2 ⇒ f(5) = 11. Bileşkede içten dışa hesaplanır." },
      { h: "Modüler aritmetik", p: "Haftanın günleri mod 7, saat mod 12/24, birler basamağı mod 10'dur. 7ⁿ'in birler basamağı 7, 9, 3, 1 döngüsüyle (uzunluk 4) tekrar eder: n mod 4'e bakılır." },
      { h: "Saat problemleri", p: "Dakikalar 60'ar, saatler 24'er gruplanır. 1000 dakika = 16 saat 40 dakika." }
    ],
    formuller: ["(a + b) mod m = ((a mod m) + (b mod m)) mod m", "(a·b) mod m = ((a mod m)(b mod m)) mod m", "n gün sonra: (bugün + n) mod 7"],
    ornekler: [
      { q: "a∆b = a + b + ab ise (1∆2)∆3 kaçtır?", steps: ["1∆2 = 1 + 2 + 2 = 5.", "5∆3 = 5 + 3 + 15 = 23."], a: "23" },
      { q: "3¹⁰⁰'ün birler basamağı?", steps: ["3, 9, 7, 1 döngüsü (4).", "100 ≡ 0 (mod 4) ⇒ döngünün 4. elemanı: 1."], a: "1" }
    ],
    pratik: ["Koşullu tanımda her adımda koşulu yeniden kontrol edin.", "Döngüde kalan 0 ise döngünün son elemanı alınır.", "Gün sorularında 'bugünden n gün sonra' ile 'n. gün' farkına dikkat."],
    hatalar: ["Tanımlı işlemde sırayı ters uygulamak.", "Kalan 0 çıkınca döngünün ilk elemanını almak."],
    notlar: ["Kuralı aynen uygula.", "Önce döngü uzunluğu.", "f(iç) → içi eşitle."]
  },
  {
    id: "sayma", area: "say", phase: 2, title: "Permütasyon, Kombinasyon ve Olasılık", group: "D. İleri Matematiksel İşlemler",
    subs: ["Sayma yöntemleri", "Permütasyon", "Kombinasyon", "Olasılık"],
    kaz: ["Çarpma ilkesini kısıtlarla uygular.", "Sıranın önemli olduğu ve olmadığı durumları ayırt eder.", "Koşullu seçimleri durumlara ayırır.", "Eş olasılıklı örnek uzayda olasılık hesaplar."],
    tanim: "Sayma, olası durumların sistemli biçimde sayılmasıdır. Permütasyonda sıra önemlidir, kombinasyonda önemli değildir. Olasılık = istenen durum / tüm durumlar.",
    kavramlar: [["P(n, r)", "n'nin r'li sıralaması = n!/(n − r)!"], ["C(n, r)", "n'nin r'li seçimi = n!/(r!(n − r)!)"], ["Tümleyen", "P(A') = 1 − P(A)."]],
    mantik: "Önce 'sıra önemli mi?' sorusu sorulur. Kısıt varsa en kısıtlı yer önce doldurulur. 'En az bir' ifadesinde tümleyen hızlıdır.",
    anlatim: [
      { h: "Çarpma ilkesi", p: "Ardışık bağımsız seçimlerde seçenek sayıları çarpılır. 0 rakamı en başa gelemez; bu yüzden basamak sorularında önce birler ve yüzler basamağı düşünülür." },
      { h: "Tekrarlı permütasyon", p: "n nesnede a, b, … tane özdeş varsa sıralama sayısı n!/(a!·b!·…)." },
      { h: "Dairesel ve blok", p: "n kişi yuvarlak masaya (n − 1)! biçimde oturur. Yan yana olacaklar tek blok sayılır ve blok içi kendi arasında sıralanır." },
      { h: "Kombinasyon", p: "'En az k' koşulunda durumlar ayrı ayrı toplanır ya da tümünden istenmeyenler çıkarılır. Kareli yolda en kısa yol sayısı C(m + n, m)." },
      { h: "Olasılık", p: "Aynı anda çekilişlerde kombinasyon, sırayla çekilişlerde ardışık olasılıkların çarpımı kullanılır. İki zarda örnek uzay 36'dır." }
    ],
    formuller: ["P(n, r) = n!/(n − r)!", "C(n, r) = n!/(r!(n − r)!)", "Dairesel: (n − 1)!", "P(A) = s(A)/s(E)"],
    ornekler: [
      { q: "5 kişiden 3 kişilik bir kurul kaç farklı biçimde seçilir?", steps: ["Sıra önemsiz: C(5, 3) = 10."], a: "10" },
      { q: "Bir torbada 3 kırmızı, 2 mavi top var. Çekilen iki topun aynı renkte olma olasılığı?", steps: ["Tüm: C(5,2) = 10. Aynı renk: C(3,2) + C(2,2) = 4."], a: "2/5" }
    ],
    pratik: ["Küçük durumları listeleyerek kuralı doğrulayın.", "'En az bir' → 1 − hiç.", "Seçenekler arasında faktöriyel katları varsa sıra önemine bakın."],
    hatalar: ["Kombinasyon yerine permütasyon kullanmak.", "Tekrarlı harfleri bölmeyi unutmak.", "Dairesel sıralamada n! almak."],
    notlar: ["Sıra önemli → P; değil → C.", "Kısıtlı yer önce.", "En az bir → tümleyen."]
  },
  {
    id: "veri", area: "say", phase: 2, title: "Tablo ve Grafik Yorumlama", group: "E. Sayısal Mantık",
    subs: ["Tablo yorumlama", "Grafik yorumlama", "Yüzde ve oran hesabı", "Ortalama", "Değişim oranı"],
    kaz: ["Tablo ve grafikten veri okur.", "Parça–bütün yüzdesini hesaplar.", "Mutlak ve oransal değişimi ayırt eder.", "Senaryoya göre veriyi günceller."],
    tanim: "Bu sorular ortak bir veri seti (tablo ya da grafik) üzerinden 2–3 soru sorar. İncelenen örneklerde Sayısal Testi'nin 23–43. soruları 'aşağıdaki bilgilere göre' başlıklı ortak bilgi gruplarından oluşmaktadır.",
    kavramlar: [["Parça–bütün", "Parça / bütün · 100."], ["Artış oranı", "(yeni − eski) / eski."], ["Ortalama", "Toplam / adet."]],
    mantik: "Önce tablonun başlığı, birimi ve satır/sütun anlamı okunur; soruların hepsi aynı veriye dayandığı için ilk okumada ara toplamlar not edilir.",
    anlatim: [
      { h: "Veri okuma", p: "Birim (bin, %, adet) ve zaman aralığı ilk okunacak bilgilerdir. 'Toplam içindeki pay' ile 'değişim oranı' en sık karıştırılan iki kavramdır." },
      { h: "Mutlak ve oransal değişim", p: "40'tan 60'a çıkış +20 (mutlak) ve %50'dir (oransal). 100'den 130'a çıkış +30 ama %30'dur: mutlak artışı büyük olan oransal olarak küçük olabilir." },
      { h: "Tahmin ve yuvarlama", p: "Seçenekler birbirinden uzaksa yaklaşık hesap yeterlidir; yakınsa kesin hesap yapılır." }
    ],
    formuller: ["Pay = parça/bütün·100", "Değişim oranı = (yeni − eski)/eski", "Ortalama = toplam/n"],
    ornekler: [
      { q: "Bir şubenin satışı Ocak 80, Mart 120 ise artış oranı yüzde kaçtır?", steps: ["(120 − 80)/80 = 0,5."], a: "%50" }
    ],
    pratik: ["İlk soruda bulduğunuz toplamları kenara yazın; sonraki sorularda kullanılır.", "Grafikte ölçeğin sıfırdan başlayıp başlamadığına bakın.", "Yüzde sorularında tabanın ne olduğunu sorunun içinden çıkarın."],
    hatalar: ["Mutlak artışı oransal artış sanmak.", "Birimi (bin) gözden kaçırmak."],
    notlar: ["Önce birim ve başlık.", "Ara toplamları not et.", "Mutlak ≠ oransal."]
  },
  {
    id: "saymantik", area: "say", phase: 2, title: "Sayısal Mantık", group: "E. Sayısal Mantık",
    subs: ["Sayı dizileri", "Şekil dizileri", "Sayısal örüntüler", "İşlem tabloları", "Şifreleme", "Koşullu işlemler", "Kural tabanlı ortak bilgi", "Çok aşamalı mantık problemleri"],
    kaz: ["Dizideki örüntüyü bulur.", "Koşullu kuralı ardışık uygular.", "Kurala dayalı kodlama yapar.", "Kuraldan eşik değer çıkarır."],
    tanim: "Sayısal mantık, verilen bir kuralı ya da örüntüyü keşfetme ve uygulama becerisidir. Ortak bilgi gruplarında bir kural (ücret tarifesi, puanlama sistemi vb.) verilir ve birbirinden bağımsız sorular sorulur.",
    kavramlar: [["Aritmetik dizi", "Ardışık farkı sabit dizi."], ["Geometrik dizi", "Ardışık oranı sabit dizi."], ["İkinci fark", "Farkların farkı; sabitse dizi ikinci dereceden bir kurala uyar."]],
    mantik: "Dizilerde sırasıyla: farklar → oranlar → ikinci farklar → iç içe iki dizi → önceki iki terimle ilişki denenir. Kural sorularında kural, en uç durum (tavan, taban, eşik) üzerinden test edilir.",
    anlatim: [
      { h: "Sayı dizileri", p: "Farklar sabitse aritmetik; oranlar sabitse geometrik. Farklar düzenli artıyorsa ikinci farka bakılır. Tek ve çift sıralardaki terimler ayrı kurallara uyabilir." },
      { h: "Koşullu kurallar", p: "'Çiftse yarısı, tekse 3 katının 1 fazlası' gibi kurallarda her adım ayrı denetlenir; döngüye giren diziler sık görülür." },
      { h: "Kural tabanlı gruplar", p: "Tarife ya da puanlama kuralları bir kez dikkatle okunup küçük bir tablo hâline getirilir; 'en az kaç', 'en fazla kaç' sorularında eşik değer aranır." }
    ],
    formuller: ["aₙ = a₁ + (n − 1)d", "aₙ = a₁·rⁿ⁻¹"],
    ornekler: [
      { q: "2, 5, 11, 23, 47, ? dizisinde ? kaçtır?", steps: ["Her terim öncekinin 2 katının 1 fazlası: 47·2 + 1."], a: "95" }
    ],
    pratik: ["Farkları dizinin altına yazın.", "Kural sorusunda verilen örneği kuralla yeniden hesaplayarak kuralı doğru anladığınızı sınayın."],
    hatalar: ["Yalnızca ilk iki farka bakıp kural uydurmak.", "Tavan/taban sınırlarını unutmak."],
    notlar: ["Fark → oran → ikinci fark → iç içe.", "Kuralı tabloya çevir."]
  },
  {
    id: "geometri", area: "say", phase: 2, title: "Geometri", group: "F. Geometri",
    subs: ["Temel geometrik kavramlar", "Açılar", "Üçgenler", "Üçgende açı ve kenar ilişkileri", "Özel üçgenler", "Eşlik ve benzerlik", "Dörtgenler", "Kare ve dikdörtgen", "Paralelkenar", "Yamuk", "Çokgenler", "Çember ve daire", "Alan ve çevre", "Hacim", "Katı cisimler", "Analitik geometriye ilişkin temel sorular"],
    kaz: ["Üçgende iç ve dış açı özelliklerini uygular.", "Pisagor bağıntısını ve özel üçgenleri kullanır.", "Benzerlikte kenar ve alan oranlarını ilişkilendirir.", "Dörtgen, çokgen ve daire alanlarını hesaplar.", "Prizma ve silindir hacmini bulur.", "Analitik düzlemde uzaklık, orta nokta ve eğim hesaplar."],
    tanim: "İncelenen örnek kitapçıklarda Sayısal Testi'nin son yedi sorusu (44–50) geometri sorusudur; görünür örnekler açı ve alan sorularıdır.",
    kavramlar: [["Dış açı", "Komşu olmayan iki iç açının toplamı."], ["Benzerlik oranı", "Karşılıklı kenarların oranı k ise alanlar oranı k²."], ["π", "ALES sorularında genellikle π = 3 alınması istenir."]],
    mantik: "Şekil verilmemişse kaba bir şekil çizin. Her soruda önce bilinen açı/kenar şekle yazılır, sonra 'hangi özel durum var?' (ikizkenar, dik üçgen, paralellik) sorusu sorulur.",
    anlatim: [
      { h: "Açılar ve üçgenler", p: "İç açılar toplamı 180°, dış açılar toplamı 360°. İkizkenar üçgende taban açıları eşittir. B ve C iç açıortaylarının kesişim açısı 90° + A/2'dir." },
      { h: "Dik üçgen", p: "a² + b² = c². Sık kullanılan üçlüler: 3-4-5, 5-12-13, 8-15-17, 7-24-25 ve katları. Hipotenüse ait yükseklik h = ab/c." },
      { h: "Benzerlik", p: "DE ∥ BC ⇒ AD/AB = AE/AC = DE/BC. Alanlar oranı benzerlik oranının karesidir." },
      { h: "Dörtgenler ve çokgenler", p: "Yamuk alanı (a + c)h/2; paralelkenar alanı taban·yükseklik; karede alan köşegen²/2. n-genin iç açıları toplamı (n − 2)·180°; düzgün n-genin bir dış açısı 360°/n." },
      { h: "Daire ve katı cisimler", p: "Daire alanı πr², çevre 2πr, dilim alanı πr²·α/360. Prizma hacmi taban alanı·yükseklik; silindir πr²h." },
      { h: "Analitik geometri", p: "|AB| = √((x₂ − x₁)² + (y₂ − y₁)²); orta nokta ((x₁ + x₂)/2, (y₁ + y₂)/2); eğim (y₂ − y₁)/(x₂ − x₁); x/a + y/b = 1 doğrusu eksenlerle a·b/2 alanlı üçgen oluşturur." }
    ],
    formuller: ["İç açılar: 180° (üçgen), (n − 2)·180° (n-gen)", "a² + b² = c²", "Alan oranı = k²", "Yamuk: (a + c)h/2", "Daire: πr²; çevre: 2πr", "Silindir: πr²h"],
    ornekler: [
      { q: "Dik kenarları 6 ve 8 olan üçgenin hipotenüse ait yüksekliği?", steps: ["c = 10; h = 6·8/10."], a: "4,8" },
      { q: "DE ∥ BC, AD = 2, DB = 3, A(ADE) = 8 ise A(ABC)?", steps: ["k = 2/5 ⇒ alan oranı 4/25.", "A(ABC) = 8·25/4 = 50."], a: "50" }
    ],
    pratik: ["Pisagor üçlülerini ezberleyin; hesap süresini yarıya indirir.", "Alan sorularında aynı yüksekliğe sahip üçgenlerin alan oranı taban oranıdır.", "Açı sorularında bilinmeyen açıyı x deyip tüm açıları x cinsinden yazın."],
    hatalar: ["Benzerlikte alan oranını kenar oranı almak.", "Dış açıyı 180° − iç açı yerine yanlış iç açılarla ilişkilendirmek.", "π değeri istendiği gibi almamak."],
    notlar: ["3-4-5, 5-12-13, 8-15-17.", "Alan oranı = k².", "Dış açı = komşu olmayan iki iç açı."]
  },
  // ===================================================================== SÖZEL
  {
    id: "sozcuk", area: "soz", phase: 1, title: "Sözcükte Anlam ve Boşluk Doldurma", group: "A. Sözcükte Anlam",
    subs: ["Gerçek anlam", "Mecaz anlam", "Terim anlam", "Eş anlamlılık", "Zıt anlamlılık", "Yakın anlamlılık", "Sözcükler arası anlam ilişkileri", "Deyimler", "Boşluk doldurma"],
    kaz: ["Sözcüğün bağlamdaki anlamını belirler.", "Gerçek, mecaz ve terim anlamı ayırt eder.", "Sözcükler arasındaki anlam ilişkisini kurar.", "Boşluğu bağlamdaki ipuçlarından yararlanarak tamamlar."],
    tanim: "İncelenen örneklerde Sözel Testi 'cümledeki veya parçadaki boşluğu anlam bakımından en uygun biçimde tamamlayan seçeneği bulunuz' yönergeli beş soruyla (1–5) başlamaktadır. Bu sorular sözcüğün bağlam içindeki anlamını ölçer.",
    kavramlar: [["Gerçek anlam", "Sözcüğün akla gelen ilk, somut anlamı."], ["Mecaz anlam", "Gerçek anlamdan uzaklaşarak kazanılan anlam (soğuk karşılama)."], ["Terim anlam", "Bir bilim ya da sanat dalına özgü anlam (denklemin kökü)."], ["Deyim", "Kalıplaşmış, çoğunlukla mecazlı söz grubu."]],
    mantik: "Boşluk sorularında cevap, cümlenin kendi içindeki ipuçlarındadır: karşıtlık bağlaçları (ancak, oysa, değil … ), neden-sonuç bağları (çünkü, bu nedenle) ve boşluktan sonraki açıklama. Önce boşluğun olumlu mu olumsuz mu bir anlam istediğini belirleyin.",
    anlatim: [
      { h: "Bağlam ipuçları", p: "'… değil, … ' yapısı iki karşıt öğe ister. 'Çünkü' sonrası gelen açıklama, boşluğun nedenini ya da sonucunu verir. Noktalı virgülden sonraki cümle çoğu zaman boşluğu açıklar." },
      { h: "Çift boşluklu sorular", p: "Önce en güçlü ipucu olan boşluğu çözün ve seçenekleri eleyin; kalan seçeneklerde ikinci boşluğu deneyin." },
      { h: "Anlam ilişkileri", p: "Araç–işlev (makas–kesmek), parça–bütün (tuğla–duvar), neden–sonuç (kuraklık–kıtlık), karşıtlık (sıcak–soğuk), kişi–yer (doktor–hastane)." },
      { h: "Akademik söz varlığı", p: "ALES metinleri akademik konulardan (bilim, sanat, toplum) seçilir; 'bütüncül, öngörü, kuramsal, bağlam, olgu' gibi sözcüklerin anlamını bilmek zaman kazandırır." }
    ],
    formuller: ["İpucu sırası: bağlaç → noktalama → açıklayıcı cümle", "Olumlu/olumsuz yön tespiti"],
    ornekler: [
      { q: "'Yazar, karmaşık konuları ---- bir dille anlatarak geniş kitlelere ulaştı.' boşluğa ne gelir?", steps: ["Geniş kitlelere ulaşmak anlaşılırlığı gerektirir.", "'Yalın' uygun; 'ağdalı', 'süslü' uygun değil."], a: "yalın" }
    ],
    pratik: ["Seçenekleri okumadan önce boşluğa kendi sözcüğünüzü koyun.", "Çift boşlukta tek bir boşlukla eleme yapın.", "Altı çizili sözcükte cümleden çıkarılınca anlamın nasıl değiştiğini düşünün."],
    hatalar: ["Cümlenin genel havasına göre değil ipuçlarına göre karar vermemek.", "Yakın anlamlı ile eş anlamlıyı karıştırmak."],
    notlar: ["Karşıtlık bağlaçları en güçlü ipucudur.", "Önce yön (olumlu/olumsuz)."]
  },
  {
    id: "cumle", area: "soz", phase: 1, title: "Cümlede Anlam ve Kesin Çıkarım", group: "B. Cümlede Anlam",
    subs: ["Neden–sonuç", "Amaç–sonuç", "Koşul–sonuç", "Karşılaştırma", "Varsayım", "Çıkarım", "Örtülü anlam", "Öznel ve nesnel yargılar", "Kesin yargı", "Cümle yorumlama"],
    kaz: ["Cümledeki anlam ilişkilerini ayırt eder.", "Kesin çıkarım ile yorumu birbirinden ayırır.", "Öznel ve nesnel yargıyı ayırt eder.", "Örtülü anlam ve varsayımı bulur."],
    tanim: "İncelenen örneklerde 6–8. sorular 'başta verilen cümleden kesin olarak çıkarılabilecek yargıyı bulunuz' yönergesini taşır. Bu tür, cümlede açıkça bulunan bilgiyle yapılan yorumu ayırma becerisini ölçer.",
    kavramlar: [["Kesin çıkarım", "Cümle doğruysa kesinlikle doğru olan yargı."], ["Varsayım", "Bir yargının dayandığı, açıkça söylenmeyen öncül."], ["Örtülü anlam", "'Bile, da, yine' gibi sözcüklerle sezdirilen anlam."], ["Nesnel yargı", "Kanıtlanabilir, kişiden kişiye değişmeyen yargı."]],
    mantik: "Kesin çıkarım sorularında her seçenek için şu soru sorulur: 'Cümle doğru olsun; bu seçenek yanlış olabilir mi?' Yanlış olabiliyorsa elenir. 'Hepsi, hiç, tek nedeni, kesinlikle' gibi aşırı güçlü sözcükler çoğu zaman yanlış seçeneğin işaretidir.",
    anlatim: [
      { h: "Anlam ilişkileri", p: "Neden–sonuç: '-dığı için, nedeniyle' (gerçekleşmiş neden). Amaç–sonuç: '-mak için, amacıyla' (henüz gerçekleşmemiş hedef). Koşul–sonuç: '-sa/-se, takdirde'. Karşılaştırma: 'daha, kadar, gibi, en'." },
      { h: "Kesin çıkarım", p: "'Yarısından fazlası' = çoğunluk (ama hepsi değil). 'Son on yılın en düşük düzeyi' = son on yılda daha düşüğü yok. Zamanlama nedensellik değildir: 'ücret kaldırılınca ziyaretçi arttı' bilgisi artışın tek nedenini vermez." },
      { h: "Örtülü anlam", p: "'Bu yıl da en son o geldi' → daha önce de en son gelmiştir. 'Annem bile beğendi' → annesi kolay beğenmez." },
      { h: "Öznel–nesnel", p: "Ölçülebilir, sayılabilir, belgelenebilir bilgiler nesneldir. Beğeni, duygu, değerlendirme içeren yargılar öznel kabul edilir." }
    ],
    formuller: ["Kesin = cümle doğruyken yanlış olamaz", "Aşırı güçlü sözcük = şüphe"],
    ornekler: [
      { q: "'Kütüphane, sınav haftasında gece yarısına kadar açık kalacak.' Kesin çıkarım?", steps: ["Kütüphanenin sınav haftası dışındaki saatleri hakkında bilgi yok.", "Kesin: Sınav haftasında kütüphaneden gece yarısına kadar yararlanılabilir."], a: "Sınav haftasında gece yarısına kadar açıktır." }
    ],
    pratik: ["Her seçenekte 'cümlede bu bilgi var mı?' diye işaretleme yapın.", "Neden ile amacı ayırmak için 'gerçekleşti mi?' diye sorun."],
    hatalar: ["Mantıklı görünen ama cümlede olmayan yargıyı seçmek.", "Çoğunluğu 'hepsi' olarak genellemek.", "Birlikteliği nedensellik saymak."],
    notlar: ["Kesin ≠ mantıklı.", "Neden gerçekleşmiş; amaç hedef.", "'Bile', 'da' örtülü anlam taşır."]
  },
  {
    id: "yapi", area: "soz", phase: 1, title: "Paragraf Yapısı: Sıralama, Bütünlük, Tamamlama", group: "C. Paragraf",
    subs: ["Paragrafın yapısı", "Paragraf tamamlama", "Paragraf sıralama (yer değiştirme)", "Akışı bozan cümle", "Anlam bütünlüğü", "Söz dizimi / sıralama"],
    kaz: ["Gönderim öğelerini izleyerek cümle sırasını kurar.", "Paragrafın konusundan sapan cümleyi bulur.", "Boşluğa düşüncenin akışına uygun cümle getirir.", "Söz öbeklerini kurallı cümle düzenine yerleştirir."],
    tanim: "İncelenen örneklerde 13–15. sorular cümlelerin yer değiştirmesini, 16–18. sorular anlam bütünlüğünü bozan cümleyi, 9–12. sorular arasında da numaralı sözlerin sıralanmasını isteyen sorular bulunur.",
    kavramlar: [["Gönderim öğesi", "Önceki bir cümleye bağlanan sözcük: bu, böylece, bu nedenle, örneğin, ancak."], ["Giriş cümlesi", "Bağımsız, genel bir yargı; gönderim öğesiyle başlamaz."], ["Sonuç cümlesi", "Yargıyı toparlar: kısacası, bu yüzden, dolayısıyla."]],
    mantik: "Paragraf yapısı soruları anlamdan çok 'bağlantı' sorusudur. Her cümlenin ilk sözcüğü okunur: 'Bu, Böylece, Örneğin, Ne var ki' ile başlayan cümle paragrafı açamaz ve hangi cümleye bağlandığı bellidir.",
    anlatim: [
      { h: "Anlam bütünlüğünü bozan cümle", p: "Paragrafın konusu ilk iki cümleden belirlenir. Konudan sapan cümle genellikle aynı genel alanda (ör. kahve örneği verilmişken kahvenin tarihi) ama farklı bir konudadır. Çıkarıldığında kalan cümleler kesintisiz akmalıdır." },
      { h: "Yer değiştirme", p: "Gönderim öğesi taşıyan cümle, gönderdiği cümleden sonra gelmelidir. İki cümle yer değiştirdiğinde tüm 'bu, böylece' bağları doğru yerlere oturmalıdır." },
      { h: "Paragraf tamamlama", p: "Boşluktan önceki ve sonraki cümleler birlikte okunur. Sonraki cümle 'Bu durum, Örneğin' ile başlıyorsa boşluk o gönderimin hedefi olmalıdır." },
      { h: "Söz sıralama", p: "Türkçede yüklem sondadır; sıfat-fiil öbekleri nitelediği adın hemen önünde yer alır; 'yalnızca … değil … de' yapısı birlikte düşünülür." }
    ],
    formuller: ["Bu/Böylece/Örneğin ile başlayan cümle açılış olamaz", "Çıkarılınca akış kesintisiz olmalı"],
    ornekler: [
      { q: "'(I) Arılar tozlaşmayı sağlar. (II) Gıdanın önemli kısmı buna bağlıdır. (III) Bal tatlandırıcıdır. (IV) Bu nedenle arı kaybı gıda sorunudur.' Bozan cümle?", steps: ["Konu: tozlaşma–gıda güvenliği.", "III balın kullanımına geçer; IV'teki 'Bu nedenle' II'ye bağlanır."], a: "III" }
    ],
    pratik: ["Cümlelerin yalnızca ilk sözcüklerini okuyarak bağlantı haritası çıkarın.", "Bozan cümle sorusunda şüpheli cümleyi çıkarıp paragrafı yeniden okuyun."],
    hatalar: ["Genel konuyla ilgili ama paragrafın özel konusundan sapan cümleyi kaçırmak.", "Gönderim öğesinin hedefini kontrol etmemek."],
    notlar: ["İlk sözcük = bağlantı ipucu.", "Konu ilk iki cümlede."]
  },
  {
    id: "paragraf", area: "soz", phase: 1, title: "Paragrafta Anlam", group: "C. Paragraf",
    subs: ["Ana düşünce", "Yardımcı düşünce", "Konu ve başlık", "Çıkarım", "Yazarın tutumu", "Metin yorumlama", "Çoklu paragraf soruları", "Uzun metin analizi"],
    kaz: ["Paragrafın ana düşüncesini belirler.", "Parçada değinilen ve değinilmeyen bilgileri ayırır.", "Metinden geçerli çıkarım yapar.", "Yazarın tutumunu ve eleştirdiği görüşü belirler.", "Uzun metinlerde birden çok soruyu aynı okumayla yanıtlar."],
    tanim: "İncelenen örneklerde Sözel Testi'nin 19–42. soruları paragraf sorularıdır (tekil paragraflar ve aynı parçaya bağlı 2–4 soruluk gruplar); bu, testin yaklaşık yarısıdır.",
    kavramlar: [["Ana düşünce", "Yazarın okura iletmek istediği temel yargı."], ["Yardımcı düşünce", "Ana düşünceyi destekleyen ayrıntılar."], ["Çıkarım", "Metindeki bilgilerden zorunlu ya da güçlü biçimde ulaşılan yargı."], ["Tutum", "Yazarın konu karşısındaki yaklaşımı (eleştirel, destekleyici, nesnel…)."]],
    mantik: "Ana düşünce çoğunlukla giriş ya da sonuç cümlesindedir; 'oysa, ancak, bu nedenle, asıl' sözcükleri ana yargıyı işaret eder. Seçeneklerde metnin tamamını kapsamayan (dar) ya da metni aşan (geniş, aşırı genelleme) yargılar elenir.",
    anlatim: [
      { h: "Ana düşünce", p: "Ana düşünce metnin tamamını kapsar, tek bir örnek değildir. 'Oysa' sonrası çoğu zaman yazarın asıl görüşüdür; öncesi yaygın görüş olabilir." },
      { h: "Değinilmeyen bilgi", p: "Seçenekleri metinle tek tek eşleştirin; metinde karşılığı olan dört seçeneği işaretleyin. Karşılığı olmayan seçenek, mantıklı görünse bile cevaptır." },
      { h: "Çıkarım", p: "Çıkarım metnin söylediğini aşamaz. 'Çoğu zaman daha değerli' ifadesinden 'değersizdir' çıkarılamaz. Gözlemden kesin nedensellik çıkarılamaz." },
      { h: "Uzun metin", p: "Önce soruları okuyun; sonra metni bir kez, soruların aradığı bilgileri işaretleyerek okuyun. Her paragrafın işlevini (tanım, sorun, neden, çözüm) not edin." }
    ],
    formuller: ["Ana düşünce = metnin tamamı", "Dar ve aşırı geniş seçenekleri ele", "Oysa/ancak sonrası = yazarın görüşü"],
    ornekler: [
      { q: "'Yetenek önemlidir ama tek başına yetmez; disiplinli çalışanlar zamanla daha ileri gider.' Ana düşünce?", steps: ["Metin yeteneği yadsımıyor, disiplinin önemini vurguluyor.", "'Yetenek gereksizdir' aşırı genellemedir."], a: "Başarıda disiplin belirleyicidir." }
    ],
    pratik: ["Her paragrafın sonuna tek cümlelik özet yazma alışkanlığı edinin.", "'Hepsi, asla, kesinlikle, tek' içeren seçenekleri iki kez kontrol edin.", "Günde en az 10 paragraf sorusu çözerek okuma hızınızı ölçün."],
    hatalar: ["Metindeki tek bir örneği ana düşünce sanmak.", "Kendi bilgisiyle metne bilgi eklemek.", "Yazarın aktardığı karşı görüşü yazarın görüşü sanmak."],
    notlar: ["Giriş/sonuç cümlesine bak.", "Metni aşma.", "Oysa = yazar konuşuyor."]
  },
  {
    id: "sozmantik", area: "soz", phase: 2, title: "Sözel Mantık", group: "D. Sözel Mantık",
    subs: ["Sıralama", "Eşleştirme", "Gruplandırma", "Yerleştirme", "Koşullu önermeler", "Tablo oluşturma", "Kısıt ve ilişki analizi", "Birden fazla koşulu değerlendirme", "Mantıksal çıkarım", "Koşullu çıkarım"],
    kaz: ["Bilgileri tabloya dönüştürür.", "Kesin bilgiden başlayarak olasılıkları daraltır.", "'Kesinlikle doğru', 'olamaz', 'olabilir' ayrımını yapar.", "Ek koşulla çözüm kümesini daraltır."],
    tanim: "İncelenen örneklerde Sözel Testi'nin son sekiz sorusu (43–50) 'aşağıdaki bilgilere göre birbirinden bağımsız olarak' cevaplanan iki dörtlü gruptan oluşmaktadır. Bu bloğun görünür örneği bulunmadığından alt türler doğrulanmamıştır; platformdaki sorular sıralama, eşleştirme ve gruplama türlerinde özgün olarak hazırlanmıştır.",
    kavramlar: [["Kesin bilgi", "Tek bir duruma izin veren bilgi (A Salı günü)."], ["Kısıt", "Olasılıkları eleyen bilgi (A Salı günü değil)."], ["Koşullu önerme", "'A ise B': A doğruysa B doğrudur; A yanlışsa B hakkında bilgi yoktur."], ["Bağımsız soru", "Sorudaki ek bilgi yalnızca o soru için geçerlidir."]],
    mantik: "Her grupta tablo kurmak zorunludur. Önce kesin bilgiler, sonra en kısıtlayıcı ilişkiler (hemen önce, yan yana) yerleştirilir. Olasılık sayısı az kalınca tüm durumlar listelenir ve sorular bu listeden yanıtlanır.",
    anlatim: [
      { h: "Tablo kurma", p: "Sıralamada kişiler × günler, eşleştirmede kişiler × iller tablosu kurulur. ✓ kesin, ✗ olanaksız anlamına gelir. Bir satırda tek boş kalırsa orası ✓ olur." },
      { h: "Soru türleri", p: "'Kesinlikle doğrudur': tüm olası durumlarda doğru. 'Olamaz': hiçbir durumda doğru değil. 'Olabilir': en az bir durumda doğru. 'X ise …': önce X'i sağlayan durumlar seçilir, soru onlarla yanıtlanır." },
      { h: "Koşullu önermeler", p: "'A, İzmir'e gittiyse B Konya'ya gitmiştir' önermesinin karşıt tersi: 'B Konya'ya gitmediyse A İzmir'e gitmemiştir.' Ters ('B Konya'ya gittiyse A İzmir'e gitmiştir') geçerli değildir." },
      { h: "Zaman yönetimi", p: "Bir grubun tablosunu kurmak 2–3 dakika alır ama dört soruyu birlikte hızlandırır. Tabloyu kurmadan soru çözmeye çalışmak zaman kaybettirir." }
    ],
    formuller: ["A ⇒ B ≡ ¬B ⇒ ¬A", "Kesin: tüm durumlarda; Olabilir: en az birinde; Olamaz: hiçbirinde"],
    ornekler: [
      { q: "A, B, C üç gün (1–3) sunum yapıyor. A 1. gün değil; B, C'den hemen önce. Kaç sıralama vardır?", steps: ["B–C bloğu (1–2) ya da (2–3).", "(1–2) ise A 3. gün; (2–3) ise A 1. gün olur ama A 1. gün olamaz.", "Tek sıralama: B, C, A."], a: "1" }
    ],
    pratik: ["Tabloyu kurşun kalemle hızlıca çizin; seçenekleri tabloya göre işaretleyin.", "'Hemen önce/sonra' gibi blok bilgilerini önce yerleştirin.", "Ek koşullu sorularda ana tabloyu bozmayın, yanına küçük bir kopya çizin."],
    hatalar: ["Bir sorunun ek koşulunu sonraki sorulara taşımak.", "'Olabilir' ile 'kesinlikle' ayrımını karıştırmak.", "Koşullu önermenin tersini doğru saymak."],
    notlar: ["Önce tablo.", "Kesin → blok → kısıt.", "Ek koşul yalnızca o soruya aittir."]
  }
];

/* ÖSYM kılavuzunun belirttiği iki testin, incelenen örneklerdeki blok düzeni */
window.EXAM_BLUEPRINT = {
  say: [
    { from: 1, to: 22, label: "Temel matematik ve problemler", topics: ["temel", "bolunebilme", "rasyonel", "esitsizlik", "uslu", "cebir", "oran", "problem", "islem", "sayma"], mode: "single" },
    { from: 23, to: 43, label: "Ortak bilgiye dayalı gruplar", topics: ["veri", "saymantik"], mode: "group" },
    { from: 44, to: 50, label: "Geometri", topics: ["geometri"], mode: "single" }
  ],
  soz: [
    { from: 1, to: 5, label: "Boşluk doldurma", topics: ["sozcuk"], mode: "single" },
    { from: 6, to: 8, label: "Kesin çıkarım", topics: ["cumle"], subs: ["Kesin çıkarım"], mode: "single" },
    { from: 9, to: 12, label: "Cümle ve sözcük", topics: ["cumle", "yapi", "sozcuk"], mode: "single" },
    { from: 13, to: 15, label: "Cümle yer değiştirme", topics: ["yapi"], subs: ["Cümle yer değiştirme"], mode: "single" },
    { from: 16, to: 18, label: "Anlam bütünlüğü", topics: ["yapi"], subs: ["Anlam bütünlüğünü bozan cümle"], mode: "single" },
    { from: 19, to: 42, label: "Paragraf", topics: ["paragraf", "yapi"], mode: "mixed" },
    { from: 43, to: 50, label: "Sözel mantık", topics: ["sozmantik"], mode: "group" }
  ]
};
