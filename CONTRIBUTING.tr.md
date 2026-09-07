# Katkıda bulunma

[English](CONTRIBUTING.md) | [Türkçe](CONTRIBUTING.tr.md)

Güvenliği, tekrar üretilebilirliği, belgeleri veya yazıcı uyumluluğunu artıran
katkılar memnuniyetle karşılanır.

## Ölçüleri değiştirmeden önce

1. `component-fit-test.stl` ve `snap-fit-test.stl` dosyalarını basın.
2. Yazıcı, malzeme, nozzle, katman yüksekliği ve geçme sonucunu kaydedin.
3. Ortak ölçüleri mümkün olduğunda `tools/project_spec.py` içinde değiştirin.
4. Türetilmiş dosyaları elle düzenlemek yerine yeniden üretin.

Bir delik veya geçme ölçüsünü yalnızca doğrulanmamış katalog çizimine göre
değiştirmeyin. Aynı adla satılan parçaların parti ve çerçeve ölçüleri farklı
olabilir.

## Geliştirme ortamı

```sh
python3 -m pip install -r requirements.txt
make dimensions artwork docs
make test
```

Şu komutlar için ayrıca OpenSCAD gerekir:

```sh
make stl
make validate
```

OpenSCAD yoksa `make validate-source`, STL dışındaki tüm çıktıları doğrular.

## Üretilen dosyalar

`artwork/` ve `docs/` altındaki İngilizce dosyalar ile `artwork/tr/` ve
`docs/tr/` altındaki Türkçe karşılıkları üretilmiş çıktılardır. İlgili
`tools/` scriptini değiştirin, iki dili birlikte üretin ve kaynakla çıktıları
aynı değişikliğe ekleyin. Bir komponent boşluğunu yalnızca tek dilde taşımayın.

## Pull request kuralları

- Değişikliği odaklı tutun; ölçü değişikliklerinin fiziksel nedenini açıklayın.
- Üretici davranışını değiştirmeden önce testi ekleyin veya güncelleyin.
- Göndermeden önce `make test` ve `make validate-source` çalıştırın.
- Fiziksel tolerans değişikliklerinde ölçü veya uyum fotoğrafı ekleyin.
- Kişisel envanter, yerel dosya yolu, tedarikçi hesabı veya özel referans
  fotoğrafı eklemeyin.
- Mühendislik kanıtı ve inceleme olmadan güvenlik uyarısını zayıflatmayın veya
  sigortayı belgelenen güç yolundan kaldırmayın.

Katkıda bulunarak çalışmanızın [`LICENSES/README.tr.md`](LICENSES/README.tr.md)
içinde açıklanan lisanslara tabi olmasını kabul etmiş olursunuz.
