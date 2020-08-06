#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
 
const char* ssid = "S.Motlaq";
const char* password = "ffd5612&78%";
int c;

void setup () {
  Serial.begin(9600);
  Serial.println("\n\r---------- START ---------");
  
  pinMode(D0, OUTPUT); 
  pinMode(D1, OUTPUT); 
  pinMode(D2, INPUT); 
  pinMode(D3, INPUT); 
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.println("Connecting...");
  }
}
 
void loop() { 
  if (WiFi.status() == WL_CONNECTED){                                           //Check WiFi connection status
    HTTPClient http;                                                            //Declare an object of class HTTPClient
    http.begin("http://176.9.199.181:5000/get_status?password=dorosteaghaye");  //Specify request destination
    int httpCode = http.GET();                                                  //Send the request
    if (httpCode > 0){                            //Check the returning code
      String payload = http.getString();          //Get the request response payload  
      int a= payload.toInt();
      int b=a%10;
      c=a/10;
      digitalWrite(D0, b);
      digitalWrite(D1, c);
    }
    int inpstr=10* digitalRead(D3)+ digitalRead(D2);
    switch (inpstr){
      case 0:
        http.begin("http://176.9.199.181:5000/set_status?password=dorosteaghaye&state=00");  //Specify request destination
        c = http.GET();                                                                  //Send the request
        if (c > 0){                                                                          //Check the returning code
          String a = http.getString();  //Get the request response payload
          Serial.println(a); 
        }
        break;
      case 10:
        http.begin("http://176.9.199.181:5000/set_status?password=dorosteaghaye&state=10");  //Specify request destination
        c = http.GET();                                                                  //Send the request
        if (c > 0){                                                                          //Check the returning code
          String a = http.getString();   //Get the request response payload
          Serial.println(a); 
        }
        break;   
      case 1:
        http.begin("http://176.9.199.181:5000/set_status?password=dorosteaghaye&state=01");  //Specify request destination
        c = http.GET();                                                                  //Send the request
        if (c > 0){                                                                          //Check the returning code
          String a = http.getString();   //Get the request response payload
          Serial.println(a); 
        }
        break;   
      case 11:
        http.begin("http://176.9.199.181:5000/set_status?password=dorosteaghaye&state=11");  //Specify request destinationint 
        c = http.GET();                                                                  //Send the request
        if (c > 0){                                                                          //Check the returning code
          String a = http.getString();   //Get the request response payload
          Serial.println(a); 
        }
        break;
    }
    http.end();    //Close connection
    delay(500);    //Send a request every .5 seconds
  }
}
