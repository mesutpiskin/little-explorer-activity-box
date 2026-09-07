# STL dışa aktarma

[English](README.md) | [Türkçe](README.tr.md)

Üretilmiş STL dosyaları repoya eklenmez. OpenSCAD'i kurduktan sonra proje
kökünde şu komutları çalıştırın:

```sh
make stl
make validate
```

Oluşturulan dosyalar:

- `activity-box-body.stl`
- `activity-box-back.stl`
- `activity-box-dial.stl`
- `snap-fit-test.stl`
- `component-fit-test.stl`

Ana kutudan önce iki test modelini basıp doğrulayın.

## Baskı yönü

- Gövde: ön yüzü tablaya gelecek şekilde basın.
- Arka kapak: dış yüzü tablaya gelecek şekilde basın.
- Çark: flanşı tablaya gelecek şekilde basın.
