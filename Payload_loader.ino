

#include <Arduino.h>
#include <Servo.h>

#include <WiFi.h>
#include <AsyncTCP.h>

#include <ESPAsyncWebServer.h>

int servo1_value = 0;
int servo2_value = 0;
bool s1_changed = false;
bool s2_changed = false;
Servo servo1,servo2;
 
AsyncWebServer server(80);
const char* ssid = "platforma_mobilna";
const char* password = "r5U^WdA&E";
//const char* ssid = "iPhone (Kajetan)";
//const char* password = "12345678";

const char* input_parameter1 = "input_servo1_value";
const char* input_parameter2 = "input_servo2_value";

const char index_html[] PROGMEM = R"rawliteral(
<!DOCTYPE HTML><html><head>
  <title>HTML Form to Input Data</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    html {font-family: Times New Roman; display: inline-block; text-align: center;}
    h2 {font-size: 3.0rem; color: #FF0000;}
  </style>
  </head><body>
  <h2>HTML Form to Input Data</h2> 
  <form action="/get">
    servo1_value: <input type="text" name="input_servo1_value">
    <input type="submit" value="Submit">
  </form><br>
  <form action="/get">
    servo2_value: <input type="text" name="input_servo2_value">
    <input type="submit" value="Submit">
  </form><br>
</body></html>)rawliteral";

void notFound(AsyncWebServerRequest *request) {
  request->send(404, "text/plain", "Not found");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  if (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connecting...");
    return;
  }
  Serial.println();
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/html", index_html);
  });

  server.on("/get", HTTP_GET, [] (AsyncWebServerRequest *request) {
    String input_message;
    String input_parameter;

    if (request->hasParam(input_parameter1)) {
      input_message = request->getParam(input_parameter1)->value();
      input_parameter = input_parameter1;
      s1_changed = true;
 
      
    }
    else if (request->hasParam(input_parameter2)) {
      input_message = request->getParam(input_parameter2)->value();
      input_parameter = input_parameter2;
      s2_changed = true;
      
    }
    else {
      input_message = "No message sent";
      input_parameter = "none";
    }
    Serial.println(input_message);
    request->send(200, "text/html", "HTTP GET request sent to your ESP on input field ("+ input_parameter + ") with value: " + input_message + "<br><a href=\"/\">Return to Home Page</a>");
  });
  server.onNotFound(notFound);
  server.begin();
  servo1.attach(13); 
  servo2.attach(12); 
  servo1.write(0);
  servo2.write(0);
}

int range = 100;
void loop() {
if(s1_changed)
{
    for (float pos = 0; pos <= range; pos += 0.5) 
    { // goes from 0 degrees to 180 degrees
        servo1.write(pos);              // tell servo to go to position in variable 'pos'      
        delay(10);   
    }
    
    for (float pos = range; pos >= 0; pos -= 0.5) 
      { // goes from 0 degrees to 180 degrees
      servo1.write(pos);              // tell servo to go to position in variable 'pos'
      delay(10);                       // waits 15ms for the servo to reach the position
      }
      s1_changed = false;
}

if(s2_changed)
{
    for (float pos = 0; pos <= range; pos += 0.5) { // goes from 0 degrees to 180 degrees
        servo2.write(pos);              // tell servo to go to position in variable 'pos'
        delay(10);           
    }// waits 15ms for the servo to reach the position
    for (float pos = range; pos >= 0; pos -= 0.5) 
      { // goes from 0 degrees to 180 degrees
      servo2.write(pos);              // tell servo to go to position in variable 'pos'
      delay(10);                       // waits 15ms for the servo to reach the position
      }
      s2_changed = false;
}

}
  
