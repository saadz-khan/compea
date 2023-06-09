#include <FirebaseESP8266.h>
#include <ESP8266WiFi.h>
#include <TimeLib.h>
#include <Wire.h>
#include "config.h"
#include <Wire.h>
#include <PolledTimeout.h>

#define SDA_PIN 4
#define SCL_PIN 5
const int16_t I2C_MASTER = 0x42;
const int16_t I2C_SLAVE = 0x08;
float current[4];

FirebaseData firebaseData1;


const int hysteresisThreshold = 100;
const int numRelays = 4;
const int relayPins[numRelays] = {D5, D6, D7, D8};
const String relayStatesPath[numRelays] = {"/S1", "/S2", "/S3", "/S4"};
const String energyProductionPath = "/Power";
const String voltagePath = "/Voltage";
const String loadEnergyConsumptionsPath[numRelays] = {"/LoadEnergy/S1", "/LoadEnergy/S2", "/LoadEnergy/S3", "/LoadEnergy/S4"};
const String manualOverridePath = "/ManualOverride";
const String recommendationsPath = "/Recommendations";
const String loadPriorityPath = "/LoadPriority";

const String zero = "0", one = "1";

unsigned long debounceDelay = 100;
unsigned long lastDebounceTime[numRelays] = {0, 0, 0, 0};
bool lastRelayState[numRelays] = {false, false, false, false};
bool relayState[numRelays] = {false, false, false, false};
int priority[numRelays];
float loadEnergyConsumptions[numRelays];
float energyProduction;
float energyConsumption;
float energyDifference;
float Voltage;
int ManualOverride = 0;
int R[5] = {0};

void setup() {
	for (int i = 0; i < numRelays; i++) {
		pinMode(relayPins[i], OUTPUT);
		digitalWrite(relayPins[i], LOW);
	}

	Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN, I2C_MASTER);  // join i2c bus (address optional for master)
	wificonnectivity();

	Firebase.begin(FIREBASE_HOST1, FIREBASE_AUTH1);
	Firebase.reconnectWiFi(true);
	delay(100);
}


void loop() {
	FirebaseReceive();
  if (ManualOverride == 0){
	dynamicLoadShedding();
  for (int i = 0; i < 5; i++) {
      R[i] = 0;
      Firebase.setInt(firebaseData1, "/Recommendations_flag/R"+ String(i+1), R[i]);
    }
  }
  else {
	generateRecommendations();
  }
  delay(100);
}


void wificonnectivity() {
	WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
	Serial.print("Connecting to ");
	Serial.print(WIFI_SSID);

	while (WiFi.status() != WL_CONNECTED) {
		Serial.print(".");
		delay(500);
	}
	Serial.print('\n');
	Serial.print("Connected to ");
	Serial.println(WIFI_SSID);
	Serial.print("IP Address is : ");
	Serial.println(WiFi.localIP());
}


bool isPeakHour() {
	int hour1 = hour(now());
	return (hour1 >= 18 && hour1 <= 22);
}

void readLoadPriorityValues(int priority[]) {
	for (int i = 0; i < numRelays; i++) {
		if (Firebase.getInt(firebaseData1, loadPriorityPath + "/relay" + String(i + 1))) {
			priority[i] = firebaseData1.intData();
		} 
		else {
			priority[i] = i + 1;
		}
	}
}

int readEnergyProduction() {
	if (Firebase.getInt(firebaseData1, energyProductionPath)) {
		return firebaseData1.intData();
	} 
	else {
		return 0;
	}
}

int readVoltage() {
	if (Firebase.getInt(firebaseData1, voltagePath)) {
		return firebaseData1.intData();
	} 
	else {
		return 0;
	}
}

void readLoadEnergyConsumptions(float loadEnergyConsumptions[]) {
  energyConsumption = 0;
  for (int i = 0; i < 4; i++){
    loadEnergyConsumptions[i] = Voltage * current[i];
    energyConsumption += loadEnergyConsumptions[i];
  }
  Serial.print("Eneryconsump:");
  Serial.println(energyConsumption);
}

void updateRelayState(int relayIndex, bool state) {
	digitalWrite(relayPins[relayIndex], state ? HIGH : LOW);
	Firebase.setString(firebaseData1, relayStatesPath[relayIndex], state ? one : zero);
}

void updateRecommendations(const String &recommendations) {
	Firebase.setString(firebaseData1, recommendationsPath, recommendations);
}

