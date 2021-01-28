#include <IRControl.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>

ESP8266WebServer server(80);
IRsend irsend(14); //D5

void handlePage();
void handleJs();
void handleCss();
void handleCommand();
void blinkLed();

void setup(){
  Serial.begin(9600);
  delay(1000);
  irsend.begin();

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  Serial.print("Starting WiFi");
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID_NAME, SSID_PSWD);
  WiFi.hostname("localir");
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  
  Serial.print("IP address:");
  Serial.println(WiFi.localIP()); 

  server.on("/", handlePage);   
  server.on("/static/actions.js", handleJs);
  server.on("/static/style.css", handleCss);
  server.on("/command-obj", HTTP_POST, handleCommand);

  server.begin();
  Serial.println("HTTP server started...");
  WiFi.hostname("webremote");
  Serial.println("host: http://webremote");
}

void handlePage() {
  String page = html_page;
  server.send(200, "text/html", page);
}

void handleJs(){
  String js = js_control;  
  server.send(200, "script", js);
}

void handleCss(){
  String css = css_style;  
  server.send(200, "text/css", css);
}

void handleCommand(){
  String plain = server.arg("plain");  
  Serial.print("plain:");Serial.println(plain);
  StaticJsonDocument<300> doc;  
  deserializeJson(doc, plain);
  processCommand(doc);
  blinkLed();
  server.send(200, "text/plain", String("{status:'ok'}") );
}

void blinkLed(){
  digitalWrite(LED_BUILTIN, LOW);
  delay(200);
  digitalWrite(LED_BUILTIN, HIGH);
}

void processCommand(StaticJsonDocument<300> doc){
  int numCodes =  doc["codes"].size();   
  String type = doc["type"];
  for(int i=0;i < numCodes;i++){    
      String rslt = doc["codes"][i]; 
      genericCommand(getLong(rslt), type.toInt());
      delay(400);
  }
}

void genericCommand(unsigned long code, int type){
  Serial.print(":::: code: ");Serial.println(code);
  Serial.print(":::: type: ");Serial.println(type);
  switch(type){    
    case decode_type_t::NEC: irsend.sendNEC(code);break;//3
    case decode_type_t::SAMSUNG: irsend.sendSAMSUNG(code);break;//7
    case decode_type_t::LG: irsend.sendLG(code);break;//10
    default: Serial.println("There are no  codes for this device.");
  }
}

unsigned long getLong(String value){
    char* bfr;
    char rslt[16];
    value.toCharArray(rslt, 16);
    unsigned long result = strtoul(rslt, &bfr, 16);
    return result;
}

void loop(){
  server.handleClient();
}
