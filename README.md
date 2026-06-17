# Teleoperation-Assisted Autonomous Excavator Design & Modeling 🚜🤖

[cite_start]This repository contains the complete conceptual design, kinematic modeling, ROS-based autonomous algorithms, and embedded systems architecture for a teleoperation-assisted autonomous excavator[cite: 4].

![Gazebo Terrain & Target Truck](docs/16.png)

![RViz OctoMap Volumetric Mapping](docs/17.jpg)

## 🎯 Project Overview
[cite_start]In industries with harsh and hazardous environments like mining and construction, minimizing human exposure while maximizing operational efficiency is a critical engineering challenge[cite: 117]. [cite_start]This project aims to transform traditional heavy machinery into smart, situational-aware systems[cite: 118, 126]. [cite_start]By developing a digital twin of a CAT 349E excavator, the system achieved an 84% operational success rate in end-to-end autonomous dig-and-load cycles across 100 simulation trials[cite: 111, 119]. 

## ⚙️ Technical Specifications
* [cite_start]**Simulation Environment:** ROS Noetic & Gazebo (ODE Physics Engine) [cite: 300]
* [cite_start]**Base Model:** 1:10 scaled Caterpillar 349E excavator [cite: 196]
* [cite_start]**Perception:** Dual RGB-D Depth Cameras (640x480 VGA, 10Hz) [cite: 207, 211]
* [cite_start]**Hardware Prototyping:** Dual-Core ESP32 microcontroller with PCA9685 PWM driver and DRV8833 H-Bridges [cite: 257, 259, 260]
* [cite_start]**Actuators:** N20 DC Gearmotors (50 RPM for torque, 1000 RPM for linear actuators) [cite: 262, 263]
* [cite_start]**Power Management:** 7.4V 2S Li-ion battery (2450 mAh) managed by a 13A BMS [cite: 275]

## 🔬 Engineering Methodology & Algorithms
[cite_start]All simulation and autonomous control phases were executed using **ROS Noetic**, while the physical prototype was driven by custom C++ embedded firmware[cite: 358]. The engineering workflow includes:

1. [cite_start]**Kinematic Modeling:** The 4-DOF manipulator (swing, boom, arm, bucket) was mapped using URDF[cite: 160]. [cite_start]Inverse kinematics were solved numerically via the MoveIt! framework and KDL library to avoid singularity states[cite: 166, 167].
2. [cite_start]**3D Perception & Mapping:** Point Cloud data from RGB-D sensors were converted into volumetric maps using the OctoMap algorithm to scan dynamic terrains[cite: 212].
3. [cite_start]**Computer Vision:** Target truck localization was achieved dynamically using HSV color space masking and image moments via OpenCV[cite: 217, 218, 219].
4. [cite_start]**Trajectory Generation:** To eliminate mechanical jerks during operations, a custom Cosine Interpolation (S-Curve) motor was developed for smooth acceleration[cite: 234].
5. [cite_start]**Hardware Proof of Concept:** A 6-axis open-loop physical prototype was manufactured, featuring low-latency teleoperation controlled by a Sony DualSense gamepad over Wi-Fi/Bluetooth[cite: 102, 286].

![Physical Prototype](docs/prototype.png)

## 📂 Repository Structure
* `/ros_workspace`: Contains ROS Noetic packages, Gazebo simulation environments, URDF models, MoveIt! configurations, and Python/OpenCV autonomy scripts.
* `/embedded_systems`: PlatformIO-based C++ source code for ESP32 teleoperation and motor driver control logic.
* `/cad_files`: SolidWorks native files and exported .STEP/.STL files for 3D printing of the 1:10 scale physical prototype.
* `/documents`: Comprehensive engineering design report (in Turkish) detailing dynamic equations, electrical schematics, and simulation outputs.

---
[cite_start]*Designed by Erdoğan Kır as a senior Mechatronics Engineering design project.* [cite: 6]

NON-COMMERCIAL USE ONLY

---
# Teleoperasyon Destekli Otonom Ekskavatör Tasarımı ve Modellemesi 🚜🤖

[cite_start]Bu depo, teleoperasyon destekli otonom bir ekskavatöre ait kavramsal tasarım, kinematik modelleme, ROS tabanlı otonom algoritmalar ve gömülü sistem mimarisini içermektedir[cite: 4].

![Gazebo Terrain & Target Truck](docs/16.png)

![RViz OctoMap Volumetric Mapping](docs/17.jpg)