void dynamicLoadShedding() {
  Serial.println("Dynamic Algo Running");
    
        for (int i = 1; i <= numRelays-1; i++) {
            for (int j = 0; j < numRelays-1; j++) {
              if (energyDifference < -hysteresisThreshold && !relayState[j] && priority[j] == i) {
                  digitalWrite(relayPins[j], HIGH);
                  energyDifference += loadEnergyConsumptions[j];
                  updateRelayState(j, true);
                  if (energyDifference >= 0) {
                        break;
                  }                      
                          
              }
        }
    }
        for (int i = numRelays-1; i >= 1; i--) {
            for (int j = 0; j < numRelays-1; j++) {
              if (energyDifference > hysteresisThreshold && relayState[j] && priority[j] == i) {
                  digitalWrite(relayPins[j], LOW);
                  energyDifference -= loadEnergyConsumptions[j];
                  updateRelayState(j, false);
                  if (energyDifference <= 0) {
                        break;
                  }
                          
              }
        }
    }

    
   
}



void generateRecommendations() {
  Serial.println("Recommendation started");

	String recommendations = "";
  float energyDifferenceR = energyProduction - energyConsumption;

  if (energyDifferenceR < 0){
    recommendations += "Turn off Manual Override for better performance.";
    R[0] = 1;
			if (priority[3] == 4 && relayState[3]) {
					recommendations += "Load 4 is highest Pirority Task. Turn it on";
          R[4] = 1;
      }
      else {
          R[4] = 0;
      }
      if (priority[2] == 3 && relayState[2]) {
          recommendations += "Load 3 is a high Pirority Task. Turn it on is Recommended.";
          R[3] = 1;
      }
      else {
          R[3] = 0;
      }
      if (priority[1] < 3 && !relayState[1]){
          recommendations += "Load 2 are low pirority and should be turned off.";
          R[2] = 1;
      }
      else{
          R[2] = 0;
      }
      if (priority[0] < 3 && !relayState[0]){
          recommendations += "Load 1 are low pirority and should be turned off.";
          R[1] = 1;
      }
      else{
          R[1] = 0;
      }
      	updateRecommendations(recommendations);
		
	}
  else {
    R[0] = 0;
  }
  for (int j = 0; j < 5; j++) {
    Firebase.setInt(firebaseData1, "/Recommendations_flag/R"+ String(j+1), R[j]);
  }
  Serial.println(energyDifferenceR);

}


void FirebaseReceive() {

	for (int i = 0; i < numRelays; i++) {
		if (Firebase.getString(firebaseData1, relayStatesPath[i])) {
			String relayStateString = firebaseData1.stringData();
			bool newRelayState = (relayStateString == "1");
      Serial.print(newRelayState);
			if (newRelayState != lastRelayState[i] && (millis() - lastDebounceTime[i]) > debounceDelay) {
				lastDebounceTime[i] = millis();
				relayState[i] = newRelayState;
				digitalWrite(relayPins[i], relayState[i] ? HIGH : LOW);
				lastRelayState[i] = relayState[i];
      			}
    		}
  	}
      if (ManualOverride == 0){
        for (int i = 0; i < 5; i++) {
            R[i] = 0;
            Firebase.setInt(firebaseData1, "/Recommendations_flag/R"+ String(i+1), R[i]);
          }
        }
      Firebase.getString(firebaseData1, "/ManualOverride");
      ManualOverride = firebaseData1.stringData().toInt();
      LoadCurrentData();
      Voltage= readVoltage();
      Serial.print(Voltage);
      readLoadPriorityValues(priority);
      readLoadEnergyConsumptions(loadEnergyConsumptions);
      energyProduction = readEnergyProduction();
      energyDifference = energyProduction - energyConsumption;
      LoadCurrentData();

}

void LoadCurrentData() {
  using periodic = esp8266::polledTimeout::periodicMs;
  static periodic nextPing(1000);

  if (nextPing) {
    Wire.requestFrom(I2C_SLAVE, 6);  // request 6 bytes from slave device #8

    while (Wire.available()) {  // slave may send less than requested
      float temp1 = Wire.read();    
      float temp2 = Wire.read();
      float temp3 = Wire.read();    
      float temp4 = Wire.read();     
      if (temp1 < 50 && temp2 < 50 && temp3 < 50 && temp4 < 50){
        current[0] = temp1/10;
        current[1] = temp2/10;
        current[2] = temp3/10;
        current[3] = temp4/10;
      } 
      Serial.println("Currents are: ");
      Serial.println(current[0]); 
      Serial.println(current[1]);
      Serial.println(current[2]); 
      Serial.println(current[3]); 
      break;
    }
  }
}