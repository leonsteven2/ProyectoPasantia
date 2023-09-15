import serial

# Abre el puerto serial
arduino = serial.Serial('COM5', 9600)

# Mensaje
mensaje = "Hola, Arduino!"
arduino.write(mensaje.encode())
print(mensaje.encode())
# # Lee los datos del puerto serial
while True:
  arduino.write(mensaje.encode())
  mensaje_arduino = arduino.readline().decode()
  print(mensaje_arduino)

