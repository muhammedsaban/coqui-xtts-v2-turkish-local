# Publish Checklist

## 1) Teknik Kontrol

- `python app.py --help` hatasiz calisiyor.
- `python app.py --mode cli` ile en az bir test sesi aliniyor.
- `python app.py --mode gradio` ile arayuz aciliyor.
- `requirements.txt` guncel.

## 2) Guvenlik ve Temizlik

- API key, token, sifre, cookie gibi gizli bilgi yok.
- Kisisel dosya yolu / kisisel veri README veya kodda yok.
- Buyuk gecici dosyalar repoda yok.
- `.gitignore` aktif ve uygun.

## 3) Dokumantasyon

- README kurulum adimlari acik.
- README kullanim adimlari acik.
- Lisans bolumu acik.
- Bilinen kisitlar yazili.

## 4) Lisans

- Repo kod lisansi secili (su an MIT).
- Coqui kutuphane/model lisanslari ayrica kontrol edildi.
- Ticari kullanim notu README icinde var.

## 5) Demo ve Ilk Izlenim

- En az bir arayuz ekran goruntusu eklendi.
- Kisa bir demo ses ornegi veya link eklendi.
- Repo aciklamasi ve etiketler (tags) yazildi.
