# 🤟 Sign Language Translator Application

## 📝 About the Project
This is a modern and user-friendly desktop application that performs **real-time sign language translation** by detecting hand movements using a webcam.

The project is named "Yasmin" after my fiancée, who inspired me to create this application.

---

# 🤟 İşaret Dili Çevirici Uygulaması

## 📝 Proje Hakkında
Bu proje, kameradan gelen görüntülerle **gerçek zamanlı işaret dili çevirisi** yapan modern ve kullanıcı dostu bir masaüstü uygulamasıdır.

Projeye, bu uygulamayı yaratmama ilham veren nişanlım Yasmin'in adını verdim.

---

## ⚡ Quick Start (Windows)

To set up and run the application easily on Windows, simply double-click or run the following command in your project directory:

```bat
run_app.bat
```

This script will automatically create a virtual environment, install all dependencies, check code quality, run tests, and start the application.

---

## ⚡ Hızlı Başlangıç (Windows)

Windows'ta uygulamayı kolayca başlatmak için proje klasöründe `run_app.bat` dosyasını çift tıklayarak veya aşağıdaki komutu kullanarak çalıştırabilirsiniz:

```bat
run_app.bat
```

Bu betik, sanal ortamı oluşturur, tüm bağımlılıkları yükler, kod kalitesini kontrol eder, testleri çalıştırır ve uygulamayı başlatır.

---

## ✨ Features
- 🎥 Real-time hand movement detection
- 🔤 Sign language letter recognition
- 🌍 Multi-language support
- 🎨 Clean, modern UI with CustomTkinter
- 📊 Performance profiling and analysis
- 📝 Logging system with custom file support
- 🧪 Automated testing infrastructure

---

## ✨ Özellikler
- 🎥 Gerçek zamanlı el hareketi algılama
- 🔤 İşaret dili harf tanıma
- 🌍 Çoklu dil desteği
- 🎨 Modern ve kullanıcı dostu arayüz
- 📊 Detaylı performans analizi
- 📝 Kapsamlı loglama sistemi
- 🧪 Otomatik test altyapısı

---

## 🛠️ Technical Stack
- **Language:** Python 3.8+
- **Image Processing:** OpenCV, MediaPipe
- **Machine Learning:** scikit-learn
- **GUI:** CustomTkinter
- **Translation API:** Google Translate API
- **Testing:** pytest, coverage

---

## 🛠️ Teknik Altyapı
- **Dil:** Python 3.8+
- **Görüntü İşleme:** OpenCV, MediaPipe
- **Makine Öğrenmesi:** scikit-learn
- **Arayüz:** CustomTkinter
- **Çeviri API:** Google Translate API
- **Test:** pytest, coverage

---

## 📋 Requirements
- Python 3.8 or higher
- Webcam
- Internet connection (for translation)

---

## 📋 Gereksinimler
- Python 3.8 veya üzeri
- Webcam
- İnternet bağlantısı (çeviri için)

---

## 🚀 Installation

```bash
git clone https://github.com/Agueria/Yasmin-SignLanguage.git
cd sign-language-translator
```

Create and activate virtual environment:
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 🚀 Kurulum

```bash
git clone https://github.com/Agueria/Yasmin-SignLanguage.git
cd sign-language-translator
```

Sanal ortamı oluştur ve aktif et:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

Gerekli paketleri yükle:
```bash
pip install -r requirements.txt
```

---

## 💻 Usage

Start the application:
```bash
python run.py
```

### Command Line Options
- `--debug` : Enable debug mode
- `--log-file=PATH` : Use a custom log file
- `--profile` : Enable performance profiling

---

## 💻 Kullanım

Uygulamayı başlat:
```bash
python run.py
```

### Komut Satırı Argümanları
- `--debug` : Hata ayıklama modunu etkinleştirir
- `--log-file=PATH` : Özel log dosyası belirtir
- `--profile` : Performans analizi modunu etkinleştirir

---

## 📚 Model Training & Data Collection

Before using the application, you need to collect your own sign language data and train a model if you don't have a pre-trained model file.

### 1. Data Collection

Run the following command to collect hand sign images using your webcam:

```bash
python sign_language_model/collect_imgs.py
```

- Images will be saved in the `data/` directory by default.
- You can specify the output directory and label via command line arguments (see script help for details).

### 2. Model Training

After collecting enough images for each sign, train the model with:

```bash
python sign_language_model/train_classifier.py
```

- The script will process the images and save the trained model as a `.p` file (default: `EnglishHandSignModel.p`).
- Make sure the model file is placed in the correct directory (default: `./sign_language_model/EnglishHandSignModel.p`).

### 3. Using Your Model

- The application will automatically use the model file in the default location.
- If the model file is missing, the application may not work correctly.

---

## 📚 Model Eğitimi & Veri Toplama

Uygulamayı kullanmadan önce, önceden eğitilmiş bir model dosyanız yoksa kendi işaret dili verinizi toplamanız ve modeli eğitmeniz gerekir.

### 1. Veri Toplama

Webcam ile işaret dili görüntüleri toplamak için aşağıdaki komutu çalıştırın:

```bash
python sign_language_model/collect_imgs.py
```

- Görüntüler varsayılan olarak `data/` klasörüne kaydedilir.
- Komut satırı argümanları ile çıktı klasörünü ve etiketi belirtebilirsiniz (detaylar için script yardımına bakın).

### 2. Model Eğitimi

Her işaret için yeterli görüntü topladıktan sonra modeli eğitmek için:

```bash
python sign_language_model/train_classifier.py
```

- Script, görüntüleri işler ve eğitilmiş modeli `.p` uzantılı dosya olarak kaydeder (varsayılan: `EnglishHandSignModel.p`).
- Model dosyasının doğru dizinde olduğundan emin olun (varsayılan: `./sign_language_model/EnglishHandSignModel.p`).

### 3. Modeli Kullanma

- Uygulama, varsayılan konumdaki model dosyasını otomatik olarak kullanır.
- Model dosyası yoksa uygulama düzgün çalışmayabilir.

---

## 📁 Project Structure
```
├── src/
│   ├── main_app.py
│   ├── hand_detector.py
│   └── ...
├── sign_language_model/
│   ├── collect_imgs.py
│   ├── train_classifier.py
├── logs/
├── tests/
├── requirements.txt
└── run.py
```

---

## 📁 Proje Yapısı
```
├── src/                    # Kaynak kod
│   ├── main_app.py         # Ana uygulama
│   ├── hand_detector.py    # El takibi
├── sign_language_model/    # Model dosyaları
│   ├── collect_imgs.py     # Veri toplama
│   ├── train_classifier.py # Eğitim
├── logs/                   # Loglar
├── tests/                  # Testler
├── requirements.txt        # Bağımlılıklar
└── run.py                  # Giriş noktası
```

---

## 🧪 Testing

```bash
pytest
pytest --cov=src tests/
```

---

## 🧪 Test

```bash
pytest
pytest --cov=src tests/
```

---

## 🛠 Debugging & Logging

```bash
python run.py --debug
python run.py --profile
python run.py --log-file=logs/custom.log
```

---

## 🛠 Hata Ayıklama & Loglama

```bash
python run.py --debug
python run.py --profile
python run.py --log-file=logs/custom.log
```

---

## 🤝 Contributing

1. Fork this repository
2. Create a branch: `git checkout -b feature/myFeature`
3. Commit changes: `git commit -am 'Add feature'`
4. Push branch: `git push origin feature/myFeature`
5. Open a Pull Request

---

## 🤝 Katkıda Bulunma

1. Bu repoyu forkla
2. Yeni branch oluştur: `git checkout -b feature/yeniOzellik`
3. Commit at: `git commit -am 'Yeni özellik eklendi'`
4. Branch'i pushla: `git push origin feature/yeniOzellik`
5. Pull Request gönder

---

## 📄 License
MIT License © 2025 — Cem Berk Çakır

---

## 📄 Lisans
MIT Lisansı © 2025 — Cem Berk Çakır

---

## 🙏 Acknowledgments
- MediaPipe team
- OpenCV community
- All contributors

---

## 🙏 Teşekkürler
- MediaPipe ekibi
- OpenCV topluluğu
- Katkıda bulunan herkes
