#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <HardwareSerial.h>
#include <TinyGPSPlus.h>
#include <LiquidCrystal_I2C.h>
#include <time.h>

const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";

const char* SERVER_URL =
    "https://6ryjqz-5000.csb.app/api/data";

const char DEVICE_NAME[] = "ESPFormaldehydeMap";

#define GPS_RX 27
#define GPS_TX 26
HardwareSerial gpsSerial(1);

#define HCHO_RX 16
#define HCHO_TX 17
HardwareSerial sensorSerial(2);

TinyGPSPlus gps;

LiquidCrystal_I2C lcd(0x27, 16, 2);

float hchoMGm3 = 0.0;
float gpsLat = 0.0;
float gpsLng = 0.0;
bool gpsFixed = false;
uint8_t sensorBuffer[9];

unsigned long lastSendTime = 0;
const unsigned long SEND_INTERVAL = 60000;

uint8_t checkSum(uint8_t *packet) {
  uint8_t sum = 0;
  for (uint8_t i = 1; i < 8; i++) {
    sum += packet[i];
  }
  sum = (~sum) + 1;
  return sum;
}

void setSensorActiveMode() {
  uint8_t cmd[] = {0xFF, 0x01, 0x78, 0x40, 0x00, 0x00, 0x00, 0x00, 0x47};
  sensorSerial.write(cmd, 9);
  delay(100);
  while (sensorSerial.available()) {
    sensorSerial.read();
  }
}

void syncTimeKyiv() {
  configTime(3 * 3600, 0, "pool.ntp.org", "time.google.com", "time.nist.gov");

  struct tm timeinfo;
  int attempts = 0;
  while (!getLocalTime(&timeinfo) && attempts < 20) {
    Serial.print(".");
    delay(500);
    attempts++;
  }

  if (getLocalTime(&timeinfo)) {
    Serial.println("\nTime synchronized!");
    char buf[64];
    strftime(buf, sizeof(buf), "%d.%m.%Y %H:%M:%S", &timeinfo);
    Serial.println(buf);
  } else {
    Serial.println("\nFailed to get time from NTP");
  }
}

bool connectWiFi() {
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Connecting WiFi");

  WiFi.begin(ssid, pass);
  unsigned long startTime = millis();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    if (millis() - startTime > 20000UL) {
      Serial.println("\nWiFi timeout");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("WiFi timeout");
      delay(1500);
      return false;
    }
  }

  syncTimeKyiv();
  IPAddress ip = WiFi.localIP();
  Serial.print("ESP32 IP: ");
  Serial.println(ip);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("WiFi OK");
  lcd.setCursor(0, 1);
  lcd.print(ip);
  delay(2000);
  return true;
}

void displayHCHO() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print(hchoMGm3, 3);
  lcd.print(" mg/m3");
  lcd.setCursor(0, 1);
  lcd.print("WiFi OK");
}

String getKyivTimeString() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    return "no_time";
  }

  char buf[25];
  strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", &timeinfo);
  return String(buf);
}

bool sendMeasurement() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi disconnected.");
    return false;
  }

  String kyivTime = getKyivTimeString();

  char json[320];
  snprintf(json, sizeof(json),
           "{\"name\":\"%s\","
           "\"lat\":%.6f,"
           "\"lon\":%.6f,"
           "\"formaldehyde_mg_m3\":%.3f,"
           "\"time\":\"%s\"}",
           DEVICE_NAME,
           gpsLat, gpsLng,
           hchoMGm3,
           kyivTime.c_str());

  WiFiClientSecure client;
  client.setInsecure();

  HTTPClient https;

  Serial.println(SERVER_URL);
  Serial.println(json);

  if (!https.begin(client, SERVER_URL)) {
    return false;
  }

  https.addHeader("Content-Type", "application/json");

  int httpCode = https.POST((uint8_t*)json, strlen(json));

  if (httpCode > 0) {
    Serial.println(httpCode);
    String response = https.getString();
    Serial.println(response);
  } else {
    Serial.println(https.errorToString(httpCode));
  }

  https.end();
  return httpCode == 201;
}

bool readHCHO(float &mgm3_out) {
  while (sensorSerial.available() >= 9) {
    if (sensorSerial.peek() != 0xFF) {
      sensorSerial.read();
      continue;
    }

    sensorSerial.readBytes(sensorBuffer, 9);

    if (sensorBuffer[0] == 0xFF && sensorBuffer[1] == 0x17) {
      if (checkSum(sensorBuffer) == sensorBuffer[8]) {
        uint16_t ppb = (uint16_t)sensorBuffer[4] * 256 + sensorBuffer[5];
        float ppm = ppb / 1000.0;
        mgm3_out = ppm * 1.25; // коефіцієнт для переводу ppm у mg/m3
        return true;
      }
    }
  }
  return false;
}

void requestHCHO() {
  uint8_t cmd[] = {0xFF, 0x01, 0x86, 0x00, 0x00, 0x00, 0x00, 0x00, 0x79};
  sensorSerial.write(cmd, 9);
}

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Starting...");
  delay(1000);
  gpsSerial.begin(9600, SERIAL_8N1, GPS_RX, GPS_TX);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("GPS starting");
  Serial.println("Starting GPS...");

  unsigned long gpsStart = millis();
  while (!gpsFixed) {
    while (gpsSerial.available()) {
      gps.encode(gpsSerial.read());
    }
    if (gps.location.isValid() && gps.location.isUpdated()) {
      gpsLat = gps.location.lat();
      gpsLng = gps.location.lng();
      gpsFixed = true;
      
      Serial.println("\nGPS FIX!");
      Serial.print("Latitude: ");  Serial.println(gpsLat, 6);
      Serial.print("Longitude: "); Serial.println(gpsLng, 6);
      
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("GPS FIX OK");
      lcd.setCursor(0, 1);
      lcd.print(gps.satellites.value());
      lcd.print(" satellites");
      delay(2000);
    }

    if (millis() - gpsStart > 120000UL) {
      Serial.println("GPS timeout");
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("GPS timeout");
      lcd.setCursor(0, 1);
      lcd.print("Continue...");
      delay(2000);
      break;
    }
  }

  sensorSerial.begin(9600, SERIAL_8N1, HCHO_RX, HCHO_TX);
  delay(500);
  setSensorActiveMode();
  connectWiFi();
  Serial.println("System ready!");
}

void loop() {
  if (readHCHO(hchoMGm3)) {

    Serial.print("HCHO: ");
    Serial.print(hchoMGm3, 3);
    Serial.print(" mg/m3  (");
    Serial.println("%)");

    displayHCHO();
  }
  if (millis() - lastSendTime >= SEND_INTERVAL) {
    lastSendTime = millis();

    bool sent = sendMeasurement();
    if (sent) {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Sent to server");
      lcd.setCursor(0, 1);
      lcd.print(hchoMGm3, 3);
      lcd.print(" mg/m3");
    } else {
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Send FAILED");
    }
  }
  static unsigned long lastWiFiCheck = 0;
  if (millis() - lastWiFiCheck >= 30000UL) {
    lastWiFiCheck = millis();
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("WiFi disconnected!");
      connectWiFi();
    }
  }

  delay(20);
}