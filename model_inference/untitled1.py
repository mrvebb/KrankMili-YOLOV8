import cv2
from ultralytics import YOLO
import time
import os

# --- Configuration ---
MODEL_PATH = r"C:\Users\hp\Desktop\krank.v1i.yolov8\best.pt"
CRANKSHAFT_CLASS_ID = 0
INITIAL_DETECTION_DURATION = 10
NO_DETECTION_RESET_THRESHOLD = 40
RECOUNT_LOCK_DURATION = 40  # Sayım sonrası kilit süresi
CONF_THRESHOLD = 0.3
IOU_THRESHOLD = 0.4

class CrankshaftCounter:
    def __init__(self):
        self.first_detection_time = None
        self.last_detection_time = None
        self.total_count = 0
        self.is_counted = False
        self.is_present = False
        self.last_count_time = None
        self.last_print_time = 0
        self.print_interval = 2.0

    def reset_detection(self):
        self.first_detection_time = None
        self.last_detection_time = None
        self.is_counted = False
        self.is_present = False

    def update(self, detected):
        current_time = time.time()

        if detected:
            self.last_detection_time = current_time

            # İlk kez algılandıysa
            if not self.is_present:
                self.first_detection_time = current_time
                self.is_present = True
                self.is_counted = False
                self.print_status("Krank mili tespit edildi, sayım için bekleniyor...")
                return

            # Sayım zamanı geldiyse
            elif not self.is_counted and (current_time - self.first_detection_time) >= INITIAL_DETECTION_DURATION:
                if self.last_count_time and (current_time - self.last_count_time) < RECOUNT_LOCK_DURATION:
                    kalan = RECOUNT_LOCK_DURATION - (current_time - self.last_count_time)
                    if current_time - self.last_print_time >= self.print_interval:
                        self.print_status(f"Sayım engellendi. Yeniden sayım kilidi ({kalan:.1f}s)")
                        self.last_print_time = current_time
                    return

                self.total_count += 1
                self.is_counted = True
                self.last_count_time = current_time
                self.print_status(f"Krank mili sayıldı! TOPLAM: {self.total_count}")
                return

            # Bekleme sürecinde
            elif not self.is_counted:
                elapsed = current_time - self.first_detection_time
                if current_time - self.last_print_time >= self.print_interval:
                    self.print_status(f"Sayım için bekleniyor... ({elapsed:.1f}/{INITIAL_DETECTION_DURATION}s)")
                    self.last_print_time = current_time
                return

            # Sayılmış ve hala görüntüdeyse
            else:
                if current_time - self.last_print_time >= self.print_interval:
                    self.print_status(f"Krank mili hala görünümde. TOPLAM: {self.total_count}")
                    self.last_print_time = current_time
                return

        else:
            if self.is_present:
                self.print_status("Krank mili görünümden çıktı. Yeni nesne için hazır.")
                self.reset_detection()
                return

            if self.last_detection_time and (current_time - self.last_detection_time) >= NO_DETECTION_RESET_THRESHOLD:
                self.print_status(f"{NO_DETECTION_RESET_THRESHOLD}s zaman aşımı - durum sıfırlanıyor.")
                self.reset_detection()
                return

            if current_time - self.last_print_time >= self.print_interval:
                self.print_status(f"Krank mili bekleniyor... TOPLAM: {self.total_count}")
                self.last_print_time = current_time
            return

    def print_status(self, message):
        print(f"[{time.strftime('%H:%M:%S')}] {message}")

def test_camera():
    print("=== KAMERA TESTİ ===")
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Kamera {i}: MEVCUT")
            ret, frame = cap.read()
            if ret:
                print(f"  - Kare boyutu: {frame.shape}")
            cap.release()
        else:
            print(f"Kamera {i}: BULUNAMADI")
    print("===================")

def setup_camera(camera_id=0):
    print(f"Kamera {camera_id} açılıyor...")
    cap = cv2.VideoCapture(camera_id)
    if not cap.isOpened():
        print(f"HATA: Kamera {camera_id} açılamadı!")
        return None
    ret, frame = cap.read()
    if not ret:
        print("HATA: Kare okunamadı!")
        cap.release()
        return None
    print(f"Kamera başarıyla açıldı. Kare boyutu: {frame.shape}")
    return cap

def load_model():
    if not os.path.exists(MODEL_PATH):
        print(f"HATA: Model dosyası bulunamadı: {MODEL_PATH}")
        return None
    try:
        print("Model yükleniyor...")
        model = YOLO(MODEL_PATH)
        print("Model başarıyla yüklendi")
        print(f"Model sınıfları: {model.names}")
        print(f"Hedef sınıf ID {CRANKSHAFT_CLASS_ID}: {model.names.get(CRANKSHAFT_CLASS_ID, 'TANIMLANMAMIŞ!')}")
        return model
    except Exception as e:
        print(f"Model yükleme hatası: {e}")
        return None

def main():
    print("=== SİSTEM BAŞLATILIYOR ===")
    test_camera()
    model = load_model()
    if model is None:
        print("Model yüklenemedi, çıkılıyor...")
        return
    cap = setup_camera(0)
    if cap is None:
        print("Kamera açılamadı, çıkılıyor...")
        return

    counter = CrankshaftCounter()
    frame_count = 0

    print("=== ANA DÖNGÜ BAŞLATILDI ===")
    print("Çıkmak için 'q' tuşuna basın")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Kare okunamadı!")
                break

            frame_count += 1
            if frame_count % 60 == 0:
                print(f"Kare {frame_count} işlendi")

            try:
                results = model(frame, verbose=False)
            except Exception as e:
                print(f"YOLO tahmin hatası: {e}")
                continue

            detected = False
            detection_info = []

            if len(results) > 0:
                result = results[0]
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        if box.cls is None or len(box.cls) == 0:
                            continue
                        cls_id = int(box.cls[0].item())
                        conf = float(box.conf[0].item())
                        cls_name = model.names.get(cls_id, f"Sınıf_{cls_id}")
                        detection_info.append(f"{cls_name}({conf:.2f})")

                        if cls_id == CRANKSHAFT_CLASS_ID:
                            detected = True
                            x1, y1, x2, y2 = map(int, box.xyxy[0])
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                            cv2.putText(frame, f"KRANK {conf:.2f}",
                                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            if detection_info and frame_count % 30 == 0:
                print(f"Tespitler: {', '.join(detection_info)}")

            counter.update(detected)

            cv2.putText(frame, f"Toplam: {counter.total_count}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if counter.is_present and not counter.is_counted:
                elapsed = time.time() - counter.first_detection_time if counter.first_detection_time else 0
                status_text = f"Sayim icin bekleniyor... {elapsed:.1f}s"
            elif counter.is_present and counter.is_counted:
                status_text = "Krank mili sayildi"
            elif detected:
                status_text = "Krank mili tespit edildi"
            else:
                status_text = "Krank mili bekleniyor..."

            cv2.putText(frame, status_text, (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            cv2.imshow('Crankshaft Counter - DEBUG', frame)

            key = cv2.waitKey(10) & 0xFF
            if key == ord('q'):
                print("Çıkış tuşuna basıldı")
                break
            elif key == ord('s'):
                cv2.imwrite(f"debug_frame_{frame_count}.jpg", frame)
                print(f"Ekran görüntüsü kaydedildi: debug_frame_{frame_count}.jpg")

    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("=== SİSTEM KAPATILIYOR ===")
        if cap:
            cap.release()
        cv2.destroyAllWindows()
        print("Sistem kapatıldı")

if __name__ == "__main__":
    main()
