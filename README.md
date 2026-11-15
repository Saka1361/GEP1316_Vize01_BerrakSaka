# Öğrenci Not Girişi ve Harf Notu Hesaplayıcı

## Uygulama ne yapar?

Uygulama menü üzerinden öğrencileri yönetir. Açılışta varsa `not_sonuclari.csv` dosyasındaki önceki kayıtları yükler. Adı, vize notunu ve final notunu alır; notları 0–100 aralığında doğrular, vizeyi %40 ve finali %60 ağırlıkla hesaplar. Öğrenci listesini ve sınıf istatistiklerini gösterir. İstenen zamanda listedeki öğrenci kayıtlarını CSV dosyasına kaydeder.

```text
1. Öğrenci ekle
2. Öğrenci güncelle
3. Öğrenci sil
4. Listeyi göster
5. Sınıf istatistikleri
6. Çıkış
```

## Sözde kod

```text
SÖZDE KOD
öğrencileri CSV dosyasından yükle; dosya yoksa boş liste oluştur
seçim 6 olana kadar menüyü göster ve seçim al
    seçim 1: ad ve notları al; doğrula; ortalama ve harf notunu hesapla;
              CSV'ye kaydetme onayı al; onaylanır ve kaydedilirse listeye ekle
    seçim 2: öğrenciyi seç; yeni ad ve notları al; doğrula;
              ortalama ve harf notunu hesapla; CSV'ye kaydet ve listeyi güncelle
    seçim 3: öğrenciyi seç; silme onayı al; onaylanır ve CSV güncellenirse sil
    seçim 4: öğrenci listesini göster; liste boşsa bilgi ver
    seçim 5: sınıf istatistiklerini hesapla ve göster; liste boşsa bilgi ver
    seçim 6: programı sonlandır
    diğer seçimler: uyarı göster
```

| Ağırlıklı ortalama | Harf notu |
|---:|:---:|
| 90 ve üzeri | AA |
| 85–89,99 | BA |
| 80–84,99 | BB |
| 75–79,99 | CB |
| 70–74,99 | CC |
| 65–69,99 | DC |
| 60–64,99 | DD |
| 50–59,99 | FD |
| 50'nin altı | FF |

## Gereksinimler

- Python 3; harici paket gerekmez.
- Windows PowerShell veya Python çalıştırabilen bir terminal.

## Çalıştırma

PowerShell'de bu klasöre geçin ve programı başlatın:

```powershell
cd "C:\Users\LENOVO\Desktop\HWS\Kodlama_Okuryazarlığı\Ödev_Briefing\MIDTERM_1"
py not_hesaplayici.py
```

Menüde `1` ile öğrenci ekleyin; notlar girildikten sonra CSV'ye kaydetme onayı istenir. `h` yanıtı öğrenciyi kaydetmez ve listeye eklemez; `e` yanıtı CSV'ye kaydeder ve ancak kayıt başarılı olursa listeye ekler. `2` ile listeden numarasını seçerek öğrencinin adını ve notlarını güncelleyin; `3` ile numarasını seçip silme işlemini onaylayın. Güncelleme ve silme CSV dosyasına da kaydedilir. `4` listeyi, `5` sınıf ortalaması, en yüksek/düşük ortalama ve harf notu dağılımını gösterir; `6` programdan çıkar. Dosya bulunmuyorsa program boş listeyle başlar. CSV okunamıyor veya kayıt biçimi geçersizse veri kaybını önlemek için hata gösterip kapanır. Ondalık puanlarda virgül veya nokta kullanılabilir. Öğrenci adları içerdiği için dosyayı paylaşırken dikkat edin.

## Testleri çalıştırma

```powershell
py -m unittest -v
```

## Test senaryoları

| Girdi / durum | Beklenen sonuç | Gerçek sonuç |
|---|---|---|
| Vize 80, final 90 | Ortalama 86,00; BA | Testte doğrulandı |
| Vize 50, final 50 | Ortalama 50,00; FD | Testte doğrulandı |
| Ortalama 90 ve 89,99 | Sırasıyla AA ve BA | Eşik testinde doğrulandı |
| Puan alanına `abc` girip ardından `72,5` girme | Uyarı verir, tekrar ister ve 72,5'i kabul eder | Doğrulama testinde doğrulandı |
| Puan alanına 101 veya -1 girme | Aralık uyarısı verir ve yeniden ister | Doğrulama testinde doğrulandı |
| Puan alanına `nan` veya `inf` girme | Sonlu olmayan puanı reddeder ve yeniden ister | Doğrulama testinde doğrulandı |
| Öğrenci adını boş bırakma | Uyarı verir ve adı yeniden ister | Doğrulama testinde doğrulandı |

## Ekran görüntüsü

Teslimden önce programı çalıştırıp örnek bir sonuç ekranının görüntüsünü alın ve bu bölüme ekleyin. Görüntüde gerçek öğrenci bilgisi kullanmayın.
