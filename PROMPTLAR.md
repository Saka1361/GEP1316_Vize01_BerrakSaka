# YZ ile çalışma günlüğü

Bu günlük, uygulamayı hazırlarken kullanılan gerçek konuşma isteklerinin kısa dökümüdür. Yanıt kararları ve gerekçeler teslimden önce öğrenci tarafından gözden geçirilmeli; kişisel değerlendirme gerektiren bölümler kendi deneyiminize göre tamamlanmalıdır.

| # | Kullanılan prompt | Yanıtın özeti | Karar ve gerekçe |
|---:|---|---|---|
| 1 | “Bu ödevde; ‘Öğrenci not girişi ve harf notu hesaplayıcı (eğitim)’ konusunda bir ödev hazırlamak istiyorum. Adım adım birlikte hazırlayalım.” | İlk taslak öğrenci, vize ve final notunu alıp ortalama ve harf notu hesaplıyordu. | **Düzenlendi.** Ödev yönergesiyle karşılaştırınca ilk taslağın döngü, liste/sözlük ve dosyaya kayıt gibi gereksinimleri karşılamadığı görüldü. Kod bu maddeleri içerecek şekilde genişletildi. |
| 2 | “Vize %40 + final %60 ağırlıklı ortalama” | Uygulamanın vize-final ağırlıklarını belirledi. | **Kabul edildi.** Bu ağırlık seçimi kullanıcı tarafından yapıldı ve hesaplama/testlerde kullanıldı. |
| 3 | “Standart aralıklar: AA 90+, BA 85+, BB 80+, CB 75+, CC 70+, DC 65+, DD 60+, FD 50+, FF 50 altı” | Harf notu eşikleri belirlendi. | **Kabul edildi.** Kullanıcı bu eşikleri seçti; sınırların kendisi ve altındaki değerler test edildi. |
| 4 | “Harf notu eşiklerini ve sınır durumlarını test edelim.” | Eşik değerleri ve hemen altındaki puanlar için testler eklendi. | **Genişletildi.** Sınır testleri korundu; geçersiz metin, aralık dışı ve sonlu olmayan puanlar ile boş ad doğrulaması da eklendi. |
| 5 | “Kodu gereksinimleri karşılayacak hale getir.” | Yönergedeki uygulama maddeleri mevcut kodla karşılaştırıldı; etkileşimli toplu giriş, CSV kaydı, biçimli çıktı ve testler eklendi. | **Uygulandı ve test edildi.** Test komutu `py -m unittest -v` ile çalıştırıldı. |
| 6 | “1. Öğrenci ekle / 2. Listeyi göster / 3. Sınıf istatistikleri / 4. CSV dosyasına kaydet / 5. Çıkış — uygulama açıldığında şu şekilde bir menü karşılasın.” | Uygulama, istenen beş seçeneği sunan bir ana menüyle çalışacak şekilde düzenlendi. | **Kabul edildi.** Öğrenci ekleme, liste/istatistik görüntüleme, CSV kaydı ve çıkış akışları menü üzerinden test edildi. |
| 7 | “Uygulama açıldığında CSV dosyasından önceki öğrencileri listeye yükle.” | Program başlangıcında CSV okunup eski kayıtların menüdeki öğrenci listesine eklenmesi istendi. | **Uygulandı ve test edildi.** CSV yoksa boş listeyle başlanıyor; geçersiz dosya veri kaybını önlemek için açık hata vererek programı durduruyor. |
| 8 | “Harf notu hesaplamayı sözlük kullanarak yap. Yaptığın kod değişimini bana göster.” | Harf notu eşikleri bir sözlükte tutulup hesaplama bu sözlüğe göre yapıldı. | **Uygulandı ve test edildi.** Önceki sınır testleri aynı harf notu sonuçlarını doğrulamaya devam ediyor. |
| 9 | “Ctrl+C yaptığım zaman uygulama hata atıyor. Bunun yerine düzgün bir mesaj yazsın.” | Ctrl+C ile oluşan kesme durumu yakalanıp düzgün kapanış mesajı gösterildi. | **Uygulandı ve test edildi.** Klavye kesintisi testi, traceback yerine kapanış mesajı verildiğini doğruluyor. |
| 10 | “''Program Ctrl+C ile sonlandırıldı. Hoşça kalın.'' mesajı yerine ''Program sonlandırıldı.'' desin.” | Kapanış mesajı istenen kısa ifadeyle değiştirildi. | **Uygulandı ve test edildi.** Ctrl+C testi yeni mesajı doğruluyor. |
| 11 | “1 numaralı ‘öğrenci ekle’ aksiyonu gerçekleştiği anda kullanıcıya CSV'ye kaydetmek isteyip istemediği sorulmalı. Eğer kaydetmek istemiyorsa öğrenciyi listeye ekleme.” | Öğrenci ekleme sırasında onay soruluyor; hayır yanıtında iptal, evet yanıtında başarılı CSV kaydından sonra listeye ekleme yapılıyor. | **Uygulandı ve test edildi.** Hem reddetme hem onay verme akışları doğrulandı. |
| 12 | “4 ‘CSV'ye kaydet’ opsiyonunu menüden kaldırabiliriz.” | Ayrı CSV kaydetme menü seçeneği kaldırıldı; çıkış 4. seçenek oldu. | **Uygulandı ve test edildi.** Onaylanan öğrenci kayıtları ekleme sırasında CSV'ye yazılır. |
| 13 | “öğrenci silme ve güncelleme özelliklerini de ekle ve bunları da menüde 2 ve 3. adımlar olarak göster.” | Menüye 2. öğrenci güncelleme ve 3. öğrenci silme seçenekleri eklendi; her işlem CSV kaydını da güncelliyor. | **Uygulandı ve test edildi.** Güncelleme, silme onayı ve iptali test edildi. |
| 14 | “Bu proje için bir sözde kod isteniyor hazırlar mısın?” | Uygulamanın CSV yükleme, menü ve öğrenci işlemlerini açıklayan sözde kod README'ye eklendi. | **Eklendi.** Adımlar mevcut uygulama davranışı ve hata durumlarıyla eşleştirildi. |

## Kendi değerlendirmeniz

Yönerge, YZ kullanımına ilişkin kararlarınızı ve gerekçelerinizi kendi sözlerinizle açıklamanızı ister. Yukarıdaki özetleri doğrulayın, YZ yanıtlarından hangilerini kabul ettiğinizi veya değiştirdiğinizi açıklayın ve süreçte karşılaştığınız en önemli hatayı ya da eksikliği kendi deneyiminize göre genişletin.
