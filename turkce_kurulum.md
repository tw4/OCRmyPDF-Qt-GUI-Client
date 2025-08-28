## Önkoşullar

- **Python 3.13+, https://www.python.org/ ( kurulumda “Add python.exe to PATH” işaretlenmeli)
    
- **Tesseract-OCR**, https://github.com/UB-Mannheim/tesseract/wiki
- **Ghostscript**, https://www.ghostscript.com/download/gsdnld.html
    

---
## Adımlar (CMD ile)

1. **Projeyi klonla**
```cmd
git clone https://github.com/tw4/OCRmyPDF-Qt-GUI-Client.git
cd OCRmyPDF-Qt-GUI-Client
```

2. **Sanal ortamı oluştur**
```cmd
python -m venv venv
```

3. **Sanal ortamı (CMD) aktifleştir**
```cmd
venv\Scripts\activate
```
Komut satırı başında `(venv)` görmelisin.

4. **Bağımlılıkları kur (pip)**
```cmd
pip install -r requirements.txt
```

5. **Uygulamayı çalıştır**
```cmd
python main.py
```

---

## Projeyi tekrar kullanırken:

```cmd
cd OCRmyPDF-Qt-GUI-Client
venv\Scripts\activate
python main.py
```