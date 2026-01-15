# 🚀 Active Fin Stabilization System using ESP32

An embedded systems and control engineering project demonstrating real-time **active fin stabilization** using sensor feedback and closed-loop PID control.

---

## 📌 Project Overview
Rocket flight stability is critical for accurate and safe trajectories. Traditional passive fins cannot respond dynamically to disturbances such as wind gusts and thrust misalignment.

This project implements an **Active Fin Stabilization System** that continuously senses the rocket’s orientation and actively corrects deviations in real time using servo-driven fins.

---

## 🔧 System Architecture
- **Microcontroller:** ESP32  
- **IMU Sensor:** MPU-6050 (3-axis accelerometer + gyroscope)  
- **Sensor Fusion:** Complementary Filter  
- **Control Algorithm:** PID Controller  
- **Actuators:** 4 × Servo motors (active fins)  
- **Telemetry:** Bluetooth-based ground station GUI (Python)

---

## 🧠 Working Principle
1. MPU-6050 measures roll and pitch angles in real time  
2. Accelerometer and gyroscope data are fused using a complementary filter  
3. PID controller computes corrective control signals  
4. Servo motors adjust fin angles dynamically  
5. Telemetry data is transmitted to a PC for monitoring

---

## 📊 Results
- Real-time correction of roll and pitch deviations  
- Smooth and stable fin actuation  
- Improved stability compared to passive fin systems  
- Reliable closed-loop control performance

---

## 📂 Repository Structure


---

## 🔮 Future Enhancements
- Thrust Vector Control (TVC) integration  
- Dual active-fin stabilization system  
- Multi-directional control for improved maneuverability  
- RF-based long-range communication  
- Dual-mode operation (air and water)  
- 3D-printed structural components  
- Infrared-based heat-seeking guidance (research-oriented)

---

## 👥 Team Members
- Pruthvik S  
- Pratik Jadhav  
- Narendrababu N Bisleri  
- Siddanth Bhatt  

---

## 🙏 Acknowledgements
Guided by **Chaitanya L**, Assistant Professor  
Department of Electrical and Electronics Engineering

---

## 📄 License
This project is intended for academic and educational purposes only.


