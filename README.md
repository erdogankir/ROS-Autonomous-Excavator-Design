# Teleoperasyon Destekli Otonom Ekskavatör Tasarımı ve Modellemesi

![ROS Noetic](https://img.shields.io/badge/ROS-Noetic-green.svg)
![Python 3](https://img.shields.io/badge/Python-3-blue.svg)
![C++](https://img.shields.io/badge/C++-14-blue.svg)
![ESP32](https://img.shields.io/badge/Platform-ESP32-orange.svg)

Bu depo, endüstriyel standartlardaki bir ekskavatörün (CAT 349E referans alınarak) ROS Noetic tabanlı dijital ikizinin oluşturulması, otonom kazı-yükleme algoritmalarının geliştirilmesi ve ESP32 tabanlı 6 eksenli bir fiziksel teleoperasyon prototipinin tasarım dosyalarını içermektedir.

<p align="center">
  <img src="docs/16.png" width="45%" alt="Gazebo Simülasyon Ortamı">
  <img src="docs/17.jpg" width="45%" alt="RViz Voxel OctoMap">
</p>

## 📂 Depo İçeriği ve Klasör Yapısı

Projeyi oluşturan mekatronik bileşenler (yazılım, donanım ve simülasyon) modüler bir yapıda organize edilmiştir:

* **`ros_workspace/`**: ROS Noetic çalışma alanı. Gazebo simülasyon ortamı, URDF kinematik modelleri, MoveIt! konfigürasyonları ve otonomi/bilgisayarlı görü (OpenCV) algoritmalarını barındırır.
* **`embedded_systems/`**: Fiziksel prototipin kontrolü için ESP32, PCA9685 ve DRV8833 sürücü topolojisini içeren PlatformIO tabanlı C++ yazılımları. DualSense ile düşük gecikmeli teleoperasyon yeteneğine sahiptir.
* **`cad_files/`**: Sistemin 3B basıma hazır (STL) ve montaj (STEP) dosyaları.
* **`documents/`**: Proje bitirme raporu ve sistem mimarisi şemaları.

## 🚀 Temel Özellikler (Otonomi ve Kinematik)

- **Çevresel Farkındalık:** Çift RGB-D derinlik sensörü füzyonu ile OctoMap tabanlı 3B hacimsel haritalandırma (Nokta bulutu / Point Cloud verilerinin işlenmesi).
- **Adaptif Yörünge Planlaması:** Kosinüs İnterpolasyon Motoru (S-Curve) ile ani sarsıntıları (jerk) engelleyen yumuşak yörünge geçişleri ve MoveIt! KDL çözücüsü ile ters kinematik (IK) hesaplamaları.
- **Hedef Tespiti:** HSV renk uzayı ve görüntü momentleri kullanılarak bilgisayarlı görü tabanlı dinamik kamyon kasası lokalizasyonu.
- **Teleoperasyon (Proof of Concept):** Wi-Fi/Bluetooth altyapısı üzerinden oyun kumandası ile açık çevrim makine kontrolü.

## 🛠️ Donanım Altyapısı (Fiziksel Prototip)

Sistemin donanımsal ispatı (Proof of Concept) amacıyla üretilen 1:10 ölçekli fiziksel prototip, kapalı çevrim endüstriyel donanımlara düşük maliyetli bir alternatif olarak geliştirilmiştir.

* **Ana Kontrolcü:** Çift çekirdekli ESP32
* **Motor Sürücü:** 4 x DRV8833 (H-Bridge) ve PCA9685 (16-Kanal PWM Genişletici)
* **Aktüatörler:** N20 Redüktörlü DC Motorlar (50 RPM Tork ve 1000 RPM Hız konfigürasyonları)
* **Güç Yönetimi:** 2S Li-ion (7.4V) batarya, BMS modülü ve lojik hat için MP1584 Step-Down konvertör.

## 🔮 Gelecek Çalışmalar (Future Works)

Projenin bir sonraki fazında, sistem mimarisinin ROS Noetic'ten **ROS 2 (Humble/Iron)** ortamına geçirilmesi (migration) planlanmaktadır. Bu sayede DDS (Data Distribution Service) altyapısının getirdiği gerçek zamanlı haberleşme avantajları ile otonom döngülerin kararlılığının artırılması ve birden fazla iş makinesinin aynı şantiye ağında (multi-agent) senkronize çalışabilmesi hedeflenmektedir.
