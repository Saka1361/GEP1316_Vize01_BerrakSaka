import csv
import math
import os
import tempfile
from datetime import datetime
from pathlib import Path


SONUC_DOSYASI = Path(__file__).with_name("not_sonuclari.csv")
CSV_SUTUNLARI = ["tarih", "ogrenci", "vize", "final", "ortalama", "harf_notu"]
HARF_NOTU_ESIKLERI = {
    90: "AA",
    85: "BA",
    80: "BB",
    75: "CB",
    70: "CC",
    65: "DC",
    60: "DD",
    50: "FD",
}


def ogrenci_adi_al():
    while True:
        ogrenci_adi = input("Öğrencinin adı: ").strip()
        if ogrenci_adi:
            return ogrenci_adi
        else:
            print("Öğrenci adı boş bırakılamaz.")


def puan_al(sinav_adi):
    while True:
        giris = input(f"{sinav_adi} notu (0-100): ").strip().replace(",", ".")

        try:
            puan = float(giris)
        except ValueError:
            print("Lütfen geçerli bir sayı girin.")
            continue

        if not math.isfinite(puan) or not 0 <= puan <= 100:
            print("Puan 0 ile 100 arasında olmalıdır.")
            continue

        return puan


def agirlikli_ortalama_hesapla(vize, final):
    return vize * 0.40 + final * 0.60


def harf_notu_hesapla(ortalama):
    for esik, harf_notu in HARF_NOTU_ESIKLERI.items():
        if ortalama >= esik:
            return harf_notu
    return "FF"


def sonucu_goster(kayit):
    print("\n--- Not Sonucu ---")
    print(f"Öğrenci: {kayit['ogrenci']}")
    print(f"Vize: {kayit['vize']:g}")
    print(f"Final: {kayit['final']:g}")
    print(f"Ağırlıklı ortalama: {kayit['ortalama']:.2f}")
    print(f"Harf notu: {kayit['harf_notu']}")


def sonucu_kaydet(kayit, dosya_yolu=None):
    if dosya_yolu is None:
        dosya_yolu = SONUC_DOSYASI

    dosya_yolu = Path(dosya_yolu)
    gecici_yol = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            newline="",
            encoding="utf-8-sig",
            dir=dosya_yolu.parent,
            prefix=f".{dosya_yolu.name}.",
            suffix=".tmp",
            delete=False,
        ) as dosya:
            gecici_yol = Path(dosya.name)
            yazici = csv.DictWriter(dosya, fieldnames=CSV_SUTUNLARI)
            yazici.writeheader()
            for ogrenci_kaydi in kayit:
                csv_kaydi = ogrenci_kaydi.copy()
                csv_kaydi["ortalama"] = f"{float(ogrenci_kaydi['ortalama']):.2f}"
                yazici.writerow(csv_kaydi)

        os.replace(gecici_yol, dosya_yolu)
        gecici_yol = None
    finally:
        if gecici_yol is not None:
            gecici_yol.unlink(missing_ok=True)


def kayitlari_yukle(dosya_yolu=None):
    if dosya_yolu is None:
        dosya_yolu = SONUC_DOSYASI
    dosya_yolu = Path(dosya_yolu)

    if not dosya_yolu.exists():
        return []

    ogrenci_kayitlari = []
    with dosya_yolu.open("r", newline="", encoding="utf-8-sig") as dosya:
        okuyucu = csv.DictReader(dosya, strict=True)
        if okuyucu.fieldnames is None or any(
            sutun not in okuyucu.fieldnames for sutun in CSV_SUTUNLARI
        ):
            raise ValueError("CSV dosyasının başlıkları beklenen biçimde değil.")

        for satir_no, satir in enumerate(okuyucu, start=2):
            if all(deger is None for deger in satir.values()):
                continue
            if None in satir or any(not satir.get(sutun) for sutun in CSV_SUTUNLARI):
                raise ValueError(f"{satir_no}. satırda eksik veya fazla alan var.")

            try:
                vize = float(satir["vize"])
                final = float(satir["final"])
            except ValueError as hata:
                raise ValueError(f"{satir_no}. satırda not değeri geçersiz.") from hata

            if (
                not math.isfinite(vize)
                or not math.isfinite(final)
                or not 0 <= vize <= 100
                or not 0 <= final <= 100
            ):
                raise ValueError(f"{satir_no}. satırdaki notlar 0-100 aralığında değil.")

            ortalama = agirlikli_ortalama_hesapla(vize, final)
            ogrenci_kayitlari.append(
                {
                    "tarih": satir["tarih"],
                    "ogrenci": satir["ogrenci"],
                    "vize": vize,
                    "final": final,
                    "ortalama": ortalama,
                    "harf_notu": harf_notu_hesapla(ortalama),
                }
            )

    return ogrenci_kayitlari


