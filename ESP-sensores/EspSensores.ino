#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>

// =================== CONFIGURACIÓN ===================
// WiFi
const char* ssid = "escaleras";
const char* password = "grupo54321";

// MQTT
const char* mqtt_server = "192.168.0.100";
const int mqtt_port = 1883;
const char* mqtt_client_id = "ESP32_SensorNode";

// Tópico MQTT - Solo suscripción
const char* TOPICO_SISTEMA = "esp32/comando/sistema";

// Configuración Hardware
const int NUM_ESCALONES = 4;
const int NUM_BOTONES = 6;

// Pines de escalones
const int pinEmisorIR[NUM_ESCALONES] = {25, 26, 27, 14};
const int pinReceptorIR[NUM_ESCALONES] = {32, 33, 34, 35};
const char* colorEscalones[NUM_ESCALONES] = {"azul", "verde", "amarillo", "anaranjado"};

// Pines de botones
const int pinBotones[NUM_BOTONES] = {16, 22, 5, 18, 19, 23};
const char* colorBotones[NUM_BOTONES] = {"azul", "anaranjado", "verde", "rosa", "morado", "amarillo"};

// Configuración de temporización
const unsigned long DEBOUNCE_TIME = 200;
const unsigned long BLOCK_TIME = 1000;
const unsigned long IR_FREQUENCY_PERIOD = 26; // 38kHz
const int IR_THRESHOLD = 2000;

// =================== VARIABLES GLOBALES ===================
WiFiClient espClient;
PubSubClient client(espClient);

bool sistemaActivo = false;

struct SensorState {
  bool lastState;
  bool isBlocked;
  unsigned long lastTrigger;
};

SensorState escalones[NUM_ESCALONES];
SensorState botones[NUM_BOTONES];

unsigned long lastIRMicros = 0;
bool irState = false;

// =================== TIEMPO ECUADOR ===================
String getTiempoEcuador() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return String(millis()); // Fallback si no hay tiempo
  }
  
  char buffer[64];
  strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", &timeinfo);
  return String(buffer);
}

// =================== CONTROL IR ===================
void setupIREmitters() {
  for (int i = 0; i < NUM_ESCALONES; i++) {
    pinMode(pinEmisorIR[i], OUTPUT);
    digitalWrite(pinEmisorIR[i], LOW);
  }
}

void generateIRSignal() {
  unsigned long currentMicros = micros();
  if (currentMicros - lastIRMicros >= IR_FREQUENCY_PERIOD) {
    lastIRMicros = currentMicros;
    irState = !irState;
    
    for (int i = 0; i < NUM_ESCALONES; i++) {
      digitalWrite(pinEmisorIR[i], irState ? HIGH : LOW);
    }
  }
}

bool readIRSensor(int index) {
  int reading = analogRead(pinReceptorIR[index]);
  return (reading < IR_THRESHOLD);
}

bool readButton(int index) {
  return (digitalRead(pinBotones[index]) == LOW);
}

// =================== ENVÍO MQTT ===================
void enviarEscalon(int index) {
  if (!sistemaActivo) return;
  
  String topico = "escalera/sensores/escalon/" + String(colorEscalones[index]);
  String tiempo = getTiempoEcuador();
  
  StaticJsonDocument<200> doc;
  doc["sensor"] = colorEscalones[index];
  doc["tiempo"] = tiempo;
  
  char jsonBuffer[300];
  serializeJson(doc, jsonBuffer);
  
  client.publish(topico.c_str(), jsonBuffer);
  Serial.printf("Escalón %s activado a las %s\n", colorEscalones[index], tiempo.c_str());
}

void enviarBoton(int index) {
  if (!sistemaActivo) return;
  
  String topico = "pared/sensores/boton/" + String(colorBotones[index]);
  String tiempo = getTiempoEcuador();
  
  StaticJsonDocument<200> doc;
  doc["sensor"] = colorBotones[index];
  doc["tiempo"] = tiempo;
  
  char jsonBuffer[300];
  serializeJson(doc, jsonBuffer);
  
  client.publish(topico.c_str(), jsonBuffer);
  Serial.printf("Botón %s activado a las %s\n", colorBotones[index], tiempo.c_str());
}

