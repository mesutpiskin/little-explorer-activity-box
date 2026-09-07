"""Generate English and Turkish wiring, BOM, and assembly documentation."""

import csv
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools.font_assets import svg_font_faces


CIRCUIT_COPY = {
    "en": {
        "branches": ("RED", "YELLOW", "GREEN", "ON/OFF", "DIMMER", "SOUND"),
        "title": "2× (2×AA) LIGHT AND SOUND BOX — WIRING DIAGRAM",
        "holder_a": "HOLDER A — 2×AA",
        "holder_b": "HOLDER B — 2×AA",
        "system_minus": "black = system −",
        "system_plus": "red = system +",
        "series_link": "A red → B black",
        "fuse": "1 A FUSE",
        "main_power": "DC120 MAIN POWER",
        "dc184": "DC184 MOMENTARY",
        "dc180": "DC180 MOMENTARY",
        "dc131a": "DC131A (contacts only)",
        "buzzer": "ACTIVE BUZZER 5–12 V",
        "pot_note": "Pot wiring: join the wiper to the outer terminal in use. Leave the other outer terminal open.",
        "switch_note": "Do not connect the DC131A lamp terminal. Check polarity and shorts before installing batteries.",
    },
    "tr": {
        "branches": ("KIRMIZI", "SARI", "YEŞİL", "AÇ/KAPA", "DİMMER", "SES"),
        "title": "2× (2×AA) IŞIK VE SES KUTUSU — BAĞLANTI ŞEMASI",
        "holder_a": "YUVA A — 2×AA",
        "holder_b": "YUVA B — 2×AA",
        "system_minus": "siyah = sistem −",
        "system_plus": "kırmızı = sistem +",
        "series_link": "A kırmızı → B siyah",
        "fuse": "1 A SİGORTA",
        "main_power": "DC120 ANA GÜÇ",
        "dc184": "DC184 ANLIK",
        "dc180": "DC180 ANLIK",
        "dc131a": "DC131A (yalnız kontak)",
        "buzzer": "AKTİF BUZZER 5–12 V",
        "pot_note": "Pot bağlantısı: orta uç (süpürücü) ile kullanılan dış ucu birbirine bağla. Diğer dış uç boş kalır.",
        "switch_note": "DC131A lamba ucu bağlanmaz. Önce kısa devre ve kutup kontrolü yap; sonra pilleri tak.",
    },
}