def menu_goster():
    print("\n--- Ana Menü ---")
    print("1. Öğrenci ekle")
    print("2. Öğrenci güncelle")
    print("3. Öğrenci sil")
    print("4. Listeyi göster")
    print("5. Sınıf istatistikleri")
    print("6. Çıkış")


def ogrenci_ekle(ogrenci_kayitlari):
    ogrenci = ogrenci_adi_al()
    vize = puan_al("Vize")
    final = puan_al("Final")
    ortalama = agirlikli_ortalama_hesapla(vize, final)

    kayit = {
        "tarih": datetime.now().isoformat(timespec="seconds"),
        "ogrenci": ogrenci,
        "vize": vize,
        "final": final,
        "ortalama": ortalama,
        "harf_notu": harf_notu_hesapla(ortalama),
    }

    if not evet_hayir_al("Öğrenciyi CSV dosyasına kaydetmek istiyor musunuz? (e/h): "):
        print(f"\n{ogrenci} kaydedilmedi ve listeye eklenmedi.")
        return

    try:
        sonucu_kaydet([*ogrenci_kayitlari, kayit])
    except OSError as hata:
        print(f"\nCSV dosyasına kaydedilemedi; öğrenci listeye eklenmedi: {hata}")
        return

    ogrenci_kayitlari.append(kayit)
    print(f"\n{ogrenci} CSV dosyasına kaydedildi ve listeye eklendi.")
    sonucu_goster(kayit)


def evet_hayir_al(soru):
    while True:
        cevap = input(soru)
        cevap = cevap.strip().lower()

        if cevap in ("e", "evet"):
            return True
        elif cevap in ("h", "hayır", "hayir"):
            return False
        else:
            print("Lütfen evet için 'e', hayır için 'h' girin.")


def listeyi_goster(ogrenci_kayitlari):
    if not ogrenci_kayitlari:
        print("\nHenüz öğrenci eklenmedi.")
        return

    print("\n--- Öğrenci Listesi ---")
    print(f"{'No':>3} {'Öğrenci':<24} {'Vize':>7} {'Final':>7} {'Ortalama':>10} {'Harf':>6}")
    print("-" * 63)
    for sira, kayit in enumerate(ogrenci_kayitlari, start=1):
        print(
            f"{sira:>3} {kayit['ogrenci']:<24} {kayit['vize']:>7.2f} "
            f"{kayit['final']:>7.2f} {kayit['ortalama']:>10.2f} "
            f"{kayit['harf_notu']:>6}"
        )


def ogrenci_indeksi_sec(ogrenci_kayitlari):
    if not ogrenci_kayitlari:
        print("\nİşlem yapmak için önce öğrenci ekleyin.")
        return None

    listeyi_goster(ogrenci_kayitlari)
    while True:
        giris = input("İşlem yapılacak öğrencinin numarası: ").strip()
        try:
            sira = int(giris)
        except ValueError:
            print("Lütfen listedeki öğrenci numarasını girin.")
            continue

        if 1 <= sira <= len(ogrenci_kayitlari):
            return sira - 1
        print(f"Öğrenci numarası 1 ile {len(ogrenci_kayitlari)} arasında olmalıdır.")


def ogrenci_guncelle(ogrenci_kayitlari):
    indeks = ogrenci_indeksi_sec(ogrenci_kayitlari)
    if indeks is None:
        return

    eski_kayit = ogrenci_kayitlari[indeks]
    print(f"\n'{eski_kayit['ogrenci']}' için yeni bilgileri girin.")
    ogrenci = ogrenci_adi_al()
    vize = puan_al("Yeni vize")
    final = puan_al("Yeni final")
    ortalama = agirlikli_ortalama_hesapla(vize, final)
    yeni_kayit = {
        "tarih": datetime.now().isoformat(timespec="seconds"),
        "ogrenci": ogrenci,
        "vize": vize,
        "final": final,
        "ortalama": ortalama,
        "harf_notu": harf_notu_hesapla(ortalama),
    }

    yeni_liste = ogrenci_kayitlari.copy()
    yeni_liste[indeks] = yeni_kayit
    try:
        sonucu_kaydet(yeni_liste)
    except OSError as hata:
        print(f"\nCSV dosyası güncellenemedi; öğrenci değişmedi: {hata}")
        return

    ogrenci_kayitlari[indeks] = yeni_kayit
    print(f"\n{yeni_kayit['ogrenci']} bilgileri güncellendi ve CSV dosyasına kaydedildi.")
    sonucu_goster(yeni_kayit)


