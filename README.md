# Teleoperation-Assisted Autonomous Excavator Design & Modeling 🚜🤖

This repository contains the complete conceptual design, kinematic modeling, ROS-based autonomous algorithms, and embedded systems architecture for a teleoperation-assisted autonomous excavator.

![Gazebo Terrain & Target Truck](media/images/13.png)

![RViz OctoMap Volumetric Mapping](media/images/14.png)

## 🎯 Project Overview
In industries with harsh and hazardous environments like mining and construction, minimizing human exposure while maximizing operational efficiency is a critical engineering challenge. This project aims to transform traditional heavy machinery into smart, situational-aware systems. By developing a digital twin of a CAT 349E excavator, the system achieved an 84% operational success rate in end-to-end autonomous dig-and-load cycles across 100 simulation trials. 

## ⚙️ Technical Specifications
* **Simulation Environment:** ROS Noetic & Gazebo (ODE Physics Engine)
* **Base Model:** 1:10 scaled Caterpillar 349E excavator
* **Perception:** Dual RGB-D Depth Cameras (640x480 VGA, 10Hz)
* **Hardware Prototyping:** Dual-Core ESP32 microcontroller with PCA9685 PWM driver and DRV8833 H-Bridges
* **Actuators:** N20 DC Gearmotors (50 RPM for torque, 1000 RPM for linear actuators)
* **Power Management:** 7.4V 2S Li-ion battery (2450 mAh) managed by a 13A BMS

## 🔬 Engineering Methodology & Algorithms
All simulation and autonomous control phases were executed using **ROS Noetic**, while the physical prototype was driven by custom C++ embedded firmware. The engineering workflow includes:

1. **Kinematic Modeling:** The 4-DOF manipulator (swing, boom, arm, bucket) was mapped using URDF. Inverse kinematics were solved numerically via the MoveIt! framework and KDL library to avoid singularity states.
2. **3D Perception & Mapping:** Point Cloud data from RGB-D sensors were converted into volumetric maps using the OctoMap algorithm to scan dynamic terrains.
3. **Computer Vision:** Target truck localization was achieved dynamically using HSV color space masking and image moments via OpenCV.
4. **Trajectory Generation:** To eliminate mechanical jerks during operations, a custom Cosine Interpolation (S-Curve) motor was developed for smooth acceleration.
5. **Hardware Proof of Concept:** A 6-axis open-loop physical prototype was manufactured, featuring low-latency teleoperation controlled by a Sony DualSense gamepad over Wi-Fi/Bluetooth.

![Physical Prototype](media/prototype.png)

## 📂 Repository Structure
* `/ros_workspace`: Contains ROS Noetic packages, Gazebo simulation environments, URDF models, MoveIt! configurations, and Python/OpenCV autonomy scripts.
* `/embedded_systems`: PlatformIO-based C++ source code for ESP32 teleoperation and motor driver control logic.
* `/cad_files`: SolidWorks native files and exported .STEP/.STL files for 3D printing of the 1:10 scale physical prototype.
* `/documents`: Comprehensive engineering design report (in Turkish) detailing dynamic equations, electrical schematics, and simulation outputs.
* `/media`: Contains project videos and high-resolution images demonstrating the Gazebo simulation and the physical prototype in action.

---
*Designed by Erdoğan Kır as a senior Mechatronics Engineering design project.*

NON-COMMERCIAL USE ONLY

---
# Teleoperasyon Destekli Otonom Ekskavatör Tasarımı ve Modellemesi 🚜🤖

Bu depo, teleoperasyon destekli otonom bir ekskavatöre ait kavramsal tasarım, kinematik modelleme, ROS tabanlı otonom algoritmalar ve gömülü sistem mimarisini içermektedir.

![Gazebo Terrain & Target Truck](media/16.png)

![RViz OctoMap Volumetric Mapping](media/17.jpg)

