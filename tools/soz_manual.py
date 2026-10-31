"""Elle yazılmış özgün sözel sorular.

Her öğe: M(topic, sub, level, soru, doğru, [4 yanlış], çözüm, kazanım, süre, group)
Doğru seçenek derleme sırasında rastgele (ama sabit tohumla) bir konuma yerleştirilir.
"""


def M(topic, sub, level, q, correct, wrongs, sol, kaz, sure=60, group=None):
    assert len(wrongs) == 4 and correct not in wrongs
    return dict(topic=topic, sub=sub, level=level, q=q, correct=correct, wrongs=wrongs, sol=sol, kaz=kaz, sure=sure, group=group)


B = "<br>"
ROMAN = ["I", "II", "III", "IV", "V"]


def para(sentences):
    return " ".join(f"({ROMAN[i]}) {s}" for i, s in enumerate(sentences))


def roman_opts(correct_idx, pool=None):
    pool = pool or ROMAN
    c = pool[correct_idx]
    return c, [r for r in pool if r != c]


ITEMS = []
A = ITEMS.append

# ============================================================ SÖZCÜKTE ANLAM / BOŞLUK DOLDURMA
SZ = "sozcuk"
BLANK = "Bu cümlede boş bırakılan yere aşağıdakilerden hangisi getirilmelidir?"
BLANK2 = "Bu cümlede boş bırakılan yerlere aşağıdakilerden hangileri sırasıyla getirilmelidir?"

A(M(SZ, "Boşluk doldurma", 3, "Bilimsel bir kuramın değeri yalnızca açıkladığı olgularla değil, ---- olgularla da ölçülür; yanlışlanabilir öngörülerde bulunmayan bir kuram, ne kadar kapsayıcı görünürse görünsün sınanamaz." + B + BLANK,
    "öngördüğü", ["görmezden geldiği", "reddettiği", "ezberlediği", "unuttuğu"],
    ["Cümlenin ikinci yarısı 'öngörülerde bulunmayan kuram sınanamaz' diyor; demek ki ölçüt, kuramın önceden kestirdiği olgulardır.", "'öngördüğü' sözcüğü bu yargıyla doğrudan uyumludur; diğerleri kuramın değerini artıran bir işlev anlatmaz."],
    "Bağlamdaki ipucundan (öngörü) yararlanarak uygun sözcüğü seçer."))
A(M(SZ, "Boşluk doldurma", 3, "Kentlerin belleği yalnızca anıtlarda değil, gündelik hayatın ---- izlerinde saklıdır; bu izler silindiğinde kent, ---- bir dekora dönüşür." + B + BLANK2,
    "sıradan – ruhsuz", ["görkemli – canlı", "yapay – özgün", "kalıcı – zengin", "belirgin – tarihî"],
    ["İlk boşluk, 'anıtlar' ile karşıtlık kuruyor: anıtların karşıtı gündelik hayatın sıradan izleridir.", "İzler silindiğinde kentin olumsuz bir duruma düşmesi beklenir: 'ruhsuz bir dekor'. Diğer çiftlerde ikinci sözcük olumlu anlamlıdır ya da ilk sözcük karşıtlığı kurmaz."],
    "Karşıtlık ve sonuç ilişkisini kullanarak sözcük çiftini belirler."))
A(M(SZ, "Boşluk doldurma", 2, "Yazarın üslubu, karmaşık düşünceleri ---- bir dille aktarmasıyla öne çıkar; okur, metnin derinliğini yorulmadan kavrar." + B + BLANK,
    "yalın", ["ağdalı", "süslü", "kapalı", "dolambaçlı"],
    ["'Okur yorulmadan kavrar' ifadesi, dilin anlaşılır ve sade olduğunu gösterir.", "'Yalın' bu anlamı karşılar; diğer seçenekler anlaşılmayı zorlaştıran nitelikler bildirir."],
    "Sonuç cümlesinden hareketle sıfatın anlamını belirler.", 45))
A(M(SZ, "Boşluk doldurma", 2, "Deneyimli bir hekim, hastanın anlattıklarının yanı sıra ---- belirtilere de dikkat eder; çünkü bazı hastalıklar kendini ancak küçük ayrıntılarla ele verir." + B + BLANK,
    "gözden kaçabilecek", ["herkesin bildiği", "hastanın abarttığı", "tedavi edilmiş", "kesinleşmiş"],
    ["Gerekçe cümlesi 'küçük ayrıntılar'dan söz ediyor.", "Küçük ayrıntılar kolayca fark edilmeyen, 'gözden kaçabilecek' belirtilerdir."],
    "Gerekçe bildiren cümleyi boşlukla ilişkilendirir.", 45))
A(M(SZ, "Boşluk doldurma", 3, "Sanatçı, eserlerinde geleneği körü körüne ---- da ondan tümüyle ---- da; geleneği yeniden yorumlayarak kendine özgü bir dil kurar." + B + BLANK2,
    "tekrarlamaz – kopmaz", ["benimser – etkilenir", "yüceltir – beslenir", "eleştirir – yararlanır", "reddetmez – uzaklaşmaz"],
    ["'Yeniden yorumlamak', geleneği ne olduğu gibi tekrar etmek ne de ondan bütünüyle ayrılmak demektir.", "Bu iki uç, 'tekrarlamaz – kopmaz' çiftiyle karşılanır. 'Reddetmez – uzaklaşmaz' çifti, 'körü körüne' ifadesiyle anlamca uyuşmaz."],
    "İki uç arasındaki orta yolu anlatan yapıyı çözümler."))
A(M(SZ, "Sözcükte anlam", 2, "Bu romanda yazar, kahramanın iç dünyasındaki <u>kırılmaları</u> ustalıkla yansıtıyor." + B + "Bu cümlede altı çizili sözcüğün anlamı aşağıdakilerden hangisidir?",
    "Duygu ve düşüncelerde yaşanan sarsıcı değişimler", ["Bir nesnenin parçalara ayrılması", "Işığın bir ortamdan ötekine geçerken yön değiştirmesi", "Fiyatların belirgin biçimde düşmesi", "İki kişi arasındaki ilişkinin sona ermesi"],
    ["'İç dünya' ifadesi sözcüğün mecaz anlamda, ruhsal bir değişimi anlatmak için kullanıldığını gösterir."],
    "Bağlama göre sözcüğün mecaz anlamını belirler.", 40))
A(M(SZ, "Gerçek ve mecaz anlam", 2, "Aşağıdaki cümlelerin hangisinde altı çizili sözcük <b>mecaz</b> anlamda kullanılmıştır?",
    "Ondan gördüğümüz <u>soğuk</u> karşılama hepimizi şaşırttı.", ["Masanın üzerindeki <u>ağır</u> kutuyu birlikte kaldırdık.", "Bahçedeki <u>kuru</u> yaprakları topladık.", "Fırından yeni çıkan <u>sıcak</u> ekmeği dilimledi.", "Derenin <u>derin</u> yerlerinde yüzmek yasaktı."],
    ["'Soğuk karşılama', sıcaklıkla değil ilgisizlik ve mesafeyle ilgilidir; sözcük mecazdır.", "Diğer cümlelerde sözcükler somut, ölçülebilir özellikleri (ağırlık, nem, sıcaklık, derinlik) bildirir."],
    "Gerçek ve mecaz anlamı ayırt eder.", 45))
A(M(SZ, "Terim anlam", 2, "Aşağıdaki cümlelerin hangisinde altı çizili sözcük <b>terim</b> anlamıyla kullanılmıştır?",
    "Bu denklemin <u>kökleri</u> birbirine eşittir.", ["Ağacın <u>kökleri</u> kaldırımı kırmış.", "Bu geleneğin <u>kökleri</u> çok eskiye dayanır.", "Sorunun <u>kökü</u> yanlış planlamadaydı.", "Bahçedeki otları <u>kökünden</u> söktük."],
    ["'Denklemin kökü', matematik alanına özgü bir kavramdır: denklemi sağlayan değer.", "Diğerlerinde sözcük gerçek (bitki kökü) ya da mecaz (kaynak, temel) anlamdadır."],
    "Terim anlamı gerçek ve mecaz anlamdan ayırır.", 45))
A(M(SZ, "Eş anlamlılık", 2, "Aşağıdaki cümlelerin hangisinde altı çizili sözcüğün yerine ayraç içindeki sözcük getirilirse cümlenin anlamı <b>değişmez</b>?",
    "Bu konuda henüz <u>kesin</u> bir karar verilmedi. (kati)", ["Yolun <u>sonunda</u> küçük bir köy göründü. (amacında)", "Sınav <u>sonuçları</u> bugün açıklandı. (nedenleri)", "Bu <u>sorun</u> bir an önce çözülmeli. (soru)", "Bugün hava biraz <u>serin</u>. (soğuk)"],
    ["'Kesin' ile 'kati' eş anlamlıdır.", "'Serin' ile 'soğuk' yakın anlamlıdır ama derece farkı taşır; diğer çiftler farklı anlamlardadır."],
    "Eş ve yakın anlamlı sözcükleri ayırt eder.", 45))
A(M(SZ, "Zıt anlamlılık", 1, "Aşağıdaki cümlelerin hangisinde <b>zıt anlamlı</b> sözcükler bir arada kullanılmıştır?",
    "Kazancı da kaybı da onu aynı ölçüde düşündürüyordu.", ["Yolculuğun sonunda yorgun ve bitkin düşmüştü.", "Dar ve uzun bir sokaktan geçtik.", "Hızlı ama dikkatli bir sürücüydü.", "Güzel ve anlamlı bir konuşma yaptı."],
    ["'Kazanç' ile 'kayıp' karşıt kavramlardır.", "'Yorgun – bitkin' yakın anlamlı; diğer çiftler ise karşıtlık bildirmez."],
    "Zıt anlam ilişkisini tanır.", 40))
A(M(SZ, "Boşluk doldurma", 2, "Araştırmacılar, verilerin ---- olduğunu fark edince sonuçları yayımlamaktan vazgeçtiler; çünkü ölçüm aletlerinden biri hatalı çalışıyordu." + B + BLANK,
    "güvenilmez", ["tutarlı", "kapsamlı", "güncel", "anlamlı"],
    ["Hatalı çalışan bir ölçüm aleti verilerin güvenilirliğini ortadan kaldırır.", "Yayımlamaktan vazgeçme kararı da olumsuz bir niteliği gerektirir: 'güvenilmez'."],
    "Gerekçeden yola çıkarak olumsuz niteleme seçer.", 40))
A(M(SZ, "Boşluk doldurma", 3, "Bilgiye erişimin kolaylaşması, ---- bilgi ile ---- bilgi arasındaki ayrımı yapmayı zorlaştırdı." + B + BLANK2,
    "güvenilir – kulaktan dolma", ["yeni – güncel", "yerel – ulusal", "kısa – uzun", "yazılı – basılı"],
    ["'Ayrımı yapmayı zorlaştırmak' iki karşıt niteliği gerektirir; erişimin kolaylaşmasının yarattığı sorun, doğru ile doğrulanmamış bilginin ayırt edilmesidir.", "Bu karşıtlığı yalnızca 'güvenilir – kulaktan dolma' çifti kurar."],
    "Karşıtlık kuran sözcük çiftini bağlama göre seçer.", 50))
A(M(SZ, "Boşluk doldurma", 3, "Eleştirmen, romanın kurgusundaki ---- dikkat çekerek olayların birbirine inandırıcı biçimde bağlanmadığını belirtti." + B + BLANK,
    "boşluklara", ["zenginliğe", "özgünlüğe", "akıcılığa", "derinliğe"],
    ["Eleştirmenin vurguladığı şey olumsuzdur: olaylar inandırıcı biçimde bağlanmıyor.", "Bu olumsuzluğu 'boşluklar' karşılar; diğer seçenekler olumlu niteliklerdir."],
    "Olumsuz yargıyla uyumlu sözcüğü seçer.", 40))
A(M(SZ, "Boşluk doldurma", 2, "Müzenin yeni sergisi, ziyaretçileri yalnızca izleyici olmaktan çıkarıp sürecin ---- dönüştürmeyi amaçlıyor." + B + BLANK,
    "etkin bir parçasına", ["uzak bir tanığına", "sessiz bir seyircisine", "dışında kalan birine", "yorgun bir takipçisine"],
    ["'Yalnızca izleyici olmaktan çıkarmak', pasif konumun karşıtına geçişi anlatır.", "Pasifliğin karşıtı 'etkin bir parça' olmaktır; diğer seçenekler yine edilgen konumları anlatır."],
    "Karşıtlık ilişkisinden hareketle boşluğu tamamlar.", 40))
A(M(SZ, "Boşluk doldurma", 2, "Göç, yalnızca bir yerden bir yere taşınmak değil, aynı zamanda alışılmış olanla ---- ve yeni olana uyum sağlama sürecidir." + B + BLANK,
    "vedalaşma", ["yarışma", "buluşma", "yetinme", "övünme"],
    ["Cümle iki yönlü bir süreç anlatıyor: eskiden ayrılma ve yeniye uyum.", "'Alışılmış olanla vedalaşma' bu ayrılmayı karşılar."],
    "Paralel yapıdaki anlam ilişkisini kurar.", 40))
A(M(SZ, "Deyimler", 2, "Yönetici, gelen eleştirilere rağmen yeni planı uygulamayı <u>göze aldı</u>." + B + "Bu cümlede altı çizili sözün anlamı aşağıdakilerden hangisidir?",
    "Olası olumsuz sonuçları kabullenerek bir işe girişmek", ["Bir konuyu dikkatle incelemek", "Bir işi başkasına devretmek", "Bir kararı ileri bir tarihe ertelemek", "Bir işi kimseye duyurmadan yürütmek"],
    ["'Eleştirilere rağmen' ifadesi riskin bilindiğini gösterir.", "'Göze almak' deyimi tam olarak riski üstlenerek harekete geçmeyi anlatır."],
    "Deyimin bağlamdaki anlamını belirler.", 40))
A(M(SZ, "Sözcükler arası ilişki", 2, "Aşağıdaki sözcük çiftlerinden hangisinde, 'kalem – yazmak' çifti arasındaki anlam ilişkisinin benzeri vardır?",
    "makas – kesmek", ["kitap – kütüphane", "öğretmen – öğrenci", "ağaç – orman", "bulut – yağmur"],
    ["Kalem bir araçtır, yazmak onun işlevidir (araç – işlev).", "Aynı ilişki yalnızca 'makas – kesmek' çiftinde vardır; diğerleri yer, karşılıklı rol, parça–bütün ve neden–sonuç ilişkileridir."],
    "Sözcükler arasındaki ilişki türünü belirler.", 40))
