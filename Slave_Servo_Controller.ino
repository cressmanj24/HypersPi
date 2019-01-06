#include <Wire.h>
#include <Servo.h>

#define SLAVE_ADDRESS 0x04
int number = 0;
int pin = 3;
int normalized = 1500;
Servo server;

void setup() {
//  pinMode(13, OUTPUT);
  Serial.begin(9600); // start serial for output
  
  // initialize i2c as slave
  Wire.begin(SLAVE_ADDRESS);

  // define callbacks for i2c communication
  Wire.onReceive(receiveData);
  //Wire.onRequest(sendData);

//  Serial.println("Ready!");
  server.attach(9);

}

void loop() {
//  delay(100);
}

// callback for received data
void receiveData(int byteCount){

  while(Wire.available()) {
    number = Wire.read();
    /*if (number <= 13) pin = number;
    
    else analogWrite(pin,number);*/
    normalized = number + 1500;

    server.writeMicroseconds(normalized);
    
    Serial.print("data received: ");
    Serial.print(number);
    Serial.print(" | Servo Microseconds: ");
    Serial.println(normalized);
//    Serial.print(pin);
//    Serial.print(" ");
//    Serial.println(number);
  }
}
