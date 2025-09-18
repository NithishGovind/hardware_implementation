const int enPin = 8;   // Enable pin for all motors (CNC shield common EN)

// Step & Dir pins for 4 motors
const int stepXPin = 2;  // X.STEP
const int dirXPin  = 5;  // X.DIR

const int stepYPin = 3;  // Y.STEP
const int dirYPin  = 6;  // Y.DIR

const int stepZPin = 4;  // Z.STEP
const int dirZPin  = 7;  // Z.DIR

const int stepAPin = 4; // A.STEP  (check CNC shield pinout, usually D12)
const int dirAPin  = 7; // A.DIR   (usually D13)

// Speed control
int pulseWidthMicros = 100;   // microseconds ON time
int millisBtwnSteps = 1000;   // microseconds OFF time (controls speed)

void setup() {
  Serial.begin(9600);

  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);  // Enable all motors

  // Set step/dir pins as output
  pinMode(stepXPin, OUTPUT);
  pinMode(dirXPin, OUTPUT);

  pinMode(stepYPin, OUTPUT);
  pinMode(dirYPin, OUTPUT);

  pinMode(stepZPin, OUTPUT);
  pinMode(dirZPin, OUTPUT);

  pinMode(stepAPin, OUTPUT);
  pinMode(dirAPin, OUTPUT);

  // Set initial direction (can change later)
  digitalWrite(dirXPin, HIGH);  
  digitalWrite(dirYPin, HIGH);  
  digitalWrite(dirZPin, HIGH);  
  digitalWrite(dirAPin, HIGH);  

  Serial.println(F("All 4 steppers running continuously..."));
}

void loop() {
  // Pulse all 4 step pins together
  digitalWrite(stepXPin, HIGH);
  digitalWrite(stepYPin, HIGH);
  digitalWrite(stepZPin, HIGH);
  digitalWrite(stepAPin, HIGH);

  delayMicroseconds(pulseWidthMicros);

  digitalWrite(stepXPin, LOW);
  digitalWrite(stepYPin, LOW);
  digitalWrite(stepZPin, LOW);
  digitalWrite(stepAPin, LOW);

  delayMicroseconds(millisBtwnSteps);
}
