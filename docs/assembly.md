# Montaj ve kontrol kılavuzu

## Önemli güvenlik notu

Bu ev yapımı ürün sertifikalı bir oyuncak değildir. 18 aylık çocuk yalnızca
yetişkin gözetiminde kullanmalıdır. Kırılan, çatlayan, gevşeyen veya ısınan bir
parça görülürse pilleri hemen çıkarın. Lityum pil kullanmayın. Vida olmaması,
kapağın veya parçaların düzenli çekme kontrolü gereğini ortadan kaldırmaz.

## 1. Parçalar gelmeden kullanılan ölçüler

Üretici çizimleri temel alınarak ana delikler 10 mm LED için 10,2 mm, DC184
için 12,2 mm, DC180 için 16,2 mm ve DC131A için 20,2 mm seçildi. DC120 yan
kesiti şimdilik 19,2×13,2 mm; 1K pot mili 6,0 mm kabul edildi. Her üretim
partisinde küçük fark olabileceği için tam gövdeyi basmadan önce test kuponunu
basın. Parçalar gelince kumpasla ölçüp gerekirse `tools/project_spec.py`
değerlerini düzeltin ve `make dimensions artwork` çalıştırın.

## 2. Önce komponent test kuponu

`component-fit-test.stl` yatay tutulduğunda delikler soldan sağa şöyledir:

![Komponent test plakası kılavuzu](component-fit-test-guide.png)

- Üst sıra: LED 10,0 / 10,2; DC184 12,0 / 12,2; DC180 16,0 / 16,2;
  DC131A 20,0 / 20,2; en sağda 12 mm buzzer kabı.
- Alt sıra: pot burcu 7,0 / 7,2; mil yuvası 5,8 / 6,0 / 6,2;
  DC120 19,0×13,0 / 19,4×13,4; 34 mm çark açıklığı.

Parça zorlamadan girmeli, somun veya tırnak bütün yüzeye oturmalı ve elle
çekildiğinde çıkmamalıdır. En iyi seçeneğin ölçüsünü `project_spec.py` içine
aktararak ana modeli yeniden üretin. İki 2×AA pil yuvası için ayrılan ortak
bölme 62×68×18 mm'dir; bu ölçü de parçalar gelince doğrulanmalıdır.

Ardından `snap-fit-test.stl` tolerans numunesini basın. Tırnak rahat girip tek
elle çıkmamalıdır. Çok sıkıysa `clearance` değerini 0,10 mm artırın; gevşekse
0,10 mm azaltın. Önerilen ayarlar: PETG, 0,20 mm katman, en az dört çevre, beş
alt/üst katman ve yüzde 25 dolgu. Katman ayrılması, sivri çapak veya tırnak
çatlağı olan parçayı kullanmayın.

## 3. Etiket

`artwork/activity-box-label-a4.pdf` dosyasını **gerçek boyut / yüzde 100**
seçeneğiyle, sayfaya sığdırmayı kapatarak basın. Önce 20 mm kontrol karesi tam
20 mm geliyor mu ölçün. Kırmızı dış kesim çizgisinden kesin; komponent
boşluklarını yalnızca yetişkin hazırlamalıdır. Yüzeyi yağdan arındırın, etiketi
deliklere hizalayın ve ortadan kenarlara doğru yapıştırın.

## 4. Ön yüz parçaları

10 mm LED'leri kutunun içinden dışarı doğru yerleştirin. Lens 10,2 mm delikten
çıkar, daha geniş LED flanşı içeride kalıp dışarı çekilmeyi mekanik olarak
engeller. Açık baskı halkası flanş çevresini korur. Halkaya az miktarda
nötr kürlenen silikon uygulayın; silikon yalnızca titreşim desteğidir, tek mekanik
tutucu değildir. Uzun bacak artı, kısa bacak veya düz kenar eksidir.

Kırmızı ve sarı DC184'leri, siyah ve mavi DC180'leri somunlarıyla sabitleyin.
DC131A'yı 20,2 mm deliğe, kendi somunuyla takın. Çarkı içeriden 34 mm açıklığa
sokun; 46 mm flanşı içeride kalmalıdır. 1K potu baskı köprüsüne somunlayın ve
mil için kuponda seçilen yuva çapını kullanın. Buzzer'ı açık yüzü ses deliklerine
bakacak biçimde baskı kabına yerleştirip kenarından sabitleyin.

