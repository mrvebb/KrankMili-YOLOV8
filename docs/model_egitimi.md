# YOLOv8 Model Eğitimi

## Kullanılan Araçlar:
- **Roboflow**: Görüntülerin etiketlenmesi ve YOLOv8 formatına dönüştürülmesi.
- **Ultralytics YOLOv8 (Python)**: Modelin eğitilmesi.
- **Spyder IDE (Anaconda ortamında)**: Tüm Python kodlarının çalıştırıldığı geliştirme ortamı.

---

## Adım Adım Eğitim Süreci

### 1. Görsellerin Hazırlanması
Krank miline ait görseller fabrika ortamında manuel olarak çekildi. Çekilen görseller yüksek çözünürlükte `.jpg` formatında kaydedildi ve `dataset/raw_images/` klasöründe toplandı.

### 2. Roboflow ile Etiketleme

- Roboflow sitesine https://roboflow.com üzerinden giriş yapıldı.

- Dashboard (gösterge paneli) üzerinde "Create New Project" butonuna tıklandı.

---

#### 2.1. Yeni Proje Oluşturma

* Project Name: Krank Mili Algılama  
* Project Type: Object Detection  
* Annotation Group: Genellikle otomatik tanımlanır; varsayılan değer kullanılabilir.

Yeni proje oluşturulduktan sonra, kullanıcı Roboflow arayüzüne yönlendirilir ve görseller yüklenmeye hazır hale gelir.

---

#### 2.2. Görsellerin Yüklenmesi

* Upload Images butonuna tıklanarak .jpg uzantılı krank mili görselleri toplu şekilde yüklendi.
* Yükleme tamamlandığında her görselin küçük bir önizlemesi Roboflow arayüzünde görüntülenir.

---

#### 2.3. Görsellerin Etiketlenmesi (Labeling)

* Görseller yüklendi.
* Krank miline ait nesne, diktörtgen çizilerek işaretlendi.
* Etiket ismi olarak "krank" yazıldı.
* Etiketleme sırasında tüm görsellerde aynı sınıf adı kullanılarak tutarlılık sağlandı.
* Gerekirse zoom yaparak küçük nesneler daha hassas şekilde etiketlendi.

---

#### 2.4. Dataset Split (Veri Bölme Ayarları)

Etiketleme tamamlandıktan sonra Roboflow, kullanıcıdan veri setinin nasıl bölüneceğini belirtmesini ister:

* Train: Modelin öğreneceği örnekler (genellikle %70-80)  
* Validation: Modelin eğitilirken doğruluğunun test edildiği kısım (genellikle %10-20)  
* Test: Eğitim bittikten sonra performansın değerlendirildiği bölüm (genellikle %10)

Roboflow bu oranları varsayılan olarak **80% train / 10% valid / 10% test** şeklinde ayarlar. Ancak istenirse manuel olarak bu oranlar değiştirilebilir:

---

#### 2.5. Versiyon Oluşturma

Etiketleme ve veri bölme tamamlandıktan sonra sağ üstte yer alan "Generate Dataset" butonuna tıklanarak yeni bir versiyon oluşturulur.

**Preprocessing Options:**

* Görüntü boyutu: 640x640 (YOLOv8 için önerilen)
* Gri tonlama, normalize etme gibi işlemler isteğe bağlı olarak eklenebilir.

**Augmentation Options (isteğe bağlı):**

* Yatay çevirme (horizontal flip)
* Gaussian blur
* Exposure değişikliği
* Dönme (rotation)

Yapılan seçimlerden sonra "Generate" butonuna basılarak veri seti işlenir ve versiyon adı (örneğin v1) ile kaydedilir.

---

#### 2.6. YOLOv8 Formatında Dışa Aktarma

Versiyon oluşturulduktan sonra "Export" sekmesine geçilir ve şu ayarlar yapılır:

* Format: YOLOv8   
* Download Method: Download .zip  
* Annotation Type: Bounding Box  
* Include: train, valid, test

---

### 3. Roboflow Veri Setini Python Ortamına Entegre Etme

Bu işlem sonucunda .zip formatında bir dosya indirilir. İçerisindeki yapılar:


dataset/
├── test/
│ ├── images/
│ └── labels/
├── train/
│ ├── images/
│ └── labels/
├── valid/
│ ├── images/
│ └── labels/
└── data.yaml


3. `data.yaml` dosyası YOLOv8 eğitiminde kullanılır. İçeriği şu şekildedir:
```yaml
train: dataset/images/train
val: dataset/images/valid

nc: 1 (sınıf sayısı)
names: ['krank_mili']
   

   Ultralytics Kurulumu
Terminal veya Spyder üzerinde aşağıdaki komutla Ultralytics paketi yüklendi: pip install ultralytics

Spyder IDE içindeki terminalde şu komut çalıştırıldı:
yolo task=detect mode=train model=yolov8n.pt data=dataset/data.yaml epochs=50 imgsz=640
task=detect: Nesne tespiti yapılacağı belirtilir.

model=yolov8n.pt: YOLOv8'in küçük (nano) modeli kullanılır.

data=dataset/data.yaml: Eğitim ve doğrulama dosyalarının yolu.

epochs=50: Eğitim 50 dönem boyunca yapılır.

imgsz=640: Görsellerin yeniden boyutlandırılacağı boyut.

runs/detect/train/
├── weights/
│   ├── best.pt         → En iyi model ağırlıkları
│   └── last.pt         → Son epoch'a ait ağırlıklar
├── results.png         → Eğitim süreci metrik grafikleri
├── confusion_matrix.png → Sınıflandırma doğruluk matrisi
├── F1_curve.png, PR_curve.png vb.


//Örnek Kod Parçası (Model Yükleme)

from ultralytics import YOLO

# Eğitilen modeli yükle
model = YOLO("runs/detect/train/weights/best.pt")

# Kamera ile test et
results = model(source=0, show=True)
