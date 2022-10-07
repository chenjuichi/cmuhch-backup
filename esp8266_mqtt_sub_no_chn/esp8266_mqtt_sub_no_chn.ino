#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#include <ArduinoJson.h>

#define LED 2

// wifi的設定資料
const char* ssid = "ZH";
const char* password = "-pmc4394";
const char* mqttServer = "192.168.32.178";

char* led_status =" LedOff";

WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// 收到信息後的CallBack函數
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message Received from [");
  Serial.print(topic);                //顯示MQTT的topic
  Serial.print("] , value: ");

  char message[10]={0x00};
  for (int i = 0; i < length; i++) {
    message[i]=(char)payload[i];
    Serial.print((char)payload[i]);   //顯示MQTT的topic value(json資料形式)
  }
  message[length]=0x00;
  Serial.println("");
  Serial.print("Message Length(Bytes) ");
  Serial.println(length);

  StaticJsonDocument <256> doc;
  deserializeJson(doc, payload);
  const char* ledStrip_layout = doc["Layout"];  //解Layout的JSON序列化(Serialize)資料
  const char* ledStrip_led = doc["Led"];        //解Led的JSON序列化(Serialize)資料
  const char* ledStrip_msg = doc["Msg"];        //解Msg的JSON序列化(Serialize)資料
  //顯示json資料
  //Serial.print("ledStrip_Layout: ");
  //Serial.print(ledStrip_layout);

  //Serial.print("  ledStrip_Led: ");
  //Serial.print(ledStrip_led);

  //Serial.print("  ledStrip_Msg: ");
  //Serial.print(ledStrip_msg);

  int myInt = atoi(ledStrip_layout);
  switch(myInt){
    case 1:
      Serial.print("ledStrip_Layout: ");
      Serial.print(ledStrip_layout);
      break;
    case 2:
      Serial.print("ledStrip_Layout: ");
      Serial.print(ledStrip_layout);
      break;
    case 3:
      Serial.print("ledStrip_Layout: ");
      Serial.print(ledStrip_layout);
      break;
    case 4:
      Serial.print("ledStrip_Layout: ");
      Serial.print(ledStrip_layout);
      break; 
    default:
      Serial.print("ledStrip_Layout: ");
      Serial.print(ledStrip_layout);                    
  }
  
  //String str_msg= String(message);
  String str_msg= String(ledStrip_msg);
  //if ((char)payload[0] == '1') {      // 如果收到的訊息以“1”為開始
  if (str_msg.equals("on")) {           // 如果收到的訊息為"on"
    //digitalWrite(LED, LOW);           // 點亮LED
    //Serial.println("Station1/Layout1/Led5 LED ON");
    String strLed("Station1/");       // 初始化字串
    strLed = strLed + ledStrip_layout+"/"+ledStrip_led+" LED_ON";
    
    Serial.println(strLed);
    led_status =" LedOn";
  } else if (str_msg.equals("off")){  // 如果收到的訊息為"off"                            
    //digitalWrite(LED, HIGH);        // 點滅LED
    //Serial.println("Station1/Layout1/Led5 LED OFF");
    String strLed("Station1/");       // 初始化字串
    strLed = strLed + ledStrip_layout+"/"+ledStrip_led+" LED_OFF";
    Serial.println(strLed);
    led_status =" LedOff";
  }
 
}

void setup() { 
  pinMode(LED, OUTPUT);     // 設定LED port為輸出模式
  digitalWrite(LED, HIGH);  // 設定LED off
  Serial.begin(9600);       // 設定serial monitor 通訊速率
 
  WiFi.mode(WIFI_STA);      // 設定ESP8266工作模式為無線終端模式
    
  connectWifi();  // 連線WiFi
  
  mqttClient.setServer(mqttServer, 1883);   // 設定MQTT服務和port  
  mqttClient.setCallback(mqttCallback);     // 設定MQTT訂閱callback
  
  connectMQTTserver();                      // 連線MQTT服務
}

void loop() {
  delay(200);
  
  mqttClient.loop();
}

// ESP8266連線wifi
void connectWifi(){ 
  WiFi.begin(ssid, password);
  //WiFi.begin(ssid);     //if no password  
 
  //等待WiFi連線,成功連線後輸出成功訊息
  Serial.print("Waitting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi Connected!");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());   // You can get IP address assigned to ESP8266    
}

// 連線MQTT服務并訂閱信息
void connectMQTTserver(){
  // 客户端ID
  String clientId = "CLIENT-esp8266-1";
 
  // 連線MQTT服務
  if (mqttClient.connect(clientId.c_str(), NULL, NULL)) { 
    Serial.println("MQTT Server Connected.");
    Serial.println("Server Address: ");
    Serial.println(mqttServer);
    Serial.println("ClientId: ");
    Serial.println(clientId);
    subscribeTopic(); // 訂閱指定主题
  } else {
    Serial.print("MQTT Server Connect Failed. Client State:");
    Serial.println(mqttClient.state());
    delay(1000);
  }   
}

// 訂閱指定主题
void subscribeTopic(){ 
  String topicString = "Station1";
  char subTopic[topicString.length() + 1];  
  strcpy(subTopic, topicString.c_str());
  
  // 確認訂閱主题是否訂閱成功
  if(mqttClient.subscribe(subTopic)){
    Serial.println("Subscrib Topic: ");
    Serial.println(subTopic);
  } else {
    Serial.print("Subscribe Fail...");
  }  
}
