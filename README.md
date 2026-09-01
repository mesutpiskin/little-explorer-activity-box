# Işık ve Ses Etkinlik Kutusu

200 × 160 × 52 mm ölçülerinde, 4×AA pille çalışan, mikrodenetleyicisiz ve
vidasız arka kapaklı etkinlik kutusu.

## Önce bunları açın

- Baskı ve montaj: [`docs/assembly.md`](docs/assembly.md)
- Devre: [`docs/circuit.svg`](docs/circuit.svg)
- Alışveriş listesi: [`docs/BOM.csv`](docs/BOM.csv)
- 3B model: [`cad/activity_box.scad`](cad/activity_box.scad)
- A4 etiket: [`artwork/activity-box-label-a4.pdf`](artwork/activity-box-label-a4.pdf)

## STL çıkarma

OpenSCAD kurulu ve izinli bir bilgisayarda proje klasöründe:

```sh
make stl
```

Bu komut gövde, arka kapak, güvenli döner çark, geçme testi ve komponent uyum
plakası STL'lerini `output/stl/` içine yazar. Tam baskıdan önce
`component-fit-test.stl` ile LED yuvası, büyük buton, rocker anahtar,
dimmer çarkı ve buzzer; `snap-fit-test.stl` ile kapak geçmesi denenmelidir.

## Ölçü değiştirme

Satın alınan parçaları kumpasla ölçün. Varsayılan ölçüler
`tools/project_spec.py` içindedir. Değişiklikten sonra:

```sh
make dimensions artwork docs
python3 -m unittest discover -s tests -v
make stl
make validate
```

Bu ürün sertifikalı oyuncak değildir; 18 aylık çocuk yalnızca yetişkin
gözetiminde kullanmalıdır.
