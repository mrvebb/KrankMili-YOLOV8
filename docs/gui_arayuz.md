# Grafik Arayüz (GUI) Kullanımı

Bu bölümde, krank mili nesnesinin gerçek zamanlı tespiti için geliştirilen grafik kullanıcı arayüzü (GUI) açıklanmaktadır. Arayüz, Python dili ile `tkinter` kütüphanesi kullanılarak oluşturulmuş, görüntü işleme için `OpenCV`, model çalıştırma için `YOLOv8 (Ultralytics)` ve görsel aktarım için `PIL` kütüphanelerinden faydalanılmıştır.

---

## Kullanılan Ana Kütüphaneler

- **`cv2 (OpenCV)`**: Kamera erişimi ve görüntü işleme.
- **`ultralytics.YOLO`**: Eğitilen YOLOv8 modelini yükleme ve çalıştırma.
- **`tkinter`**: Python GUI 
- **`PIL.Image, PIL.ImageTk`**: OpenCV görüntüsünü `tkinter` ortamında göstermek için dönüştürme.
- **`configparser`**: Arayüzde kullanılacak ayarların dışarıdan okunabilmesi için.
- **`torch`**: Modelin çalıştırılması için gerekli (CPU veya GPU).
- **`os, time, numpy`**: Dosya işlemleri, zaman yönetimi ve sayısal hesaplamalar için.

---

## Arayüzde Yer Alan Temel Fonksiyonlar

- **Model Seçme ve Yükleme**
  - Kullanıcı `best.pt` uzantılı YOLO modelini `filedialog` aracılığıyla seçer.
  - `YOLO(model_path)` ile model yüklenir.

- **Kamerayı Başlatma**
  - `cv2.VideoCapture()` ile sistem kamerası başlatılır.
  - Belirli aralıklarla görüntü alınarak `tkinter.Canvas` üzerine aktarılır.

- **Görüntü Üzerinde Algılama**
  - Her karede model tahmin çalıştırılır: `model.predict(frame)`
  - Tespit edilen krank mili nesneleri kare üzerine dikdörtgen kutularla çizilir.

- **Sayım Özelliği**
  - Her tespitte sayaç artar, kullanıcıya canlı olarak sayım gösterilir.
  - Gerekirse başlangıç-bitiş koordinatları veya zaman damgası ile birlikte sayım yapılabilir.

- **Kullanıcı Etkileşimleri**
  - Butonlar: "Model Yükle", "Kamerayı Başlat", "Sayımı Başlat", "Çıkış"
  - Mesaj Kutuları: `messagebox.showinfo()` ile kullanıcıya bilgi verilir.
  - `filedialog.askopenfilename()` ile dosya seçimi yapılır.

---

## Arayüzün Yapısı

- Ana pencere: `Tk()` objesi ile oluşturulmuştur.
- Görüntü alanı: `Label` veya `Canvas` nesnesi kullanılarak gösterilir.
- Düğmeler: `Button()` bileşenleri ile, fonksiyonlara bağlanacak şekilde tanımlanmıştır.
- Görüntü güncelleme: `after()` fonksiyonu kullanılarak sürekli çağrılır.

---

## Konfigürasyon (Varsa)

- `config.ini` dosyasından model yolu, görüntü çözünürlüğü gibi ayarlar okunabilir.
- `configparser` kütüphanesi kullanılarak şu şekilde entegre edilir:
  ```python
  import configparser

  config = configparser.ConfigParser()
  config.read('config.ini')
  model_path = config['MODEL']['Path']

# Kullanım Örneği
python app.py

    Açılan pencereden "Model Yükle" seçeneği ile eğitilmiş .pt dosyası seçilir.

    "Kamerayı Başlat" ile canlı görüntü başlatılır.

    "Sayımı Başlat" ile krank mili algılama devreye girer.

    Tespit edilen nesne sayısı arayüzde anlık olarak gösterilir.