A(M(SZ, "Sözcükler arası ilişki", 2, "Aşağıdaki sözcük çiftlerinden hangisinde, 'damla – deniz' çifti arasındaki anlam ilişkisinin benzeri vardır?",
    "tuğla – duvar", ["çekiç – çivi", "doktor – hastane", "sıcak – soğuk", "kuraklık – kıtlık"],
    ["Damla, denizi oluşturan küçük birimdir (parça – bütün).", "Tuğla da duvarı oluşturan birimdir; diğer çiftler araç–nesne, kişi–yer, karşıtlık ve neden–sonuç ilişkisi taşır."],
    "Parça–bütün ilişkisini tanır.", 40))
A(M(SZ, "Boşluk doldurma", 2, "Uzmanlara göre çocukların dil gelişimi, çevrelerinde duydukları sözcüklerin ---- yakından ilişkilidir; zengin bir söz varlığıyla büyüyen çocuk kendini daha rahat ifade eder." + B + BLANK,
    "çeşitliliğiyle", ["tekdüzeliğiyle", "azlığıyla", "yazımıyla", "kökeniyle"],
    ["İkinci cümle 'zengin söz varlığı'ndan söz ediyor; bu, sözcüklerin çeşitliliğine karşılık gelir."],
    "Açıklayıcı cümleyle boşluk arasında bağ kurar.", 40))
A(M(SZ, "Boşluk doldurma", 3, "Bu çalışma, konuyu ---- ele aldığı için alandaki dağınık bilgileri bir araya getiren temel bir başvuru kaynağı olmuştur." + B + BLANK,
    "bütüncül bir bakışla", ["yüzeysel biçimde", "tek bir açıdan", "alışılmış kalıplarla", "kişisel kaygılarla"],
    ["'Dağınık bilgileri bir araya getirmek', konuyu bütün yönleriyle ele almayı gerektirir.", "'Bütüncül bir bakış' bu sonucun nedeni olabilecek tek seçenektir."],
    "Neden–sonuç ilişkisini sözcük seçimine yansıtır.", 45))
A(M(SZ, "Boşluk doldurma", 3, "Eski fotoğraflar geçmişe ---- bir pencere sunar; ancak bu pencere, fotoğrafçının seçtiği açıyla ---- olduğundan gerçeğin yalnızca bir kısmını gösterir." + B + BLANK2,
    "aralanan – sınırlı", ["kapanan – geniş", "süslenen – özgür", "unutulan – sabit", "değişen – eksiksiz"],
    ["'Pencere sunar' olumlu bir işlev bildirir: geçmişe aralanan bir pencere.", "'Ancak … gerçeğin yalnızca bir kısmını gösterir' sınırlılık anlatır: 'sınırlı'."],
    "Ancak bağlacının kurduğu karşıtlığı çözümler.", 50))
A(M(SZ, "Çok anlamlılık", 2, "Aşağıdaki cümlelerin hangisinde 'açmak' sözcüğü 'başlatmak' anlamında kullanılmıştır?",
    "Moderatör, oturumu kısa bir konuşmayla açtı.", ["Pencereyi açınca içeri serin bir hava doldu.", "Bu kırıcı sözler aramızda yeni bir yara açtı.", "Öğleden sonra hava açınca dışarı çıktık.", "Bahçedeki güller bu yıl erken açtı."],
    ["'Oturumu açmak', oturumu başlatmak demektir.", "Diğerlerinde sözcük 'aralamak', 'oluşturmak', 'havanın aydınlanması' ve 'çiçeklenmek' anlamlarındadır."],
    "Çok anlamlı sözcüğün bağlamdaki anlamını belirler.", 45))
A(M(SZ, "Çok anlamlılık", 2, "Aşağıdaki cümlelerin hangisinde 'ağır' sözcüğü 'ciddi, tehlikeli' anlamında kullanılmıştır?",
    "Kaza sonucunda iki kişi ağır yaralandı.", ["Yaşlı adam ağır adımlarla yürüyordu.", "Bu kutu tek kişinin taşıyamayacağı kadar ağır.", "Odaya ağır bir parfüm kokusu sinmişti.", "Akşam yediğimiz yemek biraz ağırdı."],
    ["'Ağır yaralanmak', yaralanmanın ciddi olduğunu anlatır.", "Diğerlerinde 'yavaş', 'kütlesi fazla', 'yoğun' ve 'sindirimi güç' anlamları vardır."],
    "Çok anlamlı sözcüğün anlam ayrımını yapar.", 45))
A(M(SZ, "Boşluk doldurma", 1, "Başarılı bir çeviri, kaynak metne ---- kalırken hedef dilin doğallığını da korur." + B + BLANK,
    "sadık", ["yabancı", "kayıtsız", "düşman", "uzak"],
    ["'Kalırken … da korur' yapısı iki olumlu niteliği birleştirir; kaynak metne bağlılık 'sadık kalmak' ile anlatılır."],
    "Kalıplaşmış sözcük birlikteliklerini tanır.", 30))
A(M(SZ, "Boşluk doldurma", 2, "Küresel ısınmanın etkileri artık bilim insanlarının öngörüsü olmaktan çıkmış, gündelik yaşamda ---- bir gerçeğe dönüşmüştür." + B + BLANK,
    "doğrudan hissedilen", ["henüz kanıtlanmamış", "yalnızca kuramsal", "uzak geleceğe ait", "tartışmaya açık"],
    ["'Öngörü olmaktan çıkmak' soyut olandan somuta geçişi anlatır.", "Gündelik yaşamda somutlaşan gerçek 'doğrudan hissedilen' bir gerçektir; diğer seçenekler öngörü düzeyinde kalmayı anlatır."],
    "Durum değişikliğini anlatan yapıyı çözümler.", 40))
A(M(SZ, "Boşluk doldurma", 3, "Pek çok buluş, uzun ve ---- bir çalışmanın değil, beklenmedik bir ---- ürünü olarak ortaya çıkmıştır." + B + BLANK2,
    "planlı – rastlantının", ["dağınık – düzenin", "kısa – sabrın", "sıradan – alışkanlığın", "ortak – tekrarın"],
    ["'… değil, …' yapısı karşıtlık kurar: uzun ve planlı çalışma ile beklenmedik rastlantı.", "Bu karşıtlığı yalnızca 'planlı – rastlantının' çifti sağlar."],
    "'Değil' yapısıyla kurulan karşıtlığı çözer.", 50))
A(M(SZ, "Yakın anlamlılık", 1, "Aşağıdaki cümlelerin hangisinde <b>yakın anlamlı</b> sözcükler birlikte kullanılmıştır?",
    "Uzun bir yürüyüşün ardından yorgun ve halsiz eve döndü.", ["Haberi alınca hem sevinçli hem üzgündü.", "Çantasına kitabını ve defterini koydu.", "Toplantıya yaşlı genç herkes katıldı.", "Hızlı ama özensiz bir çalışma yapmıştı."],
    ["'Yorgun' ve 'halsiz' aynı duruma yakın anlamlar taşır.", "'Sevinçli – üzgün' ile 'yaşlı – genç' zıt anlamlıdır; diğerlerinde anlam ilişkisi yoktur."],
    "Yakın ve zıt anlamı ayırt eder.", 40))
A(M(SZ, "Boşluk doldurma", 2, "Bilim tarihi, bir dönemin ---- kabul edilen düşüncelerinin sonraki dönemlerde nasıl sorgulandığının örnekleriyle doludur." + B + BLANK,
    "tartışılmaz", ["geçersiz", "unutulmuş", "yasaklanmış", "gülünç"],
    ["Sorgulanmanın vurgu kazanması için düşüncelerin daha önce kesin doğru sayılmış olması gerekir: 'tartışılmaz'."],
    "Zaman içindeki karşıtlığı sezer.", 40))
A(M(SZ, "Boşluk doldurma", 4, "Şair, doğayı anlatırken ---- betimlemelerden kaçınıp okurun hayal gücüne alan bırakan ---- imgeler kullanır." + B + BLANK2,
    "her şeyi söyleyen – çağrışımı güçlü", ["kapalı – açık seçik", "yalın – karmaşık", "çağrışımı güçlü – sıradan", "kısa – uzun"],
    ["Okurun hayal gücüne alan bırakmak, her şeyi açıkça söylememekle olur; kaçınılan şey 'her şeyi söyleyen' betimlemelerdir.", "Hayal gücünü harekete geçiren imgeler 'çağrışımı güçlü' imgelerdir."],
    "İki boşluk arasındaki karşıtlığı ve amacı birlikte değerlendirir.", 60))
A(M(SZ, "Boşluk doldurma", 2, "Ekonomik krizler toplumun en ---- kesimlerini daha derinden etkiler; bu nedenle sosyal politikalar öncelikle bu kesimleri korumalıdır." + B + BLANK,
    "kırılgan", ["varlıklı", "ayrıcalıklı", "dirençli", "güçlü"],
    ["Krizden 'daha derinden etkilenen' ve 'korunması gereken' kesimler, dayanıklılığı düşük olanlardır: 'kırılgan'."],
    "Sonuç cümlesiyle uyumlu niteleme seçer.", 35))

# ============================================================ CÜMLEDE ANLAM
CM = "cumle"
KESIN = "Bu cümleden aşağıdaki yargılardan hangisi <b>kesin olarak</b> çıkarılabilir?"

A(M(CM, "Kesin çıkarım", 3, "Kentteki bisiklet yollarının uzunluğu son beş yılda iki katına çıkmış olsa da bu yolları kullananların sayısındaki artış, beklenenin oldukça altında kalmıştır." + B + KESIN,
    "Bisiklet yollarındaki artış, kullanıcı sayısını beklenen ölçüde artırmamıştır.", ["Kentte bisiklet kullananların sayısı azalmıştır.", "Kentteki bisiklet yolları hâlâ yetersizdir.", "Bisiklet yollarının uzunluğu beş yılda üç katına çıkmıştır.", "Kent yönetimi yeni bisiklet yolu yapımını durduracaktır."],
    ["Cümlede kullanıcı sayısında 'artış' olduğu ama bunun beklenenin altında kaldığı söyleniyor.", "'Azalmıştır' cümleyle çelişir; 'yetersizdir' ve 'durduracaktır' cümlede olmayan yorumlardır."],
    "Cümlede açıkça bulunan bilgiyi yorumdan ayırır."))
A(M(CM, "Kesin çıkarım", 3, "Yazarın son romanı, yayımlandığı ilk ay en çok satanlar listesine girmesine karşın eleştirmenlerden beklediği ilgiyi görmedi." + B + KESIN,
    "Romanın okurdan gördüğü ilgi ile eleştirmenlerden gördüğü ilgi örtüşmemiştir.", ["Eleştirmenler romanı olumsuz biçimde eleştirmiştir.", "Yazarın önceki romanları da çok satmıştır.", "Roman ilk aydan sonra listeden çıkmıştır.", "Yazar eleştirmenlerin tutumuna tepki göstermiştir."],
    ["Çok satma okur ilgisini, beklenen ilginin görülmemesi eleştirmen tarafını gösterir; ikisi örtüşmemiştir.", "'İlgi görmemek' olumsuz eleştiri anlamına gelmez; diğer seçenekler cümlede yoktur."],
    "Karşıtlık bildiren cümleden kesin yargı çıkarır."))
A(M(CM, "Kesin çıkarım", 2, "Bu ilaç, yalnızca hekim kontrolünde ve önerilen dozda kullanıldığında etkili ve güvenlidir." + B + KESIN,
    "İlacın güvenli kullanımı belirli koşullara bağlıdır.", ["İlaç yüksek dozda daha etkili olur.", "İlaç reçetesiz satılmaktadır.", "İlacın hiçbir yan etkisi yoktur.", "Hekimler bu ilacı sıklıkla önermektedir."],
    ["'Yalnızca … kullanıldığında' ifadesi güvenliği koşula bağlar.", "Diğer seçenekler cümlede yer almayan ya da cümleyle çelişen yargılardır."],
    "Koşul bildiren yapıdan kesin yargı çıkarır.", 45))
A(M(CM, "Neden–sonuç", 1, "Aşağıdaki cümlelerin hangisinde <b>neden–sonuç</b> ilişkisi vardır?",
    "Yoğun kar yağışı nedeniyle okullar tatil edildi.", ["Sınavı kazanmak için her gün düzenli çalışıyor.", "Erken çıkarsak trafiğe yakalanmayız.", "Bu kitap ötekinden çok daha sürükleyici.", "Hem okuyor hem de yarı zamanlı çalışıyor."],
    ["Okulların tatil edilmesi (sonuç), kar yağışına (neden) bağlanmıştır.", "Diğerlerinde sırasıyla amaç–sonuç, koşul–sonuç, karşılaştırma ve eş zamanlı iki eylem vardır."],
    "Anlam ilişkilerini ayırt eder.", 35))
A(M(CM, "Amaç–sonuç", 2, "Aşağıdaki cümlelerin hangisinde <b>amaç–sonuç</b> ilişkisi vardır?",
    "Tahtayı daha iyi görebilmek için ön sıraya oturdu.", ["Gözleri bozuk olduğundan gözlük takmaya başladı.", "Hava kararınca hepimiz eve döndük.", "Yağmur yağarsa maç ertelenecek.", "Kitabı baştan sona okudu ama pek anlamadı."],
    ["Ön sıraya oturma eylemi bir amaca (daha iyi görmek) yöneliktir; amaç henüz gerçekleşmemiştir.", "'Gözleri bozuk olduğundan' bir nedendir; amaç değil. Diğerleri zaman, koşul ve karşıtlık bildirir."],
    "Amaç ile nedeni ayırt eder.", 40))
A(M(CM, "Koşul–sonuç", 1, "Aşağıdaki cümlelerin hangisinde <b>koşul–sonuç</b> ilişkisi vardır?",
    "Düzenli çalışırsan bu sınavı rahatlıkla geçersin.", ["Düzenli çalıştığı için sınavı rahatlıkla geçti.", "Sınavı geçmek amacıyla düzenli çalışıyor.", "Sınavı geçti ama beklediği puanı alamadı.", "Sınav, geçen yılkinden daha kolaydı."],
    ["'-sa/-se' eki ile sınavı geçmek düzenli çalışma koşuluna bağlanmıştır.", "Diğerlerinde neden–sonuç, amaç–sonuç, karşıtlık ve karşılaştırma vardır."],
    "Koşul anlamını tanır.", 35))
A(M(CM, "Öznel ve nesnel yargı", 1, "Aşağıdakilerden hangisi <b>nesnel</b> bir yargıdır?",
    "Kızılırmak, tamamı Türkiye sınırları içinde kalan en uzun akarsudur.", ["Bu şehir yaşamak için dünyanın en güzel yeridir.", "Romanın sonu okuru derinden etkiliyor.", "Yazarın üslubu oldukça sıkıcı.", "Bu film, yönetmenin en başarılı işidir."],
    ["Nesnel yargı kanıtlanabilir bilgidir; akarsu uzunluğu ölçülebilir bir veridir.", "Diğerleri kişiden kişiye değişebilecek değerlendirmelerdir."],
    "Öznel ve nesnel yargıyı ayırt eder.", 35))
