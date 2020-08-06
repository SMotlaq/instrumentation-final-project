#define p1_status   7    // send      green
#define p2_status   6    // send      red
#define m1_instruct 3    // receive   yellow
#define m2_instruct 2    // receive   white
#define m1_led      11
#define m2_led      8
#define trigPin1    13                                   
#define echoPin1    12
#define trigPin2    10
#define echoPin2    9

long duration     = 0,
     distance     = 0,
     UltraSensor1 = 0,
     UltraSensor2 = 0; 

void setup()
{
  Serial.begin (9600);      
  pinMode(p1_status,  OUTPUT);
  pinMode(p2_status,  OUTPUT);
  pinMode(m1_instruct, INPUT);
  pinMode(m2_instruct, INPUT);
  
  // setup pins first sensor
  pinMode(trigPin1, OUTPUT);                        
  pinMode(echoPin1, INPUT);                         
  pinMode(m1_led, OUTPUT);                  
  
  //setup pins second sensor
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);
  pinMode(m2_led, OUTPUT);
  
  //inisialize LED status 
  digitalWrite(m1_led,LOW);
  digitalWrite(m2_led,LOW);
}

void loop() 
{
  Serial.print("Sensor 1 distance:");
  Distant_function(trigPin1, echoPin1);              
  UltraSensor1 = distance;
  Serial.print("Sensor 2 distance:");
  Distant_function(trigPin2,echoPin2);               
  UltraSensor2 = distance;                      
 
  if(UltraSensor1 >=10){                            // parking 1 khali
    digitalWrite(p1_status, LOW);
  }
  else{                                             // parking 1 por
    digitalWrite(p1_status,HIGH); 
  }
  
  if(UltraSensor2 >=10){                            // parking 2 khali
    digitalWrite(p2_status,LOW);
  }
  else{                                             // parking 2 por
    digitalWrite(p2_status,HIGH);  
  }
  
  if(digitalRead(m1_instruct) == HIGH){           //Dastur Roshan-Khamush led1
    digitalWrite(m1_led,HIGH);
  }
  else{
    digitalWrite(m1_led,LOW);
  }
  
  if(digitalRead(m2_instruct) == HIGH){           //Dastur Roshan-Khamush led2
    digitalWrite(m2_led,HIGH);
  }
  else{
    digitalWrite(m2_led,LOW);
  }

  delay(500);
}

void Distant_function(int trigPinSensor,int echoPinSensor){
  
  digitalWrite(trigPinSensor, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinSensor, HIGH);
  delayMicroseconds(10); 
  digitalWrite(trigPinSensor, LOW);
  
  duration = pulseIn(echoPinSensor, HIGH);
  distance= duration / 29 / 2;
  Serial.println((int)distance);
}
