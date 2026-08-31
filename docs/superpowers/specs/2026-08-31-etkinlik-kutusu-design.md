# 18 Aylık Çocuk İçin Işık ve Ses Etkinlik Kutusu

## Amaç ve sınırlar

Bu proje, 18 aylık bir çocuğun yetişkin gözetiminde renk, neden-sonuç,
aç/kapa ve az/çok kavramlarını deneyebileceği, mikrodenetleyici içermeyen
bir masaüstü etkinlik kutusudur. Kutu; doğrudan kablolanmış LED, anahtar,
potansiyometre ve aktif buzzer devrelerinden oluşur.

Bu tasarım ev yapımı bir oyuncaktır ve EN 71 / IEC 62115 gibi oyuncak
standartlarına göre sertifikalandırılmış sayılmaz. Küçük parçalar önden
çekilerek çıkamayacak şekilde mekanik olarak tutulacak, fakat kullanım yine de
yetişkin gözetiminde olacaktır.

## Etkileşimler

Ön yüz 3 × 2 düzende altı istasyon içerir:

1. Büyük kırmızı anlık buton kırmızı LED'i yakar.
2. Büyük sarı anlık buton sarı LED'i yakar.
3. Büyük turuncu anlık buton turuncu LED'i yakar.
4. Büyük kalıcı rocker anahtar beyaz LED'i açıp kapatır.
5. Büyük, önden sökülemeyen döner çark beyaz LED'in parlaklığını değiştirir.
6. Büyük mavi anlık buton 12 mm aktif buzzer'ı çalıştırır.

Kutunun sağ yanındaki gömme SS12F15 anahtar bütün devrenin ana gücünü açar.

## Elektrik mimarisi

- Besleme: dört adet değiştirilebilir AA alkalin pil; yeni pillerle yaklaşık
  6,4 V azami çalışma gerilimi. Lityum pil kullanılmaz. NiMH pil kullanılacaksa
  mevcut 5–12 V buzzer'ın düşük gerilimde yeterince ses verdiği ayrıca denenir.
- Koruma: pil artısından hemen sonra 1 A sigorta, ardından SS12F15 ana güç
  anahtarı.
- Kırmızı, sarı ve turuncu LED kolları: anahtarlanan artı → 220 ohm / 0,25 W
  direnç → 5 mm LED → eksi.
- Rocker kolu: anahtarlanan artı → rocker → 220 ohm / 0,25 W direnç → beyaz
  LED → eksi.
- Dimmer kolu: anahtarlanan artı → B1K doğrusal potansiyometre reostası →
  220 ohm / 0,25 W sabit direnç → beyaz LED → eksi. Sabit direnç,
  potansiyometre sıfırdayken LED akımını sınırlar.
- Ses kolu: anahtarlanan artı → mavi anlık buton → 5–12 V aktif buzzer → eksi.
- Mevcut 1 ohm ve 0 ohm dirençler LED akım sınırlaması için kullanılmaz.
- Kalıcı bağlantılar lehimlenir ve ısıyla daralan makaronla yalıtılır. Gevşek
  jumper kablolar nihai montajda kullanılmaz.

Yeni alkalin piller yaklaşık 6,4 V olduğunda 220 ohm dirençle tahmini akım;
kırmızı LED'de 20 mA, beyaz LED'de 15 mA altında kalır. Nihai LED'lerin ileri
gerilimleri montajdan önce ölçülür; akım 20 mA'yı aşarsa 270–330 ohm seçilir.

## Satın alınacak parçalar

- 1 × tek sıra, kablolu 4×AA pil yuvası; dış ölçüsü en fazla 112 × 26 × 18 mm
- 4 × 24 mm panel deliğine uygun, tek parça büyük başlıklı, normalde açık
  anlık buton (kırmızı, sarı, turuncu ve mavi)
- 1 × KCD1 sınıfı iki uçlu rocker anahtar; varsayılan panel kesiti 21,2 ×
  15,2 mm
- 1 × B1K doğrusal, panel tipi potansiyometre; 6 mm D mil
- 6 × 220 ohm / 0,25 W direnç ve alternatif ayar için birkaç 270/330 ohm
  direnç
- İnce çok telli kablo, lehim ve ısıyla daralan makaron

Mevcut parçalardan 5 mm LED'ler, LED yuvaları, SS12F15 anahtar, 1 A sigorta,
sigorta yuvası ve 12 mm aktif buzzer kullanılır.

## Mekanik tasarım

### Ana ölçüler

- Dış ölçü: 200 × 160 × 52 mm
- Köşe yarıçapı: 14 mm
- Ana duvar: 2,6 mm
- Ön panel: 3,2 mm
- Arka kapak: 2,8 mm
- Zemin ve masa temasında en küçük dış radyüs: 2 mm
- Parça geçmeleri için başlangıç boşluğu: yan başına 0,25 mm; bu değer
  OpenSCAD parametresidir ve yazıcıya göre değiştirilebilir.

Model tek parça gövde olarak 220 × 220 mm veya daha büyük tablaya düz biçimde
sığar. Varsayılan baskı yönü ön yüz tabla üzerinde, açık arka yüz yukarıdır.

### Ön panel yerleşimi

Koordinat başlangıcı ön yüzün sol üst köşesidir:

| İstasyon | Merkez / kesit |
| --- | --- |
| Kırmızı LED | (40, 28), 5 mm yuva için parametrik delik |
| Kırmızı buton | (40, 57), varsayılan 24,2 mm delik |
| Sarı LED | (100, 28), 5 mm yuva için parametrik delik |
| Sarı buton | (100, 57), varsayılan 24,2 mm delik |
| Turuncu LED | (160, 28), 5 mm yuva için parametrik delik |
| Turuncu buton | (160, 57), varsayılan 24,2 mm delik |
| Beyaz LED / rocker | (40, 101) / merkez (40, 129), 21,2 × 15,2 mm |
| Beyaz LED / dimmer | (100, 101) / merkez (100, 128), çark açıklığı 34 mm |
| Buzzer delikleri / mavi buton | merkez (160, 100) / (160, 130) |

Tüm delikler kaynak dosyada parametre olarak tutulur. Satın alınan düğmelerin
gerçek kumpas ölçüsü varsayılandan farklıysa STL yeniden üretilir; STL üzerinde
elle delik büyütülmez.

### Çocuk güvenliğine yönelik tutma özellikleri

- Her LED önden standart yuvasına geçer; arkasındaki baskılı koruma cebi,
  yuva gevşese bile LED ve yuvasının dışarı çıkmasını engeller. Silikon yalnızca
  titreşim ve dönmeye karşı yardımcıdır; ana tutucu değildir.
- Potansiyometre çarkı arkadan takılan 46 mm flanşa sahiptir. Ön yüzdeki 34 mm
  açıklıktan çekilerek çıkamaz. Delikten geçirilen görünen kısmı 32 mm
  çapındadır.
- Buzzer içerideki yuvaya geçer ve ses, çapı en fazla 3 mm olan deliklerden
  çıkar.
- Ön panelde erişilebilir vida, somun, kablo veya keskin kenar yoktur.
- Kablo güzergâhlarında çekme yükünü lehim noktalarından alan baskılı klipsler
  bulunur.

### Vidasız arka kapak ve pil erişimi

Arka kapak çevresel dil-yiv ile hizalanır ve dört iç tırnakla tutulur. İki ana
tırnak karşılıklı kenarlardaki 3 mm çaplı, 12 mm derinlikteki servis
deliklerinden iki ince aletle aynı anda bastırılmadan serbest kalmaz. Pil yuvası
bu kapağın arkasındadır. Böylece kapakta vida kullanılmaz, fakat tek parmakla
veya tırnakla açılamaz.

Tırnaklar PETG için 1,2 mm kök kalınlığı, 8 mm serbest uzunluk ve 0,7 mm
kilitleme çıkıntısıyla başlar. PLA tırnakları kırılgan olabileceğinden gövde ve
kapak için PETG önerilir. İlk tam baskıdan önce yalnızca tırnak ve geçme
geometrisini içeren küçük bir tolerans numunesi basılır.

İnce, tek sıra pil yuvası arka kapağın iç tarafında `(44, 64)` başlangıç
koordinatına yerleşir. 112 × 26 mm ayak izi iki kontrol sırası arasındaki boşluğu
kullanır ve buton/potansiyometre gövdelerinin derinlik hacmine girmez.

## Grafik tasarım

Etiket, ön yüz delikleriyle birebir hizalanan 204 × 164 mm SVG olarak üretilir;
dört kenarda 2 mm taşma payı bulunur. Kesim ölçüsü 200 × 160 mm'dir.

Grafik altı renkli, yuvarlatılmış istasyon alanı içerir. Büyük geometrik
simgeler kullanılır: ışık ışınları, aç/kapa, az/çok ve ses dalgaları. Çocuğun
okuma bilmesi gerekmediği için ön yüzde küçük metin kullanılmaz. Deliklerin
etrafında en az 3 mm yapışkansız/kesilmiş güvenlik payı gösterilir.

Üretim dosyaları:

- Ölçekli ana `SVG`
- Ev/yazıhane yazıcısı için A4'e yüzde 100 ölçekte yerleştirilmiş `PDF`
- Önizleme için 300 dpi `PNG`

Yapay raster görsel yerine deterministik vektör çizim kullanılacaktır; bunun
nedeni montaj deliklerinin ve baskı ölçeğinin tam kalmasıdır.

## Üretilecek dosyalar

- `cad/activity_box.scad`: bütün ölçüleri parametreli kaynak model
- `output/stl/activity-box-body.stl`
- `output/stl/activity-box-back.stl`
- `output/stl/activity-box-dial.stl`
- `output/stl/snap-fit-test.stl`
- `artwork/activity-box-label.svg`
- `artwork/activity-box-label-a4.pdf`
- `artwork/activity-box-label-preview.png`
- `docs/circuit.svg`: renk kodlu bağlantı şeması
- `docs/BOM.csv`: parça ve satın alma listesi
- `docs/assembly.md`: baskı, lehimleme, kontrol ve birleştirme adımları

## Doğrulama

- OpenSCAD kaynakları uyarısız derlenmeli ve tüm STL dosyaları üretilebilmelidir.
- STL'ler kapalı/manifold katılar olmalı; ters yüzey veya sıfır kalınlık
  içermemelidir.
- Ana gövdenin XY sınırı 220 × 220 mm'yi aşmamalıdır.
- SVG fiziksel ölçüsü 204 × 164 mm olmalı ve delik koordinatları CAD modeliyle
  aynı parametrelerden türetilmelidir.
- A4 PDF yüzde 100 basıldığında 20 mm kontrol karesi tam 20 mm ölçülmelidir.
- Piller takılmadan önce kısa devre ve kutup testi yapılmalıdır.
- Her LED kolunun akımı ayrı ayrı ölçülmeli ve 20 mA altında olmalıdır.
- Ana güç kapalıyken akım sıfır olmalı; açıkken kablo veya dirençte belirgin
  ısınma olmamalıdır.
- Arka kapak, iki servis tırnağı aynı anda serbest bırakılmadan elle
  açılmamalıdır.