A(M(CM, "Öznel ve nesnel yargı", 1, "Aşağıdakilerden hangisi <b>öznel</b> bir yargıdır?",
    "Sergideki tablolar renk kullanımıyla insanı büyülüyor.", ["Sergide kırk tablo yer alıyor.", "Sergi 15 Mart'ta ziyarete açılacak.", "Tablolar üç farklı salonda sergileniyor.", "Sanatçı eserlerinde yağlıboya tekniğini kullanmıştır."],
    ["'İnsanı büyülemek' kişisel bir izlenimdir; herkes için geçerli olduğu kanıtlanamaz.", "Diğerleri sayılabilir ya da doğrulanabilir bilgilerdir."],
    "Öznel yargıyı tanır.", 35))
A(M(CM, "Varsayım", 3, "Gelecek yıl kütüphane yeniden hizmete açılırsa öğrencilerin çalışma alanı sorunu büyük ölçüde çözülecek." + B + "Bu cümlede aşağıdakilerden hangisi <b>varsayılmaktadır</b>?",
    "Öğrencilerin çalışma alanı sorunu, kütüphanenin kapalı olmasıyla ilgilidir.", ["Kütüphane kesinlikle gelecek yıl açılacaktır.", "Öğrenciler kütüphanede çalışmayı sevmez.", "Kentte başka hiçbir çalışma alanı yoktur.", "Kütüphane yeniden inşa edilmektedir."],
    ["Kütüphanenin açılmasının sorunu çözeceği düşüncesi, sorunun kütüphanenin kapalı olmasından kaynaklandığı varsayımına dayanır.", "'Kesinlikle açılacak' koşul ekiyle çelişir; 'hiçbir çalışma alanı yoktur' gereğinden güçlü bir iddiadır."],
    "Yargının dayandığı örtük öncülü bulur."))
A(M(CM, "Örtülü anlam", 2, "Bu yıl da toplantıya en son gelen Kerem oldu." + B + "Bu cümleden aşağıdakilerden hangisi <b>çıkarılabilir</b>?",
    "Kerem daha önceki toplantılardan en az birine de en son gelmiştir.", ["Kerem toplantılardan hoşlanmaz.", "Toplantı geç başlamıştır.", "Kerem bu yıl toplantıya katılmamıştır.", "Herkes Kerem'i beklemek zorunda kalmıştır."],
    ["'da' bağlacı, durumun daha önce de yaşandığını sezdirir (örtülü anlam).", "Diğer seçenekler cümlede herhangi bir dayanağı olmayan yorumlardır."],
    "Ek ve bağlaçların taşıdığı örtülü anlamı sezer.", 40))
A(M(CM, "Karşılaştırma", 2, "Aşağıdaki cümlelerin hangisinde <b>karşılaştırma</b> yoktur?",
    "Kitabı bir solukta okuyup bitirdi.", ["Bu yol öbüründen daha kısa.", "Kardeşi kadar çalışkan değil.", "Artık eskisi gibi sık görüşmüyoruz.", "En sevdiği mevsim sonbahardı."],
    ["Karşılaştırma iki ya da daha çok varlık/durum arasında yapılır ('daha', 'kadar', 'gibi', 'en').", "'Bir solukta okumak' yalnızca okuma biçimini anlatır."],
    "Karşılaştırma bildiren yapıları tanır.", 40))
A(M(CM, "Kesin çıkarım", 3, "Türk edebiyatında deneme türü, Tanzimat'la birlikte gazetelerin yaygınlaşması sayesinde gelişme olanağı bulmuştur." + B + KESIN,
    "Gazetelerin yaygınlaşması, deneme türünün gelişmesine ortam hazırlamıştır.", ["Deneme türünün ilk örnekleri Tanzimat döneminde yazılmıştır.", "Tanzimat'tan önce Türkçe gazete yayımlanmamıştır.", "Deneme, dönemin en çok okunan türüdür.", "Gazeteler yalnızca deneme türünde yazılara yer vermiştir."],
    ["'… sayesinde gelişme olanağı bulmuştur' ifadesi doğrudan bu yargıyı verir.", "'Gelişme olanağı bulmak' ilk örneklerin bu dönemde yazıldığı anlamına gelmez."],
    "Gelişme ile başlangıç kavramlarını ayırt eder."))
A(M(CM, "Kesin çıkarım", 2, "Araştırmaya katılan öğrencilerin yarısından fazlası, çevrim içi derslerde dikkatlerini sınıf ortamındakinden daha zor topladıklarını belirtti." + B + KESIN,
    "Katılımcıların çoğunluğu, çevrim içi derslerde dikkat toplamakta daha çok güçlük çektiğini ifade etmiştir.", ["Çevrim içi derslerin kaldırılması gerekir.", "Bütün öğrenciler sınıf ortamını tercih etmektedir.", "Öğrencilerin başarısı çevrim içi derslerde düşmüştür.", "Araştırma yalnızca üniversite öğrencileriyle yapılmıştır."],
    ["'Yarısından fazlası' çoğunluk demektir; cümle bunların beyanını aktarır.", "'Bütün öğrenciler' aşırı genellemedir; başarıyla ilgili bir bilgi verilmemiştir."],
    "Nicelik bildiren ifadeleri doğru yorumlar."))
A(M(CM, "Cümle yorumlama", 2, "Usta bir oyuncu, rolünü oynarken seyirciye oynadığını unutturan kişidir." + B + "Bu cümleyle anlatılmak istenen aşağıdakilerden hangisidir?",
    "Oyunculukta başarı, seyircinin canlandırılanı gerçek gibi algılamasıyla ilgilidir.", ["İyi oyuncular yalnızca dram türünde rol alır.", "Seyirci, oyuncunun kim olduğunu bilmemelidir.", "Oyuncular rollerini ezberlemek zorunda değildir.", "Usta oyuncular sahnede doğaçlama yapar."],
    ["Oynadığını unutturmak, canlandırmanın doğal ve inandırıcı olmasıdır.", "Diğer seçenekler cümlede yer almayan dar ya da ilgisiz yorumlardır."],
    "Cümlenin dolaylı anlatımını çözer.", 45))
A(M(CM, "Tanım", 1, "Aşağıdakilerden hangisi bir <b>tanım</b> cümlesidir?",
    "Biyografi, bir kişinin hayatını belgelere dayanarak anlatan yazı türüdür.", ["Biyografi okumayı çok severim.", "Dün kütüphaneden bir biyografi aldım.", "Biyografiler genellikle kalın kitaplardır.", "Okuduğum son biyografi çok sürükleyiciydi."],
    ["Tanım cümlesi bir kavramın ne olduğunu, ayırt edici özellikleriyle açıklar."],
    "Tanım cümlesini tanır.", 30))
A(M(CM, "Ön yargı", 2, "Aşağıdaki cümlelerin hangisinde <b>ön yargı</b> vardır?",
    "Bu yazarın yeni kitabını okumadım ama yine sıkıcı olduğundan eminim.", ["Kitabı okuduktan sonra yazarın üslubunu sevmediğimi fark ettim.", "Eleştirmenler kitabın kurgusunu başarılı bulmuş.", "Kitabın ikinci baskısı bu ay çıkacak.", "Yazar, yeni kitabını iki yılda tamamlamış."],
    ["Ön yargı, bir şey hakkında onu tanımadan yargıya varmaktır: 'okumadım ama … eminim'.", "İlk yanlış seçenekte yargı okuma deneyimine dayanır; ön yargı değildir."],
    "Ön yargıyı deneyime dayalı yargıdan ayırır.", 40))
A(M(CM, "Tahmin", 1, "Aşağıdaki cümlelerin hangisinde <b>tahmin</b> anlamı vardır?",
    "Bu gidişle proje sanırım ay sonuna kadar tamamlanır.", ["Proje geçen ay tamamlandı.", "Projeyi bitirmek için gece gündüz çalıştık.", "Projede beş kişi görev aldı.", "Proje tamamlanınca bir tören düzenlendi."],
    ["'Sanırım' ve 'bu gidişle' ifadeleri kesin olmayan, öngörüye dayalı bir yargı bildirir."],
    "Tahmin bildiren anlatımı tanır.", 30))
A(M(CM, "Kesin çıkarım", 3, "Kurak geçen yazın ardından barajlardaki doluluk oranı son on yılın en düşük düzeyine indi." + B + KESIN,
    "Son on yıl içinde barajlarda bundan daha düşük bir doluluk oranı görülmemiştir.", ["Bu yıl hiç yağış olmamıştır.", "Yakında su kesintileri başlayacaktır.", "Barajlar on yıl önce yapılmıştır.", "Kurak yazlar her yıl yaşanmaktadır."],
    ["'Son on yılın en düşük düzeyi' ifadesi, bu dönemde daha düşük bir oranın görülmediğini kesin olarak bildirir.", "'Hiç yağış olmaması' kuraklıktan çıkarılamayacak kadar güçlü bir iddiadır; su kesintisi bir tahmindir."],
    "Üstünlük bildiren ifadeyi doğru yorumlar."))
A(M(CM, "Öneri", 1, "Aşağıdaki cümlelerin hangisinde <b>öneri</b> vardır?",
    "Metni teslim etmeden önce bir kez de yüksek sesle okumanı tavsiye ederim.", ["Metni dün akşam teslim ettim.", "Metindeki yazım yanlışları beni rahatsız etti.", "Metin, beklediğimden çok daha uzun olmuş.", "Metni okuyan herkes beğendiğini söyledi."],
    ["Öneri, karşıdakine bir davranış tavsiye etmektir: 'tavsiye ederim'."],
    "Öneri cümlesini tanır.", 30))
A(M(CM, "Kesin çıkarım", 3, "Müzenin ziyaretçi sayısı, giriş ücretinin kaldırıldığı ay bir önceki aya göre iki katına çıktı." + B + KESIN,
    "Giriş ücretinin kaldırıldığı ayda müze, bir önceki aydan daha çok ziyaretçi ağırlamıştır.", ["Ziyaretçi artışının tek nedeni ücretin kaldırılmasıdır.", "Müze ücretli olduğu dönemde zarar ediyordu.", "Ziyaretçi sayısı sonraki ayda da artmıştır.", "Müze, kentin en çok ziyaret edilen yeridir."],
    ["Cümle yalnızca iki ay arasındaki sayısal karşılaştırmayı bildirir.", "Zamanlama bir neden–sonuç ilişkisini kesinleştirmez; 'tek nedeni' seçeneği bu yüzden çıkarılamaz."],
    "Birliktelik ile nedenselliği ayırt eder."))
A(M(CM, "Kesin çıkarım", 3, "Bir sanat eseri, yaratıldığı dönemin koşulları bilinmeden de beğenilebilir; ancak o koşulları bilmek, esere ilişkin anlamı derinleştirir." + B + KESIN,
    "Bir eserin ortaya çıktığı bağlamı bilmek, onu anlamaya katkı sağlar.", ["Dönemini bilmeyen biri bir eseri beğenemez.", "Sanat eserleri yalnızca kendi dönemlerinde anlaşılır.", "Sanat eleştirmenleri eserlerin bağlamını önemsemez.", "Her sanat eseri yaratıldığı dönemi yansıtır."],
    ["'Anlamı derinleştirir' ifadesi doğrudan bu yargıyı verir.", "İlk yanlış seçenek, cümlenin 'bilinmeden de beğenilebilir' bölümüyle çelişir."],
    "Cümlenin iki bölümünü birlikte değerlendirir."))
A(M(CM, "Cümle yorumlama", 2, "Kitaplar, insanın kendi yaşamı dışında yüzlerce hayat yaşamasını sağlar." + B + "Bu cümleyle anlatılmak istenen aşağıdakilerden hangisidir?",
    "Okumak, insanın farklı deneyimleri dolaylı yoldan edinmesine olanak tanır.", ["Kitap okuyanlar daha uzun yaşar.", "Her kitap gerçek bir yaşam öyküsü anlatır.", "İnsan, kitaplardan çok kendi deneyimlerinden öğrenir.", "Kitap okumak zaman kaybıdır."],
    ["'Yüzlerce hayat yaşamak' mecazdır; başkalarının deneyimlerini okuma yoluyla tanımayı anlatır."],
    "Mecazlı anlatımı yorumlar.", 40))
A(M(CM, "Anlam ilişkisi", 2, "'Sabah erken kalktığı için otobüsü kaçırmadı.' cümlesindeki anlam ilişkisi aşağıdakilerin hangisinde de vardır?",
    "Yağmur yağdığı için piknik iptal edildi.", ["Otobüse yetişmek için erken kalktı.", "Erken kalkarsa otobüse yetişir.", "Erken kalktı ama yine de otobüsü kaçırdı.", "Kardeşinden daha erken kalkar."],
    ["Örnek cümlede neden–sonuç ilişkisi vardır ('-dığı için' + gerçekleşmiş sonuç).", "Aynı ilişki yalnızca piknik cümlesinde vardır; diğerleri amaç, koşul, karşıtlık ve karşılaştırma bildirir."],
    "Anlam ilişkisini farklı cümlelerde tanır.", 40))
A(M(CM, "Kesin çıkarım", 3, "Yeni düzenleme, yalnızca 2027 yılından sonra kurulacak işletmeleri kapsamaktadır." + B + KESIN,
    "Hâlihazırda faaliyette olan işletmeler bu düzenlemenin kapsamı dışındadır.", ["Düzenleme 2027'de yürürlükten kalkacaktır.", "2027'den sonra yeni işletme kurulması yasaklanmıştır.", "Düzenleme, işletmelerin vergilerini artırmaktadır.", "Bütün işletmeler 2027'ye kadar düzenlemeye uyum sağlamalıdır."],
    ["'Yalnızca … kurulacak işletmeler' ifadesi, şimdiki işletmeleri kapsam dışında bırakır.", "Son seçenek bu kesin yargıyla çelişir; diğerleri cümlede yoktur."],
    "'Yalnızca' sözcüğünün sınırlayıcı işlevini yorumlar."))
A(M(CM, "Örtülü anlam", 2, "Annem bile bu yemeği beğendi." + B + "Bu cümleden aşağıdakilerden hangisi <b>çıkarılabilir</b>?",
    "Konuşan kişinin annesi kolay kolay yemek beğenmez.", ["Yemeği konuşan kişinin annesi yapmıştır.", "Yemeği kimse beğenmemiştir.", "Anne bu yemeği ilk kez yemiştir.", "Yemek çok pahalı malzemelerle yapılmıştır."],
    ["'Bile' sözcüğü, beklenmeyen bir durumun gerçekleştiğini sezdirir: annenin beğenmesi beklenmedik bir şeydir."],
    "'Bile' sözcüğünün katkısını sezer.", 35))
