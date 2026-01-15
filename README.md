# Active-Fin-Stabilization-ESP32
Active fin stabilization system using ESP32, MPU6050, PID control, and servo-actuated fins.

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

