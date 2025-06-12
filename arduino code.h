const int ledA_Pin   = 8;    // LED for status 'a'
const int ledB_Pin   = 9;    // LED for status 'b'
const int buzzer_Pin = 10;   // passive buzzer pin

char sleep_status = 0;

void setup() {
  Serial.begin(9600);
  pinMode(ledA_Pin,   OUTPUT);
  pinMode(ledB_Pin,   OUTPUT);
  pinMode(buzzer_Pin, OUTPUT);
  digitalWrite(ledA_Pin, LOW);
  digitalWrite(ledB_Pin, LOW);
  noTone(buzzer_Pin);
}

void loop() {
  if (Serial.available() > 0) {
    sleep_status = Serial.read();

    if (sleep_status == 'a') {
      digitalWrite(ledA_Pin, HIGH);
      digitalWrite(ledB_Pin, LOW);
      tone(buzzer_Pin, 2000);   
    }
    else if (sleep_status == 'b') {
      digitalWrite(ledB_Pin, HIGH);
      digitalWrite(ledA_Pin, LOW);
      noTone(buzzer_Pin);
    }
  }
}
