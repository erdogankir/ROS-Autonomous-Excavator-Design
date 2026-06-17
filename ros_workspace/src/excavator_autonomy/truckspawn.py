#!/usr/bin/env python3

import rospy
from gazebo_msgs.srv import SpawnModel
from geometry_msgs.msg import Pose

def urdf_olustur(kasa_renk, robot_adi):

    return f"""<?xml version="1.0" encoding="utf-8"?>
<robot name="{robot_adi}">
  <link name="kamyon_sasi">
    <inertial>
      <origin xyz="-0.03713 0.061767 1.0529E-15" rpy="0 0 0" />
      <mass value="54.71" />
      <inertia ixx="0.46006" ixy="-0.080279" ixz="5.93E-15" iyy="2.4002" iyz="3.1818E-15" izz="2.1019" />
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_sasi.STL" /> </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_sasi.STL" /> </geometry>
      <surface>
        <friction><ode><mu>1.0</mu><mu2>1.0</mu2></ode></friction>
      </surface>
    </collision>
  </link>

  <link name="kamyon_kasa">
    <inertial>
      <origin xyz="-0.002355 -8.2293E-16 0.09596" rpy="0 0 0" />
      <mass value="10.506" />
      <inertia ixx="0.17224" ixy="4.7533E-16" ixz="-0.013304" iyy="0.33738" iyz="2.934E-17" izz="0.39088" />
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_kasa.STL" /> </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_kasa.STL" /> </geometry>
    </collision>
  </link>
  <joint name="joint_kasa" type="fixed">
    <origin xyz="-0.12718 0 0.08" rpy="0 0 0" />
    <parent link="kamyon_sasi" />
    <child link="kamyon_kasa" />
  </joint>

  <link name="kamyon_kupa">
    <inertial>
      <origin xyz="-0.011543 -9.2883E-16 0.070709" rpy="0 0 0" />
      <mass value="6.9933" />
      <inertia ixx="0.092084" ixy="-5.5632E-17" ixz="0.02008" iyy="0.077981" iyz="4.824E-17" izz="0.0953" />
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_kupa.STL" /> </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_kupa.STL" /> </geometry>
    </collision>
  </link>
  <joint name="joint_kupa" type="fixed">
    <origin xyz="0.35405 0 0" rpy="0 0 0" />
    <parent link="kamyon_kasa" />
    <child link="kamyon_kupa" />
  </joint>

  <link name="kamyon_cam">
    <inertial>
      <origin xyz="0.012687 -1.8762E-15 0.050267" rpy="0 0 0" />
      <mass value="1.8507" />
      <inertia ixx="0.02373" ixy="1.1604E-19" ixz="0.0010759" iyy="0.0084887" iyz="1.1195E-17" izz="0.024871" />
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_cam.STL" /> </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry> <mesh filename="package://kamyon/meshes/kamyon_cam.STL" /> </geometry>
    </collision>
  </link>
  <joint name="joint_cam" type="fixed">
    <origin xyz="0.019053 0 0.098354" rpy="0 0 0" />
    <parent link="kamyon_kupa" />
    <child link="kamyon_cam" />
  </joint>

  <gazebo> <static>false</static> </gazebo>
  
  <gazebo reference="kamyon_sasi">
    <visual>
      <material>
        <ambient>0.23 0.23 0.23 1</ambient>
        <diffuse>0.23 0.23 0.23 1</diffuse>
        <specular>0.1 0.1 0.1 1</specular>
      </material>
    </visual>
  </gazebo>
  
  <gazebo reference="kamyon_kasa">
    <visual>
      <material>
        <ambient>{kasa_renk}</ambient>
        <diffuse>{kasa_renk}</diffuse>
        <specular>0.1 0.1 0.1 1</specular>
      </material>
    </visual>
  </gazebo>
  
  <gazebo reference="kamyon_kupa">
    <visual>
      <material>
        <ambient>0.8 0.8 0.8 1</ambient>
        <diffuse>0.8 0.8 0.8 1</diffuse>
        <specular>0.1 0.1 0.1 1</specular>
      </material>
    </visual>
  </gazebo>
  
  <gazebo reference="kamyon_cam">
    <visual>
      <material>
        <ambient>0.15 0.15 0.15 1</ambient>
        <diffuse>0.15 0.15 0.15 1</diffuse>
        <specular>0.1 0.1 0.1 1</specular>
      </material>
    </visual>
  </gazebo>

</robot>
"""

def kamyon_spawn_et():
    rospy.init_node("santiye_kurucu_node")

    rospy.loginfo("Gazebo fırlatma servisi bekleniyor...")
    rospy.wait_for_service("/gazebo/spawn_urdf_model")
    spawn_model = rospy.ServiceProxy("/gazebo/spawn_urdf_model", SpawnModel)
    rospy.loginfo("Servis bulundu! Kamyonlar fırlatılıyor...")

    # ==========================================
    # SARI KASALI KAMYON
    # ==========================================
    pose_sari = Pose()
    pose_sari.position.x = 4.3  
    pose_sari.position.y = -0.4  
    pose_sari.position.z = 0.0  

    urdf_sari = urdf_olustur("0.98 0.78 0.07 1", "sari_kamyon")

    spawn_model(
        "sari_kamyon", 
        urdf_sari,
        "",
        pose_sari,
        "world"
    )
    rospy.loginfo("Sarı kasalı kamyon sahaya indi!")

    # ==========================================
    # MAVİ KASALI KAMYON
    # ==========================================
    pose_mavi = Pose()
    pose_mavi.position.x = 4.3   
    pose_mavi.position.y = -0.7  
    pose_mavi.position.z = 0.0   

    urdf_mavi = urdf_olustur("0.24 0.55 0.89 1", "mavi_kamyon")

    spawn_model(
        "mavi_kamyon", 
        urdf_mavi,
        "",
        pose_mavi,
        "world"
    )
    rospy.loginfo("Mavi kasalı kamyon sahaya indi!")
    
    # ==========================================
    # YESIL KASALI KAMYON
    # ==========================================
    pose_mavi = Pose()
    pose_mavi.position.x = 4.3   
    pose_mavi.position.y = -1  
    pose_mavi.position.z = 0.0   

    urdf_mavi = urdf_olustur("0.43 0.93 0.26 1", "yesil_kamyon")

    spawn_model(
        "yesil_kamyon", 
        urdf_mavi,
        "",
        pose_mavi,
        "world"
    )
    rospy.loginfo("Yesil kasalı kamyon sahaya indi!")

if __name__ == "__main__":
    kamyon_spawn_et()
