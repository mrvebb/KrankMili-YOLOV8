# YOLOv8 Model Kullanımı

Bu belgede, Roboflow ile eğitilen YOLOv8 modelinin Python ortamında nasıl yükleneceği, kamera görüntüsü üzerinde nasıl uygulanacağı ve sonuçların nasıl yorumlanacağı detaylı bir şekilde açıklanmıştır.

---
## Gereksinimler

- Python 3.9 veya üzeri
- OpenCV (`opencv-python`)
- Ultralytics YOLOv8 (`ultralytics`)
- Kamera

Kurulum için:

```bash
pip install ultralytics opencv-python

  ##Model Dosyasının Yolu
##Eğitim sonrası oluşturulan .pt dosyasının yolunu buraya yazınız.
MODEL_PATHr"C:\Users\...\weights\best.pt"


##Algılama ve Sayma Mantığı
- Krank mili görüntüde ilk kez göründüğünde süre başlatılır.
- INITIAL_DETECTION_DURATION süresi dolduktan sonra 1 kez sayılır.
- RECOUNT_LOCK_DURATION = 40 ile 40 saniye içinde tekrar nesne algılanırsa onu toplam sayıya eklemez.

##Önemli Notlar
Kamera ID’si farklıysa (0 yerine 1 vb.) VideoCapture() parametresini değiştirin.

conf parametresi algılama hassasiyetini belirler. İhtiyaç halinde değiştirilebilir.
results = model.predict(frame, conf=0.5)
      (conf=0.5: %50 üzerindeki doğruluk değerlerinde tespit yapar.)

Model sadece 1 sınıf (krank mili) için eğitildiği için 
if box.cls[0] == 0    şartı kullanılır.


##Örnek Konsol Çıktısı
    Model yükleniyor...
    Model başarıyla yüklendi
    Model sınıfları: {0: 'crankshaft'}
    Hedef sınıf ID 0: crankshaft
    Kamera 0 açılıyor...
    Kamera başarıyla açıldı. Kare boyutu: (480, 640, 3)
    === ANA DÖNGÜ BAŞLATILDI ===
    Çıkmak için 'q' tuşuna basın
    [09:28:05] Krank mili bekleniyor... TOPLAM: 0
    [09:28:06] Krank mili tespit edildi, sayım için bekleniyor...
    [09:28:11] Sayım için bekleniyor... (0.7/10s)
    Kare 180 işlendi
    Tespitler: crankshaft(0.86)
    [09:28:13] Sayım için bekleniyor... (2.7/10s)
    Tespitler: crankshaft(0.86)
    Kare 240 işlendi
    [09:28:20] Krank mili sayıldı! TOPLAM: 1
    Tespitler: crankshaft(0.83)
    [09:28:21] Krank mili hala görünümde. TOPLAM: 1
    [09:28:24] Krank mili görünümden çıktı. Yeni nesne için hazır.
    [09:28:29] Krank mili bekleniyor... TOPLAM: 1
    Çıkış tuşuna basıldı
    === SİSTEM KAPATILIYOR ===
    Sistem kapatıldı