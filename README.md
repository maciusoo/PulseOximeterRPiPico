# Pulse Oximeter Project

A low-cost, reliable pulse oximeter designed using optoelectronic and photonic components. Built with the Raspberry Pi Pico H and powered by 3 AAA batteries, this device measures blood oxygen saturation (SpO₂) and heart rate (BPM) in real-time and displays the data on an OLED screen.

## Table of Contents

- [Project Overview](#project-overview)
- [Theoretical Background](#theoretical-background)
- [Assumptions](#assumptions)
- [Hardware Description](#hardware-description)
- [Software Overview](#software-overview)
- [Start-up and Calibration](#start-up-and-calibration)
- [Tests and Measurements](#tests-and-measurements)
- [User Manual](#user-manual)
- [Summary](#summary)
- [Appendix](#appendix)
- [Bibliography](#bibliography)

---

## Project Overview

This project is a student-built pulse oximeter that detects blood oxygen saturation and pulse rate using a phototransistor and alternating red/IR LEDs. It leverages a Raspberry Pi Pico H and an SSD1306 0.96" OLED display, enclosed in a custom-designed mechanical casing.

---

## Theoretical Background

Pulse oximetry relies on the differential absorption of red and infrared light by oxygenated and deoxygenated hemoglobin. This project uses a phototransistor to measure the light transmitted through a fingertip from alternating red (660nm) and IR (940nm) LEDs.

---

## Assumptions

### Functional
- Real-time SpO₂ and BPM monitoring.
- Battery-powered, portable, and user-friendly design.

### Design
- Red and IR LEDs, phototransistor for detection.
- Raspberry Pi Pico H for signal processing.
- 0.96" OLED screen for GUI.

---

## Hardware Description

- **Microcontroller:** Raspberry Pi Pico H
- **Sensors:** Red and IR LEDs, SFH 313 FA phototransistor
- **Display:** OLED SSD1306 (128x64)
- **Power:** 3 × AAA batteries (4.5V)
- **Enclosure:** Modified nail clip inside a custom box

### Electrical Schematic

- LEDs connected to GPIO via 100Ω resistors
- Phototransistor output read by ADC pin
- I2C used for OLED communication (GP4 and GP5)

---

## Software Overview

### Language
- **MicroPython**

### Key Features
- Real-time calculation of SpO₂ and BPM
- Dynamic thresholding for heartbeat detection
- Graphical display of signal trends

### Core Functions
- `calculate_spo2()`: Estimates SpO₂ from red/IR ratios.
- `calculate_bpm()`: Measures pulse rate from signal peaks.
- `normalize()`: Maps signal values for OLED plotting.
- `set_threshold()`: Adapts threshold based on signal range.

### GUI
- OLED shows:
  - SpO₂ (%)
  - BPM
  - Graphs for red and IR light
- Updates every 50 ms using `ssd1306` library

---

## Start-up and Calibration

Initial testing with a 9V battery caused overheating. The final design uses 3 × AAA batteries connected directly to the VSYS pin of the Pico. Components were later soldered for improved reliability.

---

## Tests and Measurements

### Hardware Tests
- Measured current/voltage to verify connections.
- Verified resistor values and LED functionality.

### Software Tests
- Validated LED toggling and signal acquisition.
- Chose optimal GUI layout after multiple iterations.

### Specifications

- **SpO₂ Accuracy:** ±2%
- **BPM Accuracy:** ±10 BPM
- **Sampling Rate:** ~20Hz

---

## User Manual

### What’s Included
- 1 × Pulse Oximeter Unit (pre-assembled)
- 3 × AAA batteries
- 1 × User manual
- 1 × USB Micro-B cable

### Using the Device
1. Insert finger into the clip.
2. Device powers on automatically.
3. OLED shows SpO₂, BPM, and signal graphs.
4. Remove finger to power off.

### Maintenance
- Replace batteries when display dims.
- Clean gently with a dry cloth.
- Store in a dry place.

### Troubleshooting

| Issue                | Solution                       |
|---------------------|--------------------------------|
| No display          | Replace batteries              |
| Inconsistent data   | Re-align finger properly       |
| Dim display         | Replace batteries              |
| No readings         | Minimize motion during use     |

---

## Summary

- **Goal:** Build a functional and portable pulse oximeter.
- **Achievements:** Accurate SpO₂ and BPM readings, simple user interface.
- **Challenges:** Overheating, signal noise, component alignment.
- **Future Plans:**
  - Noise filtering and digital signal processing
  - Wearable form factor
  - Improved power efficiency
  - Broader testing with diverse users

---

## Appendix

The full source code is available in the [`pulse_oximeter.py`](./pulse_oximeter.py) file. It includes:

- GPIO setup
- Light measurements
- Signal processing
- OLED display updates

---

## Bibliography

- [DIY Pulse Oximeter - Instructables](https://www.instructables.com/DIY-Pulse-Oximeter/)
- [Arduino Health Monitor - Instructables](https://www.instructables.com/Arduino-Based-Pulse-Oximeter-Health-Monitoring/)
- [Electronics For You - Pulse Oximeter](https://www.electronicsforu.com/electronics-projects/hardware-diy/pulse-oximeter-back-pack)

---

> Developed by Maciej Otwiaska & Bartosz Piotrowski  
> Optoelectronics Project, Group E22 – 2024  
> Laboratory of Optoelectronics and Photonics, Chair of Electronic and Photonic Metrology