A(M(CM, "Abartma", 1, "Aşağıdaki cümlelerin hangisinde <b>abartma</b> vardır?",
    "Seni görmeyeli neredeyse bin yıl oldu.", ["Seni görmeyeli üç yıl oldu.", "Seninle en son geçen bayram görüşmüştük.", "Seni görmek beni çok mutlu etti.", "Haftaya yeniden görüşebiliriz."],
    ["'Bin yıl', bir durumu olduğundan çok büyük gösteren abartılı bir anlatımdır."],
    "Abartmayı tanır.", 30))

# ============================================================ PARAGRAF YAPISI
YP = "yapi"
BOZAN = "Numaralanmış cümlelerden hangisi, parçanın <b>anlam bütünlüğünü bozmaktadır</b>?"
YER = "Bu parçada numaralanmış cümlelerin anlamlı bir bütün oluşturacak biçimde sıralanması için hangi iki cümlenin <b>yer değiştirmesi</b> gerekir?"

def bozan(sents, k, why, level=3):
    c, w = roman_opts(k)
    return M(YP, "Anlam bütünlüğünü bozan cümle", level, para(sents) + B + BOZAN, c, w,
             why, "Paragrafın konusunu ve akışını izleyerek konudan sapan cümleyi bulur.", 75)

A(bozan(["Uyku, beynin gün boyunca edindiği bilgileri düzenlediği bir süreçtir.", "Özellikle derin uyku evresinde öğrenilen bilgiler kalıcı belleğe aktarılır.",
         "Bu nedenle sınavdan önceki gece uykusuz kalmak, sanıldığının aksine öğrenmeyi zayıflatabilir.", "Araştırmalar da sınav öncesinde yeterince uyuyan öğrencilerin hatırlama testlerinde daha başarılı olduğunu göstermektedir.",
         "Öte yandan bazı araştırmacılar, rüyaların içeriğinin kişinin kültürel çevresine göre değiştiğini öne sürmektedir."], 4,
        ["Parçanın konusu uyku ile öğrenme/bellek arasındaki ilişkidir.", "V. cümle rüyaların kültürle ilişkisine geçerek konudan sapar."]))
A(bozan(["Arılar, bitkilerin tozlaşmasında kilit bir rol üstlenir.", "Dünyadaki gıda ürünlerinin önemli bir kısmı doğrudan ya da dolaylı olarak bu tozlaşmaya bağlıdır.",
         "Bal, antik çağlardan beri tatlandırıcı olarak kullanılmaktadır.", "Bu nedenle arı popülasyonlarındaki azalma yalnızca bir çevre sorunu değil, aynı zamanda bir gıda güvenliği sorunudur.",
         "Tarım ilaçlarının bilinçsiz kullanımı bu azalmanın başlıca nedenleri arasında gösterilmektedir."], 2,
        ["Parça tozlaşma – gıda güvenliği ilişkisini anlatır.", "III. cümle balın tarihsel kullanımına değinerek akışı keser; IV. cümledeki 'Bu nedenle' de II. cümleye bağlanır."]))
A(bozan(["Çocuklarda okuma alışkanlığı büyük ölçüde evde kazanılır.", "Kitapların kolayca ulaşılabilir olduğu, anne babanın da okuduğu evlerde büyüyen çocuklar okumayı doğal bir etkinlik olarak benimser.",
         "Okulda verilen zorunlu okuma ödevleri ise bazen bu alışkanlığı desteklemek yerine okumayı bir yüke dönüştürebilir.", "Çocuk edebiyatı son yıllarda resimli kitaplarla görsel açıdan oldukça zenginleşmiştir.",
         "Bu nedenle okuma sevgisinin kazandırılmasında ailenin örnek olması, okulun dayatmalarından daha belirleyicidir."], 3,
        ["Parça okuma alışkanlığının kazanılmasında aile ve okulun rolünü karşılaştırır.", "IV. cümle çocuk kitaplarının görsel niteliğine geçer; V. cümledeki sonuç ise I–III'e dayanır."]))
A(bozan(["Kentlerdeki ağaçlar yaz aylarında çevre sıcaklığını birkaç derece düşürebilmektedir.", "Kentlerde yaşayan nüfus, kırsal kesimdeki nüfusu çoktan geride bırakmıştır.",
         "Ağaçlar gölge oluşturmalarının yanı sıra yapraklarından buharlaşan suyla da havayı serinletir.", "Bu yönüyle ağaçlandırma, kentlerin iklim değişikliğine uyum sağlamasında düşük maliyetli bir çözüm sunar.",
         "Ancak ağaç türleri seçilirken kentin iklimi ve su kaynakları dikkate alınmalıdır."], 1,
        ["Parçanın konusu ağaçların kentleri serinletme işlevidir.", "II. cümle nüfus dağılımına geçerek konudan sapar."]))
A(bozan(["Türkçe, eklemeli bir dil olduğundan sözcük türetme olanakları oldukça geniştir.", "Çeviri, bir metni yalnızca bir dilden ötekine aktarmak değildir.",
         "Çevirmen, kaynak metnin kültürel göndermelerini hedef dilin okuruna da anlamlı gelecek biçimde yeniden kurmak zorundadır.", "Bu nedenle iyi bir çevirmen iki dili bildiği kadar iki kültürü de tanımalıdır.",
         "Deyimler ve atasözleri bu bağlamda çevirmeni en çok zorlayan öğelerdir."], 0,
        ["II–V. cümleler çevirinin kültürel boyutunu anlatır.", "I. cümle Türkçenin yapısına ilişkin genel bir bilgi verir ve paragrafın konusuyla bağlantı kurmaz."], 4))
A(bozan(["Düzenli fiziksel etkinlik yalnızca bedensel değil ruhsal sağlık için de önemlidir.", "Egzersiz sırasında salgılanan bazı hormonlar kişinin kendini daha iyi hissetmesini sağlar.",
         "Olimpiyat oyunlarının kökeni Antik Yunan'a dayanmaktadır.", "Bu nedenle hekimler hafif depresyonun tedavisinde düzenli yürüyüşü de önermektedir.",
         "Üstelik grup sporları bireyin sosyal bağlarını güçlendirerek yalnızlık duygusunu azaltır."], 2,
        ["Konu sporun ruh sağlığına etkisidir.", "III. cümle olimpiyatların tarihine geçer; IV. cümledeki 'Bu nedenle' II. cümleye bağlanır."]))
A(bozan(["Pek çok müze, koleksiyonlarını dijital ortama aktararak dünyanın her yerinden erişime açmaktadır.", "Bu sayede müzeyi ziyaret etme olanağı bulamayanlar da eserleri ayrıntılı biçimde inceleyebilmektedir.",
         "Araştırmacılar da eserlere ilişkin verilere zaman ve mekân sınırı olmadan ulaşabilmektedir.", "Müzelerin büyük bölümü hafta başında bakım ve temizlik için kapalıdır.",
         "Ne var ki dijital kopya, eserin karşısında durmanın verdiği deneyimin yerini tam olarak tutamaz."], 3,
        ["Parça müzelerin dijitalleşmesinin yararlarını ve sınırını anlatır.", "IV. cümle müzelerin kapalı olduğu günlere değinir; dijital erişim konusuyla ilgisizdir."]))
A(bozan(["Su ayak izi, bir ürünün üretiminde kullanılan toplam su miktarını ifade eder.", "Örneğin bir fincan kahvenin, çekirdeğin yetiştirilmesinden paketlenmesine kadar yaklaşık 130 litre su gerektirdiği hesaplanmaktadır.",
         "Bu tür hesaplamalar, tüketicilerin görünmeyen su tüketimini fark etmesini sağlar.", "Su ayak izi kavramı, tüketim tercihlerimizin su kaynakları üzerindeki etkisini görünür kılar.",
         "Kahve, ilk olarak Etiyopya'da keşfedildiği kabul edilen bir bitkidir."], 4,
        ["Parçanın konusu su ayak izi kavramıdır; kahve yalnızca örnek olarak kullanılmıştır.", "V. cümle örnekteki kahvenin kökenine geçerek ana konudan uzaklaşır."]))

def yer(order_true, swap, why, level=3):
    """order_true: tutarlı cümleler; swap: (i, j) gösterimde yer değiştirilmiş sıra."""
    shown = list(order_true)
    i, j = swap
    shown[i], shown[j] = shown[j], shown[i]
    c = f"{ROMAN[i]} ile {ROMAN[j]}"
    pairs = [f"{ROMAN[a]} ile {ROMAN[b]}" for a in range(5) for b in range(a + 1, 5)]
    wr = [p for p in pairs if p != c]
    return M(YP, "Cümle yer değiştirme", level, para(shown) + B + YER, c, wr[:0] + [wr[k] for k in (0, 3, 5, 8, 2, 7) if k < len(wr)][:4],
             why, "Gönderim öğelerini (bu, böylece, örneğin) izleyerek cümle sırasını kurar.", 90)

A(yer(["Kâğıdın icadından önce yazı taş, kil tablet ve parşömen gibi malzemelere yazılıyordu.", "Bu malzemeler ya çok ağırdı ya da üretimleri çok pahalıydı.",
       "Kâğıt Çin'de bulunduktan sonra yüzyıllar içinde İpek Yolu üzerinden batıya yayıldı.", "Böylece yazılı bilgi hem daha ucuz hem de daha kolay taşınır hâle geldi.",
       "Bu gelişme matbaanın icadıyla birleşince bilginin yayılma hızı benzeri görülmemiş bir düzeye ulaştı."], (1, 3),
      ["'Bu malzemeler' ifadesi I. cümledeki malzemelere, 'Böylece' ise kâğıdın yayılmasına (III) bağlanmalıdır.", "II ve IV yer değiştirince sıra: malzemeler → sorunları → kâğıdın yayılması → sonuç → matbaa."]))
A(yer(["Göçmen kuşlar binlerce kilometrelik yolculuklarında yönlerini şaşırmadan hedeflerine ulaşır.", "Uzun süre bu yeteneğin nasıl işlediği bir sır olarak kaldı.",
       "Günümüzde araştırmacılar, kuşların güneşin konumunu, yıldızları ve dünyanın manyetik alanını birlikte kullandığını düşünüyor.", "Hatta bazı türlerin gözlerinde manyetik alanı algılayan özel proteinler bulundu.",
       "Bu bulgular, kuşların adeta doğal bir pusulaya sahip olduğunu gösteriyor."], (2, 4),
      ["'Bu bulgular' ifadesi bulguların anlatıldığı cümlelerden sonra gelmelidir.", "III ile V yer değiştirince: yetenek → sır → açıklama → kanıt → sonuç."]))
A(yer(["Kahvehaneler Osmanlı kentlerinde 16. yüzyıldan itibaren yaygınlaşmaya başladı.", "Kısa sürede yalnızca kahve içilen yerler olmaktan çıkıp sohbetin, haber alışverişinin ve tartışmanın merkezi hâline geldiler.",
       "Meddahların hikâyelerini anlattığı, şiirlerin okunduğu mekânlar olarak kültürel yaşamı da beslediler.", "Bu canlılık, zaman zaman yönetimin kaygıyla izlediği bir kamusal alan yarattı.",
       "Nitekim bazı dönemlerde kahvehaneler geçici olarak kapatıldı."], (0, 1),
      ["'Kısa sürede' ifadesi bir başlangıçtan sonra gelmelidir; parça bu nedenle yaygınlaşmayı anlatan cümleyle açılmalıdır."], 2))
A(yer(["İnsan beyni, yeni bir beceri öğrenildiğinde yapısal olarak değişebilir.", "Bu özelliğe nöroplastisite adı verilir.",
       "Örneğin müzik aleti çalmayı öğrenen yetişkinlerde ilgili beyin bölgelerinde belirgin değişimler saptanmıştır.", "Bu bulgu, öğrenmenin yalnızca çocuklukla sınırlı olmadığını gösterir.",
       "Dolayısıyla hayat boyu öğrenme beynin sağlığını korumanın da bir yoludur."], (2, 3),
      ["'Bu bulgu' ifadesi, örnekteki bulgudan (müzik aleti) sonra gelmelidir.", "III ile IV yer değiştirince örnek → bulgu → sonuç sırası kurulur."]))
A(yer(["Bir ürünün fiyatı yalnızca üretim maliyetiyle belirlenmez.", "Tüketicilerin o ürüne biçtiği değer de fiyatı doğrudan etkiler.",
       "Örneğin aynı kalitedeki iki ürün, markalarının algılanış biçimine göre çok farklı fiyatlarla satılabilir.", "Bu yüzden şirketler ürün geliştirmeye harcadıkları kadar markalarına da yatırım yapar.",
       "Reklam bütçelerinin üretim bütçelerini aştığı sektörler bu durumun açık örnekleridir."], (0, 3),
      ["'Bu yüzden' ile başlayan cümle parçayı açamaz; bir gerekçeden sonra gelmelidir.", "I ile IV yer değiştirince: genel yargı → ek etken → örnek → sonuç → örnek sektörler."]))

SIRA = "Yukarıda numaralanmış sözler anlamlı ve kurallı bir cümle oluşturacak biçimde sıralandığında"
A(M(YP, "Söz dizimi / sıralama", 2, "I. yalnızca<br>II. bilgi aktarmakla kalmamalı<br>III. iyi bir öğretmen<br>IV. öğrencilerine<br>V. merak duygusunu da aşılamalıdır" + B + SIRA + " hangisi <b>sondan ikinci</b> olur?",
    "II", ["I", "III", "IV", "V"],
    ["Kurallı cümle: 'İyi bir öğretmen (III) öğrencilerine (IV) yalnızca (I) bilgi aktarmakla kalmamalı (II), merak duygusunu da aşılamalıdır (V).'", "I ile IV yer değiştirse de II sondan ikinci kalır."],
    "Söz öbeklerini kurallı cümle düzenine yerleştirir.", 60))
A(M(YP, "Söz dizimi / sıralama", 2, "I. kentlerin<br>II. yeşil alanlar<br>III. hava kalitesini artırmanın<br>IV. en etkili yollarından biri<br>V. olmaya devam ediyor" + B + SIRA + " hangisi <b>baştan üçüncü</b> olur?",
    "III", ["I", "II", "IV", "V"],
    ["Kurallı cümle: 'Yeşil alanlar (II), kentlerin (I) hava kalitesini artırmanın (III) en etkili yollarından biri (IV) olmaya devam ediyor (V).'"],
    "Özne–tümleç–yüklem düzenini kurar.", 60))
A(M(YP, "Söz dizimi / sıralama", 2, "I. özenle<br>II. sınav öncesinde<br>III. hazırlanan bir çalışma planı<br>IV. adayın kaygısını<br>V. önemli ölçüde azaltır" + B + SIRA + " hangisi <b>baştan dördüncü</b> olur?",
    "IV", ["I", "II", "III", "V"],
    ["Kurallı cümle: 'Sınav öncesinde (II) özenle (I) hazırlanan bir çalışma planı (III) adayın kaygısını (IV) önemli ölçüde azaltır (V).'"],
    "Sıfat-fiil öbeğini doğru konumlandırır.", 60))