## 🎯 Proje Özeti
[cite_start]Madencilik ve inşaat gibi zorlu saha koşullarına sahip sektörlerde, operasyonel verimliliği maksimize ederken insan riskini minimize etmek kritik bir mühendislik hedefidir[cite: 117]. [cite_start]Bu proje, geleneksel ağır iş makinelerini çevresel farkındalığa sahip akıllı sistemlere dönüştürmeyi amaçlamaktadır[cite: 118, 126]. [cite_start]CAT 349E ekskavatörünün dijital ikizi geliştirilmiş ve sistem, 100 simülasyon denemesinde uçtan uca otonom kazı-yükleme döngülerinde %84 operasyonel başarı oranına ulaşmıştır[cite: 111, 119].

## ⚙️ Teknik Özellikler
* [cite_start]**Simülasyon Ortamı:** ROS Noetic ve Gazebo (ODE Fizik Motoru) [cite: 300]
* [cite_start]**Referans Model:** 1:10 ölçekli Caterpillar 349E ekskavatör [cite: 196]
* [cite_start]**Algılayıcılar:** Çift RGB-D Derinlik Kamerası (640x480 VGA, 10Hz) [cite: 207, 211]
* [cite_start]**Donanım Prototipi:** PCA9685 PWM sürücü ve DRV8833 köprülerine sahip Çift Çekirdekli ESP32 mikrodenetleyici [cite: 257, 259, 260]
* [cite_start]**Aktüatörler:** N20 Redüktörlü DC Motorlar (Tork için 50 RPM, lineer aktüatörler için 1000 RPM) [cite: 262, 263]
* [cite_start]**Güç Yönetimi:** 13A BMS ile yönetilen 7.4V 2S Li-ion batarya (2450 mAh) [cite: 275]

## 🔬 Mühendislik Metodolojisi ve Algoritmalar
[cite_start]Tüm simülasyon ve otonom kontrol aşamaları **ROS Noetic** kullanılarak gerçekleştirilmiş, fiziksel prototip ise özel C++ gömülü yazılımlarla sürülmüştür[cite: 358]. Mühendislik iş akışı şunları içerir:

1. [cite_start]**Kinematik Modelleme:** 4 serbestlik dereceli manipülatör (kule, bom, arm, kova) URDF kullanılarak modellenmiştir[cite: 160]. [cite_start]Ters kinematik hesaplamaları, tekillik (singularity) durumlarından kaçınmak için MoveIt! ve KDL kütüphanesi ile nümerik olarak çözülmüştür[cite: 166, 167].
2. [cite_start]**3B Algılama ve Haritalama:** Dinamik arazileri taramak için RGB-D sensörlerden gelen Nokta Bulutu (Point Cloud) verileri, OctoMap algoritması kullanılarak hacimsel haritalara dönüştürülmüştür[cite: 212].
3. [cite_start]**Bilgisayarlı Görü:** Hedef kamyonun dinamik tespiti, OpenCV üzerinden HSV renk uzayı maskelemesi ve görüntü momentleri (image moments) kullanılarak sağlanmıştır[cite: 217, 218, 219].
4. [cite_start]**Yörünge Planlaması:** Operasyonlar sırasında mekanik sarsıntıları önlemek ve ivmelenmeyi yumuşatmak için Kosinüs İnterpolasyon (S-Curve) motoru geliştirilmiştir[cite: 234].
5. [cite_start]**Donanımsal İspat (Proof of Concept):** Wi-Fi/Bluetooth üzerinden Sony DualSense oyun kumandası ile kontrol edilen, düşük gecikmeli teleoperasyon yeteneğine sahip 6 eksenli açık çevrim bir fiziksel prototip üretilmiştir[cite: 102, 286].

![Physical Prototype](docs/prototype.png)

## 📂 Depo Yapısı
* `/ros_workspace`: ROS Noetic paketlerini, Gazebo simülasyon ortamlarını, URDF modellerini, MoveIt! yapılandırmalarını ve Python/OpenCV otonomi algoritmalarını içerir.
* `/embedded_systems`: ESP32 teleoperasyon ve motor sürücü kontrol mantığı için PlatformIO tabanlı C++ kaynak kodları.
* `/cad_files`: 1:10 ölçekli fiziksel prototipin 3B basımı için SolidWorks yerel parça dosyaları ve dışa aktarılmış .STEP/.STL dosyaları.
* `/documents`: Dinamik denklemleri, elektronik şemaları ve simülasyon çıktılarını detaylandıran kapsamlı mühendislik bitirme raporu.

---
[cite_start]*Mekatronik Mühendisliği tasarım projesi olarak Erdoğan Kır tarafından tasarlanmıştır.* [cite: 6]

SADECE TİCARİ OLMAYAN KULLANIM İÇİNDİR