## 5. İki pil yuvasını seri bağlama ve ana güç

Piller takılı değilken iki pil yuvasını seri bağlayın:

1. Yuva A siyah kablo → sistem eksi dağıtım hattı.
2. Yuva A kırmızı kablo → Yuva B siyah kablo; ek yerini lehimleyip makaronla
   tamamen kapatın.
3. Yuva B kırmızı kablo → 1 A sigorta → DC120 2P ana güç anahtarı → sistem
   artı dağıtım hattı.

Bu bağlantı dört AA pili seri yapar: nominal 6 V, taze alkalin pillerle en çok
yaklaşık 6,4 V. İki pil yuvasına da aynı marka, tip ve dolulukta pil takın.

## 6. Altı paralel kol

1. Artı hat → kırmızı DC184 → 330 ohm 1 W → kırmızı LED uzun bacak; LED kısa
   bacak → eksi hat.
2. Artı hat → sarı DC184 → 330 ohm 1 W → sarı LED → eksi hat.
3. Artı hat → siyah DC180 → 330 ohm 1 W → yeşil LED → eksi hat.
4. Artı hat → DC131A anahtar kontakları → 330 ohm 1 W → mavi LED → eksi hat.
   DC131A'nın 12 V lamba ucu boş kalır. Pin dizilimini varsaymayın; kullanılacak
   iki anahtar kontağını multimetrenin süreklilik moduyla bulun.
5. Artı hat → 1K potun birbirine bağlı orta ucu ve bir dış ucu → 330 ohm 1 W
   → beyaz LED → eksi hat. Potun diğer dış ucu boş kalır.
6. Artı hat → mavi DC180 → aktif buzzer artı; buzzer eksi → eksi hat.

Dirençlerin yönü yoktur; her LED kendi 330 ohm direncini kullanır. 1 W direnç
elektriksel olarak uygundur, yalnızca 0,25 W tipten fiziksel olarak büyüktür.
Kalıcı oyuncakta breadboard kullanmayın ve jumper kablo bırakmayın. Çok telli
kabloyu lehimleyip her açık ek yerine ısıyla daralan makaron uygulayın.

## 7. Elektrik kontrolü

Piller yokken artı ve eksi arasında kısa devre olmadığını multimetreyle
doğrulayın. Ana güç kapalıyken pil akımı sıfır olmalıdır. Taze pillerle teorik
en yüksek LED akımları kırmızıda yaklaşık 13,3 mA, sarıda 13,0 mA, yeşil/mavi/
beyazda 10,3 mA'dır; her kolu ayrı çalıştırıp ölçülen değerin 20 mA altında
olduğunu kontrol edin. Buzzer'ı birkaç saniye deneyin; sesi fazla yüksekse önüne
ince keçe koyun, ses deliklerini tamamen kapatmayın.

## 8. Kapatma ve son mekanik kontrol

İki pil yuvasını arka kapaktaki ayrı raylara yerleştirip kabloların tırnaklara
gelmediğini kontrol edin. Kapağın dilini gövdenin yivine düz biçimde bastırın;
dört tırnak oturmalıdır. Kapak, karşılıklı iki servis mandalı aynı anda ince iki
aletle bastırılmadan elle açılmamalıdır. Her buton, LED, anahtar ve çarkı önden
kuvvetlice çekerek gevşeklik kontrolü yapın. İlk kullanımdan sonra ve ardından
her hafta bu kontrolü tekrarlayın.

## Kullanılmayan satın alınmış parçalar

Mini breadboardlar, 22 mm devresiz buzzer, DHT11, 4,7K/22K potlar, toggle
anahtarlar ve diğer ışıklı anahtarlar bu basit devrede kullanılmaz. Ayrıntılı
renkli şema `docs/circuit.svg` dosyasındadır; mikrodenetleyici veya elektronik
kart gerekmez.
