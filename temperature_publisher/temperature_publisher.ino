
#include "arduino_secrets.h"
#include <ArduinoMqttClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include <WiFiNINA.h>


// Sensor
#define DHTPIN 6     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
const int sensorId = 1;
const int interval = 2000;

// Wifi
char ssid[] = SECRET_SSID;   // your network SSID (name)
char pass[] = SECRET_PASS;   // your network passwxsord

// MQTT
const char broker[] = SECRET_MQTT_BROKER;
const int port = 1883;
const char topic[]  = "sensors/temperature";

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);
DHT dht(DHTPIN, DHTTYPE);


void setup() {

  Serial.begin(9600);

  // Connect to Wifi network:
  Serial.println("Connecting to network");
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    // failed, retry
    Serial.print(".");
    delay(5000);
  }

  Serial.println("Connected to network"); 
  Serial.println();

  // Connect to mqtt broker
  Serial.println("Connecting to MQTT broker");
  if (!mqttClient.connect(broker, port)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("Connected to the MQTT broker");
  Serial.println();

  // Initialize sensor
  Serial.println("Initializing DHT sensor");
  dht.begin();
  Serial.println("Initialized DHT sensor");

}


void loop() {

  mqttClient.poll();

  Serial.print("Reading temperature: ");
  float temperature = dht.readTemperature();
  Serial.println(temperature);

  // Send measurement via MQTT.
  Serial.println("Publishing MQTT message.");

  mqttClient.beginMessage(topic);
  serializeJson(getPayload(temperature), mqttClient);
  mqttClient.endMessage();

  Serial.println("Published MQTT message.");

  // Once a minute
  delay(interval);

}


DynamicJsonDocument getPayload(float temperature) {

  DynamicJsonDocument doc(128);
  JsonObject metadata = doc.createNestedObject("metadata");

  metadata["sensorId"] = sensorId;  
  doc["temperature"] = temperature;

  return doc;

}
