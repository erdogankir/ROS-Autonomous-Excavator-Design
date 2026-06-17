#!/usr/bin/env python3
from std_srvs.srv import Empty
import sys
import rospy
import moveit_commander
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import Joy, PointCloud2, Image, JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np
import math
import tf2_ros
import tf2_sensor_msgs

class NihaiHibritKomutan:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('exca_nihai_otonom', anonymous=True)

        self.move_group = moveit_commander.MoveGroupCommander("exca_grup")
        self.move_group.set_max_velocity_scaling_factor(1)
        self.move_group.set_max_acceleration_scaling_factor(1)
        self.move_group.set_pose_reference_frame("base_link")
        self.move_group.set_planning_time(10.0) 
        self.move_group.set_num_planning_attempts(5)

        self.direkt_surucu = rospy.Publisher('/exca_grup_controller/command', JointTrajectory, queue_size=10)
        
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer)
        self.bulut_on = None     
        self.bulut_cukur = None  
        self.bridge = CvBridge()
        
        rospy.sleep(0.5)

        self.joy_data = None
        self.current_joints = [0.0, 0.0, 0.0, 0.0]
        self.otonom_mesaide = False 
        self.iptal_istendi = False 
        self.tarama_modu_aktif = False
        
        self.axis_kule, self.axis_arm, self.axis_kova, self.axis_bom = 0, 1, 3, 4
        self.btn_auto, self.btn_iptal, self.btn_deadman = 0, 2, 5   
        self.max_hiz = 1.0

        # Kamyon Hafızası
        self.bulunan_hedef_acisi = 0.0
        self.en_iyi_merkez_farki = 9999.0 
        self.kamyon_x = 0.0
        self.kamyon_y = 0.0
        self.kamyon_z = 0.0
        self.img_genislik = 640 
        
        self.topoloji_haritasi = {}

        rospy.Subscriber("/joy", Joy, self.joy_callback)
        rospy.Subscriber("/joint_states", JointState, self.joint_callback)
        rospy.Subscriber("/kamera_on/depth/points", PointCloud2, self.pc_on_callback)
        rospy.Subscriber("/kamera_cukur/depth/points", PointCloud2, self.pc_cukur_callback)
        rospy.Subscriber("/kamera_on/rgb/image_raw", Image, self.rgb_callback)

        rospy.loginfo("=== NİHAİ YAPAY ZEKA: NON-STOP KAZI SİSTEMİ AKTİF ===")

    def apply_deadzone(self, value, deadzone=0.15):
        return 0.0 if abs(value) < deadzone else value

    def pc_on_callback(self, data): self.bulut_on = data
    def pc_cukur_callback(self, data): self.bulut_cukur = data

    def joint_callback(self, data):
        try:
            idx1, idx2 = data.name.index("joint_1"), data.name.index("joint_2")
            idx3, idx4 = data.name.index("joint_3"), data.name.index("joint_4")
            self.current_joints = [data.position[idx1], data.position[idx2], data.position[idx3], data.position[idx4]]
        except ValueError: pass

    def joy_callback(self, data):
        self.joy_data = data
        if self.otonom_mesaide and data.buttons[self.btn_iptal] == 1:
            if not self.iptal_istendi: 
                rospy.logwarn("!!! ACİL İPTAL TETİKLENDİ !!!")
                self.iptal_istendi = True
                self.move_group.stop()
                self.move_group.clear_pose_targets()

    def rgb_callback(self, data):
        if not self.tarama_modu_aktif or self.iptal_istendi or self.bulut_on is None: return
        try: cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError: return

        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        # Mavi rengin OpenCV HSV karşılığı (H: 100-130 arası geniştir, mavinin her tonunu kapsar)
        maske = cv2.inRange(hsv, np.array([100, 100, 50]), np.array([130, 255, 255]))
        M = cv2.moments(maske)
        if M['m00'] > 5000: 
            cx = int(M['m10'] / M['m00'])
            merkez_farki = abs(cx - (self.img_genislik / 2))
            if merkez_farki < self.en_iyi_merkez_farki:
                self.en_iyi_merkez_farki = merkez_farki
                self.bulunan_hedef_acisi = self.current_joints[0]

    def guvenli_uyku(self, saniye):
        hedef = rospy.Time.now() + rospy.Duration(saniye)
        while rospy.Time.now() < hedef and not rospy.is_shutdown():
            if self.iptal_istendi: return False 
            rospy.sleep(0.1)
        return True

    def koordinat_cikar_ortalama(self):
        cx_cam, cy_cam, cz_cam = 0.08, 0.08, 0.51304
        k_x, k_z, k_d = [], [], []
        for p in pc2.read_points(self.bulut_on, field_names=("x", "y", "z"), skip_nans=True):
            if 0.4 < p[2] < 3.0 and abs(p[0]) <= 0.15:
                gercek_z = cz_cam - p[1]
                if 0.02 < gercek_z < 0.40:
                    k_x.append(p[0]); k_z.append(gercek_z); k_d.append(p[2])
        if len(k_z) > 10:
            avg_x = sum(k_x) / len(k_x)
            avg_d = sum(k_d) / len(k_d)
            theta = self.bulunan_hedef_acisi
            L1_x, L1_y = cx_cam + avg_d, cy_cam - avg_x
            self.kamyon_x = L1_x * math.cos(theta) - L1_y * math.sin(theta)
            self.kamyon_y = L1_x * math.sin(theta) + L1_y * math.cos(theta)
            self.kamyon_z = max(k_z)
            return True
        return False

    def koordinat_cikar_zirve(self):
        cx_cam, cy_cam, cz_cam = 0.08, 0.08, 0.51304
        noktalar = []
        for p in pc2.read_points(self.bulut_on, field_names=("x", "y", "z"), skip_nans=True):
            if 0.4 < p[2] < 3.0 and abs(p[0]) <= 0.15:
                gercek_z = cz_cam - p[1]
                if 0.02 < gercek_z < 0.40:
                    noktalar.append((p[0], gercek_z, p[2]))
        if len(noktalar) > 10:
            noktalar.sort(key=lambda n: n[1], reverse=True)
            tepeler = noktalar[:max(5, int(len(noktalar) * 0.15))]
            avg_x = sum(n[0] for n in tepeler) / len(tepeler)
            max_h = sum(n[1] for n in tepeler) / len(tepeler) 
            avg_d = sum(n[2] for n in tepeler) / len(tepeler)
            theta = self.bulunan_hedef_acisi
            L1_x, L1_y = cx_cam + avg_d, cy_cam - avg_x
            self.kamyon_x = L1_x * math.cos(theta) - L1_y * math.sin(theta)
            self.kamyon_y = L1_x * math.sin(theta) + L1_y * math.cos(theta)
            self.kamyon_z = max_h
            return True
        return False

    def s_curve_nokta_ekle(self, traj_msg, bas_acilar, bitis_acilar, bas_zamani, gecen_sure, n=30):
        for i in range(1, n + 1):
            oran = (1.0 - math.cos(math.pi * (i / n))) / 2.0
            p = JointTrajectoryPoint()
            p.positions = [bas_acilar[j] + (bitis_acilar[j] - bas_acilar[j]) * oran for j in range(4)]
            p.time_from_start = rospy.Duration(bas_zamani + (gecen_sure * (i / n)))
            traj_msg.points.append(p)
        return bitis_acilar

    def canli_z_yuksekligini_bul(self, hedef_x, hedef_y):
        if self.bulut_cukur is None: return 0.0
        try:
            trans = self.tf_buffer.lookup_transform("base_link", self.bulut_cukur.header.frame_id, rospy.Time(0), rospy.Duration(1.0))
            bulut_bl = tf2_sensor_msgs.do_transform_cloud(self.bulut_cukur, trans)
            z_list = [p[2] for p in pc2.read_points(bulut_bl, field_names=("x", "y", "z"), skip_nans=True) 
                      if math.hypot(p[0] - hedef_x, p[1] - hedef_y) < 0.15]
            return sum(z_list) / len(z_list) if z_list else 0.0
        except Exception: return 0.0

    def yaklas_ve_kaza(self, aci_radyan, z_zemin):
        rospy.loginfo(f"[KAZI] {math.degrees(aci_radyan):.0f}° Yönüne Dönülüyor...")
        
        # 1. ÖNCE YÜZÜNÜ TOPRAĞA DÖN (Kol yukarıda, kova açık)
        j_goal = self.move_group.get_current_joint_values()
        j_goal[0] = aci_radyan
        j_goal[1] = 0.0   
        j_goal[2] = -1.5  
        j_goal[3] = 0.0   
        self.move_group.go(j_goal, wait=True)

        self.guvenli_uyku(0.3)

        hedef_x = 1.0 * math.cos(aci_radyan)
        hedef_y = 1.0 * math.sin(aci_radyan)
        
        rospy.loginfo(f"[KAZI] Hedefe İniş Başlıyor... (Z: {z_zemin:.2f})")

        self.move_group.clear_path_constraints()
        self.move_group.set_position_target([hedef_x, hedef_y, z_zemin + 0.20])
        
        success, plan, _, _ = self.move_group.plan()
        if not success:
            rospy.logwarn("Kazı Hedefine Ulaşılamadı (IK Hatası)!")
            return False

        idx_kova = plan.joint_trajectory.joint_names.index('joint_4')
        for point in plan.joint_trajectory.points:
            pos_list = list(point.positions)
            pos_list[idx_kova] = 0.0  
            point.positions = tuple(pos_list)
            
            # Motorlar çıldırmasın diye Hız ve İvmeyi de sıfırlıyoruz!
            if len(point.velocities) > 0:
                vel_list = list(point.velocities)
                vel_list[idx_kova] = 0.0
                point.velocities = tuple(vel_list)
            if len(point.accelerations) > 0:
                acc_list = list(point.accelerations)
                acc_list[idx_kova] = 0.0
                point.accelerations = tuple(acc_list)

        # Hacklenmiş planı uygula
        self.move_group.execute(plan, wait=True)
        self.move_group.clear_pose_targets()

        # 3. KÖR KAZI (S-CURVE)
        rospy.loginfo("[KAZI] Dalış Kavisi (S-Curve) Devrede...")
        msg = JointTrajectory()
        msg.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4']
        bas = self.current_joints
        
        if z_zemin >= 0.18:
            d_boom, s_boom, s_arm, k_boom = 0.27, 0.01, 0.60, 0.25
        elif z_zemin <= -0.16:
            d_boom, s_boom, s_arm, k_boom = 0.35, 0.11, 0.85, 0.40
        else:
            d_boom, s_boom, s_arm, k_boom = 0.32, 0.20, 0.80, 0.35

        t = 0.0
        h1 = [bas[0], max(bas[1] - d_boom, -1.919), bas[2], 0.0]
        self.s_curve_nokta_ekle(msg, bas, h1, t, 2.5); t += 2.5
        h2 = [h1[0], min(h1[1] + s_boom, 0.0), max(h1[2] - s_arm, -2.268), -1.8]
        self.s_curve_nokta_ekle(msg, h1, h2, t, 3.5); t += 3.5
        h3 = [h2[0], min(h2[1] + k_boom, 0.0), min(h2[2] + 0.8, 0.0), -3.141]
        self.s_curve_nokta_ekle(msg, h2, h3, t, 2.0)

        self.direkt_surucu.publish(msg)
        return self.guvenli_uyku(9.0)

    def kamyona_dok(self):
        rospy.loginfo(f"[DÖKÜM] Kamyona Gidiliyor (X:{self.kamyon_x:.2f}, Y:{self.kamyon_y:.2f}, Z:{self.kamyon_z:.2f})...")
        
        self.move_group.clear_path_constraints()
        self.move_group.set_position_target([self.kamyon_x, self.kamyon_y, self.kamyon_z + 0.20])
        
        success, plan, _, _ = self.move_group.plan()
        if not success: 
            rospy.logwarn("Kamyon rotası çizilemedi!")
            return False

        idx_kova = plan.joint_trajectory.joint_names.index('joint_4')
        for point in plan.joint_trajectory.points:
            pos_list = list(point.positions)
            pos_list[idx_kova] = -3.141  
            point.positions = tuple(pos_list)

            if len(point.velocities) > 0:
                vel_list = list(point.velocities)
                vel_list[idx_kova] = 0.0
                point.velocities = tuple(vel_list)
            if len(point.accelerations) > 0:
                acc_list = list(point.accelerations)
                acc_list[idx_kova] = 0.0
                point.accelerations = tuple(acc_list)

        self.move_group.execute(plan, wait=True)
        self.move_group.clear_pose_targets()
        
        rospy.loginfo("[DÖKÜM] Orijinal Tek Kademeli S-Curve Boşaltma Başlıyor...")
        anlik = self.move_group.get_current_joint_values()
        bypass_msg = JointTrajectory()
        bypass_msg.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4']
        
        h1 = [anlik[0], min(anlik[1]+0.23, 0.0), max(anlik[2]-0.67, -2.268), 0.0]
        self.s_curve_nokta_ekle(bypass_msg, anlik, h1, 0.0, 4.0)
        
        self.direkt_surucu.publish(bypass_msg)
        return self.guvenli_uyku(5.0)

    def baslat_nihai_dongu(self):
        self.otonom_mesaide = True
        self.iptal_istendi = False 
        self.en_iyi_merkez_farki = 9999.0
        self.topoloji_haritasi.clear()

        rospy.loginfo("--- FAZ 1: KAMYON TESPİTİ VE KALİBRASYON ---")
        self.move_group.set_named_target("home_small")
        self.move_group.go(wait=True)
        if self.iptal_istendi or not self.guvenli_uyku(0.5): 
            self.otonom_mesaide = False; return

        try:
            rospy.wait_for_service('/clear_octomap', timeout=2.0)
            kor_et = rospy.ServiceProxy('/clear_octomap', Empty)
            kor_et()
            rospy.loginfo("Octomap temizlendi. Tarama başlatılıyor...")
        except Exception: pass

        self.tarama_modu_aktif = True
        for durak in [2.094, -2.094, 0.0]:
            if self.iptal_istendi: break
            acilar = self.move_group.get_current_joint_values()
            acilar[0] = durak
            self.move_group.go(acilar, wait=True) 
        self.tarama_modu_aktif = False

        acilar = self.move_group.get_current_joint_values()
        acilar[0] = self.bulunan_hedef_acisi
        self.move_group.go(acilar, wait=True)
        if self.iptal_istendi or not self.guvenli_uyku(1.0): return
        
        koordinat_bulundu = self.koordinat_cikar_ortalama()
        if not koordinat_bulundu:
            koordinat_bulundu = self.koordinat_cikar_zirve()
            
        if not koordinat_bulundu:
            rospy.logerr("KAMYON BULUNAMADI! Otonomi İptal.")
            self.otonom_mesaide = False; return
            
        rospy.loginfo(f"Kamyon Hafızaya Kazındı -> X: {self.kamyon_x:.2f}, Y: {self.kamyon_y:.2f}, Z: {self.kamyon_z:.2f}")

        rospy.loginfo("--- FAZ 2: ARAZİ TOPOLOJİSİ HARİTALANIYOR ---")
        bas_aci, bit_aci, adim = math.radians(-45), math.radians(45), math.radians(15)
        su_anki_aci = bas_aci
        
        while su_anki_aci <= bit_aci and not self.iptal_istendi:
            # Sadece kuleyi çeviriyoruz (Kollar hala home_small'da, güvende)
            j_goal = self.move_group.get_current_joint_values()
            j_goal[0] = su_anki_aci
            self.move_group.go(j_goal, wait=True)
            self.guvenli_uyku(0.3) # Kameranın okuması için minik es
            
            hedef_x = 1.0 * math.cos(su_anki_aci)
            hedef_y = 1.0 * math.sin(su_anki_aci)
            z_zemin = self.canli_z_yuksekligini_bul(hedef_x, hedef_y)
            
            self.topoloji_haritasi[su_anki_aci] = z_zemin
            rospy.loginfo(f"Dilim {math.degrees(su_anki_aci):.0f}° Hafızaya Alındı -> Z: {z_zemin:.2f}")
            
            su_anki_aci += adim

        rospy.loginfo("--- FAZ 3: KESİNTİSİZ KAZI VE DÖKÜM BAŞLIYOR ---")
        
        for aci_radyan, z_zemin in self.topoloji_haritasi.items():
            if self.iptal_istendi: break
            
            # 1. Bekleme yapmadan direkt hafızadaki bilgiyle uç ve kaz
            if not self.yaklas_ve_kaza(aci_radyan, z_zemin): break
            
            # 2. Direkt kamyona dön
            if not self.kamyona_dok(): break
            
            rospy.loginfo("Döküm tamam. Es vermeden sıradaki dilime uçuluyor...")

        if not self.iptal_istendi:
            rospy.loginfo("+++ TÜM RADYAL ALAN TEMİZLENDİ. OTONOMİ BİTTİ. +++")
        self.otonom_mesaide = False

    def run(self):
        rate = rospy.Rate(20) 
        dt = 1.0 / 20.0
        while not rospy.is_shutdown():
            if self.joy_data is not None:
                if self.joy_data.buttons[self.btn_auto] == 1 and not self.otonom_mesaide:
                    self.baslat_nihai_dongu()
                elif not self.otonom_mesaide and len(self.joy_data.buttons) > 5 and self.joy_data.buttons[self.btn_deadman] == 1:
                    v_k = self.apply_deadzone(self.joy_data.axes[self.axis_kule])
                    v_b = self.apply_deadzone(self.joy_data.axes[self.axis_bom])
                    v_a = self.apply_deadzone(self.joy_data.axes[self.axis_arm])
                    v_ko = self.apply_deadzone(self.joy_data.axes[self.axis_kova])
                    if v_k != 0 or v_b != 0 or v_a != 0 or v_ko != 0:
                        msg = JointTrajectory()
                        msg.joint_names = ['joint_1', 'joint_2', 'joint_3', 'joint_4']
                        point = JointTrajectoryPoint()
                        point.positions = [
                            self.current_joints[0] + (v_k * self.max_hiz * dt),
                            self.current_joints[1] + (v_b * self.max_hiz * dt),
                            self.current_joints[2] + (v_a * self.max_hiz * dt),
                            self.current_joints[3] + (v_ko * self.max_hiz * dt)
                        ]
                        point.time_from_start = rospy.Duration(dt) 
                        msg.points.append(point)
                        self.direkt_surucu.publish(msg)
            rate.sleep()

if __name__ == '__main__':
    try: op = NihaiHibritKomutan(); op.run()
    except rospy.ROSInterruptException: pass
