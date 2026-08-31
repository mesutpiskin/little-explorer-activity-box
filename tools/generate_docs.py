"""Generate the wiring diagram, BOM, and Turkish assembly guide."""

import csv
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.project_spec import ELECTRICAL


def circuit_svg():
    columns = [150, 330, 510, 690, 870, 1050]
    labels = ["KIRMIZI", "SARI", "TURUNCU", "AÇ/KAPA", "DİMMER", "SES"]
    colors = ["#E84A5F", "#E0B51B", "#F08A24", "#56A5D8", "#49B985", "#7B62B3"]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="780" viewBox="0 0 1200 780">',
        '<rect width="1200" height="780" fill="#FFFDF7"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#263548}.title{font-size:25px;font-weight:bold}.label{font-size:17px;font-weight:bold}.small{font-size:14px}.wire{fill:none;stroke:#263548;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}</style>',
        '<text x="40" y="42" class="title">4×AA IŞIK VE SES KUTUSU — BAĞLANTI ŞEMASI</text>',
        '<rect x="40" y="75" width="82" height="62" rx="8" fill="#F2E3A0" stroke="#263548" stroke-width="3"/>',
        '<text x="81" y="101" text-anchor="middle" class="label">4×AA</text>',
        '<text x="81" y="124" text-anchor="middle" class="small">6,4 V maks.</text>',
        '<path class="wire" d="M 122 92 H 164"/>',
        '<rect x="164" y="82" width="72" height="20" rx="4" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
        '<text x="200" y="73" text-anchor="middle" class="small">1 A SİGORTA</text>',
        '<path class="wire" d="M 236 92 H 285 M 285 92 L 325 76 M 325 92 H 365"/>',
        '<circle cx="285" cy="92" r="5" fill="#263548"/><circle cx="325" cy="92" r="5" fill="#263548"/>',
        '<text x="325" y="62" text-anchor="middle" class="small">SS12F15 ANA GÜÇ</text>',
        '<path class="wire" d="M 365 92 H 1140 V 120 H 85"/>',
        '<text x="1145" y="112" class="label" fill="#C42D2D">+ BUS</text>',
        '<path class="wire" d="M 85 690 H 1140"/>',
        '<path class="wire" d="M 81 137 V 690 H 85"/>',
        '<text x="1145" y="697" class="label">− BUS</text>',
    ]

    for index, (x, label, color) in enumerate(zip(columns, labels, colors)):
        parts.extend([
            f'<rect x="{x - 68}" y="150" width="136" height="500" rx="18" fill="{color}" opacity="0.14"/>',
            f'<text x="{x}" y="181" text-anchor="middle" class="label">{label}</text>',
            f'<path class="wire" d="M {x} 120 V 225"/>',
            f'<circle cx="{x - 21}" cy="248" r="5" fill="#263548"/><circle cx="{x + 21}" cy="248" r="5" fill="#263548"/>',
            f'<path class="wire" d="M {x - 21} 248 L {x + 15} 232"/>',
            f'<path class="wire" d="M {x} 225 V 248 H {x - 21} M {x + 21} 248 H {x} V 300"/>',
        ])
        switch_label = "ANLIK BUTON" if index in (0, 1, 2, 5) else ("ROCKER" if index == 3 else "B1K POT")
        parts.append(f'<text x="{x}" y="278" text-anchor="middle" class="small">{switch_label}</text>')
        if index < 4:
            parts.extend([
                f'<path class="wire" d="M {x} 300 V 335"/>',
                f'<path d="M {x - 25} 335 h 10 l 8 -13 l 14 26 l 14 -26 l 8 13 h 10" fill="none" stroke="#263548" stroke-width="3"/>',
                f'<text x="{x}" y="375" text-anchor="middle" class="small">220 Ω</text>',
                f'<path class="wire" d="M {x} 335 V 420"/>',
                f'<path d="M {x - 20} 420 H {x + 20} L {x} 448 Z" fill="none" stroke="#263548" stroke-width="3"/>',
                f'<path class="wire" d="M {x - 21} 455 H {x + 21} M {x} 455 V 690"/>',
                f'<path d="M {x + 18} 414 l 18 -16 M {x + 27} 423 l 18 -16" stroke="{color}" stroke-width="3"/>',
                f'<text x="{x}" y="495" text-anchor="middle" class="small">LED (uzun bacak +)</text>',
            ])
        elif index == 4:
            parts.extend([
                f'<path class="wire" d="M {x} 300 V 325"/>',
                f'<rect x="{x - 25}" y="325" width="50" height="60" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                f'<path d="M {x + 42} 340 L {x + 5} 355" stroke="#263548" stroke-width="3"/><path d="M {x + 42} 340 l -9 -2 l 4 9 Z" fill="#263548"/>',
                f'<text x="{x}" y="410" text-anchor="middle" class="small">0–1000 Ω + 220 Ω</text>',
                f'<path class="wire" d="M {x} 385 V 430"/>',
                f'<path d="M {x - 20} 430 H {x + 20} L {x} 458 Z" fill="none" stroke="#263548" stroke-width="3"/>',
                f'<path class="wire" d="M {x - 21} 465 H {x + 21} M {x} 465 V 690"/>',
                f'<text x="{x}" y="500" text-anchor="middle" class="small">BEYAZ LED</text>',
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
        '<text x="40" y="758" class="small">Önce multimetre ile kısa devre ve kutup kontrolü yap; sonra pilleri tak.</text>',
        '</svg>',
    ])
    return "\n".join(parts) + "\n"


