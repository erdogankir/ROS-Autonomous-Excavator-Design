#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <ps5Controller.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

bool wasConnected = false;

void setup() {
  Serial.begin(115200);
  
  Wire.begin(21, 22); 
  pwm.begin();
  pwm.setPWMFreq(1000); 
  
  // Kullanılan tüm H-Bridge kanallarını güvenlik amacıyla sıfırla
  for(int i = 0; i <= 11; i++) {
    pwm.setPWM(i, 0, 0);
  }

  // DualSense MAC adresini buraya gir (kendi adresinle değiştirmeyi unutma)
  ps5.begin("E8:47:3A:51:B5:67"); 
  Serial.println("Ekskavator ESP32 Baslatildi. DualSense bekleniyor...");
}

void loop() {
  if (ps5.isConnected()) {
    
    if (!wasConnected) {
      Serial.println("\n--- DUALSENSE BAGLANDI! EKSKAVATOR AKTIF ---");
      wasConnected = true;
    }

    // =========================================================
    // 1. KULE DÖNÜŞÜ (PWM 0-1) | Sol Analog X Ekseni
    // Min: 300, Max: 3000
    // =========================================================
    int lX = ps5.LStickX();
    if (lX <= -15) { // Sol Analog Sola
      int duty = map(lX, -15, -128, 300, 3000);
      pwm.setPWM(0, 0, duty);
      pwm.setPWM(1, 0, 0);
    } 
    else if (lX >= 15) { // Sol Analog Sağa
      int duty = map(lX, 15, 127, 300, 3000);
      pwm.setPWM(0, 0, 0);
      pwm.setPWM(1, 0, duty);
    } 
    else { // Ölü bölge (Dur)
      pwm.setPWM(0, 0, 0);
      pwm.setPWM(1, 0, 0);
    }

    // =========================================================
    // 2. ARM (PWM 4-5) | Sol Analog Y Ekseni
    // Min: 1400, Max: 4095
    // =========================================================
    int lY = ps5.LStickY();
    if (lY <= -15) { // Sol Analog Aşağı
      int duty = map(lY, -15, -128, 1400, 4095);
      pwm.setPWM(4, 0, duty);
      pwm.setPWM(5, 0, 0);
    } 
    else if (lY >= 15) { // Sol Analog Yukarı
      int duty = map(lY, 15, 127, 1400, 4095);
      pwm.setPWM(4, 0, 0);
      pwm.setPWM(5, 0, duty);
    } 
    else {
      pwm.setPWM(4, 0, 0);
      pwm.setPWM(5, 0, 0);
    }

    // =========================================================
    // 3. BUCKET (PWM 6-7) | Sağ Analog Y Ekseni
    // Min: 2000, Max: 4095
    // =========================================================
    int rY = ps5.RStickY();
    if (rY <= -15) { // Sağ Analog Aşağı
      int duty = map(rY, -15, -128, 2000, 4095);
      pwm.setPWM(6, 0, duty);
      pwm.setPWM(7, 0, 0);
    } 
    else if (rY >= 15) { // Sağ Analog Yukarı
      int duty = map(rY, 15, 127, 2000, 4095);
      pwm.setPWM(6, 0, 0);
      pwm.setPWM(7, 0, duty);
    } 
    else {
      pwm.setPWM(6, 0, 0);
      pwm.setPWM(7, 0, 0);
    }

    // =========================================================
    // 4. SAĞ PALET (PWM 8-9) | R2 (İleri) ve R1 (Geri)
    // Min: 500, Max: 4095
    // =========================================================
    int r2Val = ps5.R2Value(); // 0 ile 255 arası değer döner
    bool r1Pressed = ps5.R1(); // Buton olduğu için True/False döner
    
    // Hem R1 hem R2'ye yanlışlıkla aynı anda basılırsa motoru korumak için öncelik atadık
    if (r2Val > 5) { // R2'ye basıldıysa (Analog İleri)
      int duty = map(r2Val, 5, 255, 500, 4095);
      pwm.setPWM(8, 0, duty);
      pwm.setPWM(9, 0, 0);
    } 
    else if (r1Pressed) { // R1'e basıldıysa (Dijital Geri)
      pwm.setPWM(8, 0, 0);
      pwm.setPWM(9, 0, 4095); // Geri giderken sabit maksimum güç
    } 
    else {
      pwm.setPWM(8, 0, 0);
      pwm.setPWM(9, 0, 0);
    }

    // =========================================================
    // 5. SOL PALET (PWM 10-11) | L2 (İleri) ve L1 (Geri)
    // Min: 500, Max: 4095
    // =========================================================
    int l2Val = ps5.L2Value(); 
    bool l1Pressed = ps5.L1(); 
    
    if (l2Val > 5) { // L2'ye basıldıysa (Analog İleri)
      int duty = map(l2Val, 5, 255, 500, 4095);
      pwm.setPWM(10, 0, duty);
      pwm.setPWM(11, 0, 0);
    } 
    else if (l1Pressed) { // L1'e basıldıysa (Dijital Geri)
      pwm.setPWM(10, 0, 0);
      pwm.setPWM(11, 0, 4095); // Geri giderken sabit maksimum güç
    } 
    else {
      pwm.setPWM(10, 0, 0);
      pwm.setPWM(11, 0, 0);
    }
    
  } 
  else {
    // Bağlantı koparsa tüm motorları acil durdur
    if (wasConnected) {
      Serial.println("\n!!! DUALSENSE BAGLANTISI KOPTU - MOTORLAR DURDURULUYOR !!!");
      wasConnected = false;
      for(int i = 0; i <= 11; i++) {
        pwm.setPWM(i, 0, 0);
      }
    }
  }
  
  delay(15); // I2C hattını ve ESP'yi rahatlatmak için küçük gecikme
}