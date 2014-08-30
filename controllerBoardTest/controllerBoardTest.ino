// Rapiro bord simple check program 
// connect servo port to SDA(A4),SCL(A5),A6,A7.
// Servo control ports are digital output.
// Analog pors are analog read.
#define R 0          // Red LED
#define G 1          // Green LED
#define B 2          // Blue LED
#define POWER 17
#define MAXSN 12
int i = 0;
int j = 0;
uint8_t servo[MAXSN];
uint8_t eyes[3] = {0, 0, 0};
boolean DATA = HIGH;
int Value[4][MAXSN] = 
{
{0,0,0,0,0,0,0,0,0,0,0,0},  //SDA
{0,0,0,0,0,0,0,0,0,0,0,0},  //SCL
{0,0,0,0,0,0,0,0,0,0,0,0},  //A6
{0,0,0,0,0,0,0,0,0,0,0,0},  //A7
};
int A6Value = 0;
int A7Value = 0;
void setup()  {
  servo[0]  = 16;  // L Foot pitch
  servo[1]  = 15;  // L Foot yaw
  servo[2]  = 14;   // L Hand grip
  servo[3]  = 13;   // L Sholder pitch
  servo[4]  = 12;   // L Sholder roll
  servo[5]  = 11;   // Waist yaw
  servo[6]  = 10;   // Head yaw
  servo[7]  = 9;    // R Sholder roll
  servo[8]  = 8;    // R Sholder pitch
  servo[9]  = 7;    // R Hand grip
  servo[10] = 4;    // R Foot yaw
  servo[11] = 2;    // R Foot pitch

  eyes[R] = 6;           // Red LED of eyes
  eyes[G] = 5;           // Green LED of eyes
  eyes[B] = 3;           // Blue LED of eyes

  for (i=0; i <MAXSN; i++) {
    pinMode(servo[i], OUTPUT);
  }
  Serial.begin(9600);
  delay(500);
}

void loop() {
 Serial.print("Check Serov port output & Analog read \n");
  for (i=0; i < MAXSN; i++) {
    for (j=0; j <MAXSN; j++) {
      if (i==j) {
        digitalWrite(servo[j],DATA); 
      }
      else {
        digitalWrite(servo[j],!DATA); 
      }
    }
    delay(100);
    Value[0][i] = analogRead(A4);
    Value[1][i] = analogRead(A5);
    Value[2][i] = analogRead(A6);
    Value[3][i] = analogRead(A7);
   digitalWrite(servo[i],!DATA); 
  }
  for (i=0; i<4; i++){
    Serial.print("A");
    Serial.print(i+4);
    Serial.print(" ");
    for (j=0; j <MAXSN; j++){
      if (Value[i][j] > 1000) {
        Serial.print("*");
      }
      else {
        Serial.print("-");
      }
        Serial.print(" ");
    }
    Serial.print("\n");
  }
  Serial.print("\n");
  Serial.print("Check Serov power switch and output voltage.\n");
  digitalWrite(POWER, HIGH);
  delay(100);
  A6Value = analogRead(A6);
  A7Value = analogRead(A7);
  Serial.print("ON");
  Serial.print(A6Value);
  Serial.print(" ");
  Serial.print(A7Value);
  Serial.print("\n");
  digitalWrite(POWER, LOW);
  for (i=0;  i<20; i++) {
  delay(1000);
  A6Value = analogRead(A6);
  A7Value = analogRead(A7);
  Serial.print(i);
  Serial.print(" ");
  Serial.print(A6Value);
  Serial.print(" ");
  Serial.print(A7Value);
  Serial.print("\n");
  }
}


