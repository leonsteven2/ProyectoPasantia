import serial
import time
# Abre el puerto serial
fluke = serial.Serial('COM5', 9600)

while True:
    mensaje = "DP?\r"
    fluke.write(mensaje.encode())
    mensaje_desde_fluke = fluke.readline().decode().strip()
    print(mensaje_desde_fluke)

    mensaje = "Tx?\r"
    fluke.write(mensaje.encode())
    mensaje_desde_fluke = fluke.readline().decode().strip()
    print(mensaje_desde_fluke)

    time.sleep(2)
    print("\n")