// =================== CALLBACK MQTT ===================
void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  if (String(topic) == TOPICO_SISTEMA) {
    if (message == "1" || message.equalsIgnoreCase("true")) {
      sistemaActivo = true;
      Serial.println("Sistema ACTIVADO");
    }
    else if (message == "0" || message.equalsIgnoreCase("false")) {
      sistemaActivo = false;
      Serial.println("Sistema DESACTIVADO");
    }
  }
}

// =================== PROCESAMIENTO SENSORES ===================
void procesarEscalones() {
  if (!sistemaActivo) return;
  
  unsigned long currentTime = millis();
  
  for (int i = 0; i < NUM_ESCALONES; i++) {
    if (escalones[i].isBlocked && 
        (currentTime - escalones[i].lastTrigger > BLOCK_TIME)) {
      escalones[i].isBlocked = false;
    }
    
    bool currentState = readIRSensor(i);
    
    if (!escalones[i].lastState && currentState && !escalones[i].isBlocked) {
      if (currentTime - escalones[i].lastTrigger > DEBOUNCE_TIME) {
        escalones[i].lastTrigger = currentTime;
        escalones[i].isBlocked = true;
        enviarEscalon(i);
      }
    }
    
    escalones[i].lastState = currentState;
  }
}

void procesarBotones() {
  if (!sistemaActivo) return;
  
  unsigned long currentTime = millis();
  
  for (int i = 0; i < NUM_BOTONES; i++) {
    if (botones[i].isBlocked && 
        (currentTime - botones[i].lastTrigger > BLOCK_TIME)) {
      botones[i].isBlocked = false;
    }
    
    bool currentState = readButton(i);
    
    if (!botones[i].lastState && currentState && !botones[i].isBlocked) {
      if (currentTime - botones[i].lastTrigger > DEBOUNCE_TIME) {
        botones[i].lastTrigger = currentTime;
        botones[i].isBlocked = true;
        enviarBoton(i);
      }
    }
    
    botones[i].lastState = currentState;
  }
}

// =================== CONECTIVIDAD ===================
void setupWiFi() {
  WiFi.begin(ssid, password);
  Serial.print("Conectando WiFi");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.printf("\nWiFi conectado - IP: %s\n", WiFi.localIP().toString().c_str());
  
  // Configurar tiempo Ecuador (UTC-5)
  configTime(-5 * 3600, 0, "pool.ntp.org", "time.nist.gov");
}

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Conectando MQTT...");
    if (client.connect(mqtt_client_id)) {
      Serial.println("MQTT conectado");
      client.subscribe(TOPICO_SISTEMA);
    } else {
      Serial.printf("Error MQTT: %d\n", client.state());
      delay(5000);
    }
  }
}

// =================== SETUP ===================
void setup() {
  Serial.begin(115200);
  Serial.println("\n=== ESP32 StepClimb Sensor ===");
  
  setupWiFi();
  
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  setupIREmitters();
  
  // Inicializar escalones
  for (int i = 0; i < NUM_ESCALONES; i++) {
    escalones[i].lastState = readIRSensor(i);
    escalones[i].isBlocked = false;
    escalones[i].lastTrigger = 0;
  }
  
  // Inicializar botones
  for (int i = 0; i < NUM_BOTONES; i++) {
    pinMode(pinBotones[i], INPUT_PULLUP);
    botones[i].lastState = readButton(i);
    botones[i].isBlocked = false;
    botones[i].lastTrigger = 0;
  }
  
  reconnectMQTT();
  Serial.println("Sistema listo");
}

// =================== LOOP ===================
void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
  
  generateIRSignal();
  
  procesarEscalones();
  procesarBotones();
  
  delayMicroseconds(100);
}