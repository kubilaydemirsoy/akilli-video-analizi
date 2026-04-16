import cv2
import numpy as np
import math
import tkinter as tk
from tkinter import filedialog, scrolledtext, Scale, HORIZONTAL
from PIL import Image, ImageTk
from ultralytics import YOLO

class Oruntu:
    def __init__(self, root):
        self.root = root
        self.root.title("Akıllı Video Analizi")
        self.root.geometry("1050x700") # Arayüzü biraz daha uzatıldı

        # Sistem Durumu Değişkenleri
        self.cap = None
        self.action = "normal"  
        self.target_class = None
        self.is_running = False
        
        # Optik akış için önceki kare hafızası
        self.prev_gray = None 

        self.log_message("[BİLGİ] YOLO26 Modeli yükleniyor, lütfen bekleyin...")
        try:
            self.model = YOLO("yolo26n.pt")
            self.log_message("[BAŞARILI] Model yüklendi.")
        except Exception as e:
            self.log_message(f"[HATA] Model yüklenemedi: {e}")

        # COCO Veri Seti - Kelime eşleştirmeleri
        self.CLASS_MAP = {
            "insan": 0, "yaya": 0, "kişi": 0,
            "araba": 2, "araç": 2, "otomobil": 2,
            "motosiklet": 3, "otobüs": 5, "kamyon": 7
        }
        # Araç sınıflarının listesi (Kaza tespiti için)
        self.vehicle_classes = [2, 3, 5, 7] 

        self.setup_ui()

    def setup_ui(self):
        """Arayüz bileşenlerini oluşturur ve yerleştirir."""
        # Sol Panel (Video)
        self.video_frame = tk.Frame(self.root, bg="black", width=640, height=480)
        self.video_frame.pack(side=tk.LEFT, padx=10, pady=10)
        self.video_label = tk.Label(self.video_frame, bg="black")
        self.video_label.pack()

        # Sağ Panel (Kontroller)
        self.control_frame = tk.Frame(self.root, width=350)
        self.control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        self.btn_select = tk.Button(self.control_frame, text="📁 Video Seç", command=self.load_video, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
        self.btn_select.pack(pady=10, fill=tk.X)

        # YENİ ÖZELLİK: Güven Eşiği (Confidence Threshold) Kaydırıcısı
        self.conf_slider = Scale(self.control_frame, from_=0.10, to=1.00, resolution=0.05, orient=HORIZONTAL, label="Hassasiyet / Güven Eşiği (Conf)")
        self.conf_slider.set(0.25) # Varsayılan olarak bizim tespit ettiğimiz optimum değer (0.25) ile başlar
        self.conf_slider.pack(fill=tk.X, pady=(0, 10))

        tk.Label(self.control_frame, text="Komut Örnekleri:\n- arabaları bul\n- insanları takip et\n- kaza tespiti yap\n- optik akışı göster\n- araçları say\n- temizle", justify="left", font=("Arial", 9)).pack(anchor="w", pady=(0, 5))
        
        self.cmd_entry = tk.Entry(self.control_frame, font=("Arial", 12))
        self.cmd_entry.pack(fill=tk.X, pady=5)
        self.cmd_entry.bind("<Return>", lambda event: self.process_command())

        self.btn_send = tk.Button(self.control_frame, text="🚀 Komut Çalıştır", command=self.process_command, font=("Arial", 10, "bold"), bg="#2196F3", fg="white")
        self.btn_send.pack(fill=tk.X)

        tk.Label(self.control_frame, text="Sistem Analiz Logları:", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 0))
        self.log_area = scrolledtext.ScrolledText(self.control_frame, height=14, width=40, font=("Consolas", 9), bg="#1e1e1e", fg="#00ff00")
        self.log_area.pack(fill=tk.BOTH, expand=True)

    def log_message(self, message):
        if hasattr(self, 'log_area'):
            self.log_area.insert(tk.END, message + "\n")
            self.log_area.see(tk.END)
        else:
            print(message)

    def load_video(self):
        video_path = filedialog.askopenfilename(title="İşlenecek Videoyu Seçin", filetypes=[("Video Dosyaları", "*.mp4 *.avi *.mov")])
        if video_path:
            self.cap = cv2.VideoCapture(video_path)
            self.is_running = True
            self.action = "normal"
            self.prev_gray = None
            self.log_message(f"--- YENİ VİDEO YÜKLENDİ ---")
            self.update_frame()

    def process_command(self):
        cmd = self.cmd_entry.get().lower().strip()
        self.cmd_entry.delete(0, tk.END)

        if not cmd: return
        self.log_message(f"\n> Komut: '{cmd}'")

        if cmd in ["temizle", "durdur", "normal"]:
            self.action = "normal"
            self.prev_gray = None
            self.log_message("Mod: NORMAL (Analizler durduruldu).")
            return

        if "kaza" in cmd or "çarpışma" in cmd:
            self.action = "crash_detect"
            self.log_message("Mod: KAZA TESPİTİ.")
            return
            
        if "akış" in cmd or "optik" in cmd or "hareket" in cmd:
            self.action = "optical_flow"
            self.prev_gray = None 
            self.log_message("Mod: OPTİK AKIŞ.")
            return

        if "say" in cmd:
            self.action = "count"
            self.log_message("Mod: NESNE SAYIMI aktif.")
            for key, val in self.CLASS_MAP.items():
                if key in cmd:
                    self.target_class = val
                    self.log_message(f"-> Sayılacak hedef: Sınıf ID {val}")
                    return
            self.target_class = 2 
            return

        detected_class = None
        for key, val in self.CLASS_MAP.items():
            if key in cmd:
                detected_class = val
                break
        
        if detected_class is not None:
            self.target_class = detected_class
            if "takip" in cmd or "izle" in cmd:
                self.action = "track"
                self.log_message(f"Mod: TAKİP (Sınıf ID: {detected_class})")
            elif "bul" in cmd or "işaretle" in cmd:
                self.action = "detect"
                self.log_message(f"Mod: TESPİT (Sınıf ID: {detected_class})")
        else:
            self.log_message("[HATA] Bilinmeyen komut örüntüsü.")

    def update_frame(self):
        if self.is_running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 480))
                overlay = frame.copy()
                
                # Arayüzden anlık eşik (confidence) değerini al
                current_conf = self.conf_slider.get()

                # 1. TEMEL TESPİT VE TAKİP
                if self.action in ["track", "detect"] and self.target_class is not None:
                    if self.action == "track":
                        results = self.model.track(frame, classes=[self.target_class], persist=True, verbose=False, conf=current_conf)
                    else:
                        results = self.model(frame, classes=[self.target_class], verbose=False, conf=current_conf)
                    frame = results[0].plot()

                # 2. KAZA TESPİTİ (Heuristic Yaklaşım)
                elif self.action == "crash_detect":
                    results = self.model(frame, classes=self.vehicle_classes, verbose=False, conf=current_conf)
                    boxes = results[0].boxes.xyxy.cpu().numpy() 
                    centers = []
                    
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box)
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        centers.append((cx, cy, x1, y1, x2, y2))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

                    for i in range(len(centers)):
                        for j in range(i + 1, len(centers)):
                            c1, c2 = centers[i], centers[j]
                            distance = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
                            
                            if distance < 50:
                                cv2.line(frame, (c1[0], c1[1]), (c2[0], c2[1]), (0, 0, 255), 3)
                                cv2.putText(frame, "!!! KAZA RISKI !!!", (min(c1[0], c2[0]), min(c1[1], c2[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                                cv2.rectangle(overlay, (0, 0), (640, 480), (0, 0, 255), -1)
                                cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)

                # 3. OPTİK AKIŞ (Hareket Analizi)
                elif self.action == "optical_flow":
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    if self.prev_gray is not None:
                        flow = cv2.calcOpticalFlowFarneback(self.prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
                        step = 16
                        for y in range(0, gray.shape[0], step):
                            for x in range(0, gray.shape[1], step):
                                fx, fy = flow[y, x]
                                if abs(fx) > 2 or abs(fy) > 2: 
                                    cv2.line(frame, (x, y), (int(x + fx), int(y + fy)), (0, 255, 0), 1)
                                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                    self.prev_gray = gray

                # 4. NESNE SAYIMI
                elif self.action == "count":
                    results = self.model(frame, classes=[self.target_class], verbose=False, conf=current_conf)
                    count = len(results[0].boxes)
                    frame = results[0].plot() 
                    cv2.rectangle(frame, (10, 10), (350, 70), (0, 0, 0), -1)
                    cv2.putText(frame, f"Ekranda {count} Nesne Var", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                # Görüntüyü arayüze yansıt
                cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(cv2_image)
                imgtk = ImageTk.PhotoImage(image=pil_image)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

                self.root.after(30, self.update_frame)
            else:
                self.log_message("[BİLGİ] Video sona erdi.")
                self.cap.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = Oruntu(root)
    root.mainloop()