BOM_ROWS = [
    ("mevcut", "1", "1 A sigorta", "Uygun kapalı yuvasıyla", "Pil artısına en yakın noktaya"),
    ("satın al", "1", "4xAA pil yuvası", "Tek sıra, kablolu, en çok 112×26×18 mm", "Alkalin AA pil için"),
    ("satın al", "4", "24 mm anlık buton", "NO, tek parça büyük başlık", "Kırmızı/sarı/turuncu/mavi"),
    ("satın al", "1", "KCD1 rocker anahtar", "2 uç, 21,2×15,2 mm kesit", "Beyaz LED kolu"),
    ("satın al", "1", "B1K potansiyometre", "Doğrusal, panel tipi, 6 mm D mil", "Dimmer"),
    ("satın al", "6", "220 ohm direnç", "0,25 W", "5 kullanım + 1 yedek"),
    ("opsiyonel", "4", "270/330 ohm direnç", "0,25 W", "LED akımı yüksekse"),
    ("mevcut", "5", "5 mm LED", "Kırmızı, sarı, turuncu, 2×beyaz", "İleri gerilimi ölç"),
    ("mevcut", "5", "5 mm LED yuvası", "Tek parça", "Gerçek delik çapını ölç"),
    ("mevcut", "1", "SS12F15 anahtar", "SPDT", "Gömme ana güç"),
    ("mevcut", "1", "12 mm aktif buzzer", "5–12 V", "6 V ile dene"),
    ("satın al", "2 m", "çok telli kablo", "0,22–0,50 mm²", "İki renk önerilir"),
    ("satın al", "1 set", "ısıyla daralan makaron", "2–4 mm", "Tüm lehim ekleri"),
    ("baskı", "yaklaşık 450 g", "PETG filament", "1,75 mm", "Gövde, kapak, çark"),
]


ASSEMBLY = """# Montaj ve kontrol kılavuzu

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

Önce `snap-fit-test.stl` tolerans numunesini basın. Tırnak rahat girip tek elle
çıkmamalıdır. Çok sıkıysa `clearance` değerini 0,10 mm artırın; gevşekse 0,10 mm
azaltın. Önerilen ayarlar: PETG, 0,20 mm katman, en az dört çevre, beş alt/üst
katman, yüzde 25 dolgu. Gövdeyi ön yüzü, kapağı dış yüzü ve çarkı flanşı tabla
üzerinde olacak şekilde basın. Katman ayrılması, sivri çapak veya tırnak çatlağı
olan parçayı kullanmayın.

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
"""


def main():
    docs = Path("docs")
    docs.mkdir(parents=True, exist_ok=True)
    (docs / "circuit.svg").write_text(circuit_svg(), encoding="utf-8")
    with (docs / "BOM.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["durum", "adet", "parca", "ozellik", "not"])
        writer.writerows(BOM_ROWS)
    (docs / "assembly.md").write_text(ASSEMBLY, encoding="utf-8")
    print("wrote circuit.svg, BOM.csv, and assembly.md")


if __name__ == "__main__":
    main()