A(M(YP, "Söz dizimi / sıralama", 2, "I. bugünü<br>II. tarih<br>III. yalnızca geçmişi değil<br>IV. de anlamamızı<br>V. sağlayan bir bilimdir" + B + SIRA + " hangisi <b>baştan üçüncü</b> olur?",
    "I", ["II", "III", "IV", "V"],
    ["Kurallı cümle: 'Tarih (II), yalnızca geçmişi değil (III) bugünü (I) de anlamamızı (IV) sağlayan bir bilimdir (V).'"],
    "'Yalnızca … değil … de' yapısını doğru kurar.", 60))

TAM = "Bu parçada boş bırakılan yere düşüncenin akışına göre aşağıdakilerden hangisi getirilmelidir?"
A(M(YP, "Paragraf tamamlama", 3, "Bir dilin zenginliği yalnızca sözcük sayısıyla ölçülmez. ---- Örneğin Türkçede ekler aracılığıyla tek bir kökten onlarca yeni sözcük türetilebilir." + B + TAM,
    "Dilin yeni kavramları kendi olanaklarıyla karşılayabilme gücü de bu zenginliğin önemli bir göstergesidir.", ["Türkçe, dünyada en çok konuşulan diller arasında yer alır.", "Sözlükler her yıl yeni baskılarla güncellenmektedir.", "Yabancı sözcükler bir dili zamanla zayıflatır.", "Dil, düşüncenin aynasıdır."],
    ["Boşluktan sonraki örnek 'türetme' ile ilgilidir; boşluk bu örneğin desteklediği bir yargı içermelidir.", "Yalnızca ilk seçenek 'sözcük sayısı dışında bir zenginlik ölçütü' getirir ve örnekle bağ kurar."],
    "Örnekten geriye doğru düşüncenin akışını kurar.", 75))
A(M(YP, "Paragraf tamamlama", 3, "Bilimsel bilgi kesin değil, sürekli sınanan ve gerektiğinde düzeltilen bir bilgidir. ---- Bu durum bilimin zayıflığı değil, tam tersine gücüdür." + B + TAM,
    "Yeni kanıtlar ortaya çıktığında en köklü kuramlar bile değiştirilebilir.", ["Bilim insanları çalışmalarının çoğunu laboratuvarda yürütür.", "Bilimsel bilgi deneylerle kesinlik kazanır ve bir daha değişmez.", "Bilim tarihinde pek çok kadın bilim insanı önemli katkılar yapmıştır.", "Felsefe, bilimin annesi olarak kabul edilir."],
    ["'Bu durum' ifadesi, boşluktaki cümlenin bir 'değişebilirlik' durumu anlatmasını gerektirir.", "İkinci yanlış seçenek ilk cümleyle çelişir."],
    "Gönderim öğesine (bu durum) uygun cümleyi seçer.", 75))
A(M(YP, "Paragraf tamamlama", 3, "Kentlerde bisiklet kullanımını artırmak için yalnızca yol yapmak yeterli değildir. Güvenli park alanları, toplu taşımayla bağlantı ve sürücülerin bilinçlendirilmesi de en az yollar kadar önemlidir. ----" + B + "Bu parça aşağıdakilerden hangisiyle <b>tamamlanabilir</b>?",
    "Yani bisiklet dostu bir kent tek bir yatırımla değil, birbirini tamamlayan düzenlemelerle oluşur.", ["Bisiklet, sağlıklı ve çevreci bir ulaşım aracıdır.", "Avrupa kentlerinde bisiklet kullanımı oldukça yaygındır.", "Bu nedenle öncelikle yeni bisiklet yolları yapılmalıdır.", "Bisikletin ilk örnekleri 19. yüzyılda ortaya çıkmıştır."],
    ["Parça birden çok etkenin birlikte gerektiğini söyler; sonuç cümlesi bunu özetlemelidir.", "'Öncelikle yeni yollar' seçeneği ilk cümleyle çelişir."],
    "Paragrafı uygun bir sonuç cümlesiyle bağlar.", 75))
A(M(YP, "Paragraf tamamlama", 2, "Bir romanda karakterlerin inandırıcılığı, onların kusurlarıyla birlikte verilmesine bağlıdır. ---- Okur kendisine benzeyen, hata yapabilen karakterlerle daha kolay bağ kurar." + B + TAM,
    "Hiç hata yapmayan, her durumda doğru kararı veren bir kahraman okura yapay gelir.", ["Romanların çoğu birinci tekil şahıs ağzından anlatılır.", "Okurlar mutlu sonla biten romanları daha çok sever.", "Karakter adları romanın geçtiği döneme uygun seçilmelidir.", "İyi bir roman her şeyden önce sürükleyici olmalıdır."],
    ["Boşluk, 'kusurlu karakter inandırıcıdır' yargısının karşıt durumu üzerinden açıklanmasına uygundur.", "Sonraki cümle de bu açıklamayı okur açısından tamamlar."],
    "Karşıt örnekle düşünceyi destekleyen cümleyi bulur.", 60))
A(M(YP, "Paragraf tamamlama", 3, "---- Bu nedenle sağlıklı beslenme, tek tek besinlerden çok bunların nasıl bir araya getirildiğiyle ilgilidir. Dengeli bir tabak farklı besin gruplarını uygun oranlarda içerir." + B + "Bu parça aşağıdakilerden hangisiyle <b>başlatılmalıdır</b>?",
    "Hiçbir besin, vücudun ihtiyaç duyduğu öğelerin tümünü tek başına karşılayamaz.", ["Hazır yiyecek tüketimi gençler arasında giderek artmaktadır.", "Bazı besinler vücudun bütün ihtiyaçlarını tek başına karşılar.", "Diyetisyenler kilo vermek için öğün atlamayı önermez.", "Yemek kültürü bölgeden bölgeye farklılık gösterir."],
    ["'Bu nedenle' ifadesi, birleştirmenin önemini doğuran bir gerekçe ister: tek besinin yetmemesi.", "Üçüncü seçenek bu gerekçenin tam tersidir."],
    "Giriş cümlesini sonraki cümlenin bağlacından hareketle belirler.", 75))
A(M(YP, "Paragraf tamamlama", 3, "Teknoloji, insanların birbirleriyle iletişim kurmasını hiç olmadığı kadar kolaylaştırdı. ---- Ekranlar aracılığıyla sürekli bağlantıda olmak, çoğu zaman yüz yüze ilişkilerin derinliğinin yerini tutmuyor." + B + TAM,
    "Ne var ki iletişim olanaklarının artması, ilişkilerin niteliğinin de arttığı anlamına gelmiyor.", ["Bu sayede insanlar hiç olmadığı kadar derin dostluklar kuruyor.", "Akıllı telefonların satışı her yıl artıyor.", "İletişim teknolojileri ilk olarak askerî amaçlarla geliştirildi.", "Yüz yüze görüşmeler zaman kaybı olarak görülmelidir."],
    ["İlk cümle olumlu, son cümle olumsuz bir durum anlatıyor; boşluk bu geçişi sağlayan 'ne var ki' cümlesidir.", "'Derin dostluklar' seçeneği son cümleyle çelişir."],
    "Düşünce yönünü değiştiren geçiş cümlesini bulur.", 75))

# ============================================================ PARAGRAFTA ANLAM
PG = "paragraf"
ASIL = "Bu parçada asıl anlatılmak istenen aşağıdakilerden hangisidir?"

A(M(PG, "Ana düşünce", 2, "Yetenek, bir alanda başarılı olmak için gerekli bir başlangıç noktasıdır; ancak tek başına yeterli değildir. Pek çok yetenekli kişi, disiplinli çalışma alışkanlığı kazanamadığı için potansiyelini gerçekleştiremez. Buna karşın orta düzeyde yetenekli olup düzenli çalışan kişiler, zamanla çok daha ileri noktalara ulaşabilir." + B + ASIL,
    "Başarıda düzenli ve disiplinli çalışma, yetenek kadar hatta ondan daha çok belirleyici olabilir.", ["Yetenekli insanlar genellikle tembel olur.", "Yetenek doğuştan gelir, sonradan kazanılamaz.", "Başarı için yetenek gereksizdir.", "Orta düzeyde yetenekli kişiler her zaman daha başarılıdır."],
    ["Parça 'ancak tek başına yeterli değildir' diyerek yeteneği yadsımadan disiplinin önemini vurgular.", "'Gereksizdir' ve 'her zaman' içeren seçenekler parçadan daha güçlü iddialardır; 'genellikle tembel' ise aşırı genellemedir."],
    "Parçanın ana düşüncesini aşırı genellemelerden ayırır.", 75))
A(M(PG, "Ana düşünce", 2, "Eskiden bir bilgiye ulaşmak için kütüphanelerde saatler harcanırdı; bugün aynı bilgiye saniyeler içinde erişebiliyoruz. Ancak bu hız beraberinde başka bir sorunu getirdi: Hangi bilginin doğru olduğunu ayırt etmek. Artık asıl beceri bilgiye ulaşmak değil, ulaşılan bilgiyi sorgulayabilmek ve kaynağını değerlendirebilmektir." + B + ASIL,
    "Günümüzde bilgiye erişmekten çok bilgiyi eleştirel biçimde değerlendirebilmek önem kazanmıştır.", ["Kütüphaneler artık işlevini yitirmiştir.", "İnternetteki bilgilerin tamamı yanlıştır.", "Bilgiye hızlı erişim yalnızca olumlu sonuçlar doğurmuştur.", "Eskiden insanlar daha doğru bilgiye sahipti."],
    ["Son cümle ana düşünceyi doğrudan verir: asıl beceri sorgulamaktır.", "Diğer seçenekler parçada yer almayan ya da parçayla çelişen yargılardır."],
    "Ana düşüncenin yerini (çoğunlukla sonuç cümlesi) belirler.", 75))
A(M(PG, "Çıkarım", 3, "Antik kentlerde yapılan kazılarda bulunan çanak çömlek parçaları, arkeologlar için çoğu zaman altın sikkelerden daha değerlidir. Çünkü sikkeler genellikle seçkin kesimin elindeydi ve kolayca başka yerlere taşınabiliyordu. Oysa gündelik kullanımdaki kaplar, sıradan insanların ne yiyip içtiğini, hangi bölgelerle ticaret yaptığını ve nasıl yaşadığını doğrudan yansıtır." + B + "Bu parçadan aşağıdakilerden hangisi <b>çıkarılabilir</b>?",
    "Arkeologlar için bir buluntunun değeri, maddi değerinden çok sunduğu bilgiyle ilgilidir.", ["Altın sikkeler arkeolojik açıdan değersizdir.", "Antik kentlerde ticaret yapılmazdı.", "Çanak çömlekler yalnızca seçkinlerce kullanılırdı.", "Kazılarda sikke bulunması son derece ender görülür."],
    ["Çanak çömleğin altından 'daha değerli' sayılması, değerin bilgi sağlama gücüne bağlandığını gösterir.", "'Değersizdir' fazla güçlüdür (parça 'çoğu zaman daha değerli' diyor); ticaret ve seçkinler seçenekleri parçayla çelişir."],
    "Örtük ölçütü (bilgi değeri) metinden çıkarır.", 90))
A(M(PG, "Yardımcı düşünce", 2, "Bonsai, ağaçların küçük saksılarda doğadaki görünümlerini koruyacak biçimde yetiştirilmesi sanatıdır. Kökeni Çin'e dayanan bu uygulama daha sonra Japonya'da gelişerek bugünkü biçimini almıştır. Bir bonsainin şekillendirilmesi yıllar, hatta on yıllar sürebilir; bu nedenle sabır bu sanatın vazgeçilmez öğesidir. Düzenli budama ve sulama yapılmadığında ağaç kısa sürede biçimini kaybeder." + B + "Bu parçada aşağıdakilerden hangisine <b>değinilmemiştir</b>?",
    "Bonsai yetiştirmeye en uygun ağaç türlerine", ["Bonsainin kökenine", "Şekillendirme sürecinin uzunluğuna", "Bu sanatın gerektirdiği kişisel özelliğe", "Bakım aksatıldığında ortaya çıkan duruma"],
    ["Köken (Çin–Japonya), süre (yıllar), kişisel özellik (sabır) ve bakım eksikliğinin sonucu parçada vardır.", "Hangi ağaç türlerinin uygun olduğuna hiç değinilmemiştir."],
    "Parçada bulunan ve bulunmayan bilgiyi ayırır.", 60))
A(M(PG, "Ana düşünce", 3, "Bir şehrin kimliği, gökdelenlerinden çok sokaklarında gizlidir. Mahalle fırınları, küçük esnaf dükkânları, çocukların oynadığı meydanlar şehri yaşanılır kılan asıl öğelerdir. Hızlı kentsel dönüşüm projeleri bu dokuyu yok ettiğinde şehir, birbirinin aynısı yapı yığınlarına dönüşür." + B + ASIL,
    "Bir şehri özgün kılan, gündelik yaşamın sürdüğü küçük ölçekli mekânlardır.", ["Gökdelenler şehirlerin en önemli simgeleridir.", "Kentsel dönüşüm projeleri tümüyle durdurulmalıdır.", "Mahalle fırınları ekonomik açıdan verimsizdir.", "Büyük şehirlerde çocuklar için yeterli oyun alanı yoktur."],
    ["İlk cümle ana düşünceyi verir; ikinci cümle bu 'sokak' öğelerini örnekler, üçüncüsü bu dokunun kaybının sonucunu gösterir.", "'Tümüyle durdurulmalıdır' parçada savunulmayan aşırı bir sonuçtur."],
    "Örneklerle desteklenen ana yargıyı bulur.", 75))
A(M(PG, "Yazarın tutumu", 3, "Bazı eleştirmenler popüler romanları edebî değeri olmayan tüketim ürünleri olarak görür. Oysa bugün klasik kabul ettiğimiz pek çok eser, yazıldığı dönemde geniş kitlelerin okuduğu popüler eserlerdi. Bir eserin çok okunması, onun değersiz olduğunun kanıtı olamaz." + B + "Bu parçada yazar aşağıdakilerden hangisini <b>eleştirmektedir</b>?",
    "Çok okunmayı edebî değersizliğin ölçütü sayan yaklaşımı", ["Klasik eserlerin artık okunmamasını", "Popüler romanların çok satmasını", "Yazarların eserlerinden para kazanmasını", "Eleştirmenlerin klasikleri övmesini"],
    ["'Oysa' ile başlayan cümle ve son yargı, popülerliğin değersizlik kanıtı sayılmasına karşı çıkar."],
    "Yazarın karşı çıktığı görüşü belirler.", 75))
