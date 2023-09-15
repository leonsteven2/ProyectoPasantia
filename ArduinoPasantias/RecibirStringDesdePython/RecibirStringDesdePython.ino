int i = 1;
char mensaje;
void setup() {
  // Inicializa el puerto serial a 9600 baudios
  Serial.begin(9600);
}

void loop() {
  // Envía el valor del sensor al puerto serial
  // Serial.println(i);
  // Espera 1 segundo
  // delay(1000);
  // i += 1;
    String mensaje = Serial.readStringUntil('\n');  // Lee la cadena hasta encontrar un salto de línea
    Serial.print("Mensaje recibido desde Python: ");
    Serial.println(mensaje);
    delay(1000);
  
}
