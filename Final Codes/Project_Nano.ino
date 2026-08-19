#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

/* SMART GLOVE TRANSMITTER (8-Value Version) */

Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x28);

const int PIN_THUMB   = A0;
const int PIN_INDEX   = A1;
const int PIN_MIDDLE  = A2;
const int PIN_RING    = A3; 
const int PIN_PINKY   = A6; 

void setup() {
  Serial.begin(9600);
  if(!bno.begin()) {
    while(1); // Error: IMU not found
  }
  bno.setExtCrystalUse(true);
}

void loop() {
  // Read Fingers
  int t = analogRead(PIN_THUMB);
  int i = analogRead(PIN_INDEX);
  int m = analogRead(PIN_MIDDLE);
  int r = analogRead(PIN_RING);
  int p = analogRead(PIN_PINKY);

  // Read Orientation
  sensors_event_t event;
  bno.getEvent(&event);
  
  // Send 8 values: T, I, M, R, P, Yaw(X), Roll(Y), Pitch(Z)
  Serial.print(t); Serial.print(",");
  Serial.print(i); Serial.print(",");
  Serial.print(m); Serial.print(",");
  Serial.print(r); Serial.print(",");
  Serial.print(p); Serial.print(",");
  Serial.print(event.orientation.x, 0); Serial.print(",");
  Serial.print(event.orientation.y, 0); Serial.print(",");
  Serial.println(event.orientation.z, 0); 
  
  delay(50); // Faster update (20 times/sec) for smoother UI
}