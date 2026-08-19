# vocalizer.py
# Flow A: Arduino → Serial → Mac TTS

import serial
import pyttsx3
import time

SERIAL_PORT = "/dev/cu.usbmodem1301"   # Your Mac port
BAUD = 115200

VALID = {"HELP", "YES", "NO", "THANK YOU", "HELLO"}

engine = pyttsx3.init()

try:
    ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)
    print("Connected to", SERIAL_PORT)
except Exception as e:
    print("Error opening port:", e)
    exit()

time.sleep(2)

print("Listening...")

while True:
    try:
        line = ser.readline().decode("utf-8", errors="ignore").strip()
        if not line:
            continue

        print("Serial:", line)

        if line.startswith("Recognized:"):
            phrase = line.split(":", 1)[1].strip()
            up = phrase.upper()

            if up in VALID:
                print("Speaking:", phrase)
                engine.say(phrase)
                engine.runAndWait()

    except KeyboardInterrupt:
        print("\nExit.")
        break