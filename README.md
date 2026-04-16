# Akıllı Video Analizi: Doğal Dil Komutlu Örüntü Tanıma Sistemi

[cite_start]Bu proje, Eskişehir Osmangazi Üniversitesi Bilgisayar Mühendisliği Yüksek Lisans Programı kapsamında yer alan "Örüntü Tanıma Sistemleri" dersi için geliştirilmiş bütünleşik bir yapay zeka sistemidir[cite: 22, 179, 203]. 

[cite_start]Dışarıdan yüklenen herhangi bir video akışını analiz eden sistem, kullanıcının girdiği doğal dil komutlarına (Örn: "arabaları bul", "kaza tespiti yap") göre gerçek zamanlı tepki verebilmektedir[cite: 4, 8, 203]. [cite_start]Projenin temel amacı salt nesne tanıma işleminin ötesine geçerek; sahadaki fiziksel olayları (kaza riski, trafik akış yönü) anlamlandıran mühendislik odaklı bir analiz aracı oluşturmaktır[cite: 5, 204].

## 🚀 Temel Özellikler ve Algoritmik Yaklaşımlar

**Asenkron Komut İşleme (HCI):** Sistem, "arabaları bul", "insanları takip et" veya "temizle" gibi komutları asenkron olarak ayrıştırıp hedef sınıfları belirler[cite: 8]. [cite_start]GUI ile modelin çalışma thread'leri birbirinden izole edilerek akıcı bir kullanıcı deneyimi sağlanmıştır[cite: 19, 238].
**Sezgisel (Heuristic) Kaza Tespiti:** Ekrandaki araçların merkez koordinatları anlık olarak tespit edilir[cite: 9]. [cite_start]Ardışık araçların birbirine olan Öklid mesafesi sürekli hesaplanarak, çarpışma eşiğinden fazla yaklaşılması durumunda sistem görsel uyarı (kırmızı flaş ve vektör çizgisi) üretir[cite: 10].
**Farneback Optik Akış Analizi:** İki ardışık kare arasındaki piksel değişimleri analiz edilerek videodaki genel hareket yönü ve büyüklüğü yoğun optik akış algoritması ile hesaplanır ve hareket eden pikseller vektörel olarak görselleştirilir[cite: 11, 12, 18, 194].
**Nesne Sayımı ve Çoklu Takip (Tracking):** Seçilen hedef sınıflar ardışık karelerde benzersiz kimliklerle (ID) izlenir ve ekrandaki toplam sayıları canlı sayaç ile arayüze yansıtılır[cite: 13, 210].
**Dinamik Güven Eşiği Yönetimi:** Modelin tespit hassasiyeti (Confidence Threshold), arayüze entegre edilen bir kontrol paneli üzerinden canlı olarak yönetilebilir[cite: 6, 205]. [cite_start]Bu sayede Precision/Recall dengesi sahada ayarlanabilmektedir[cite: 236].

## 🛠 Kullanılan Teknolojiler

* **YOLO26 (Ultralytics):** Derin öğrenme tabanlı nesne tespiti ve takibi. [cite_start]NMS-free (Non-Maximum Suppression gerektirmeyen) yapısı sayesinde video akışlarında yüksek hızlı çıkarım (inference) sağlar[cite: 16, 17, 212].
* [cite_start]**OpenCV (cv2) & NumPy:** Video kare okuma işlemleri, matris operasyonları, Farneback optik akış algoritması ve ekrana vektörel grafiklerin (sınırlayıcı kutu, uyarı çizgileri) çizilmesi görevlerini üstlenir[cite: 18, 213].
* [cite_start]**Python:** Sistemin temel dili olup, model, arayüz ve donanım arasındaki asenkron iletişimi sağlar[cite: 19, 214].
* [cite_start]**Tkinter & Pillow (PIL):** Etkileşimli GUI tasarımı ve OpenCV matris formatındaki görüntülerin arayüze entegrasyonu için kullanılmıştır[cite: 20, 215].