def circuit_svg(locale="en"):
    copy = CIRCUIT_COPY[locale]
    font_css = svg_font_faces(
        "../../assets/fonts" if locale == "tr" else "../assets/fonts"
    )
    columns = [150, 330, 510, 690, 870, 1050]
    colors = ["#E84A5F", "#E0B51B", "#3DAA68", "#56A5D8", "#49B985", "#7B62B3"]
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="780" viewBox="0 0 1200 780">',
        '<rect width="1200" height="780" fill="#FFFDF7"/>',
        f"<style>{font_css}text{{font-family:'DejaVu Sans',sans-serif;fill:#263548}}.title{{font-size:25px;font-weight:bold}}.label{{font-size:17px;font-weight:bold}}.power{{font-size:13px;font-weight:bold}}.tiny{{font-size:12px}}.small{{font-size:14px}}.wire{{fill:none;stroke:#263548;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}}</style>",
        f'<text x="40" y="40" class="title">{copy["title"]}</text>',
        '<rect x="40" y="65" width="105" height="48" rx="8" fill="#F2E3A0" stroke="#263548" stroke-width="3"/>',
        f'<text x="92" y="86" text-anchor="middle" class="power">{copy["holder_a"]}</text>',
        f'<text x="92" y="105" text-anchor="middle" class="tiny">{copy["system_minus"]}</text>',
        '<rect x="165" y="65" width="105" height="48" rx="8" fill="#F2E3A0" stroke="#263548" stroke-width="3"/>',
        f'<text x="217" y="86" text-anchor="middle" class="power">{copy["holder_b"]}</text>',
        f'<text x="217" y="105" text-anchor="middle" class="tiny">{copy["system_plus"]}</text>',
        '<path class="wire" d="M 145 89 H 165"/>',
        f'<text x="155" y="58" text-anchor="middle" class="small">{copy["series_link"]}</text>',
        '<path class="wire" d="M 270 89 H 300"/>',
        '<rect x="300" y="79" width="72" height="20" rx="4" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
        f'<text x="336" y="70" text-anchor="middle" class="small">{copy["fuse"]}</text>',
        '<path class="wire" d="M 372 89 H 410 M 410 89 L 450 73 M 450 89 H 490"/>',
        '<circle cx="410" cy="89" r="5" fill="#263548"/><circle cx="450" cy="89" r="5" fill="#263548"/>',
        f'<text x="430" y="57" text-anchor="middle" class="small">{copy["main_power"]}</text>',
        '<path class="wire" d="M 490 89 H 1140 V 120 H 85"/>',
        '<text x="1145" y="112" class="label" fill="#C42D2D">+ BUS</text>',
        '<path class="wire" d="M 85 690 H 1140"/>',
        '<path class="wire" d="M 40 89 H 25 V 690 H 85"/>',
        '<text x="1145" y="697" class="label">− BUS</text>',
    ]

    for index, (x, label, color) in enumerate(
        zip(columns, copy["branches"], colors)
    ):
        parts.extend(
            [
                f'<rect x="{x - 68}" y="150" width="136" height="500" rx="18" fill="{color}" opacity="0.14"/>',
                f'<text x="{x}" y="181" text-anchor="middle" class="label">{label}</text>',
                f'<path class="wire" d="M {x} 120 V 225"/>',
            ]
        )
        if index != 4:
            switch_label = (
                copy["dc184"]
                if index in (0, 1)
                else copy["dc180"]
                if index in (2, 5)
                else copy["dc131a"]
            )
            parts.extend(
                [
                    f'<circle cx="{x - 21}" cy="248" r="5" fill="#263548"/><circle cx="{x + 21}" cy="248" r="5" fill="#263548"/>',
                    f'<path class="wire" d="M {x - 21} 248 L {x + 15} 232"/>',
                    f'<path class="wire" d="M {x} 225 V 248 H {x - 21} M {x + 21} 248 H {x} V 300"/>',
                    f'<text x="{x}" y="278" text-anchor="middle" class="small">{switch_label}</text>',
                ]
            )
        else:
            parts.append(f'<path class="wire" d="M {x} 225 V 300"/>')
        if index < 4:
            parts.extend(
                [
                    f'<path class="wire" d="M {x} 300 V 320"/>',
                    f'<rect class="series-resistor" x="{x - 43}" y="320" width="86" height="38" rx="7" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                    f'<text x="{x}" y="345" text-anchor="middle" class="small">330 Ω / 1 W</text>',
                    f'<path class="wire" d="M {x} 358 V 400"/>',
                    f'<rect class="series-led" x="{x - 43}" y="400" width="86" height="50" rx="12" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                    f'<circle cx="{x - 23}" cy="425" r="10" fill="{color}" stroke="#263548" stroke-width="2"/>',
                    f'<path d="M {x - 28} 421 L {x - 22} 427 L {x - 17} 418" fill="none" stroke="#FFFFFF" stroke-width="2"/>',
                    f'<text x="{x + 13}" y="430" text-anchor="middle" class="small">LED</text>',
                    f'<path class="wire" d="M {x} 450 V 690"/>',
                ]
            )
        elif index == 4:
            parts.extend(
                [
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
                ]
            )
        else:
            parts.extend(
                [
                    f'<path class="wire" d="M {x} 300 V 395"/>',
                    f'<circle cx="{x}" cy="440" r="44" fill="#FFFFFF" stroke="#263548" stroke-width="3"/>',
                    f'<path d="M {x - 18} 440 h 13 l 15 -15 v 30 l -15 -15" fill="none" stroke="#263548" stroke-width="3"/>',
                    f'<path d="M {x + 14} 430 q 16 10 0 20 M {x + 22} 419 q 30 21 0 42" fill="none" stroke="#263548" stroke-width="3"/>',
                    f'<text x="{x}" y="510" text-anchor="middle" class="small">{copy["buzzer"]}</text>',
                    f'<path class="wire" d="M {x} 484 V 690"/>',
                ]
            )

    parts.extend(
        [
            f'<text x="40" y="735" class="small">{copy["pot_note"]}</text>',
            f'<text x="40" y="758" class="small">{copy["switch_note"]}</text>',
            "</svg>",
        ]
    )
    return "\n".join(parts) + "\n"


