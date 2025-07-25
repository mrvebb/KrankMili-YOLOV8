# Krank Mili YOLOv8 Algılama Projesi

Bu proje, krank mili nesnesini gerçek zamanlı olarak tespit etmek amacıyla Python, YOLOv8 ve OpenCV kullanılarak geliştirilmiştir. Geliştirme süreci boyunca Spyder IDE ortamı tercih edilmiştir.  
Eğitilen model, kamera üzerinden alınan görüntülerde krank milini anlık olarak algılar ve kullanıcıya grafik arayüz (GUI) aracılığıyla görsel olarak sunar.

---

## Proje Aşamaları

### 1. Veri Seti Hazırlama
Roboflow kullanılarak krank mili görselleri etiketlenmiş ve YOLO formatında dışa aktarılmıştır.

### 2. YOLOv8 Model Eğitimi
Ultralytics kütüphanesi ile veri seti üzerinde YOLOv8 eğitimi gerçekleştirilmiştir.

### 3. Model Yükleme ve Test
Eğitilen model, OpenCV ile gerçek zamanlı kamera görüntüleri üzerinde test edilmiştir.

### 4. GUI Arayüz Geliştirme
Kullanıcı etkileşimini kolaylaştırmak için Python tabanlı bir grafik arayüz geliştirilmiştir.  
Bu arayüz üzerinden kamera başlatma, sayım başlatma ve anlık sonuçları görüntüleme işlemleri yapılabilmektedir.

---

Detaylı bilgi, teknik dökümantasyon ve kurulum yönergeleri için `docs/` klasörünü inceleyebilirsiniz.