A(M(PG, "Ana düşünce", 2, "Bir yabancı dili öğrenmek yalnızca yeni sözcükler ve dil bilgisi kuralları ezberlemek değildir. Her dil, onu konuşan toplumun dünyayı algılayış biçimini de taşır. Bu yüzden bir dili gerçekten öğrenen kişi, farklı bir bakış açısı da kazanır." + B + ASIL,
    "Yabancı dil öğrenmek, insana yeni bir dünya görüşü kazandırır.", ["Dil bilgisi kuralları ezberlenmeden dil öğrenilemez.", "Her toplum dünyayı aynı biçimde algılar.", "Yabancı dil öğrenmek yalnızca çocuklukta mümkündür.", "Sözcük ezberlemek dil öğrenmenin en etkili yoludur."],
    ["'Bu yüzden' ile başlayan son cümle sonucu, yani ana düşünceyi verir."],
    "Sonuç cümlesinden ana düşünceye ulaşır.", 60))
A(M(PG, "Çıkarım", 3, "Kuraklığa dayanıklı tohum çeşitleri üzerine yapılan çalışmalar son yıllarda hız kazandı. Bunun başlıca nedeni, iklim değişikliğiyle birlikte yağış düzeninin öngörülemez hâle gelmesi. Uzmanlar, geleneksel tarım yöntemlerinde ısrar eden bölgelerde verimin önümüzdeki on yılda belirgin biçimde düşebileceği uyarısında bulunuyor." + B + "Bu parçadan aşağıdakilerden hangisi <b>çıkarılabilir</b>?",
    "Tarımda değişen iklim koşullarına uyum sağlamak giderek önem kazanmaktadır.", ["Geleneksel tarım yöntemleri tamamen terk edilmiştir.", "Kuraklığa dayanıklı tohumlar her bölgede verimi kesinlikle artırır.", "Son yıllarda yağış miktarı düzenli olarak artmıştır.", "Tohum çalışmaları yalnızca tek bir ülkede yürütülmektedir."],
    ["Çalışmaların hız kazanması ve uzman uyarıları, iklime uyumun öneminin arttığını gösterir.", "'Tamamen terk edilmiştir' parçayla çelişir ('ısrar eden bölgeler' var); 'kesinlikle artırır' parçada yoktur."],
    "Parçadaki verilerden makul ve sınırlı bir çıkarım yapar.", 75))
A(M(PG, "Başlık", 2, "Ergenlik döneminde biyolojik saat ileri kayar; gençler doğal olarak geç uyuyup geç uyanmaya eğilim gösterir. Erken başlayan okul saatleri ise bu ritimle çatışır. Araştırmalar, okul başlangıç saatini bir saat ileri alan okullarda öğrencilerin derslere katılımının ve başarısının arttığını gösteriyor." + B + "Bu parçaya en uygun başlık aşağıdakilerden hangisidir?",
    "Okul Saatleri ve Ergenlerin Biyolojik Ritmi", ["Uykusuzluğun Kısa Tarihi", "Ergenlerde Beslenme Sorunları", "Öğretmenlerin Çalışma Saatleri", "Ev Ödevlerinin Gereksizliği"],
    ["Parçanın konusu, ergenlerin uyku ritmi ile okul başlangıç saatleri arasındaki ilişkidir; başlık iki öğeyi de kapsamalıdır."],
    "Konuyu kapsayan başlığı seçer.", 50))
A(M(PG, "Ana düşünce", 2, "Eleştiri, karşısındakini küçük düşürmek için değil, onun daha iyiye ulaşmasına katkı sağlamak için yapıldığında anlam kazanır. Yapıcı bir eleştiri, eksikleri gösterirken güçlü yönleri de görmezden gelmez ve somut öneriler içerir. Böyle bir eleştiriyi alan kişi, savunmaya geçmek yerine kendini geliştirmeye yönelir." + B + ASIL,
    "Eleştirinin değeri, kişinin gelişimine katkı sağlamasından gelir.", ["Eleştiri her zaman kırıcıdır.", "İnsanlar eleştiriye karşı daima savunmaya geçer.", "Güçlü yönleri söylemek eleştirinin etkisini azaltır.", "Eleştiri yalnızca uzmanlar tarafından yapılmalıdır."],
    ["İlk cümle ana düşünceyi verir; diğer cümleler yapıcı eleştirinin özelliklerini ve sonucunu açıklar."],
    "Giriş cümlesinde verilen ana düşünceyi belirler.", 60))
A(M(PG, "Yardımcı düşünce", 2, "Ahşap binlerce yıldır yapı malzemesi olarak kullanılmaktadır. Hafif olması, kolay işlenmesi ve ısıyı iyi yalıtması onu cazip kılar. Günümüzde mühendislik ürünü ahşap paneller sayesinde çok katlı ahşap binalar da yapılabilmektedir. Üstelik ağaçlar büyürken karbon depoladığından, sürdürülebilir ormanlardan elde edilen ahşap çevre açısından da avantajlıdır." + B + "Bu parçada ahşapla ilgili aşağıdakilerden hangisine <b>değinilmemiştir</b>?",
    "Maliyetinin diğer yapı malzemeleriyle karşılaştırılmasına", ["Uzun bir kullanım geçmişi olduğuna", "Kolay işlenebildiğine", "Yalıtım özelliğine", "Çevresel yararlarına"],
    ["Kullanım geçmişi (binlerce yıl), işlenebilirlik, yalıtım ve karbon depolama parçada yer alır; maliyet karşılaştırması yoktur."],
    "Parçadaki bilgileri tek tek denetler.", 60))
A(M(PG, "Çıkarım", 3, "Kitap kulüpleri, okumayı bireysel bir etkinlik olmaktan çıkarıp paylaşılan bir deneyime dönüştürür. Katılımcılar aynı kitabı farklı açılardan okuduklarını fark ettikçe kendi yorumlarını sorgulamaya başlar. Ayrıca düzenli buluşmalar, okumayı erteleyenler için bir tür motivasyon kaynağı olur." + B + "Bu parçadan aşağıdakilerden hangisi <b>çıkarılamaz</b>?",
    "Kitap kulüplerine katılanlar daha çok kitap satın alır.", ["Kitap kulüpleri farklı bakış açılarıyla karşılaşma olanağı sunar.", "Düzenli buluşmalar okumanın sürekliliğini destekler.", "Okuma, paylaşıldığında farklı bir deneyime dönüşebilir.", "Katılımcılar kendi yorumlarını yeniden değerlendirme fırsatı bulur."],
    ["Kitap satın alma alışkanlığına parçada hiç değinilmemiştir.", "Diğer dört seçenek sırasıyla ikinci, üçüncü, ilk ve ikinci cümlelerden çıkarılabilir."],
    "Metne dayanmayan yargıyı belirler.", 75))
A(M(PG, "Ana düşünce", 2, "Bilim tarihindeki pek çok önemli buluş, başarısız sayılan deneylerin ardından gelmiştir. Beklenen sonucu vermeyen bir deney, araştırmacıyı sorunu farklı bir açıdan düşünmeye zorlar. Bu nedenle başarısızlık, bilimsel süreçte kaçınılması gereken bir durum değil, öğrenmenin doğal bir parçasıdır." + B + ASIL,
    "Başarısızlık, bilimsel ilerlemenin yapıcı bir öğesidir.", ["Bilim insanları deneylerinde çoğunlukla başarısız olur.", "Başarılı deneyler bilime katkı sağlamaz.", "Bütün önemli buluşlar tesadüfen yapılmıştır.", "Deney sonuçları her zaman beklentilere uygun çıkar."],
    ["Son cümle 'bu nedenle' ile ana düşünceyi bağlar.", "'Bütün' ve 'her zaman' içeren seçenekler parçayı aşan genellemelerdir."],
    "Ana düşünceyi aşırı genellemelerden ayırır.", 60))
A(M(PG, "Çıkarım", 2, "Yönetmenin son filmi, büyük bütçeli yapımların aksine yalnızca üç oyuncu ve tek bir mekânla çekilmiş. Film, diyaloglarının gücüyle izleyiciyi iki saat boyunca ekrana bağlıyor. Görsel efektlere hiç başvurulmaması ise hikâyenin ve oyunculuğun öne çıkmasını sağlıyor." + B + "Bu parçada sözü edilen filmle ilgili aşağıdakilerden hangisi <b>söylenebilir</b>?",
    "Filmin etkisi teknik olanaklardan çok anlatım ve oyunculuktan kaynaklanır.", ["Film gişede beklenen ilgiyi görmemiştir.", "Yönetmen ilk kez bir film çekmiştir.", "Filmde çok sayıda farklı mekân kullanılmıştır.", "Film görsel efektleriyle öne çıkmaktadır."],
    ["Diyalogların gücü ve efektlerin bulunmaması, etkinin anlatım ve oyunculuktan geldiğini gösterir.", "Mekân ve efekt seçenekleri parçayla çelişir; gişe ve ilk film bilgisi parçada yoktur."],
    "Parçadaki bilgilerden geçerli bir yargıya ulaşır.", 60))
A(M(PG, "Ana düşünce", 2, "Çocukların oyun oynaması çoğu zaman boşa geçen zaman olarak görülür. Oysa oyun, çocuğun sorun çözme, iş birliği yapma ve duygularını düzenleme becerilerini geliştirdiği en doğal öğrenme ortamıdır. Serbest oyuna yeterince zaman tanınmayan çocuklar bu becerileri kazanmakta güçlük çekebilir." + B + ASIL,
    "Oyun, çocuğun gelişiminde önemli bir öğrenme aracıdır.", ["Çocuklar okulda yeterince oyun oynamaktadır.", "Oyun yalnızca eğlence amacı taşır.", "İş birliği becerisi yetişkinlikte kazanılır.", "Serbest oyun çocuklar için zararlıdır."],
    ["'Oysa' ile başlayan cümle yaygın görüşe karşı ana düşünceyi verir."],
    "'Oysa' sonrasında gelen ana yargıyı yakalar.", 60))
A(M(PG, "Yardımcı düşünce", 3, "Peri bacaları, volkanik kül ve lavların oluşturduğu tüf katmanlarının rüzgâr ve yağmur sularıyla aşınması sonucu oluşmuştur. Üst kısımlarındaki daha sert kaya, alttaki yumuşak tabakayı aşınmaya karşı korur ve bu kendine özgü şapkalı görünümü ortaya çıkarır. Bölge, sunduğu bu doğal manzara nedeniyle her yıl çok sayıda yerli ve yabancı turisti ağırlar." + B + "Bu parçada peri bacalarıyla ilgili aşağıdakilerden hangisine <b>değinilmemiştir</b>?",
    "Oluşumlarının ne kadar sürdüğüne", ["Hangi malzemeden oluştuklarına", "Oluşumlarında etkili olan doğal etkenlere", "Şapkalı görünümlerinin nedenine", "Turizm açısından önemlerine"],
    ["Malzeme (tüf), etkenler (rüzgâr, yağmur), şapkanın nedeni (sert kaya) ve turizm parçada vardır.", "Oluşum süresine ilişkin bir bilgi verilmemiştir."],
    "Bilgi taraması yaparak eksik olanı belirler.", 60))
A(M(PG, "Yazarın tutumu", 3, "Yapay zekâ araçlarının öğrencilerin ödevlerini yapmasından kaygı duyanlar haklıdır; ancak bu araçları yasaklamak sorunu çözmez. Hesap makinesinin icadı matematik eğitimini bitirmedi, yalnızca neyin öğretilmesi gerektiğini değiştirdi. Asıl yapılması gereken, ölçme yöntemlerini ezberlenmiş bilgiyi değil düşünme sürecini değerlendirecek biçimde yeniden tasarlamaktır." + B + "Bu parçaya göre yazarın yapay zekâ araçlarına ilişkin görüşü aşağıdakilerden hangisidir?",
    "Bu araçlar yasaklanmak yerine eğitimin yeniden düzenlenmesiyle ele alınmalıdır.", ["Bu araçlar eğitim için hiçbir risk taşımamaktadır.", "Bu araçların okullarda kullanımı yasaklanmalıdır.", "Bu araçlar matematik eğitimini sona erdirecektir.", "Ödevler tümüyle kaldırılmalıdır."],
    ["Yazar kaygıyı haklı bulur ('haklıdır') ama yasağı çözüm saymaz; ölçme yöntemlerinin değişmesini önerir.", "'Hiçbir risk' seçeneği yazarın kaygıyı haklı bulmasıyla çelişir."],
    "Yazarın görüşünü karşı görüşlerden ayırır.", 75))
A(M(PG, "Ana düşünce", 2, "Okur, bir şiiri okuduğunda şairin anlatmak istediğini birebir yakalamak zorunda değildir. Şiir, her okurun kendi deneyimleriyle yeniden anlam kazanan açık bir metindir. Bu nedenle aynı şiir farklı okurlarda, hatta aynı okurda farklı zamanlarda başka duygular uyandırabilir." + B + ASIL,
    "Şiirin anlamı, okurun yorumuyla zenginleşir.", ["Şiirin tek ve doğru bir anlamı vardır.", "Şairler şiirlerini açıklamalıdır.", "Okurlar şiiri anlamakta güçlük çeker.", "Şiir yalnızca bir kez okunmalıdır."],
    ["Parça şiirin 'açık metin' olduğunu ve okura göre anlam kazandığını söyler."],
    "Metnin temel yargısını belirler.", 60))
A(M(PG, "Çıkarım", 4, "Bir mağaza zinciri, şubelerinde müzik çalmayı bıraktıktan sonra müşterilerin mağazada geçirdiği ortalama sürenin kısaldığını fark etti. Yeniden müzik çalınmaya başlandığında süre eski düzeyine döndü. Şirket yöneticileri, müziğin satışlar üzerindeki etkisini ölçmek için yeni bir araştırma başlattı." + B + "Bu parçadan aşağıdakilerden hangisi <b>kesin olarak</b> çıkarılabilir?",
    "Mağazada müzik çalınması ile müşterilerin mağazada kalma süresi arasında bir ilişki gözlenmiştir.", ["Mağazada müzik çalınması satışları kesinlikle artırır.", "Müşteriler mağazada çalan müzikten rahatsız olmaktadır.", "Şirket, araştırmanın sonucunu kamuoyuyla paylaşmıştır.", "Mağaza zinciri bazı şubelerini kapatmıştır."],
    ["Parça yalnızca süre ile müzik arasında gözlenen birlikteliği bildirir.", "Satış etkisi henüz araştırılmaktadır; bu yüzden 'kesinlikle artırır' çıkarılamaz."],
    "Gözlem ile kanıtlanmış sonucu ayırt eder.", 75))