BOM_HEADERS = {
    "en": ("quantity", "part", "specification", "use"),
    "tr": ("adet", "parca", "ozellik", "not"),
}
BOM_ROWS = {
    "en": [
        ("1", "1 A fuse", "Enclosed holder or inline type", "As close as possible to Holder B positive"),
        ("2", "2×AA semi-enclosed battery holder", "Approx. 58×32×15 mm", "Series connection for 4×AA"),
        ("4", "AA alkaline battery", "1.5 V; matching brand and state of charge", "6 V nominal supply"),
        ("2", "DC184 momentary push button", "Red and yellow; Ø12.0 mm tested hole", "Red and yellow LED branches"),
        ("2", "DC180 momentary push button", "Black and blue; Ø16.0 mm tested hole", "Green LED and buzzer"),
        ("1", "DC131A on/off switch", "Ø20.2 mm; 12 V illuminated type", "Use switch contacts only"),
        ("1", "DC120 2P on/off switch", "19.0×13.0 mm tested cutout", "Main power"),
        ("1", "1K potentiometer", "7.0 mm bushing; 6.2 mm shaft socket", "White LED dimmer"),
        ("10", "330 ohm 1 W resistor", "Orange-orange-brown", "5 used plus spares"),
        ("4", "10 mm LED", "Red, yellow, green, blue", "One 330 Ω resistor per LED"),
        ("1", "10 mm white LED", "Clear, standard two-lead", "Dimmer branch"),
        ("1", "12 mm active buzzer", "5–12 V, self-driven", "Do not use the passive 22 mm buzzer"),
        ("2 m", "stranded wire", "0.22–0.50 mm²", "Red and black recommended"),
        ("1 set", "heat-shrink tubing", "2–4 mm", "Insulate every solder joint"),
        ("1 tube", "neutral-cure silicone", "Electronics-safe", "LED vibration support; not the sole retainer"),
        ("print", "approximately 450 g", "1.75 mm PETG filament", "Body, back plate, and dial"),
    ],
    "tr": [
        ("1", "1 A sigorta", "Kapalı yuva veya kablolu tip", "Yuva B artısına en yakın noktaya"),
        ("2", "2×AA yarı kapalı pil yuvası", "Yaklaşık 58×32×15 mm", "Seri bağlanarak 4×AA olur"),
        ("4", "AA alkalin pil", "1,5 V; aynı marka ve dolulukta", "Nominal 6 V besleme"),
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
    ],
}


