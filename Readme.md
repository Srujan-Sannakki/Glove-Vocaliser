# Glove Vocaliser

A wearable glove-based system that converts hand gestures into speech using flex sensors, an Arduino, and Python.

This project was developed as an assistive technology project to explore how hand gestures can be detected electronically and converted into understandable speech output.

## About the Project

The Glove Vocaliser uses sensors attached to a glove to detect the movement and position of the fingers.

The sensor readings are processed by an Arduino and then passed to a Python program. Based on the detected gesture, the system produces a corresponding voice output.

The main idea is to provide a simple way of converting predefined hand gestures into spoken words.

## How It Works

The basic workflow of the system is:

```text
Hand Gesture
     ↓
Flex Sensors
     ↓
Arduino
     ↓
Sensor Data
     ↓
Python Program
     ↓
Gesture Recognition
     ↓
Speech Output
```

The flex sensors change their resistance as the fingers bend. The Arduino reads these values and sends the sensor data to the computer. The Python program processes the received data and generates the corresponding speech output.

## Features

- Glove-based gesture detection
- Finger movement detection using flex sensors
- Arduino-based sensor processing
- Python-based gesture processing
- Speech output for recognised gestures
- Serial communication between Arduino and computer
- Simple and low-cost approach to assistive technology

## Hardware

The project uses hardware such as:

- Arduino Nano Every
- Flex Sensors
- BNO055 IMU sensor
- Glove
- Jumper wires
- Supporting electronic components

The exact hardware configuration may vary depending on the version of the project.

## Software

The software side of the project includes:

- Arduino code
- Python
- Serial communication
- Python speech/voice processing

### Main Files

```text
glove_speech.py
vocalizer.py
```

The repository also contains the Arduino project files used for reading and processing the glove sensors.

## Project Structure

```text
Glove-Vocaliser/
│
├── Final Codes/
│   └── Final project code
│
├── project_Nano_Code/
│   └── Arduino code
│
├── glove_speech.py
├── vocalizer.py
│
├── Glove Vocaliser Project Report.pdf
├── Group34.pdf
│
└── README.md
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Srujan-Sannakki/Glove-Vocaliser.git
cd Glove-Vocaliser
```

### 2. Hardware Setup

Connect the flex sensors and other required components to the Arduino according to the circuit used in the project.

Make sure the glove sensors are properly connected before starting the program.

### 3. Upload the Arduino Code

Open the Arduino code from:

```text
project_Nano_Code/
```

Open it using the Arduino IDE, select the correct Arduino board and port, and upload the program.

### 4. Install Python Dependencies

Make sure Python is installed on your system.

Install the required packages used by the Python programs. Depending on the version of the code, this may include:

```bash
pip install pyserial
```

If additional Python libraries are imported by the selected program, install those libraries before running it.

### 5. Run the Python Program

After connecting the Arduino to the computer, run the appropriate Python file:

```bash
python glove_speech.py
```

or:

```bash
python vocalizer.py
```

Make sure the serial port used by the Python program matches the port assigned to your Arduino.

## Usage

1. Wear the glove.
2. Connect the Arduino to the computer.
3. Upload the Arduino program.
4. Start the Python program.
5. Perform one of the gestures supported by the program.
6. The system reads the sensor values and produces the corresponding speech output.

## Project Goals

The project was developed with the following goals:

- Explore gesture-based human-computer interaction.
- Build a low-cost wearable prototype.
- Understand sensor-based gesture detection.
- Combine embedded systems with Python.
- Explore assistive technology for communication.

## Current Limitations

This is a prototype system and has some limitations:

- The system currently works with a predefined set of gestures.
- Sensor readings may vary between users and glove positions.
- Calibration may be required for reliable gesture detection.
- The current prototype depends on a computer for Python processing and speech output.
- Recognition accuracy can be affected by sensor placement and hand movement.

## Future Improvements

Possible improvements include:

- Adding more gestures and vocabulary.
- Improving sensor calibration.
- Using machine learning for gesture classification.
- Making the system completely portable.
- Adding wireless communication.
- Improving real-time recognition.
- Adding a mobile application.
- Supporting multiple languages.
- Reducing the dependency on a computer for speech generation.

## Project Documentation

The repository contains the project reports and documentation used during development:

- `Glove Vocaliser Project Report.pdf`
- `Group34.pdf`

## Project Context

This project was developed as an academic/engineering project to explore the use of embedded systems and software for assistive technology.

## Author

**S Srujan**

GitHub:  
https://github.com/Srujan-Sannakki

---

If you find this project useful or interesting, feel free to explore the code and documentation.