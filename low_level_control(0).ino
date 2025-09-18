// CNC Shield Skid Steering with Speed Control
// Left motors: X + Y
// Right motors: Z + A (A mirrors Z)

const int enPin = 8;   // Enable pin (active LOW)
const int stepX = 2;   // X.STEP
const int dirX  = 5;   // X.DIR
const int stepY = 3;   // Y.STEP
const int dirY  = 6;   // Y.DIR
const int stepZ = 4;   // Z.STEP
const int dirZ  = 7;   // Z.DIR
// A axis mirrors Z automatically

int speedDelay = 500;  // default delay (µs)
char cmd = 's';        // current command

void setup() {
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW); // Enable motors

  pinMode(stepX, OUTPUT); pinMode(dirX, OUTPUT);
  pinMode(stepY, OUTPUT); pinMode(dirY, OUTPUT);
  pinMode(stepZ, OUTPUT); pinMode(dirZ, OUTPUT);

  Serial.begin(9600);
}

void stepMotor(int stepPin) {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(2);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(speedDelay);
}

void loop() {
  if (Serial.available()) {
    char incoming = Serial.read();

    if (incoming >= '0' && incoming <= '9') {
      int level = incoming - '0';
      speedDelay = 1000 - (level * 100);  // 1000 → 100 µs
    } else {
      cmd = incoming; // update movement command
    }
  }

  if (cmd == 'f') { // forward
    digitalWrite(dirX, HIGH); digitalWrite(dirY, HIGH);
    digitalWrite(dirZ, HIGH);
    stepMotor(stepX); stepMotor(stepY); stepMotor(stepZ);

  } else if (cmd == 'b') { // backward
    digitalWrite(dirX, LOW); digitalWrite(dirY, LOW);
    digitalWrite(dirZ, LOW);
    stepMotor(stepX); stepMotor(stepY); stepMotor(stepZ);

  } else if (cmd == 'l') { // left turn
    digitalWrite(dirX, LOW); digitalWrite(dirY, LOW);
    digitalWrite(dirZ, HIGH);
    stepMotor(stepX); stepMotor(stepY); stepMotor(stepZ);

  } else if (cmd == 'r') { // right turn
    digitalWrite(dirX, HIGH); digitalWrite(dirY, HIGH);
    digitalWrite(dirZ, LOW);
    stepMotor(stepX); stepMotor(stepY); stepMotor(stepZ);
  }
  // 's' = stop → do nothing
}
