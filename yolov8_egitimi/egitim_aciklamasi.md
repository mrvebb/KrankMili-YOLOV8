#  yolov8_egitimi Açıklaması

Bu klasör, YOLOv8 modelinin özel bir krank mili veri setiyle eğitildiği Python dosyasını içerir. Eğitim işlemleri sınıf yapısıyla düzenlenmiştir ve hiperparametreler küçük veri setine uygun olarak optimize edilmiştir.


##  denemee.py

###  Ne işe yarar?
- Bu dosya, `YOLOTrainer` adında bir sınıf tanımlayarak, verilen bir `data.yaml` dosyasına göre YOLOv8 modelini eğitir.
- Küçük veri setleri için ayarlanmış hiperparametrelerle daha verimli bir eğitim sağlar.


##  Temel Bileşenler

### 1. `YOLOTrainer` sınıfı
- Giriş olarak iki parametre alır:
  - `data_yaml_path`: Roboflow'dan dışa aktarılan `data.yaml` dosyasının yolu.
  - `pretrained_model_name`: Eğitim başlangıcında kullanılacak YOLOv8 modeli. (Önerilen: `yolov8n.pt`)
- `train()` fonksiyonu, modelin eğitilmesini sağlar ve çıktı olarak eğitim sonuçlarını döner.


##  Eğitim Parametreleri

| Parametre        | Açıklama |
|------------------|----------|
| `epochs=100`     | Model 100 tur boyunca eğitilir. Küçük veri setlerinde yeterlidir. |
| `patience=20`    | Eğer 20 epoch boyunca gelişme olmazsa eğitim erken durdurulur. |
| `batch=8`        | Her eğitim adımında işlenecek görüntü sayısı (GPU belleğine göre ayarlanabilir). |
| `imgsz=640`      | Görüntü boyutu. YOLO için standart. |
| `lr0=0.001`      | Başlangıç öğrenme oranı. Ezberlemeyi önlemek için düşürülmüştür. |
| `hsv_h, hsv_s...`| Renk, boyut ve pozisyonla ilgili veri artırma (augmentation) parametreleri. |
| `project` & `name` | Eğitim çıktılarının klasör adları. Her eğitimi birbirinden ayırmak için kullanılır. |



- `data.yaml` dosyasının yolu doğru şekilde `yaml_path` değişkenine yazılmalıdır.

##  Eğitim Sonucu

- Eğitim tamamlandıktan sonra `runs/train/YOLOv8_Custom_Training/small_dataset_run_1/weights/` klasöründe `best.pt` adlı en iyi model dosyası oluşur.
- Bu model, daha sonra gerçek zamanlı algılama yapmak üzere `model_inference/untitled1.py` dosyasında kullanılacaktır.


##  Notlar
- Eğitim sırasında hata alırsanız terminaldeki çıktı mesajlarını dikkatle inceleyin.
- Bu yapı sayesinde farklı veri setleri veya farklı model konfigürasyonlarıyla kolayca yeniden eğitim yapılabilir.

