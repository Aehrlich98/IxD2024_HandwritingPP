#define CLK 2  // Pin für CLK (Clock)
#define DT 3   // Pin für DT (Data)
#define PEN_PIN 9

volatile int impulseCount = 0; // Anzahl der Impulse
int lastCLKState;             // Speichert den vorherigen CLK-Status
String movement = "";


void setup() {
  pinMode(PEN_PIN, OUTPUT); // Solenoid
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  Serial.begin(230400); // Serieller Monitor
  delay(10);

  Serial.println("Ready"); //Signal that Arduino is ready

  // Den ersten CLK-Status speichern
  lastCLKState = digitalRead(CLK);
  digitalWrite(PEN_PIN, LOW);
}

//TO DO: listen for commands(U or D) and do that then Move Pen
void loop() {
  // Aktuellen CLK-Status lesen
  int currentCLKState = digitalRead(CLK);
  //Serial lesen

  if (Serial.available()) {
    movement = Serial.readStringUntil('\n');
    movement.trim(); // Entfernt führende und nachfolgende Leerzeichen

    if (movement == "U") {
      digitalWrite(PEN_PIN, LOW); //Pen hoch
      Serial.println(movement);
    } else if( movement == "D") {
      digitalWrite(PEN_PIN, HIGH); // Pen down
    } else if (movement == "N"){
      impulseCount = 0;
      digitalWrite(PEN_PIN, LOW);
    }
  }
  
  // Wenn sich der CLK-Zustand ändert, hat sich der Encoder bewegt
  if (currentCLKState != lastCLKState) {
    // Überprüfen der Drehrichtung
    if (digitalRead(DT) != currentCLKState) {
      impulseCount--;
    } else {
      impulseCount++;
    }
  
   // Impulse ausgeben
    Serial.println(impulseCount);
  }
  // Den aktuellen CLK-Zustand speichern
  lastCLKState = currentCLKState;
}