## 🎯 Proje Özeti
Madencilik ve inşaat gibi zorlu saha koşullarına sahip sektörlerde, operasyonel verimliliği maksimize ederken insan riskini minimize etmek kritik bir mühendislik hedefidir. Bu proje, geleneksel ağır iş makinelerini çevresel farkındalığa sahip akıllı sistemlere dönüştürmeyi amaçlamaktadır. CAT 349E ekskavatörünün dijital ikizi geliştirilmiş ve sistem, 100 simülasyon denemesinde uçtan uca otonom kazı-yükleme döngülerinde %84 operasyonel başarı oranına ulaşmıştır.

## ⚙️ Teknik Özellikler
* **Simülasyon Ortamı:** ROS Noetic ve Gazebo (ODE Fizik Motoru)
* **Referans Model:** 1:10 ölçekli Caterpillar 349E ekskavatör
* **Algılayıcılar:** Çift RGB-D Derinlik Kamerası (640x480 VGA, 10Hz)
* **Donanım Prototipi:** PCA9685 PWM sürücü ve DRV8833 köprülerine sahip Çift Çekirdekli ESP32 mikrodenetleyici
* **Aktüatörler:** N20 Redüktörlü DC Motorlar (Tork için 50 RPM, lineer aktüatörler için 1000 RPM)
* **Güç Yönetimi:** 13A BMS ile yönetilen 7.4V 2S Li-ion batarya (2450 mAh)

## 🔬 Mühendislik Metodolojisi ve Algoritmalar
Tüm simülasyon ve otonom kontrol aşamaları **ROS Noetic** kullanılarak gerçekleştirilmiş, fiziksel prototip ise özel C++ gömülü yazılımlarla sürülmüştür. Mühendislik iş akışı şunları içerir:

1. **Kinematik Modelleme:** 4 serbestlik dereceli manipülatör (kule, bom, arm, kova) URDF kullanılarak modellenmiştir. Ters kinematik hesaplamaları, tekillik (singularity) durumlarından kaçınmak için MoveIt! ve KDL kütüphanesi ile nümerik olarak çözülmüştür.
2. **3B Algılama ve Haritalama:** Dinamik arazileri taramak için RGB-D sensörlerden gelen Nokta Bulutu (Point Cloud) verileri, OctoMap algoritması kullanılarak hacimsel haritalara dönüştürülmüştür.
3. **Bilgisayarlı Görü:** Hedef kamyonun dinamik tespiti, OpenCV üzerinden HSV renk uzayı maskelemesi ve görüntü momentleri (image moments) kullanılarak sağlanmıştır.
4. **Yörünge Planlaması:** Operasyonlar sırasında mekanik sarsıntıları önlemek ve ivmelenmeyi yumuşatmak için Kosinüs İnterpolasyon (S-Curve) motoru geliştirilmiştir.
5. **Donanımsal İspat (Proof of Concept):** Wi-Fi/Bluetooth üzerinden Sony DualSense oyun kumandası ile kontrol edilen, düşük gecikmeli teleoperasyon yeteneğine sahip 6 eksenli açık çevrim bir fiziksel prototip üretilmiştir.

![Physical Prototype](media/prototype.png)

## 📂 Depo Yapısı
* `/ros_workspace`: ROS Noetic paketlerini, Gazebo simülasyon ortamlarını, URDF modellerini, MoveIt! yapılandırmalarını ve Python/OpenCV otonomi algoritmalarını içerir.
* `/embedded_systems`: ESP32 teleoperasyon ve motor sürücü kontrol mantığı için PlatformIO tabanlı C++ kaynak kodları.
* `/cad_files`: 1:10 ölçekli fiziksel prototipin 3B basımı için SolidWorks yerel parça dosyaları ve dışa aktarılmış .STEP/.STL dosyaları.
* `/documents`: Dinamik denklemleri, elektronik şemaları ve simülasyon çıktılarını detaylandıran kapsamlı mühendislik bitirme raporu.
* `/media`: Gazebo simülasyonunu ve fiziksel prototipin çalışmasını gösteren proje videolarını ve yüksek çözünürlüklü görselleri içerir.

---
*Mekatronik Mühendisliği tasarım projesi olarak Erdoğan Kır tarafından tasarlanmıştır.*

SADECE TİCARİ OLMAYAN KULLANIM İÇİNDİR
