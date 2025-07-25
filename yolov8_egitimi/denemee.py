# Gerekli kütüphaneyi içe aktar
from ultralytics import YOLO
import os

class YOLOTrainer:
    """
    YOLOv8 modelini özel bir veri seti ile eğitmek için kullanılan sınıf.
    Küçük veri setleri için optimize edilmiş hiperparametreler içerir.
    """
    def __init__(self, data_yaml_path: str, pretrained_model_name: str = 'yolov8n.pt'):
        """
        Eğitici sınıfını başlatır.

        Args:
            data_yaml_path (str): 'data.yaml' dosyasının tam yolu.
            pretrained_model_name (str): Eğitimi başlatmak için kullanılacak
                                         önceden eğitilmiş modelin adı.
                                         Küçük veri setleri için 'yolov8n.pt' (Nano)
                                         iyi bir başlangıçtır.
        """
        if not os.path.exists(data_yaml_path):
            raise FileNotFoundError(f"Veri YAML dosyası bulunamadı: {data_yaml_path}")

        self.data_yaml_path = data_yaml_path
        self.pretrained_model = pretrained_model_name
        self.model = YOLO(self.pretrained_model)

    def train(self):
        """
        Modeli, küçük veri setleri için ayarlanmış hiperparametrelerle eğitir.
        """
        print(f"'{self.pretrained_model}' modeli yüklenerek eğitim başlatılıyor...")
        print(f"Veri seti konfigürasyonu: {self.data_yaml_path}")

        try:
            results = self.model.train(
                # --- Temel Ayarlar ---
                data=self.data_yaml_path,
                epochs=200,  # Küçük veri setinde ezberlemeyi görmek için epoch sayısı yeterli.
                             # Gerekirse artırılabilir ancak overfitting'e dikkat edin.
                patience=20, # 20 epoch boyunca val_loss iyileşmezse eğitimi durdur.
                batch=8,     # GPU belleğinize göre ayarlayın. Küçük set için 4 veya 8 ideal.
                imgsz=640,   # Görüntü boyutu. Standart 640.

                # --- Küçük Veri Seti İçin Kritik Hiperparametreler ---
                # Modelin sıfırdan öğrenmesi yerine mevcut bilgiyi yavaşça adapte etmesi için
                # daha düşük bir öğrenme oranı kullanıyoruz.
                lr0=0.001,    # Başlangıç öğrenme oranı (varsayılan: 0.01).
                lrf=0.01,     # Son öğrenme oranı (lr0'a göre oran).

                # Aşırı ezberlemeyi (overfitting) önlemek için veri artırma (augmentation)
                # ayarlarını aktif tutuyoruz. Bu, 31 görüntüyü sanki daha fazlaymış gibi gösterir.
                hsv_h=0.015,  # Renk tonu değişimi
                hsv_s=0.7,    # Doygunluk değişimi
                hsv_v=0.4,    # Parlaklık değişimi
                degrees=10.0, # Rastgele döndürme derecesi
                translate=0.1,# Görüntüyü kaydırma oranı
                scale=0.5,    # Görüntüyü ölçekleme (yakınlaştırma/uzaklaştırma)
                fliplr=0.5,   # Yatayda rastgele çevirme ihtimali

                # --- Proje Yönetimi ---
                project='YOLOv8_Custom_Training', # Sonuçların kaydedileceği ana klasör
                name='small_dataset_run_1'      # Bu spesifik eğitimin adı
            )
            print("Eğitim tamamlandı!")
            print(f"En iyi modelin yolu: {results.save_dir}/weights/best.pt")
            return results

        except Exception as e:
            print(f"Eğitim sırasında bir hata oluştu: {e}")
            return None

# --- BU BÖLÜMÜ KENDİ BİLGİLERİNİZLE GÜNCELLEYİN ---
if __name__ == '__main__':
    # 1. data.yaml dosyanızın tam yolunu buraya yazın.
    # Örnek: "C:/Users/KullaniciAdi/Desktop/my_dataset/data.yaml"
    # Windows'ta yolları belirtirken ya çift ters eğik çizgi (\\) ya da
    # tek düz eğik çizgi (/) kullanın.
    yaml_path = r"C:\Users\hp\Desktop\krank.v3i.yolov8\data.yaml"

    # 2. Sınıfı oluştur ve eğitimi başlat
    trainer = YOLOTrainer(data_yaml_path=yaml_path, pretrained_model_name='yolov8n.pt')
    trainer.train()
