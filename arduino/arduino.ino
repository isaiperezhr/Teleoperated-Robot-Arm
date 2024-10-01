#include <Servo.h>

Servo servo1, servo2, servo3, servo4, servo5, servo6;

void setup() {
  Serial.begin(9600);
  servo1.attach(9);  // Conectar el Servo 1 al pin 9
  servo2.attach(10); // Conectar el Servo 2 al pin 10
  servo3.attach(11); // Conectar el Servo 3 al pin 11
  servo4.attach(5);  // Conectar el Servo 4 al pin 5
  servo5.attach(6);  // Conectar el Servo 5 al pin 6
  servo6.attach(7);  // Conectar el Servo 6 al pin 7
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n'); // Leer los datos enviados
    int s1 = getValue(input, 'S', 1);
    int s2 = getValue(input, 'S', 2);
    int s3 = getValue(input, 'S', 3);
    int s4 = getValue(input, 'S', 4);
    int s5 = getValue(input, 'S', 5);
    int s6 = getValue(input, 'S', 6);

    // Mover los servos a los ángulos recibidos
    servo1.write(s1);
    servo2.write(s2);
    servo3.write(s3);
    servo4.write(s4);
    servo5.write(s5);
    servo6.write(s6);
  }
}

int getValue(String data, char delimiter, int index) {
  int startIndex = data.indexOf(delimiter + String(index) + ":") + 3;
  int endIndex = data.indexOf(" ", startIndex);
  if (endIndex == -1) {  // Si es el último valor de la cadena
    endIndex = data.length();
  }
  return data.substring(startIndex, endIndex).toInt();  // Convertir a entero
}
