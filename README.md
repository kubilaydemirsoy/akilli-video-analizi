# Akıllı Video Analizi

Dışarıdan yüklenen herhangi bir video akışını analiz eden sistem, kullanıcının girdiği doğal dil komutlarına (Örn: "arabaları bul", "kaza tespiti yap") göre gerçek zamanlı tepki verebilmektedir. Projenin temel amacı salt nesne tanıma işleminin ötesine geçerek; sahadaki fiziksel olayları (kaza riski, trafik akış yönü) anlamlandıran mühendislik odaklı bir analiz aracı oluşturmaktır.

## 🚀 Temel Özellikler ve Algoritmik Yaklaşımlar

* **Asenkron Komut İşleme (HCI):** Sistem, "arabaları bul", "insanları takip et" veya "temizle" gibi komutları asenkron olarak ayrıştırıp hedef sınıfları belirler. GUI ile modelin çalışma thread'leri birbirinden izole edilerek akıcı bir kullanıcı deneyimi sağlanmıştır.

* **Sezgisel (Heuristic) Kaza Tespiti:** Ekrandaki araçların merkez koordinatları anlık olarak tespit edilir. Ardışık araçların birbirine olan Öklid mesafesi sürekli hesaplanarak, çarpışma eşiğinden fazla yaklaşılması durumunda sistem görsel uyarı (kırmızı flaş ve vektör çizgisi) üretir.

* **Farneback Optik Akış Analizi:** İki ardışık kare arasındaki piksel değişimleri analiz edilerek videodaki genel hareket yönü ve büyüklüğü yoğun optik akış algoritması ile hesaplanır ve hareket eden pikseller vektörel olarak görselleştirilir.

* **Nesne Sayımı ve Çoklu Takip (Tracking):** Seçilen hedef sınıflar ardışık karelerde benzersiz kimliklerle (ID) izlenir ve ekrandaki toplam sayıları canlı sayaç ile arayüze yansıtılır.
* **Dinamik Güven Eşiği Yönetimi:** Modelin tespit hassasiyeti (Confidence Threshold), arayüze entegre edilen bir kontrol paneli üzerinden canlı olarak yönetilebilir. Bu sayede Precision/Recall dengesi sahada ayarlanabilmektedir.

## 🛠 Kullanılan Teknolojiler

* **YOLO26 (Ultralytics):** Derin öğrenme tabanlı nesne tespiti ve takibi. [cite_start]NMS-free (Non-Maximum Suppression gerektirmeyen) yapısı sayesinde video akışlarında yüksek hızlı çıkarım (inference) sağlar.
* **OpenCV (cv2) & NumPy:** Video kare okuma işlemleri, matris operasyonları, Farneback optik akış algoritması ve ekrana vektörel grafiklerin (sınırlayıcı kutu, uyarı çizgileri) çizilmesi görevlerini üstlenir.
* **Python:** Sistemin temel dili olup, model, arayüz ve donanım arasındaki asenkron iletişimi sağlar.
* **Tkinter & Pillow (PIL):** Etkileşimli GUI tasarımı ve OpenCV matris formatındaki görüntülerin arayüze entegrasyonu için kullanılmıştır.
