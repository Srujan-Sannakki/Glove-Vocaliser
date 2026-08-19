import serial
import pyttsx3
import time

engine = pyttsx3.init()
engine.say("Gesture Voice system ready")
engine.runAndWait()

ser = serial.Serial('/dev/cu.usbmodem1201', 9600)  
time.sleep(2)

while True:
    try:
        data = ser.readline().decode().strip()
        
        if data.isdigit():
            flex = int(data)
            print("Flex:", flex)

            # Thresholds (adjust after your tests)
            if flex > 750:
                text = "Hello"
            elif flex > 600:
                text = "Yes"
            elif flex > 450:
                text = "No"
            else:
                text = ""

            if text != "":
                print("Speaking:", text)
                engine.say(text)
                engine.runAndWait()

    except KeyboardInterrupt:
        print("Stopped")
        break