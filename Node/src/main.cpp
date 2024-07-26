#include "ESP8266_SHT3X.h"
#include <iostream>
#include <cstring>
#include <LoRa.h>

#define ss D8
#define rst D0
#define dio0 D4
#define frequency 433E6

unsigned long previousMillis = 0; 
const long interval = 10000; 

SHT3X sht30(0x44);


String formatSensorData(const char* id, int temp, int hum, int soil) {
  String json = "{";
  json += "\"id\": \"" + String(id) + "\", ";
  json += "\"temp\": " + String(temp) + ", ";
  json += "\"hum\": " + String(hum) + ", ";
  json += "\"soil\": " + String(soil);
  json += "}";
  return json;
}

void setup() {
  Serial.begin(9600);
  LoRa.setPins(ss, rst, dio0);
  if (!LoRa.begin(frequency)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
}

void loop() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    int temp = 0;
    int hum = 0;
    int value = 0;

    // Read temperature and humidity
    if (sht30.get() == 0) {
      temp = sht30.cTemp;
      hum = sht30.humidity;
    } else {
      Serial.println("Failed to read from SHT3X sensor!");
    }

    // Read soil moisture
    for (int i = 0; i <= 9; i++) {
      value += analogRead(A0);
    }
    int soil = map(value, 5800, 2600, 0, 100);
    if (soil > 100 || soil < 0){
      Serial.println("Failed to read from Soil mosture sensor!");
    }
    // Format data to JSON
    String jsonData = formatSensorData("Node_1", temp, hum, soil);
    Serial.print(jsonData);
    
    // Send data via LoRa
    if (LoRa.beginPacket() == 1) {
      LoRa.print(jsonData);
      if (LoRa.endPacket() == 1) {
        Serial.println(" Packet sent successfully");
      } else {
        Serial.println(" Failed to send packet");
      }
    } else {
      Serial.println(" Failed to start packet");
    }
  }
}


