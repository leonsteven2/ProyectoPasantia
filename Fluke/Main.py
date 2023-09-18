import serial
import time
# Abre el puerto serial
fluke = serial.Serial('COM2', 9600)

# Mensaje si es que se necesita
mensaje = "READ? 1\r"

while True:
    mensaje_desde_fluke = fluke.readline().decode()
    mensaje_desde_fluke = mensaje_desde_fluke.split(",")
    print(f'Temperatura 1: {mensaje_desde_fluke[1].strip()} °C ; Humedad Relativa 1: {mensaje_desde_fluke[3].strip()} %')
    print(f'Temperatura 2: {mensaje_desde_fluke[5].strip()} °C ; Humedad Relativa 2: {mensaje_desde_fluke[7].strip()} %\n')
