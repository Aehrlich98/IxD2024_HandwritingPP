#define CLK 2  // Pin für CLK (Clock)
#define DT 3   // Pin für DT (Data)
#define PEN_PIN 9

volatile int impulseCount = 0; // Anzahl der Impulse
int lastCLKState;             // Speichert den vorherigen CLK-Status
String inputString = "";      // Eingabewort
String morseString = "";      // Eingabewort in Morse
String binaryString = "0";    // Eingabewort in Binary
int8_t lookUpSymbol[1000];        // Array für Ziffern (max. 100 Ziffern als Beispiel)
int lookUpIndex = 0;          // Index für das Array

// Morsecode-Mapping
const char* morseCodeTable[36] = {
  ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---",  // A-J
  "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-",    // K-T
  "..-", "...-", ".--", "-..-", "-.--", "--..",                           // U-Z
  "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----." // 0-9
};

// Funktion die Eingabe String in Morse Code umwandelt
String toMorseCode(String input) {
  input.toUpperCase(); // Konvertiere in Großbuchstaben
  String morseCode = "";

  for (unsigned int i = 0; i < input.length(); i++) {
    char c = input[i];

    if (c >= 'A' && c <= 'Z') {
      morseCode += String(morseCodeTable[c - 'A']);
    } else if (c >= '0' && c <= '9') {
      morseCode += String(morseCodeTable[c - '0' + 26]);
    } else if (c == ' ') {
      morseCode += "/"; // Trennung für Leerzeichen
    } else {
      // Unbekannte Zeichen überspringen
      continue;
    }

    morseCode += " "; // Trennung zwischen Buchstaben
  }
  morseCode.trim();
  return morseCode;
}

// Funktion die Morse in Binary umwandelt
String toBinaryString(String morseCode) {
  String binaryString = "";
  int symbolCount = 0;

  for (unsigned int i = 0; i < morseCode.length(); i++) {
    char c = morseCode[i];

    if (c == '.') {
      binaryString += "001100"; // Punkt
      for (unsigned int j = 0; j < 6; j++) {
        lookUpSymbol[lookUpIndex++] = symbolCount; // Ziffer zum Array hinzufügen
      }
      symbolCount++;
    } else if (c == '-') {
      binaryString += "0011111100"; // Strich
      for (unsigned int j = 0; j < 10; j++) {
        lookUpSymbol[lookUpIndex++] = symbolCount; // Ziffer zum Array hinzufügen
      }
      symbolCount++;
    } else if (c == ' ') {
      binaryString += "0000"; // Leerzeichen zwischen Buchstaben
      for (unsigned int j = 0; j < 4; j++) {
        lookUpSymbol[lookUpIndex++] = symbolCount; // Ziffer zum Array hinzufügen
      }
      symbolCount++;
    } else if (c == '/') {
      binaryString += "0000"; // Leerzeichen zwischen Wörtern
      for (unsigned int j = 0; j < 4; j++) {
        lookUpSymbol[lookUpIndex++] = symbolCount; // Ziffer zum Array hinzufügen
      }
      symbolCount++;
    }
  }
  return binaryString;
}

void requestNewWord() {
  // Benutzeraufforderung zur Eingabe eines Strings
  inputString = ""; // Zurücksetzen des Eingabeworts
  lookUpIndex = 0; // Zurücksetzen des LookUp-Index
  impulseCount = 0; // Zurücksetzen des Impulszählers

  Serial.println("Bitte einen neuen String eingeben:");
  while (inputString.length() == 0) {
    if (Serial.available()) {
      inputString = Serial.readStringUntil('\n');
      inputString.trim(); // Entfernt führende und nachfolgende Leerzeichen
    }
  }

  // Eingabe bestätigen
  Serial.print("Eingabe: ");
  Serial.println(inputString);

  morseString = toMorseCode(inputString);
  Serial.println("Morsecode: " + morseString);

  binaryString = toBinaryString(morseString);
  Serial.println("Binärstring: " + binaryString);
  Serial.println(binaryString.length());

  // Ausgabe des LookUp Arrays
  Serial.print("LookUp: ");
  for (int i = 0; i < lookUpIndex; i++) {
    Serial.print(lookUpSymbol[i]);
    if (i < lookUpIndex - 1) {
      Serial.print(",");
    }
  }
  Serial.println();
}

void setup() {
  pinMode(PEN_PIN, OUTPUT); // Solenoid
  pinMode(CLK, INPUT);
  pinMode(DT, INPUT);
  Serial.begin(115200); // Serieller Monitor
  delay(10);

  // Initiales Wort abfragen
  requestNewWord();

  // Den ersten CLK-Status speichern
  lastCLKState = digitalRead(CLK);
}

void loop() {
  // Aktuellen CLK-Status lesen
  int currentCLKState = digitalRead(CLK);

  // Wenn sich der CLK-Zustand ändert, hat sich der Encoder bewegt
  if (currentCLKState != lastCLKState) {
    // Überprüfen der Drehrichtung
    if (digitalRead(DT) != currentCLKState) {
      impulseCount++;
    } else {
      impulseCount--;
    }

    // Grenzen überprüfen
    if (impulseCount < 0) {
      impulseCount = 0;
    } else if (impulseCount >= binaryString.length()) {
      // Wenn das Ende des Binary-Strings erreicht ist, neues Wort abfragen
      requestNewWord();
      return;
    }

    // Impulse ausgeben
    Serial.println(impulseCount);

    if (binaryString[impulseCount] == '1') {
      // Pen runter
      digitalWrite(PEN_PIN, HIGH);
    } else if (binaryString[impulseCount] == '0') {
      // Pen hoch
      digitalWrite(PEN_PIN, LOW);
    }
  }

  // Den aktuellen CLK-Zustand speichern
  lastCLKState = currentCLKState;
}
