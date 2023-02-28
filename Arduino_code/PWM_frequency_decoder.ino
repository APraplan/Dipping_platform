/*
  PWM frequency decoder
*/
# include <Servo.h>

# define PIN_in   A3
# define PIN_out  D6
# define PERIODE  1000

volatile long StartTime = 0;
volatile long CurrentTime = 0;
int PulseWidth = 0;

Servo Servo1;

void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // configure input/output pin:
  pinMode(PIN_in, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_in), PulseTimerReset, RISING);
  attachInterrupt(digitalPinToInterrupt(PIN_in), PulseTimer, FALLING);
  
  Servo1.attach(PIN_out);
}

void loop() {
  Serial.println(PulseWidth);
  int angle = map(PulseWidth, 0, PERIODE, 0, 180);
  Servo1.write(angle);  
}

void PulseTimerReset(){
  CurrentTime = micros();
  StartTime = CurrentTime;
}

void PulseTimer(){
  CurrentTime = micros();
  if (CurrentTime > StartTime){
    PulseWidth = CurrentTime - StartTime;
  }
}