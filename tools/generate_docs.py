"""Generate the wiring diagram, BOM, and Turkish assembly guide."""

import csv
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_spec import ELECTRICAL


def circuit_svg():
    columns = [150, 330, 510, 690, 870, 1050]
    labels = ["KIRMIZI", "SARI", "YEŞİL", "AÇ/KAPA", "DİMMER", "SES"]
    colors = ["#E84A5F", "#E0B51B", "#3DAA68", "#56A5D8", "#49B985", "#7B62B3"]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="780" viewBox="0 0 1200 780">',
        '<rect width="1200" height="780" fill="#FFFDF7"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#263548}.title{font-size:25px;font-weight:bold}.label{font-size:17px;font-weight:bold}.power{font-size:13px;font-weight:bold}.tiny{font-size:12px}.small{font-size:14px}.wire{fill:none;stroke:#263548;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}</style>',
        '<text x="40" y="40" class="title">2× (2×AA) IŞIK VE SES KUTUSU — BAĞLANTI ŞEMASI</text>',
        '<rect x="40" y="65" width="105" height="48" rx="8" fill="#F2E3A0" stroke="#263548" stroke-width="3"/>',
        '<text x="92" y="86" text-anchor="middle" class="power">YUVA A — 2×AA</text>',
        '<text x="92" y="105" text-anchor="middle" class="tiny">siyah = sistem −</text>',
        '<rect x="165" y="65" width="105" height="48" rx="8" fill="#F2E3A0" stroke="#263548" stroke-width="3"/>',
        '<text x="217" y="86" text-anchor="middle" class="power">YUVA B — 2×AA</text>',
        '<text x="217" y="105" text-anchor="middle" class="tiny">kırmızı = sistem +</text>',
        '<path class="wire" d="M 145 89 H 165"/>',
        '<text x="155" y="58" text-anchor="middle" class="small">A kırmızı → B siyah</text>',
        '<path class="wire" d="M 270 89 H 300"/>',
        '<rect x="300" y="79" width="72" height="20" rx="4" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
        '<text x="336" y="70" text-anchor="middle" class="small">1 A SİGORTA</text>',
        '<path class="wire" d="M 372 89 H 410 M 410 89 L 450 73 M 450 89 H 490"/>',
        '<circle cx="410" cy="89" r="5" fill="#263548"/><circle cx="450" cy="89" r="5" fill="#263548"/>',
        '<text x="430" y="57" text-anchor="middle" class="small">DC120 ANA GÜÇ</text>',
        '<path class="wire" d="M 490 89 H 1140 V 120 H 85"/>',
        '<text x="1145" y="112" class="label" fill="#C42D2D">+ BUS</text>',
        '<path class="wire" d="M 85 690 H 1140"/>',
        '<path class="wire" d="M 40 89 H 25 V 690 H 85"/>',
        '<text x="1145" y="697" class="label">− BUS</text>',
    ]

    for index, (x, label, color) in enumerate(zip(columns, labels, colors)):
        parts.extend([
            f'<rect x="{x - 68}" y="150" width="136" height="500" rx="18" fill="{color}" opacity="0.14"/>',
            f'<text x="{x}" y="181" text-anchor="middle" class="label">{label}</text>',
            f'<path class="wire" d="M {x} 120 V 225"/>',
        ])
        if index != 4:
            switch_label = (
                "DC184 ANLIK" if index in (0, 1)
                else "DC180 ANLIK" if index in (2, 5)
                else "DC131A (yalnız kontak)"
            )
            parts.extend([
                f'<circle cx="{x - 21}" cy="248" r="5" fill="#263548"/><circle cx="{x + 21}" cy="248" r="5" fill="#263548"/>',
                f'<path class="wire" d="M {x - 21} 248 L {x + 15} 232"/>',
                f'<path class="wire" d="M {x} 225 V 248 H {x - 21} M {x + 21} 248 H {x} V 300"/>',
                f'<text x="{x}" y="278" text-anchor="middle" class="small">{switch_label}</text>',
            ])
        else:
            parts.append(f'<path class="wire" d="M {x} 225 V 300"/>')
        if index < 4:
            parts.extend([
                f'<path class="wire" d="M {x} 300 V 320"/>',
                f'<rect class="series-resistor" x="{x - 43}" y="320" width="86" height="38" rx="7" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                f'<text x="{x}" y="345" text-anchor="middle" class="small">330 Ω / 1 W</text>',
                f'<path class="wire" d="M {x} 358 V 400"/>',
                f'<rect class="series-led" x="{x - 43}" y="400" width="86" height="50" rx="12" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                f'<circle cx="{x - 23}" cy="425" r="10" fill="{color}" stroke="#263548" stroke-width="2"/>',
                f'<path d="M {x - 28} 421 L {x - 22} 427 L {x - 17} 418" fill="none" stroke="#FFFFFF" stroke-width="2"/>',
                f'<text x="{x + 13}" y="430" text-anchor="middle" class="small">LED</text>',
                f'<path class="wire" d="M {x} 450 V 690"/>',
            ])
        elif index == 4:
            parts.extend([
                f'<path class="wire" d="M {x} 300 V 320"/>',
                f'<rect x="{x - 43}" y="320" width="86" height="38" rx="7" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                f'<text x="{x}" y="345" text-anchor="middle" class="small">1K POT</text>',
                f'<path d="M {x + 52} 312 L {x + 24} 330" stroke="#263548" stroke-width="3"/><path d="M {x + 52} 312 l -9 0 l 5 8 Z" fill="#263548"/>',
                f'<path class="wire" d="M {x} 358 V 375"/>',
                f'<rect class="series-resistor" x="{x - 43}" y="375" width="86" height="38" rx="7" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                f'<text x="{x}" y="400" text-anchor="middle" class="small">330 Ω / 1 W</text>',
                f'<path class="wire" d="M {x} 413 V 430"/>',
                f'<rect class="series-led" x="{x - 43}" y="430" width="86" height="50" rx="12" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                f'<circle cx="{x - 23}" cy="455" r="10" fill="#F4F7FF" stroke="#263548" stroke-width="2"/>',
                f'<text x="{x + 13}" y="460" text-anchor="middle" class="small">LED</text>',
                f'<path class="wire" d="M {x} 480 V 690"/>',
            ])
        else:
            parts.extend([
                f'<path class="wire" d="M {x} 300 V 395"/>',
                f'<circle cx="{x}" cy="440" r="44" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                f'<path d="M {x - 18} 440 h 13 l 15 -15 v 30 l -15 -15" fill="none" stroke="#263548" stroke-width="3"/>',
                f'<path d="M {x + 14} 430 q 16 10 0 20 M {x + 22} 419 q 30 21 0 42" fill="none" stroke="#263548" stroke-width="3"/>',
                f'<text x="{x}" y="510" text-anchor="middle" class="small">AKTİF BUZZER 5–12 V</text>',
                f'<path class="wire" d="M {x} 484 V 690"/>',
            ])

    parts.extend([
        '<text x="40" y="735" class="small">Pot bağlantısı: orta uç (süpürücü) ile kullanılan dış ucu birbirine bağla. Diğer dış uç boş kalır.</text>',
        '<text x="40" y="758" class="small">DC131A lamba ucu bağlanmaz. Önce kısa devre ve kutup kontrolü yap; sonra pilleri tak.</text>',
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


BOM_ROWS = [
    ("1", "1 A sigorta", "Kapalı yuva veya kablolu tip", "Yuva B artısına en yakın noktaya"),
    ("2", "2xAA yarı kapalı pil yuvası", "Yaklaşık 58×32×15 mm", "Seri bağlanarak 4×AA olur"),
    ("2", "DC184 anlık buton", "Kırmızı ve sarı; Ø12,0 mm test deliği", "Kırmızı/sarı LED kolları"),
    ("2", "DC180 anlık buton", "Siyah ve mavi; Ø16,0 mm test deliği", "Yeşil LED ve buzzer"),
    ("1", "DC131A aç/kapat anahtar", "Ø20,2 mm; 12 V lambalı", "Yalnız anahtar kontakları kullanılır"),
    ("1", "DC120 2P aç/kapat anahtar", "19,0×13,0 mm test kesiti", "Ana güç"),
    ("1", "1K potansiyometre", "7,0 mm burç; 6,2 mm mil yuvası", "Beyaz LED dimmeri"),
    ("10", "330 ohm 1 W direnç", "Turuncu-turuncu-kahverengi", "5 kullanım + yedekler"),
    ("4", "10 mm LED", "Kırmızı, sarı, yeşil, mavi", "Her birine ayrı 330 Ω"),
    ("1", "10 mm beyaz LED", "Şeffaf, standart iki bacaklı", "Dimmer kolu"),
    ("1", "12 mm aktif buzzer", "5–12 V, devreli", "Pasif 22 mm buzzer kullanılmaz"),
    ("2 m", "çok telli kablo", "0,22–0,50 mm²", "Kırmızı ve siyah önerilir"),
    ("1 set", "ısıyla daralan makaron", "2–4 mm", "Tüm lehim ekleri"),
    ("1 tüp", "nötr kürlenen silikon", "Elektroniğe uygun", "LED titreşim desteği; tek tutucu değildir"),
    ("baskı", "yaklaşık 450 g", "PETG filament, 1,75 mm", "Gövde, kapak, çark"),
]


ASSEMBLY = """# Montaj ve kontrol kılavuzu

## Önemli güvenlik notu

Bu ev yapımı ürün sertifikalı bir oyuncak değildir. 18 aylık çocuk yalnızca
yetişkin gözetiminde kullanmalıdır. Kırılan, çatlayan, gevşeyen veya ısınan bir
parça görülürse pilleri hemen çıkarın. Lityum pil kullanmayın. Vida olmaması,
kapağın veya parçaların düzenli çekme kontrolü gereğini ortadan kaldırmaz.

## 1. Test baskısında doğrulanan ölçüler

Komponent test kuponuyla ana delikler 10 mm LED için 10,2 mm, DC184 için
12,0 mm, DC180 için 16,0 mm ve DC131A için 20,2 mm olarak doğrulandı. Pot
burcu 7,0 mm, pot mili 6,2 mm ve DC120 kesiti 19,0×13,0 mm seçildi. Buzzer
kabı test edildi; 34 mm çark açıklığı varsayılan ölçüde bırakıldı. Yazıcı,
filament veya komponent partisi değişirse tam gövdeden önce test kuponunu
yeniden basın ve gerekirse `tools/project_spec.py` değerlerini düzeltin.

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
"""


def main():
    docs = Path("docs")
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "circuit.svg").write_text(circuit_svg(), encoding="utf-8")
    with (docs / "BOM.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["adet", "parca", "ozellik", "not"])
        writer.writerows(BOM_ROWS)
    (docs / "assembly.md").write_text(ASSEMBLY, encoding="utf-8")
    print("wrote circuit.svg, BOM.csv, and assembly.md")


if __name__ == "__main__":
    main()
