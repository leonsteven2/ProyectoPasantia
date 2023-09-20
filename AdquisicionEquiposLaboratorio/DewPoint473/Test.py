import serial
import time
# Abre el puerto serial
dew_473 = serial.Serial('COM5', 9600)

while True:
    mensaje = "DP?\r"
    dew_473.write(mensaje.encode())
    mensaje_desde_fluke = dew_473.readline().decode().strip()
    print(mensaje_desde_fluke)

    mensaje = "Tx?\r"
    dew_473.write(mensaje.encode())
    mensaje_desde_fluke = dew_473.readline().decode().strip()
    print(mensaje_desde_fluke)

    time.sleep(2)
    print("\n")