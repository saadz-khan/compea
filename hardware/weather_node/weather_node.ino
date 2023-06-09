#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "DHT.h"
#include <Wire.h>
#include <BH1750.h>
#include <RF24Network.h>
BH1750 lightMeter;

//const uint64_t pipeOut = 0xE8E8F0F0E1LL; 
#define DHTPIN 7
#define DHTTYPE DHT22 
DHT dht(DHTPIN, DHTTYPE);
RF24 radio(9,10); //  CN and CSN  pins of nrf
RF24Network network(radio);
const uint16_t this_node = 01; // Address of this node in Octal format
const uint16_t node00 = 00;
const uint16_t node03 = 03;

float data[6];
/*struct MyData {
  float h;
  float t;
  float irr;
};*/
//MyData data;
void setup()
{
  Serial.begin(9600); 
  dht.begin();
  Wire.begin();
  lightMeter.begin();
 // radio.begin();
  //radio.setAutoAck(false);
 // radio.setDataRate(RF24_250KBPS);
  //radio.openWritingPipe(pipeOut);
  SPI.begin();
radio.begin();
network.begin(90, this_node); //(channel, node address)
radio.setDataRate(RF24_250KBPS);
}
void loop()
{
  
  data[0] = dht.readHumidity();
  data[1] = dht.readTemperature();
   float lux = lightMeter.readLightLevel();
  data[2] = (lux*0.0079);
  if (isnan(data[0]) || isnan(data[1])){
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  Serial.print("Humidity: ");
  Serial.println(data[0]);
  Serial.print("Temperature: ");
  Serial.println(data[1]);
  Serial.print("SolarIrradiance: ");
  Serial.println(data[2]);
  TransData(node00);
  //TransData(node03);
  delay(2000);
}

void TransData(const uint16_t address){
  network.update();
  RF24NetworkHeader header7(address);
  bool ok = network.write(header7, &data, sizeof(data));
}