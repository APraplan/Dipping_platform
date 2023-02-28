#include "pyCommsLib.h"
#include <Servo.h>

Servo servo1;
int pos = 0;

void setup() {
  Serial.begin(9600);           // set up Serial library at 9600 bps
  servo1.attach(9);
  init_python_communication();
}

void loop() {
  String received_message = latest_received_msg();
  //WATER
  if (received_message == "open") {
    pos = 50;
    servo1.write(pos);
  }
  if (received_message == "close") {
    pos = 105;
    servo1.write(pos);
  }
  sync();

}