def ogrenci_sil(ogrenci_kayitlari):
    indeks = ogrenci_indeksi_sec(ogrenci_kayitlari)
    if indeks is None:
        return

    kayit = ogrenci_kayitlari[indeks]
    soru = f"'{kayit['ogrenci']}' adlı öğrenciyi silmek istiyor musunuz? (e/h): "
    if not evet_hayir_al(soru):
        print("\nSilme işlemi iptal edildi.")
        return

    yeni_liste = ogrenci_kayitlari.copy()
    del yeni_liste[indeks]
    try:
        sonucu_kaydet(yeni_liste)
    except OSError as hata:
        print(f"\nCSV dosyası güncellenemedi; öğrenci silinmedi: {hata}")
        return

    ogrenci_kayitlari[:] = yeni_liste
    print(f"\n{kayit['ogrenci']} listeden ve CSV dosyasından silindi.")


def sinif_istatistiklerini_goster(ogrenci_kayitlari):
    if not ogrenci_kayitlari:
        print("\nİstatistikleri göstermek için önce öğrenci ekleyin.")
        return

    ortalamalar = [kayit["ortalama"] for kayit in ogrenci_kayitlari]
    harf_dagilimi = {}
    for kayit in ogrenci_kayitlari:
        harf = kayit["harf_notu"]
        harf_dagilimi[harf] = harf_dagilimi.get(harf, 0) + 1

    print("\n--- Sınıf İstatistikleri ---")
    print(f"Öğrenci sayısı: {len(ogrenci_kayitlari)}")
    print(f"Sınıf ortalaması: {sum(ortalamalar) / len(ortalamalar):.2f}")
    print(f"En yüksek ortalama: {max(ortalamalar):.2f}")
    print(f"En düşük ortalama: {min(ortalamalar):.2f}")
    print("Harf notu dağılımı:")
    for harf in ("AA", "BA", "BB", "CB", "CC", "DC", "DD", "FD", "FF"):
        if harf in harf_dagilimi:
            print(f"  {harf}: {harf_dagilimi[harf]} öğrenci")


def menu_secimi_al():
    while True:
        secim = input("\nSeçiminiz (1-6): ").strip()
        if secim in ("1", "2", "3", "4", "5", "6"):
            return secim
        else:
            print("Geçersiz seçim. Lütfen 1 ile 6 arasında bir seçenek girin.")


def main():
    try:
        ogrenci_kayitlari = kayitlari_yukle()
    except (OSError, ValueError, csv.Error) as hata:
        print(f"Uyarı: Önceki öğrenci kayıtları yüklenemedi: {hata}")
        print("Verilerin korunması için program kapatılıyor; CSV dosyasını kontrol edin.")
        return

    print("Öğrenci Not Girişi ve Harf Notu Hesaplayıcı")
    if ogrenci_kayitlari:
        print(f"CSV dosyasından {len(ogrenci_kayitlari)} öğrenci yüklendi.")
    else:
        print("Yüklenecek önceki öğrenci kaydı bulunamadı.")

    try:
        while True:
            menu_goster()
            secim = menu_secimi_al()

            if secim == "1":
                ogrenci_ekle(ogrenci_kayitlari)
            elif secim == "2":
                ogrenci_guncelle(ogrenci_kayitlari)
            elif secim == "3":
                ogrenci_sil(ogrenci_kayitlari)
            elif secim == "4":
                listeyi_goster(ogrenci_kayitlari)
            elif secim == "5":
                sinif_istatistiklerini_goster(ogrenci_kayitlari)
            else:
                print("\nProgram kapatıldı.")
                break
    except KeyboardInterrupt:
        print("\n\nProgram sonlandırıldı.")

if __name__ == "__main__":
    main()