ASSEMBLY_EN = """# Assembly and verification guide

## Important safety notice

This community hardware project is not a certified toy. A child aged 18
months must use it only under direct adult supervision. Remove the batteries
immediately if any part cracks, loosens, or becomes warm. Do not use lithium
batteries. A screwless enclosure still requires regular pull testing of the
back plate and every exposed component.

## 1. Verified fit dimensions

The component coupon confirmed 10.2 mm for 10 mm LEDs, 12.0 mm for DC184,
16.0 mm for DC180, and 20.2 mm for DC131A. The selected potentiometer sizes
are a 7.0 mm bushing hole and a 6.2 mm shaft socket. The DC120 cutout is
19.0×13.0 mm. The buzzer cup was tested and the dial opening remains 34 mm.
Print the coupon again whenever the printer, filament, or component batch
changes, then update `tools/project_spec.py` if needed.

## 2. Print the component coupon first

With `component-fit-test.stl` horizontal, read the openings from left to right:

![Component fit-test guide](component-fit-test-guide.png)

- Top row: LED 10.0 / 10.2; DC184 12.0 / 12.2; DC180 16.0 / 16.2;
  DC131A 20.0 / 20.2; 12 mm buzzer cup at the far right.
- Bottom row: pot bushing 7.0 / 7.2; shaft socket 5.8 / 6.0 / 6.2;
  DC120 19.0×13.0 / 19.4×13.4; 34 mm dial opening.

The part should enter without force while its nut or clips seat fully. It must
not pull out by hand. Transfer the best dimension to `tools/project_spec.py`
before regenerating the body. The shared bay for two 2×AA holders measures
62×68×18 mm and must also be checked against the purchased parts.

Print `snap-fit-test.stl` next. The tab should engage easily but resist opening
with one hand. Increase `clearance` by 0.10 mm if too tight or reduce it by
0.10 mm if loose. Recommended print settings: PETG, 0.20 mm layers, at least
four walls, five top/bottom layers, and 25% infill. Reject parts with sharp
burrs, layer separation, or cracked clips.

## 3. Apply the label

Print `artwork/activity-box-label-a4.pdf` at **actual size / 100%** with
“fit to page” disabled. Verify that the control square measures exactly 20 mm.
For ordinary white adhesive paper, keep mirror/transfer printing disabled; the
printed face points outward. Cut on the red trim line and have an adult remove
the component openings. Degrease the panel, align the label to the holes, and
apply it from the center outward.

## 4. Install front-panel components

![Component placement guide](component-placement-guide.png)

Insert each 10 mm LED from inside the enclosure. The lens passes through the
10.2 mm hole while the wider flange remains inside as the mechanical retainer.
Apply a small amount of neutral-cure silicone around the printed guard for
vibration support only. Keep silicone away from the lens. The long lead is
positive; the short lead or flat edge is negative.

Secure the red and yellow DC184 buttons and the black and blue DC180 buttons
with their nuts. Fit the DC131A in the 20.2 mm opening. Insert the dial from
inside the 34 mm opening; its 36 mm diameter, 4 mm thick flange remains captive
and clears the LED guard. Fasten the 1K pot to the printed bridge, using the
shaft socket selected with the coupon. Place the buzzer in its cup with its
opening toward the sound holes and retain it only around the edge.

## 5. Wire the battery holders and main power

With all batteries removed, connect the holders in series:

1. Holder A black wire → system negative bus.
2. Holder A red wire → Holder B black wire; solder and fully cover the joint
   with heat-shrink tubing.
3. Holder B red wire → 1 A fuse → DC120 2P main switch → system positive bus.

This produces four AA cells in series: 6 V nominal and approximately 6.4 V
with fresh alkaline cells. Use matching cells of the same brand, chemistry,
and state of charge in both holders.

## 6. Wire the six parallel branches

1. Positive → red DC184 → 330 ohm 1 W → red LED long lead; short lead → negative.
2. Positive → yellow DC184 → 330 ohm 1 W → yellow LED → negative.
3. Positive → black DC180 → 330 ohm 1 W → green LED → negative.
4. Positive → DC131A switch contacts → 330 ohm 1 W → blue LED → negative.
   Leave the DC131A 12 V lamp terminal disconnected. Do not assume pin order;
   identify the two switch contacts with a multimeter in continuity mode.
5. Positive → joined pot wiper and one outer terminal → 330 ohm 1 W → white
   LED → negative. Leave the other outer pot terminal disconnected.
6. Positive → blue DC180 → active buzzer positive; buzzer negative → negative.

Resistors have no polarity, and every LED requires its own 330 ohm resistor.
The 1 W resistor is electrically suitable but physically larger than a 0.25 W
part. Do not leave breadboards or loose jumper wires in the finished product.
Use stranded wire, solder every joint, and cover all exposed conductors with
heat-shrink tubing.

## 7. Electrical verification

With batteries removed, use a multimeter to verify there is no short between
the positive and negative buses. Battery current must be zero when DC120 is
off. With fresh cells, theoretical maximum LED currents are approximately
13.3 mA red, 13.0 mA yellow, and 10.3 mA green/blue/white. Test one branch at a
time and confirm each measured LED current stays below 20 mA. Sound the buzzer
for only a few seconds; if it is too loud, place thin felt in front without
blocking every sound hole.

## 8. Close and inspect the enclosure

Place the two battery holders in their separate rear rails and keep wires away
from all clips. Press the back plate tongue squarely into the body groove until
all four clips engage. The back must not open by hand unless both opposing
service latches are pressed at the same time with two thin tools. Pull-test
every button, LED, switch, and the dial before each use. Do not give the box to
the child if any part moves, cracks, or loosens.
"""


