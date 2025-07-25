# gui_app Açıklaması

Bu klasör, kullanıcı dostu bir arayüz üzerinden YOLOv8 tabanlı krank mili nesne tespiti yapmayı sağlayan GUI (grafiksel kullanıcı arayüzü) uygulamasını içerir. Kullanıcı, görüntü (resim, video) veya canlı kamera kullanarak tespit işlemi gerçekleştirebilir.


### Ne işe yarar?

- Resim, video veya kamera verisi üzerinden krank mili algılaması yapar.
- Kullanıcıya tespit sonuçlarını gerçek zamanlı olarak görsel şekilde sunar.
- Güven eşiği, model ayarı, ROI gibi kontroller sağlar.

## Uygulamanın İşleyişi

### 1. Modelin Yüklenmesi
- Uygulama başlar başlamaz, belirtilen `MODEL_PATH` üzerinden eğitilmiş YOLOv8 modeli yüklenir.
- Model Yolu Tanımı

Kod içinde modelin yolu aşağıdaki şekilde belirtilmiştir:
- MODEL_PATH = r"C:/Users/.../best.pt"

### 2. Görüntü Kaynağı Seçimi
- Kullanıcı, arayüzdeki butonlar ile istediği görüntü kaynağını seçebilir:
  - **Resim Yükle**: Bilgisayardan bir veya daha fazla görsel dosyası seçilir.
  - **Video Yükle**: Video dosyası seçilip analiz başlatılır.
  - **Canlı Kamera**: Bilgisayara bağlı kamera kullanılarak gerçek zamanlı tespit yapılır.

### 3. Nesne Tespiti ve Görüntü İşleme
- Seçilen kaynak üzerindeki her kare veya görüntü modeli kullanılarak analiz edilir.
- Tespit edilen krank mili nesneleri, görüntü üzerinde kutucuklar (bounding box) ve etiketlerle gösterilir.
- Ayrıca, GUI üzerinde toplam tespit sayısı, FPS gibi bilgiler de anlık olarak güncellenir.

### 4. Kullanıcı Kontrolleri
- **Durdur** butonu ile canlı tespit veya video oynatma durdurulabilir.
- **ROI (Region of Interest)** seçimi ile sadece belirli bir alan içinde tespit yapılabilir.
- **Güven Eşiği (Confidence Threshold)** ayarı ile modelin hassasiyeti artırılabilir veya azaltılabilir.
- **Ön Ayarları Yükle** butonu ile daha önce kaydedilmiş ayarlar geri yüklenebilir.


## Arayüz Özellikleri

| Alan              | Açıklama                                                                 |
|-------------------|--------------------------------------------------------------------------|
| Resim Yükle       | .jpg, .png gibi görselleri yükleyerek nesne tespiti yapar                |
| Video Yükle       | .mp4, .avi gibi videolar üzerinden nesne tespiti yapılabilir             |
| Canlı Kamera      | Bilgisayara bağlı kamerayı açarak gerçek zamanlı tespit başlatır         |
| Durdur            | Aktif görüntü işlemesini durdurur                                        |
| ROI Temizle       | Seçilen bölge temizlenir (Region of Interest)                            |
| Ön Ayarları Yükle | Modelin başlangıç ayarlarını yükler.(config.ini dosyasındaki verileri çeker)                                      |
| Güven Eşiği       | Algılamaların hassasiyetini belirleyen threshold değeri                  |
| Sistem Bilgisi    | FPS, tespit sayısı ve kullanılan cihaz (CUDA/CPU) bilgisi                |


## Teknik Notlar

- Model ve görüntü işleme için **Ultralytics YOLOv8** ve **OpenCV** kullanılır.
- Arayüz, **Tkinter** kütüphanesi ile oluşturulmuştur.
- Görüntü işleme ve GUI döngüsü arasındaki uyumu sağlamak için zamanlayıcılar ve threading teknikleri kullanılabilir.
- ROI seçimi için OpenCV pencere üzerinde fare olayları yakalanır ve seçilen bölge sınırlanır.
- Kullanıcı deneyimini artırmak için hata yönetimi, dosya kontrolü ve performans optimizasyonları yapılmıştır.


İlgili Dosyalar

 Dosya/Klasör      Açıklama                                            
 `app.py`          GUI uygulamasının ana kodu                          
 `config.ini`      Uygulama ayarlarını tutan konfigürasyon dosyası (varsa) 
 `best.bt`         Eğitilen modelin dosya yolu