A(M(PG, "Ana düşünce", 2, "Çok şey bilmek, bilge olmak için yeterli değildir. Bilgi, ancak ne zaman ve nasıl kullanılacağı bilindiğinde değer kazanır. Bilge kişi, bildiklerini yaşamın karmaşık durumlarında yerinde ve ölçülü biçimde uygulayabilen kişidir." + B + ASIL,
    "Bilgelik, bilgiyi yerinde ve ölçülü kullanabilme becerisidir.", ["Bilgi, bilgelikten daha değerlidir.", "Çok okuyan herkes bilge olur.", "Bilge kişiler az şey bilir.", "Bilgi zamanla değerini yitirir."],
    ["Parça bilgi ile bilgeliği ayırır; bilgeliği bilginin yerinde kullanımı olarak tanımlar."],
    "Tanıma dayalı ana düşünceyi belirler.", 50))

# --- Ortak parça grupları (ÖSYM 29–42 düzenine benzer)
G1 = {"id": "pg-dikkat", "info": "Günümüzde dijital platformların temel hedefi, kullanıcıların dikkatini olabildiğince uzun süre ekranda tutmaktır. Bu nedenle bildirimler, sonsuz kaydırma ve otomatik oynatma gibi özellikler, kullanıcının kendi isteğiyle durmasını zorlaştıracak biçimde tasarlanır. Uzmanlar bu duruma 'dikkat ekonomisi' adını veriyor: Dikkat sınırlı bir kaynaktır ve şirketler bu kaynağı reklam gelirine dönüştürmek için birbiriyle yarışır. Bunun bedelini ise çoğu zaman kullanıcılar öder; uzun süre kesintisiz odaklanma becerisi zayıflar, derin okuma yerini yüzeysel taramaya bırakır. Yine de çözüm teknolojiyi reddetmek değil, onu bilinçli kullanmayı öğrenmektir. Bildirimleri sınırlamak, belirli saatlerde ekrandan uzak durmak gibi küçük alışkanlıklar dikkatin denetimini yeniden kullanıcıya verebilir."}
A(M(PG, "Uzun metin analizi", 2, "Bu parçaya göre dijital platformlardaki bazı özellikler hangi amaçla tasarlanmaktadır?",
    "Kullanıcıların platformda geçirdiği süreyi artırmak", ["Kullanıcıların bilgiye daha hızlı ulaşmasını sağlamak", "Derin okuma alışkanlığını desteklemek", "Reklamları tümüyle ortadan kaldırmak", "Kullanıcıların ekran süresini sınırlamak"],
    ["İkinci cümle bu özelliklerin kullanıcının 'kendi isteğiyle durmasını zorlaştıracak biçimde' tasarlandığını söyler; amaç ekranda kalma süresini uzatmaktır."],
    "Uzun metinden doğrudan bilgi bulur.", 50, G1))
A(M(PG, "Uzun metin analizi", 3, "Parçada sözü edilen 'dikkat ekonomisi' kavramıyla anlatılmak istenen aşağıdakilerden hangisidir?",
    "Sınırlı bir kaynak olan insan dikkatinin gelir elde etmek için rekabet konusu hâline gelmesi", ["İnsanların dikkatlerini tasarruflu kullanmayı öğrenmesi", "Reklam harcamalarının giderek azalması", "Ekonomi haberlerinin dijital ortamda daha çok okunması", "Kullanıcıların dijital platformlara para ödemesi"],
    ["Kavram, iki nokta üst üsteden sonra açıklanır: dikkat sınırlıdır ve şirketler onu reklam gelirine dönüştürmek için yarışır."],
    "Kavramı metindeki açıklamasından yola çıkarak yorumlar.", 60, G1))
A(M(PG, "Uzun metin analizi", 3, "Yazarın önerdiği çözümle ilgili aşağıdakilerden hangisi <b>söylenebilir</b>?",
    "Teknolojinin kullanım biçimine yönelik bireysel düzenlemeleri öne çıkarmaktadır.", ["Dijital platformların yasaklanmasını savunmaktadır.", "Sorunun yalnızca şirketlerce çözülebileceğini düşünmektedir.", "Teknolojinin tümüyle bırakılmasını önermektedir.", "Kullanıcıların sorumluluğu olmadığını vurgulamaktadır."],
    ["'Çözüm teknolojiyi reddetmek değil, onu bilinçli kullanmayı öğrenmektir' ve verilen örnekler (bildirim sınırlama, ekran molası) bireysel düzenlemelerdir."],
    "Yazarın önerisini doğru biçimde nitelendirir.", 60, G1))
G2 = {"id": "pg-odunc", "info": "Diller tarih boyunca birbirleriyle etkileşerek değişir. Ticaret, göç ve kültürel alışveriş, bir dilden ötekine sözcük geçişini kaçınılmaz kılar. Türkçe de yüzyıllar içinde Arapça, Farsça, Fransızca ve İngilizce gibi dillerden çok sayıda sözcük almıştır. Bu durum kimi zaman dilin bozulduğu kaygısına yol açsa da ödünç sözcüklerin önemli bir kısmı, zamanla Türkçenin ses ve yapı özelliklerine uyarak dilin doğal bir parçası hâline gelmiştir. Asıl tehlike ödünç almak değil, dilin kendi türetme olanaklarını kullanmaktan vazgeçmektir."}
A(M(PG, "Uzun metin analizi", 2, "Yazara göre bir dil için asıl tehlike aşağıdakilerden hangisidir?",
    "Kendi sözcük türetme olanaklarını kullanmaktan vazgeçmek", ["Başka dillerden sözcük almak", "Ticaret ve göç yoluyla değişmek", "Ses özelliklerinin zamanla değişmesi", "Yabancı dil öğrenen sayısının artması"],
    ["Son cümle bunu doğrudan söyler: 'Asıl tehlike ödünç almak değil, … türetme olanaklarını kullanmaktan vazgeçmektir.'"],
    "Yazarın vurguladığı yargıyı bulur.", 45, G2))
A(M(PG, "Uzun metin analizi", 3, "Bu parçadan aşağıdakilerden hangisi <b>çıkarılabilir</b>?",
    "Ödünç sözcükler zamanla alıcı dilin kurallarına uyum sağlayabilir.", ["Türkçe başka dillere hiç sözcük vermemiştir.", "Ödünç sözcük kullanımı yasaklanmalıdır.", "Türkçe yalnızca Arapçadan sözcük almıştır.", "Diller etkileşim olmadan da hızla değişir."],
    ["Dördüncü cümle, ödünç sözcüklerin Türkçenin ses ve yapı özelliklerine uyduğunu belirtir.", "'Yalnızca Arapça' parçayla çelişir; diğerleri parçada yer almaz."],
    "Uzun metinden doğrulanabilir çıkarım yapar.", 60, G2))

# ============================================================ EK SORULAR (v1.1)
A(M(CM, "Kesin çıkarım", 3, "Kentteki toplu taşıma araçlarının tamamı 2027 yılı sonuna kadar elektrikli araçlarla değiştirilecek." + B + KESIN,
    "Kentteki toplu taşıma araçlarının en az bir kısmı şu anda elektrikli değildir.", ["Elektrikli araçlar diğer araçlardan daha ucuzdur.", "Kentte hava kirliliği son yıllarda artmıştır.", "Yeni araçların tamamı yerli üretim olacaktır.", "Toplu taşıma kullanımı 2027'de artacaktır."],
    ["Araçların elektrikli araçlarla 'değiştirilecek' olması, mevcut araçların hiç değilse bir kısmının elektrikli olmadığını gösterir.", "Maliyet, kirlilik, üretim yeri ve kullanım artışı cümlede yer almaz."],
    "Bir planın dayandığı mevcut durumu kesin olarak çıkarır."))
A(M(CM, "Kesin çıkarım", 4, "Ankete katılan öğretmenlerin yalnızca beşte biri, yeni ders kitaplarını yeterli bulduğunu belirtti." + B + KESIN,
    "Katılımcı öğretmenlerin çoğunluğu, yeni ders kitaplarını yeterli bulduğunu belirtmemiştir.", ["Öğretmenlerin beşte dördü yeni ders kitaplarını yetersiz bulmaktadır.", "Yeni ders kitapları gelecek yıl değiştirilecektir.", "Ankete okuldaki bütün öğretmenler katılmıştır.", "Öğrenciler de yeni ders kitaplarını yetersiz bulmuştur."],
    ["Beşte birin 'yeterli' dediği bilinir; geri kalan beşte dört yalnızca bu görüşü belirtmemiştir.", "Bu beşte dördün kararsız ya da görüş bildirmemiş olabileceği için 'yetersiz buluyor' denemez; bu seçenek sık yapılan bir tuzaktır."],
    "Bir oranın tümleyenini aşırı yorumlamaktan kaçınır.", 75))
A(M(CM, "Amaç–sonuç", 2, "Aşağıdaki cümlelerin hangisinde <b>amaç</b> bildiren bir anlatım <b>yoktur</b>?",
    "Yol çalışması yüzünden servis bu sabah geç geldi.", ["Kuyrukta beklememek için biletini önceden aldı.", "Sınava hazırlanmak amacıyla bir kursa yazıldı.", "Herkes duysun diye yüksek sesle konuştu.", "Gün doğumunu izlemek üzere tepeye tırmandılar."],
    ["'Yüzünden' gerçekleşmiş bir nedeni bildirir (neden–sonuç).", "Diğerlerinde 'için, amacıyla, diye, üzere' ile henüz gerçekleşmemiş bir hedef anlatılır."],
    "Amaç ile nedeni ayırt eder.", 45))
A(M(CM, "Karşıtlık", 1, "Aşağıdaki cümlelerin hangisinde <b>karşıtlık</b> ilişkisi vardır?",
    "Proje zamanında bitti, ancak bütçe aşıldı.", ["Proje zamanında bittiği için ödül aldık.", "Proje bitince hep birlikte tatile çıktık.", "Proje bitmeden kimse ayrılmayacak.", "Projeyi bitirmek için hafta sonu da çalıştık."],
    ["'Ancak' bağlacı, beklenen olumlu sonuca ters düşen bir durumu bağlar.", "Diğerlerinde neden, zaman, koşul ve amaç ilişkileri vardır."],
    "Karşıtlık bildiren bağlaçları tanır.", 35))
A(M(CM, "Varsayım", 4, "Bu yıl kütüphaneye yeni kitap alınmazsa öğrenciler güncel kaynaklara ulaşamayacak." + B + "Bu yargı aşağıdakilerden hangisi <b>varsayılarak</b> ileri sürülmüştür?",
    "Öğrencilerin güncel kaynaklara ulaşması büyük ölçüde kütüphaneye bağlıdır.", ["Kütüphaneye bu yıl kesinlikle kitap alınmayacaktır.", "Öğrenciler kitap okumaktan hoşlanmaz.", "Kütüphane bütçesi geçen yıl artırılmıştır.", "Öğrencilerin hepsi kütüphaneye her gün gider."],
    ["Kitap alınmamasının erişimi engelleyeceği sonucu, öğrencilerin başka kaynaklardan bu kaynaklara ulaşamayacağı öncülüne dayanır.", "'Kesinlikle alınmayacak' koşul ekiyle çelişir; 'hepsi her gün gider' gereksiz derecede güçlü bir iddiadır."],
    "Koşullu yargının dayandığı örtük öncülü bulur.", 75))
A(M(CM, "Cümle yorumlama", 2, "Eleştiriye kulak tıkayan, aynı hatayı yeniden yapmaya kendini mahkûm eder." + B + "Bu cümleyle anlatılmak istenen aşağıdakilerden hangisidir?",
    "Eleştirileri dikkate almamak, hatalardan ders çıkarmayı engeller.", ["Her eleştiri haklıdır.", "Hata yapmak kaçınılmazdır.", "Eleştiri yapanlar hata yapmaz.", "İnsan hatalarını her zaman kendi başına fark eder."],
    ["'Kulak tıkamak' dinlememek, 'kendini mahkûm etmek' kaçınılmaz sonuca sürüklenmek demektir: Eleştiriyi dinlemeyen, hatasını düzeltemez."],
    "Deyimli anlatımı yorumlar.", 45))

A(bozan(["Gönüllülük, bireyin karşılık beklemeden topluma katkı sunmasıdır.", "Araştırmalar, düzenli gönüllü çalışmalara katılanların kendilerini daha anlamlı bir yaşamın parçası olarak hissettiğini gösteriyor.",
         "Gönüllüler, yeni insanlarla tanışarak sosyal çevrelerini de genişletiyor.", "Pek çok ülkede asgari ücret her yıl yeniden belirlenmektedir.",
         "Kısacası gönüllülük, yardım edilen kadar yardım edene de kazandıran bir etkinliktir."], 3,
        ["Parçanın konusu gönüllülüğün gönüllüye sağladığı yararlardır.", "IV. cümle ücretli çalışmaya ilişkin bir düzenlemeye geçer; V. cümledeki 'Kısacası' ise II ve III'ü toparlar."], 2))
A(bozan(["Mikroplastikler, boyutu 5 milimetreden küçük plastik parçacıklardır.", "Bu parçacıklar büyük plastik atıkların zamanla parçalanmasıyla ya da kozmetik ürünlerdeki mikro boncuklardan doğrudan oluşur.",
         "Plastik, hafifliği ve dayanıklılığı sayesinde ambalaj sektöründe yaygın biçimde kullanılmaktadır.", "Denizlere ulaşan mikroplastikler besin zinciri yoluyla insan vücuduna kadar girebilmektedir.",
         "Bu nedenle bilim insanları, tek kullanımlık plastiklerin azaltılmasını acil bir öncelik olarak görüyor."], 2,
        ["Parça mikroplastiklerin tanımını, kaynağını, yayılışını ve buna karşı önerilen önlemi anlatır.", "III. cümle plastiğin ambalajda neden tercih edildiğine geçer; aynı genel alanda olsa da mikroplastik konusundan sapar."], 4))
A(bozan(["Bir dili konuşanların sayısı azaldığında o dil yalnızca sözcüklerini değil, taşıdığı bilgi birikimini de yitirme tehlikesiyle karşılaşır.", "Dünyanın en çok konuşulan dilleri arasında Çince, İngilizce ve İspanyolca yer alır.",
         "Örneğin bazı yerel dillerde bitkilerin tıbbi özelliklerine ilişkin yüzyıllık bilgiler yalnızca sözlü olarak aktarılmaktadır.", "Son konuşurlar öldüğünde bu bilgiler çoğu zaman kayıt altına alınmadan kaybolur.",
         "Bu yüzden dilbilimciler, tehlike altındaki dilleri belgeleme çalışmalarına öncelik vermektedir."], 1,
        ["Parçanın konusu, yok olma tehlikesindeki dillerle birlikte kaybolan bilgi birikimidir.", "II. cümle en çok konuşulan dillere geçer; III. cümledeki 'Örneğin' de I. cümleye bağlanır."]))
