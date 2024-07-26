#include <SPI.h>
#include <LoRa.h>
#include "ESP8266WiFi.h"
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"

#define ss D8
#define rst D0
#define dio0 D2
#define frequency 433E6

#define WLAN_SSID       "Kim Dung"
#define WLAN_PASS       "1234567890"

#define AIO_SERVER      "io.adafruit.com"
#define AIO_SERVERPORT  1883                   // use 8883 for SSL
#define AIO_USERNAME    "phanAn3123"
#define AIO_KEY         "aio_UZXY79JgqU0wMOlt2CR5OCkJdwox"

WiFiClient client;
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);
Adafruit_MQTT_Publish json_feed = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "/feeds/loragateway");


void MQTT_connect() {
  int8_t ret;
  if (mqtt.connected()) {
    return;
  }
  Serial.print("Connecting to MQTT... ");
  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) {
    Serial.println(mqtt.connectErrorString(ret));
    Serial.println("Retrying MQTT connection in 5 seconds...");
    mqtt.disconnect();
    delay(5000);
    retries--;
    if (retries == 0) {
      Serial.println("Failed to connect to MQTT after 3 attempts.");
      return;
    }
  }
  Serial.println("MQTT Connected!");
}

void onReceive(int packetSize) {
  if (packetSize == 0) return;

  // received a packet
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.print("Received packet '");

  String received = "";
  // read packet
  for (int i = 0; i < packetSize; i++) {
    received += (char)LoRa.read();
  }
  // Debug Data Receive 
  Serial.print(received);
  // Serial.print(" with RSSI ");
  // Serial.println(LoRa.packetRssi());
  if (!json_feed.publish(received.c_str())) {
    Serial.println("Failed to publish JSON to Adafruit IO");
  } else {
    Serial.println("Successfully published JSON to Adafruit IO");
  }
}

void Wifi_connect(){
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);
  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());
}


void Lora_connect(){
  Serial.println("LoRa Receiver Callback");
  LoRa.setPins(ss, rst, dio0);
  Serial.println("Init LoRa");
  if (!LoRa.begin(433E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
  Serial.println("Init Success");
}



void setup() {
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  Lora_connect();
  Wifi_connect();
  LoRa.onReceive(onReceive);
  LoRa.receive();
}

void loop() {
  digitalWrite(LED_BUILTIN, LOW);
  MQTT_connect();
}
