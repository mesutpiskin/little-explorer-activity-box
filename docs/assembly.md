# Montaj ve kontrol kılavuzu

## Önemli güvenlik notu

Bu ev yapımı ürün sertifikalı bir oyuncak değildir. 18 aylık çocuk yalnızca
yetişkin gözetiminde kullanmalıdır. Kırılan, çatlayan, gevşeyen veya ısınan bir
parça görülürse pilleri hemen çıkarın. Lityum pil kullanmayın.

## 1. Satın almadan ve baskıdan önce ölç

Kumpasla buton gövdesini, rocker tırnakları arasındaki kesiti, LED yuvasının
geçme çapını, potansiyometrenin D milini ve 4xAA pil yuvasını ölçün. Varsayılan
değerler sırasıyla 24,2 mm, 21,2×15,2 mm, 8,2 mm, 6 mm ve en fazla
112×26×18 mm'dir. Pil yuvası tek sıra ince tip olmalıdır. Fark varsa
`tools/project_spec.py` değerlerini düzeltip
`make dimensions artwork` çalıştırın; tam gövde baskısından önce ölçüyü
düzeltmek çok daha ucuzdur.

## 2. Baskı

Önce `component-fit-test.stl` plakasını basıp LED yuvasını, büyük butonu,
rocker anahtarı, dimmer çarkını ve buzzer'ı deneyin. Ardından
`snap-fit-test.stl` tolerans numunesini basın. Tırnak rahat girip tek elle
çıkmamalıdır. Çok sıkıysa `clearance` değerini 0,10 mm artırın; gevşekse 0,10 mm
azaltın. Önerilen ayarlar: PETG, 0,20 mm katman, en az dört çevre, beş alt/üst
katman, yüzde 25 dolgu. Test plakasını ve gövdeyi ön yüzleri, kapağı dış yüzü ve
çarkı flanşı tabla üzerinde olacak şekilde basın. Katman ayrılması, sivri çapak
veya tırnak çatlağı olan parçayı kullanmayın.

## 3. Etiket

`artwork/activity-box-label-a4.pdf` dosyasını **gerçek boyut / yüzde 100**
seçeneğiyle, sayfaya sığdırmayı kapatarak basın. Önce 20 mm kontrol karesi tam
20 mm geliyor mu ölçün. Kırmızı dış kesim çizgisinden kesin; komponent
boşluklarını keskin bir maket bıçağıyla yalnızca yetişkin hazırlamalıdır.
Yüzeyi yağdan arındırın, etiketi deliklere hizalayın ve ortadan kenarlara doğru
yapıştırın.

## 4. Ön yüz parçaları

LED'leri önden yuvalarına yerleştirin; uzun bacak artı, kısa bacak/LED'in düz
kenarı eksidir. Ayırıcı ceplerin içinden bacakları geçirin. Silikon yalnızca
titreşim önleyici olabilir; mekanik tutmanın yerine geçmez. Dört büyük butonu
ve rocker anahtarı kendi somun/tırnaklarıyla arkadan kilitleyin. Çarkı arkadan
34 mm açıklığa sokun; 46 mm flanş içeride kalmalıdır. Potansiyometre milini
çarkın D yuvasına geçirin ve iç brakete sabitleyin.

## 5. Güç hattı

Pil yuvasının kırmızı kablosunu önce 1 A sigortaya, sigortadan çıkan kabloyu
SS12F15 anahtarın orta ucuna bağlayın. Anahtarın bir dış ucu artı dağıtım
hattıdır; diğer dış uç kullanılmaz. Pil yuvasının siyah kablosu ortak eksi
hattıdır. Lehimlerden önce piller takılı olmamalıdır.

## 6. Altı paralel kol

1. Artı hat → kırmızı anlık buton → 220 ohm → kırmızı LED uzun bacak; LED kısa
   bacak → eksi hat.
2. Aynı bağlantıyı sarı buton/LED için yapın.
3. Aynı bağlantıyı turuncu buton/LED için yapın.
4. Artı hat → rocker → 220 ohm → beyaz LED → eksi hat.
5. Artı hat → B1K potun birbirine bağlanmış orta ucu ve bir dış ucu → 220 ohm
   → beyaz LED → eksi hat. Potun diğer dış ucu boş kalır.
6. Artı hat → mavi anlık buton → buzzer artı; buzzer eksi → eksi hat.

Mevcut 0 ohm veya 1 ohm dirençleri LED'lerde kullanmayın. Kalıcı montajda
jumper kablo bırakmayın; çok telli kabloyu lehimleyip her açık ek yerine ısıyla
daralan makaron uygulayın. Kablo klipsleri lehimlere çekme yükü gelmeyecek
şekilde kullanılmalıdır.

## 7. Elektrik kontrolü

Piller yokken multimetrenin süreklilik moduyla artı ve eksi arasında kısa devre
olmadığını doğrulayın. Ana güç kapalıyken pil akımı sıfır olmalıdır. Her LED
kolunu ayrı çalıştırıp seri akımı ölçün; değer 20 mA altında olmalıdır. Daha
yüksekse 220 ohm yerine 270 veya 330 ohm kullanın. Buzzer'ı birkaç saniye
deneyip rahatsız edici yüksekliği azaltmak için önüne ince keçe koyabilirsiniz;
elektrik bandıyla ses deliklerini tamamen kapatmayın.

## 8. Kapatma ve son mekanik kontrol

Pil yuvasını arka kapaktaki raya yerleştirip kabloların tırnaklara gelmediğini
kontrol edin. Kapağın dilini gövdenin yivine düz biçimde bastırın; dört tırnak
oturmalıdır. Kapak, karşılıklı iki servis mandalı aynı anda ince iki aletle
bastırılmadan elle açılmamalıdır. Her buton, LED yuvası, rocker ve çarkı önden
kuvvetlice çekerek gevşeklik kontrolü yapın. İlk kullanımdan sonra ve sonra her
hafta bu kontrolü tekrarlayın.

## Devre özeti

Ayrıntılı renkli şema için `docs/circuit.svg` dosyasını açın. Devrede hiçbir
mikrodenetleyici, LM2596 veya motor sürücü kullanılmaz.
