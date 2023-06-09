#include <Wire.h>

float current1 = 0;
float current2 = 0;
float current3 = 0;
float current4 = 0;

const int sensor1 = A0;      // pin where the OUT pin from sensor is connected on Arduino
const int sensor2 = A1; 
const int sensor3 = A3; 
const int sensor4 = A2; 
int mVperAmp = 185;           // this the 5A version of the ACS712 -use 100 for 20A Module and 66 for 30A Module
int Watt = 0;

void setup() {
  Serial.begin(9600); 
  Wire.begin(8);                // join I2C bus with address #8
  Wire.onRequest(requestEvent); // register event
}

void loop() {
  current1 = getVPP(sensor1);
  current2 = getVPP(sensor2);
  current3 = getVPP(sensor3);
  current4 = getVPP(sensor4);
  //Serial.println(current1);

  delay(300);
}

// function that executes whenever data is requested by master
// this function is registered as an event, see setup()
void requestEvent() {
  Wire.write((byte)current1);
  Wire.write((byte)current2); 
  Wire.write((byte)current3);
  Wire.write((byte)current4); 
  Serial.println(current1);
  // as expected by master
}

float getVPP(const int sensorIn)
{
  float result;
  int readValue;                // value read from the sensor
  int maxValue = 0;             // store max value here
  int minValue = 1024;          // store min value here
  float VRMS = 0;
  float Voltage = 0;
  float temp = 0;
   uint32_t start_time = millis();
   while((millis()-start_time) < 1000) //sample for 1 Sec
   {
       readValue = analogRead(sensorIn);
       // see if you have a new maxValue
       if (readValue > maxValue) 
       {
           /*record the maximum sensor value*/
           maxValue = readValue;
       }
       if (readValue < minValue) 
       {
           /*record the minimum sensor value*/
           minValue = readValue;
       }
   }
   
   // Subtract min from max
   Voltage = ((maxValue - minValue) * 5.0)/1024.0;
   VRMS = (Voltage/2.0) *0.707;   //root 2 is 0.707
   temp = (VRMS * 1000)/mVperAmp;
   if (temp <= 0.09){
     result = 0;
   }
   else if (temp > 5){
     result = 0;
   }
   else {
     result = temp;
   }
      
   return result;
 }
