import serial
import time
# Abre el puerto serial
fluke = serial.Serial('COM9', 9600)

print("Entra a bucle")
mensaje = "READ? \r\n"
while True:
    fluke.write(mensaje.encode())
    mensaje_desde_fluke = fluke.readline().decode()
    if mensaje_desde_fluke == "READ? \r\n":
        continue
    print(mensaje_desde_fluke)
    time.sleep(2)


# # Mensaje si es que se necesita
# mensaje = "READ? 1\r\n"
#
# while True:
#     mensaje = "READ? 1\r\n"
#     fluke.write(mensaje.encode())
#     mensaje_desde_fluke = fluke.readline().decode()
#     mensaje_desde_fluke = mensaje_desde_fluke.strip().split(",")
#     print(f'Temperatura 1: {mensaje_desde_fluke[0]}, HR 1: {mensaje_desde_fluke[1]}')
#
#     mensaje = "READ? 2\r\n"
#     fluke.write(mensaje.encode())
#     mensaje_desde_fluke = fluke.readline().decode()
#     mensaje_desde_fluke = mensaje_desde_fluke.strip().split(",")
#     print(f'Temperatura 2: {mensaje_desde_fluke[0]}, HR 2: {mensaje_desde_fluke[1]}')
#     #print(f'Temperatura 1: {mensaje_desde_fluke[1].strip()} °C ; Humedad Relativa 1: {mensaje_desde_fluke[3].strip()} %')
#     #print(f'Temperatura 2: {mensaje_desde_fluke[5].strip()} °C ; Humedad Relativa 2: {mensaje_desde_fluke[7].strip()} %\n')