ASSEMBLY_TR = """# Montaj ve kontrol kılavuzu

## Önemli güvenlik notu

Bu topluluk donanım projesi sertifikalı bir oyuncak değildir. 18 aylık çocuk
yalnızca bir yetişkinin doğrudan gözetiminde kullanmalıdır. Kırılan, çatlayan,
gevşeyen veya ısınan bir parça görülürse pilleri hemen çıkarın. Lityum pil
kullanmayın. Vida kullanılmaması, kapağın ve dış parçaların düzenli çekme
kontrolü gereğini ortadan kaldırmaz.

## 1. Doğrulanan geçme ölçüleri

Komponent kuponunda 10 mm LED için 10,2 mm, DC184 için 12,0 mm, DC180 için
16,0 mm ve DC131A için 20,2 mm doğrulandı. Pot burcu 7,0 mm, pot mili 6,2 mm,
DC120 kesiti 19,0×13,0 mm'dir. Buzzer kabı test edildi; çark açıklığı 34 mm'dir.
Yazıcı, filament veya komponent partisi değişirse tam gövdeden önce kuponu
yeniden basın ve gerekirse `tools/project_spec.py` değerlerini düzeltin.

## 2. Önce komponent test kuponunu basın

`component-fit-test.stl` yatay tutulduğunda delikler soldan sağa şöyledir:

![Komponent test plakası kılavuzu](component-fit-test-guide.png)

- Üst sıra: LED 10,0 / 10,2; DC184 12,0 / 12,2; DC180 16,0 / 16,2;
  DC131A 20,0 / 20,2; en sağda 12 mm buzzer kabı.
- Alt sıra: pot burcu 7,0 / 7,2; mil yuvası 5,8 / 6,0 / 6,2;
  DC120 19,0×13,0 / 19,4×13,4; 34 mm çark açıklığı.

Parça zorlamadan girmeli, somun veya tırnak bütün yüzeye oturmalı ve elle
çekildiğinde çıkmamalıdır. En iyi ölçüyü `tools/project_spec.py` içine aktarıp
ana modeli yeniden üretin. İki 2×AA pil yuvasının ortak bölmesi 62×68×18 mm'dir;
bu ölçüyü de satın alınan parçalarla doğrulayın.

Ardından `snap-fit-test.stl` tolerans numunesini basın. Tırnak rahat girip tek
elle çıkmamalıdır. Çok sıkıysa `clearance` değerini 0,10 mm artırın; gevşekse
0,10 mm azaltın. Önerilen ayarlar: PETG, 0,20 mm katman, en az dört çevre, beş
alt/üst katman ve yüzde 25 dolgu. Katman ayrılması, sivri çapak veya tırnak
çatlağı olan parçayı kullanmayın.

## 3. Etiketi uygulayın

`artwork/tr/activity-box-label-a4.pdf` dosyasını **gerçek boyut / yüzde 100**
seçeneğiyle, sayfaya sığdırmayı kapatarak basın. Kontrol karesinin tam 20 mm
olduğunu ölçün. Normal beyaz yapışkanlı kâğıtta ayna/transfer seçeneği kapalı
olmalı; baskılı yüz dışa bakmalıdır. Kırmızı kesim çizgisinden kesin ve
komponent boşluklarını yalnızca bir yetişkin çıkarsın. Yüzeyi yağdan arındırın,
etiketi deliklere hizalayın ve ortadan kenarlara doğru yapıştırın.

## 4. Ön panel bileşenlerini takın

![Bileşen yerleşim şeması](component-placement-guide.png)

10 mm LED'leri kutunun içinden dışarı doğru yerleştirin. Lens 10,2 mm delikten
çıkar; geniş LED flanşı içeride mekanik tutucu olarak kalır. Baskı koruma
halkasına yalnız titreşim desteği için az miktarda nötr kürlenen silikon sürün.
Lense silikon sürmeyin. Uzun bacak artı, kısa bacak veya düz kenar eksidir.

Kırmızı ve sarı DC184'leri, siyah ve mavi DC180'leri somunlarıyla sabitleyin.
DC131A'yı 20,2 mm deliğe takın. Çarkı 34 mm açıklığa içeriden yerleştirin;
Ø36 mm ve 4 mm kalınlığındaki flanşı içeride hapsolur ve LED yuvasına çarpmaz.
1K potu baskı köprüsüne somunlayın ve kuponda seçilen mil yuvasını kullanın.
Buzzer'ı açık yüzü ses deliklerine bakacak şekilde kaba yerleştirip yalnızca
kenarından sabitleyin.

## 5. Pil yuvalarını ve ana gücü bağlayın

Piller takılı değilken iki pil yuvasını seri bağlayın:

1. Yuva A siyah kablo → sistem eksi dağıtım hattı.
2. Yuva A kırmızı kablo → Yuva B siyah kablo; ek yerini lehimleyip makaronla
   tamamen kapatın.
3. Yuva B kırmızı kablo → 1 A sigorta → DC120 2P ana güç anahtarı → sistem
   artı dağıtım hattı.

Bu bağlantı dört AA pili seri yapar: nominal 6 V, taze alkalin pillerle yaklaşık
6,4 V. İki yuvada da aynı marka, tip ve dolulukta pil kullanın.

## 6. Altı paralel kolu bağlayın

1. Artı → kırmızı DC184 → 330 ohm 1 W → kırmızı LED uzun bacak; kısa bacak → eksi.
2. Artı → sarı DC184 → 330 ohm 1 W → sarı LED → eksi.
3. Artı → siyah DC180 → 330 ohm 1 W → yeşil LED → eksi.
4. Artı → DC131A anahtar kontakları → 330 ohm 1 W → mavi LED → eksi.
   DC131A'nın 12 V lamba ucunu bağlamayın. Pin dizilimini varsaymayın;
   kullanılacak iki kontağı multimetrenin süreklilik moduyla bulun.
5. Artı → birbirine bağlanan pot orta ucu ve bir dış uç → 330 ohm 1 W → beyaz
   LED → eksi. Potun diğer dış ucunu boş bırakın.
6. Artı → mavi DC180 → aktif buzzer artı; buzzer eksi → eksi.

Dirençlerin yönü yoktur; her LED kendi 330 ohm direncini kullanır. 1 W direnç
elektriksel olarak uygundur, yalnızca 0,25 W tipten daha büyüktür. Kalıcı
oyuncakta breadboard veya gevşek jumper bırakmayın. Çok telli kablo kullanın,
tüm ekleri lehimleyin ve açık iletkenleri makaronla kapatın.

## 7. Elektrik kontrolünü yapın

Piller yokken artı ve eksi arasında kısa devre olmadığını multimetreyle
doğrulayın. DC120 kapalıyken pil akımı sıfır olmalıdır. Taze pillerle teorik en
yüksek LED akımı kırmızıda yaklaşık 13,3 mA, sarıda 13,0 mA, yeşil/mavi/beyazda
10,3 mA'dır. Her kolu ayrı çalıştırın ve ölçülen akımın 20 mA altında kaldığını
doğrulayın. Buzzer'ı yalnızca birkaç saniye deneyin; fazla yüksekse ses
deliklerini tamamen kapatmadan önüne ince keçe yerleştirin.

## 8. Kutuyu kapatın ve denetleyin

İki pil yuvasını arka kapaktaki ayrı raylara yerleştirin; kablolar tırnaklardan
uzak kalsın. Kapağın dilini gövdenin yivine düz bastırıp dört tırnağı oturtun.
Karşılıklı iki servis mandalı aynı anda iki ince aletle bastırılmadan kapak elle
açılmamalıdır. Her kullanımdan önce her buton, LED, anahtar ve çarkı çekerek
kontrol edin. Bir parça hareket ediyor, çatlıyor veya gevşiyorsa kutuyu çocuğa
vermeyin.
"""


ASSEMBLY = {"en": ASSEMBLY_EN, "tr": ASSEMBLY_TR}


def write_locale(locale, output):
    output.mkdir(parents=True, exist_ok=True)
    (output / "circuit.svg").write_text(circuit_svg(locale), encoding="utf-8")
    with (output / "BOM.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(BOM_HEADERS[locale])
        writer.writerows(BOM_ROWS[locale])
    (output / "assembly.md").write_text(ASSEMBLY[locale], encoding="utf-8")


def main():
    write_locale("en", Path("docs"))
    write_locale("tr", Path("docs/tr"))
    print("wrote English and Turkish circuit, BOM, and assembly guides")


if __name__ == "__main__":
    main()
