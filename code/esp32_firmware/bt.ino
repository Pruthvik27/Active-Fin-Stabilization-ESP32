#include <Wire.h>
#include <BluetoothSerial.h>
#include <Adafruit_PWMServoDriver.h>

BluetoothSerial SerialBT;
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);

float angle_pitch = 0, angle_roll = 0;
float alpha = 0.98; 
unsigned long last_time = 0;
unsigned long last_bt_time = 0; // NEW: Timer for Bluetooth stability

void setup() {
  Serial.begin(115200);
  SerialBT.begin("rocket");
  
  Wire.begin(21, 22);
  Wire.setClock(400000); 
  
  Wire.beginTransmission(0x68);
  Wire.write(0x6B); Wire.write(0); 
  Wire.endTransmission(true);

  pwm.begin();
  pwm.setPWMFreq(50);
  last_time = micros();
}

void loop() {
  // 1. SENSOR DATA (Max CPU Speed)
  Wire.beginTransmission(0x68);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(0x68, 14, true);

  int16_t AcX = Wire.read()<<8|Wire.read();
  int16_t AcY = Wire.read()<<8|Wire.read();
  int16_t AcZ = Wire.read()<<8|Wire.read();
  Wire.read(); Wire.read(); 
  int16_t GyX = Wire.read()<<8|Wire.read();
  int16_t GyY = Wire.read()<<8|Wire.read();

  unsigned long current_time = micros();
  float dt = (float)(current_time - last_time) / 1000000.0;
  last_time = current_time;

  float acc_p = atan2(AcY, AcZ) * 180.0 / M_PI;
  float acc_r = atan2(AcX, AcZ) * 180.0 / M_PI;

  angle_pitch = alpha * (angle_pitch + (GyX / 131.0) * dt) + (1.0 - alpha) * acc_p;
  angle_roll  = alpha * (angle_roll + (GyY / 131.0) * dt) + (1.0 - alpha) * acc_r;

  // 2. SERVO CONTROL (High Frequency for Stability)
  pwm.setPWM(6, 0, map(90 + angle_pitch, 0, 180, 150, 600));
  pwm.setPWM(7, 0, map(90 - angle_pitch, 0, 180, 150, 600));
  pwm.setPWM(8, 0, map(90 - angle_roll, 0, 180, 150, 600));
  pwm.setPWM(9, 0, map(90 + angle_roll, 0, 180, 150, 600));

  // 3. TELEMETRY (Asynchronous - 50Hz)
  // This fixed the 3-second disconnect by preventing buffer overflow
  if (millis() - last_bt_time >= 20) { 
    SerialBT.print(angle_pitch, 1);
    SerialBT.print(",");
    SerialBT.println(angle_roll, 1);
    last_bt_time = millis();
  }
}