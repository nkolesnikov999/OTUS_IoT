#include "Arduino.h"
#include "EspMQTTClient.h" /* https://github.com/plapointe6/EspMQTTClient */
                           /* https://github.com/knolleary/pubsubclient */
#define PUB_DELAY (5 * 1000) /* 5 seconds */

EspMQTTClient client(
  "HOME",
  "Home4568",
  "192.168.1.94",
  "login",
  "password",
  "mqtt-esp"
);

void setup() {
  Serial.begin(9600);  
}

void onConnectionEstablished() {
  Serial.println("ESP connected!");
}

long last = 0;
void publishTopic() {
  long now = millis();
  if (client.isConnected() && (now - last > PUB_DELAY)) {
    client.publish("led/single", "It's me!");
    last = now;
  }
}

void loop() {
  client.loop();
  publishTopic();
}