A(yer(["Kentlerde gece aydınlatmasının artması, ışık kirliliği adı verilen bir sorunu beraberinde getirdi.", "Bu sorun yalnızca gökyüzünü gözlemleyen astronomları etkilemiyor.",
       "Gece göç eden kuşlar yapay ışıklar nedeniyle yönlerini şaşırabiliyor.", "İnsanlarda ise gece boyunca ışığa maruz kalmak uyku düzenini bozabiliyor.",
       "Bu nedenle bazı kentler sokak lambalarını yalnızca aşağıyı aydınlatacak biçimde yeniden tasarlıyor."], (2, 4),
      ["'Bu nedenle' ile başlayan çözüm cümlesi, sorunun etkileri sayıldıktan sonra gelmelidir.", "III ile V yer değiştirince: sorun → yalnızca astronomlar değil → kuşlar → insanlar → çözüm."]))
A(yer(["Arkeologlar bir yerleşim yerinin ne zaman kurulduğunu belirlemek için çeşitli tarihleme yöntemleri kullanır.", "Bunlardan en bilineni, organik kalıntılardaki karbon-14 miktarının ölçülmesine dayanır.",
       "Canlılar öldükten sonra karbon-14 düzenli bir hızla azaldığından kalan miktar, ölüm zamanını gösterir.", "Ancak bu yöntem yaklaşık 50 bin yıldan eski kalıntılarda güvenilir sonuç vermez.",
       "Daha eski buluntular için ise volkanik katmanlara dayanan farklı yöntemler tercih edilir."], (1, 2),
      ["'Bunlardan en bilineni' ifadesi I. cümledeki 'tarihleme yöntemleri'ne bağlanır ve hemen ardından gelmelidir.", "Karbon-14'ün azalması ancak yöntem tanıtıldıktan sonra açıklanabilir; II ile III yer değiştirmelidir."], 4))
A(M(YP, "Söz dizimi / sıralama", 2, "I. bir toplumun<br>II. kültürel mirası<br>III. yalnızca müzelerde değil<br>IV. gündelik alışkanlıklarında da<br>V. yaşamaya devam eder" + B + SIRA + " hangisi <b>baştan ikinci</b> olur?",
    "II", ["I", "III", "IV", "V"],
    ["Kurallı cümle: 'Bir toplumun (I) kültürel mirası (II) yalnızca müzelerde değil (III) gündelik alışkanlıklarında da (IV) yaşamaya devam eder (V).'", "İlgi hâlindeki 'bir toplumun' tamlanan olan 'kültürel mirası'ndan hemen önce gelir."],
    "Tamlama ve '… değil … da' yapısını doğru sıralar.", 60))
A(M(YP, "Paragraf tamamlama", 3, "Uzaktan çalışma, çalışanlara zaman ve mekân esnekliği sağlıyor. ---- Bu nedenle pek çok şirket, haftanın birkaç gününü ofiste geçirmeyi öngören karma modellere yöneliyor." + B + TAM,
    "Ancak ekip içi iletişimin ve kurum kültürünün zayıflaması, bu modelin göz ardı edilemeyecek bir bedeli olarak görülüyor.", ["Uzaktan çalışma ilk kez geçen yüzyılın ikinci yarısında tartışılmaya başlandı.", "Bu esneklik sayesinde çalışanlar ofise artık hiç ihtiyaç duymuyor.", "Şirketler ofis kira giderlerini düşürmek istiyor.", "Çalışanların çoğu evden çalışmayı tercih ediyor."],
    ["Karma modele yönelişin 'nedeni' boşlukta olmalıdır: Tamamen uzaktan çalışmanın bir sakıncası.", "'Ofise hiç ihtiyaç duymuyor' sonuç cümlesiyle çelişir; kira ve tercih seçenekleri ofise dönüşü değil uzaktan çalışmayı destekler."],
    "Sonuç cümlesinden geriye doğru gerekçeyi bulur.", 75))
A(M(YP, "Paragraf tamamlama", 3, "---- Örneğin aynı sözcük, söylenişteki vurguya göre soru, şaşkınlık ya da öfke anlatabilir. Bu nedenle yazılı iletişimde yanlış anlaşılmalar sözlü iletişime göre daha sık yaşanır." + B + "Bu parça aşağıdakilerden hangisiyle <b>başlatılmalıdır</b>?",
    "Konuşurken iletilen anlamın önemli bir kısmı, sözcüklerden çok ses tonu ve vurguyla taşınır.", ["Yazılı iletişim, sözlü iletişimden daha eski bir yöntemdir.", "Sözcükler her bağlamda aynı anlamı taşır.", "Telefonla konuşmak mektup yazmaktan daha pahalıdır.", "Dil bilgisi kuralları yazı dilinde daha katıdır."],
    ["'Örneğin' cümlesi vurgunun anlamı değiştirdiğini örnekler; giriş cümlesi bu genel yargıyı vermelidir.", "Son cümledeki sonuç da yazıda tonun kaybolmasına dayanır."],
    "Örnek ve sonuç cümlelerinden giriş cümlesini çıkarır.", 75))
A(M(YP, "Paragraf tamamlama", 2, "Bir kentin turizm potansiyeli yalnızca tarihî yapılarıyla ölçülmez. Yerel mutfağı, el sanatları ve festivalleri de ziyaretçilerin o kenti seçmesinde belirleyici olabilir. ----" + B + "Bu parça aşağıdakilerden hangisiyle <b>tamamlanabilir</b>?",
    "Dolayısıyla turizm planlaması, somut mirasın yanında yaşayan kültürü de gözetmelidir.", ["Tarihî yapılar turizm açısından hiçbir önem taşımaz.", "Festivaller genellikle yaz aylarında düzenlenir.", "El sanatları kırsal bölgelerde daha yaygındır.", "Bu nedenle yalnızca tarihî yapıların restorasyonuna kaynak ayrılmalıdır."],
    ["Parça iki öğeyi (tarihî yapılar + yaşayan kültür) birlikte önemser; sonuç cümlesi bu ikisini birleştirmelidir.", "İlk ve son yanlış seçenekler parçanın iki yönünden birini dışlar."],
    "Paragrafı uygun bir sonuç cümlesiyle tamamlar.", 60))

A(M(PG, "Ana düşünce", 3, "Bilimsel bir buluşun değeri çoğu zaman ortaya çıktığı anda anlaşılmaz. Kimi buluşlar yıllarca kullanım alanı bulunamadan bekler; sonra bambaşka bir alandaki gelişme onları birdenbire vazgeçilmez kılar. Bu nedenle 'Ne işe yarayacak?' sorusuyla temel araştırmaları değerlendirmek, geleceğin olanaklarını bugünden kısıtlamak anlamına gelebilir." + B + ASIL,
    "Temel araştırmalar yalnızca hemen sağlayacakları yarara göre değerlendirilmemelidir.", ["Bilimsel buluşların çoğu hiçbir işe yaramaz.", "Uygulamalı araştırmalara kaynak ayrılmamalıdır.", "Buluşlar yalnızca ortaya çıktıkları alanda kullanılır.", "Bilim insanları buluşlarının değerini bilmez."],
    ["Son cümle 'Bu nedenle' ile yazarın asıl görüşünü verir: Anlık yarar ölçütü temel araştırmaları değerlendirmek için yetersizdir.", "Diğer seçenekler parçayı aşan ya da parçayla çelişen genellemelerdir."],
    "Sonuç cümlesindeki ana yargıyı belirler.", 75))
A(M(PG, "Çıkarım", 4, "Bir araştırmada, öğle arasında yirmi dakikalık kısa bir şekerleme yapan çalışanların öğleden sonraki dikkat testlerinde daha başarılı olduğu görüldü. Ancak şekerlemesi bir saati aşanlarda uyandıktan sonra kısa süreli bir sersemlik gözlendi. Araştırmacılar, şekerlemenin süresinin en az kendisi kadar önemli olduğunu vurguluyor." + B + "Bu parçadan aşağıdakilerden hangisi <b>çıkarılamaz</b>?",
    "Uzun şekerleme yapanların gece uykusu bozulur.", ["Kısa şekerleme, öğleden sonraki dikkat performansıyla olumlu ilişkilidir.", "Şekerlemenin süresi sonuçlarını etkileyebilir.", "Uzun bir şekerlemeden sonra geçici sersemlik yaşanabilir.", "Araştırma çalışanlar üzerinde yapılmıştır."],
    ["Parça yalnızca uyanıştan sonraki kısa süreli sersemlikten söz eder; gece uykusuna ilişkin bir bilgi yoktur.", "Diğer dört yargı parçadaki bulgulardan doğrudan çıkarılabilir."],
    "Metne dayanmayan yargıyı ayırt eder.", 75))
A(M(PG, "Yazarın tutumu", 3, "Her yeni teknolojinin ardından 'Gençler artık okumuyor.' yakınması yükselir. Oysa yayın ve kütüphane verileri, gençlerin önemli bir kısmının okumayı sürdürdüğünü gösteriyor; değişen, okunan metinlerin türü ve okuma ortamı. Bu dönüşümü bir çöküş olarak görmek yerine anlamaya çalışmak, eğitimcilere daha çok şey kazandıracaktır." + B + "Bu parçada yazarın tutumu aşağıdakilerden hangisidir?",
    "Gençlerin okuma alışkanlığına ilişkin karamsar genellemelere karşı çıkmakta, değişimi anlamaya çağırmaktadır.", ["Gençlerin artık hiç okumadığını kabul etmektedir.", "Ekrandan okumanın kitap okumaktan üstün olduğunu savunmaktadır.", "Kütüphanelerin gereksizleştiğini ileri sürmektedir.", "Eğitimcileri okuma alışkanlığının yok olmasından sorumlu tutmaktadır."],
    ["'Oysa' sonrası yazarın görüşüdür: Okuma sürüyor, biçimi değişiyor.", "Yazar iki ortamı karşılaştırıp birini üstün saymaz; bu yüzden ikinci yanlış seçenek parçayı aşar."],
    "Yazarın karşı çıktığı görüşü ve önerisini belirler.", 75))
A(M(PG, "Başlık", 2, "Son yıllarda pek çok kentte apartman çatıları ve boş arsalar, mahalle sakinlerinin birlikte işlediği bahçelere dönüşüyor. Bu bahçeler taze sebze sağlamanın yanında, birbirini tanımayan komşuları ortak bir uğraşta buluşturuyor. Çocuklar da toprağa dokunarak besinin nereden geldiğini öğreniyor." + B + "Bu parçaya en uygun başlık aşağıdakilerden hangisidir?",
    "Kent Bahçeleri: Sebzeden Fazlası", ["Apartman Yönetiminde Sorunlar", "Kırsaldan Kente Göç", "Organik Gübre Nasıl Yapılır?", "Çatı Yalıtımının Önemi"],
    ["Parça kent bahçelerinin besin üretimi dışındaki toplumsal ve eğitsel yararlarını anlatır; başlık hem konuyu hem bu vurguyu kapsamalıdır."],
    "Konuyu ve vurguyu kapsayan başlığı seçer.", 50))
A(M(PG, "Yardımcı düşünce", 2, "Kâğıt üretiminde geri dönüştürülmüş lif kullanmak hem ağaç kesimini hem de su ve enerji tüketimini azaltır. Ancak lifler her geri dönüşümde kısalır ve kâğıt ancak sınırlı sayıda geri dönüştürülebilir. Bu nedenle sistemin sürmesi için belirli oranda yeni lif eklemek gerekir." + B + "Bu parçada aşağıdakilerden hangisine <b>değinilmemiştir</b>?",
    "Geri dönüşüm tesislerinin sayısına", ["Geri dönüşümün çevresel yararlarına", "Kâğıdın sınırsız biçimde geri dönüştürülemeyeceğine", "Liflerin geri dönüşümle değiştiğine", "Üretimde yeni life duyulan ihtiyaca"],
    ["Çevresel yararlar, sınırlı dönüşüm, liflerin kısalması ve yeni lif gereği parçada vardır; tesis sayısına değinilmemiştir."],
    "Parçadaki bilgileri tek tek denetler.", 50))
A(M(PG, "Ana düşünce", 4, "Bir çevirmenin görünmez olması uzun süre iyi çevirinin ölçütü sayıldı: Okur, metnin bir çeviri olduğunu fark etmemeliydi. Ne var ki bu yaklaşım, kaynak kültürün tuhaf ve yabancı gelen öğelerini hedef dilin alışkanlıklarına uydurarak silikleştirme tehlikesi taşır. Bazı çevirmenler bu yüzden okurun yabancılığı hissetmesine bilinçli olarak izin vermenin, metne daha sadık kalmak anlamına geldiğini savunur." + B + ASIL,
    "Çeviride akıcılık uğruna kaynak kültürün farklılıklarının silinmesi sorgulanmaktadır.", ["Çevirmenler kendilerini okurdan tümüyle gizlemelidir.", "Yabancı kültür öğeleri çeviriden çıkarılmalıdır.", "İyi bir çeviri her zaman zor okunur.", "Çeviriler okuru kaynak dili öğrenmeye yöneltir."],
    ["'Ne var ki' ile geleneksel ölçüt eleştirilir: Akıcılık, kaynak kültürü silikleştirebilir.", "İlk iki yanlış seçenek eleştirilen görüşün kendisidir; 'her zaman zor okunur' parçayı aşan bir genellemedir."],
    "Eleştirilen görüş ile yazarın vurguladığı düşünceyi ayırt eder.", 90))
A(M(PG, "Çıkarım", 3, "Kutup bölgelerindeki buzullarda açılan sondaj kuyularından çıkarılan buz örnekleri, içlerinde hapsolmuş küçük hava kabarcıkları barındırır. Bu kabarcıklar, buzun oluştuğu dönemdeki atmosferin bileşimini korur. Araştırmacılar farklı derinliklerden alınan örnekleri karşılaştırarak geçmiş dönemlerin iklimine ilişkin bilgi edinebilmektedir." + B + "Bu parçadan aşağıdakilerden hangisi <b>çıkarılabilir</b>?",
    "Buzulun farklı derinliklerdeki katmanları farklı dönemlere ait bilgiler taşır.", ["Buzul araştırmaları yalnızca kutup bölgelerinde yapılabilir.", "Geçmişte atmosferin bileşimi hiç değişmemiştir.", "Buz örnekleri gelecekteki iklimi kesin olarak gösterir.", "Hava kabarcıkları buzun erimesine yol açar."],
    ["Derinlikler karşılaştırılarak 'geçmiş dönemler' hakkında bilgi edinilmesi, katmanların farklı dönemleri temsil ettiğini gösterir.", "'Hiç değişmemiştir' karşılaştırmanın amacıyla çelişir; diğer seçenekler parçada yer almaz ya da onu aşar."],
    "Metindeki yöntemden örtük bilgiyi çıkarır.", 75))
