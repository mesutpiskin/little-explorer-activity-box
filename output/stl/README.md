# STL dışa aktarma

Şirket bilgisayarındaki uygulama politikası OpenSCAD'i çalıştırmadığı için STL
ikili dosyaları bu ortamda oluşturulamadı. Parametrik model tamamlandı.

OpenSCAD'in çalıştığı bir bilgisayarda proje kökünde `make stl` komutunu
çalıştırın. Şu beş dosya üretilecektir:

- `activity-box-body.stl`
- `activity-box-back.stl`
- `activity-box-dial.stl`
- `snap-fit-test.stl`
- `component-fit-test.stl`

Ardından `make validate` çalıştırın.
