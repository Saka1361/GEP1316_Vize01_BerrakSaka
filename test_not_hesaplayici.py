import io
import csv
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import not_hesaplayici
from not_hesaplayici import (
    agirlikli_ortalama_hesapla,
    harf_notu_hesapla,
    kayitlari_yukle,
    ogrenci_adi_al,
    puan_al,
    sonucu_kaydet,
)


class NotHesaplayiciTestleri(unittest.TestCase):
    def test_harf_notu_esikleri_ve_alt_sinirlar(self):
        test_verileri = [
            (100, "AA"),
            (90, "AA"),
            (89.99, "BA"),
            (85, "BA"),
            (84.99, "BB"),
            (80, "BB"),
            (79.99, "CB"),
            (75, "CB"),
            (74.99, "CC"),
            (70, "CC"),
            (69.99, "DC"),
            (65, "DC"),
            (64.99, "DD"),
            (60, "DD"),
            (59.99, "FD"),
            (50, "FD"),
            (49.99, "FF"),
            (0, "FF"),
        ]

        for ortalama, beklenen_not in test_verileri:
            with self.subTest(ortalama=ortalama):
                self.assertEqual(harf_notu_hesapla(ortalama), beklenen_not)

    def test_vize_ve_final_agirliklari(self):
        self.assertAlmostEqual(agirlikli_ortalama_hesapla(100, 0), 40)
        self.assertAlmostEqual(agirlikli_ortalama_hesapla(0, 100), 60)
        self.assertAlmostEqual(agirlikli_ortalama_hesapla(80, 90), 86)

    def test_puan_al_hatalilari_reddedip_virgullu_puani_kabul_eder(self):
        girdiler = ["abc", "101", "-1", "nan", "inf", "72,5"]
        with patch("builtins.input", side_effect=girdiler), patch("builtins.print"):
            self.assertEqual(puan_al("Vize"), 72.5)

    def test_bos_ogrenci_adi_yeniden_istenir(self):
        with patch("builtins.input", side_effect=["   ", " Deniz "]), patch(
            "builtins.print"
        ):
            self.assertEqual(ogrenci_adi_al(), "Deniz")

    def test_sonuc_csv_dosyasina_baslikla_kaydedilir(self):
        kayitlar = [
            {
                "tarih": "2026-11-14T12:00:00",
                "ogrenci": "Test Öğrencisi",
                "vize": 80,
                "final": 90,
                "ortalama": 86,
                "harf_notu": "BA",
            },
            {
                "tarih": "2026-11-14T12:01:00",
                "ogrenci": "İkinci Öğrenci",
                "vize": 70,
                "final": 80,
                "ortalama": 76,
                "harf_notu": "CB",
            },
        ]

        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            sonucu_kaydet(kayitlar, dosya_yolu)

            with dosya_yolu.open("r", newline="", encoding="utf-8-sig") as dosya:
                satirlar = list(csv.DictReader(dosya))

        self.assertEqual(len(satirlar), 2)
        self.assertEqual(satirlar[0]["ogrenci"], "Test Öğrencisi")
        self.assertEqual(satirlar[0]["ortalama"], "86.00")
        self.assertEqual(satirlar[0]["harf_notu"], "BA")

    def test_onceki_ogrenciler_csv_dosyasindan_yuklenir(self):
        kayitlar = [
            {
                "tarih": "2026-11-14T12:00:00",
                "ogrenci": "Test Öğrencisi",
                "vize": 80,
                "final": 90,
                "ortalama": 86,
                "harf_notu": "BA",
            }
        ]

        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            sonucu_kaydet(kayitlar, dosya_yolu)
            yuklenenler = kayitlari_yukle(dosya_yolu)

        self.assertEqual(len(yuklenenler), 1)
        self.assertEqual(yuklenenler[0]["ogrenci"], "Test Öğrencisi")
        self.assertEqual(yuklenenler[0]["ortalama"], 86)
        self.assertEqual(yuklenenler[0]["harf_notu"], "BA")

    def test_csv_yoksa_bos_liste_doner(self):
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "olmayan.csv"
            self.assertEqual(kayitlari_yukle(dosya_yolu), [])

    def test_gecersiz_csv_kaydi_acik_hata_verir(self):
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "bozuk.csv"
            dosya_yolu.write_text(
                "tarih,ogrenci,vize,final,ortalama,harf_notu\n"
                "2026-11-14T12:00:00,Test,101,90,94.4,AA\n",
                encoding="utf-8-sig",
            )
            with self.assertRaisesRegex(ValueError, "0-100"):
                kayitlari_yukle(dosya_yolu)

    def test_menu_ogrenci_ekler_istatistik_gosterir_ve_csv_kaydeder(self):
        girdiler = ["1", "Ayşe", "80", "90", "e", "5", "4", "6"]

        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            cikti = io.StringIO()
            with patch.object(not_hesaplayici, "SONUC_DOSYASI", dosya_yolu):
                with patch("builtins.input", side_effect=girdiler):
                    with redirect_stdout(cikti):
                        not_hesaplayici.main()

            with dosya_yolu.open("r", newline="", encoding="utf-8-sig") as dosya:
                satirlar = list(csv.DictReader(dosya))

        self.assertIn("1. Öğrenci ekle", cikti.getvalue())
        self.assertIn("2. Öğrenci güncelle", cikti.getvalue())
        self.assertIn("3. Öğrenci sil", cikti.getvalue())
        self.assertIn("4. Listeyi göster", cikti.getvalue())
        self.assertIn("5. Sınıf istatistikleri", cikti.getvalue())
        self.assertIn("6. Çıkış", cikti.getvalue())
        self.assertNotIn("CSV dosyasına kaydet", cikti.getvalue())
        self.assertIn("Sınıf ortalaması: 86.00", cikti.getvalue())
        self.assertIn("Ağırlıklı ortalama: 86.00", cikti.getvalue())
        self.assertEqual([satir["harf_notu"] for satir in satirlar], ["BA"])

    def test_ogrenci_guncelleme_csv_ve_listeyi_gunceller(self):
        kayitlar = [
            {
                "tarih": "2026-11-14T12:00:00",
                "ogrenci": "Eski Ad",
                "vize": 50,
                "final": 50,
                "ortalama": 50,
                "harf_notu": "FD",
            }
        ]
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            sonucu_kaydet(kayitlar, dosya_yolu)
            with patch.object(not_hesaplayici, "SONUC_DOSYASI", dosya_yolu):
                with patch(
                    "builtins.input",
                    side_effect=["1", "Yeni Ad", "90", "100"],
                ):
                    not_hesaplayici.ogrenci_guncelle(kayitlar)

            yuklenenler = kayitlari_yukle(dosya_yolu)

        self.assertEqual(len(kayitlar), 1)
        self.assertEqual(kayitlar[0]["ogrenci"], "Yeni Ad")
        self.assertEqual(kayitlar[0]["ortalama"], 96)
        self.assertEqual(kayitlar[0]["harf_notu"], "AA")
        self.assertEqual(yuklenenler[0]["ogrenci"], "Yeni Ad")

    def test_ogrenci_silme_onayi_csv_ve_listeyi_gunceller(self):
        kayitlar = [
            {
                "tarih": "2026-11-14T12:00:00",
                "ogrenci": "Silinecek",
                "vize": 80,
                "final": 90,
                "ortalama": 86,
                "harf_notu": "BA",
            }
        ]
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            sonucu_kaydet(kayitlar, dosya_yolu)
            with patch.object(not_hesaplayici, "SONUC_DOSYASI", dosya_yolu):
                with patch("builtins.input", side_effect=["1", "e"]):
                    not_hesaplayici.ogrenci_sil(kayitlar)

            yuklenenler = kayitlari_yukle(dosya_yolu)

        self.assertEqual(kayitlar, [])
        self.assertEqual(yuklenenler, [])

    def test_silme_iptali_listeyi_ve_csvyi_degistirmez(self):
        kayitlar = [
            {
                "tarih": "2026-11-14T12:00:00",
                "ogrenci": "Korunacak",
                "vize": 80,
                "final": 90,
                "ortalama": 86,
                "harf_notu": "BA",
            }
        ]
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            sonucu_kaydet(kayitlar, dosya_yolu)
            onceki_icerik = dosya_yolu.read_bytes()
            with patch.object(not_hesaplayici, "SONUC_DOSYASI", dosya_yolu):
                with patch("builtins.input", side_effect=["1", "h"]):
                    not_hesaplayici.ogrenci_sil(kayitlar)

            self.assertEqual(dosya_yolu.read_bytes(), onceki_icerik)
        self.assertEqual([kayit["ogrenci"] for kayit in kayitlar], ["Korunacak"])

    def test_ogrenci_kaydetmeyi_reddederse_listeye_eklenmez(self):
        kayitlar = []
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            with patch.object(not_hesaplayici, "SONUC_DOSYASI", dosya_yolu):
                with patch("builtins.input", side_effect=["Yeni Öğrenci", "80", "90", "h"]):
                    not_hesaplayici.ogrenci_ekle(kayitlar)

            self.assertEqual(kayitlar, [])
            self.assertFalse(dosya_yolu.exists())

    def test_ogrenci_onay_verince_csvye_yazilir_ve_listeye_eklenir(self):
        kayitlar = []
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            with patch.object(not_hesaplayici, "SONUC_DOSYASI", dosya_yolu):
                with patch("builtins.input", side_effect=["Yeni Öğrenci", "80", "90", "e"]):
                    not_hesaplayici.ogrenci_ekle(kayitlar)

            self.assertEqual(len(kayitlar), 1)
            self.assertEqual(kayitlari_yukle(dosya_yolu)[0]["ogrenci"], "Yeni Öğrenci")

    def test_bos_liste_ve_gecersiz_menu_secimi(self):
        cikti = io.StringIO()
        with patch("builtins.input", side_effect=["x", "6"]), redirect_stdout(cikti):
            not_hesaplayici.listeyi_goster([])
            not_hesaplayici.sinif_istatistiklerini_goster([])
            self.assertIsNone(not_hesaplayici.ogrenci_indeksi_sec([]))
            self.assertEqual(not_hesaplayici.menu_secimi_al(), "6")

        self.assertIn("Henüz öğrenci eklenmedi.", cikti.getvalue())
        self.assertIn("önce öğrenci ekleyin", cikti.getvalue())
        self.assertIn("Geçersiz seçim. Lütfen 1 ile 6 arasında", cikti.getvalue())

    def test_program_acilisinda_csv_kayitlarini_listeye_yukler(self):
        kayitlar = [
            {
                "tarih": "2026-11-14T12:00:00",
                "ogrenci": "Önceki Öğrenci",
                "vize": 80,
                "final": 90,
                "ortalama": 86,
                "harf_notu": "BA",
            }
        ]
        with tempfile.TemporaryDirectory() as gecici_dizin:
            dosya_yolu = Path(gecici_dizin) / "notlar.csv"
            sonucu_kaydet(kayitlar, dosya_yolu)
            cikti = io.StringIO()
            with patch.object(not_hesaplayici, "SONUC_DOSYASI", dosya_yolu):
                with patch("builtins.input", side_effect=["4", "6"]):
                    with redirect_stdout(cikti):
                        not_hesaplayici.main()

        self.assertIn("CSV dosyasından 1 öğrenci yüklendi.", cikti.getvalue())
        self.assertIn("Önceki Öğrenci", cikti.getvalue())
        self.assertIn("86.00", cikti.getvalue())

    def test_ctrl_c_duzgun_kapanis_mesaji_gosterir(self):
        cikti = io.StringIO()
        with patch("builtins.input", side_effect=KeyboardInterrupt), redirect_stdout(
            cikti
        ):
            not_hesaplayici.main()

        self.assertIn("Program sonlandırıldı.", cikti.getvalue())


if __name__ == "__main__":
    unittest.main()
