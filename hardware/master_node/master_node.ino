#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include <Wire.h>
#include <NTPClient.h>
#include <WiFiUdp.h>
#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <RF24Network.h>

#define FIREBASE_HOST "homeautomation-6f713-default-rtdb.firebaseio.com" // Your Firebase Project URL goes here without "http:" , "\" and "/"
#define FIREBASE_AUTH "Aah1FYW7z8B4Xt3tLRf96SW9ZgEmoWTtw3QiIXz0"    // Your Firebase Database Secret goes here
#define WIFI_SSID "mansoor&gang"                                             // your WiFi SSID for which your NodeMCU connects
#define WIFI_PASSWORD "seecs1609"

// Declare the Firebase Data object in the global scope
FirebaseData firebaseData;

RF24 radio(2,4);
RF24Network network(radio); // Include the radio in the network
const uint16_t this_node = 00;
float data[6];
float data1[3];
float data2[3];


// Database main path (to be updated in setup with the user UID)
String databasePath;

// Define NTP Client to get time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

// Variable to save current epoch time
int timestamp;

void setup()
{

  Serial.begin(115200);
  Wire.begin();
  wificonnectivity();
  timeClient.begin();
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH); // connect to firebase
  Firebase.reconnectWiFi(true);
  SPI.begin();
  radio.begin();
  network.begin(90, this_node); //(channel, node address)
  radio.setDataRate(RF24_250KBPS);
  delay(1000);
}

void loop()
{
  recvData();
  timestamp = getTime();
  databasePath = "/DataGeneration/" + String(timestamp);
  FirebaseSend();
  delay(1000);
}
void wificonnectivity()
{
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD); //try to connect with wifi
  Serial.print("Connecting to ");
  Serial.print(WIFI_SSID);

    while (WiFi.status() != WL_CONNECTED)
    {
      Serial.print(".");
      delay(500);
    }
  Serial.print('\n');
  Serial.print("Connected to ");
  Serial.println(WIFI_SSID);
  Serial.print("IP Address is : ");
  Serial.println(WiFi.localIP()); //print local IP address
}
unsigned long getTime() {
  timeClient.update();
  unsigned long now = timeClient.getEpochTime();
  return now;
}

void FirebaseSend()
{

  // Write values to Firebase
  Firebase.setString(firebaseData, databasePath + "/Humidity", data1[0]);
  Firebase.setString(firebaseData, databasePath + "/Temperature", data1[1]);
  Firebase.setString(firebaseData, databasePath + "/SolarIntensity", data1[2]);
  Firebase.setString(firebaseData, databasePath + "/Voltage", data2[0]);
  Firebase.setString(firebaseData, databasePath + "/Current", data2[1]);
  Firebase.setString(firebaseData, databasePath + "/Power", data2[2]);
  Firebase.setString(firebaseData, databasePath + "/TimeStamp", String(timestamp));
  Firebase.setString(firebaseData, "/Power", data2[2]);
  Firebase.setString(firebaseData, "/Voltage", data2[0]);

  Serial.println("Writing Value");
}

void recvData()
{

    network.update();
    while ( network.available() ) { // Is there any incoming data?
      RF24NetworkHeader header;
    
      network.read(header, &data, sizeof(data)); // Read the incoming data
    
      if (header.from_node == 1) { // If data comes from Node 01
      data1[0] = data[0];
      data1[1] = data[1];
      data1[2] = data[2];
      }
      
      if (header.from_node == 2) { // If data comes from Node 02
      data2[0] = data[3];
      data2[1] = data[4];
      data2[2] = data[5]; 
      }

    
    }

}