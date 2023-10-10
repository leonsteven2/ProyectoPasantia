import serial
import time
# Abre el puerto serial
thunder = serial.Serial(
    port='COM5',  # Reemplaza 'COM1' con el puerto COM correcto en Windows
    baudrate=9600,      # Velocidad de baudios
    bytesize=serial.EIGHTBITS, # 8 bits de datos
    parity=serial.PARITY_NONE, # Sin paridad
    stopbits=serial.STOPBITS_ONE, # 1 bit de parada
    timeout=1            # Tiempo de espera en segundos (ajusta según sea necesario)
)

while True:
    mensaje = "?\r"
    thunder.write(mensaje.encode())
    #mensaje_desde_thunder = thunder.readline().decode().strip().split(",")
    #print(mensaje_desde_thunder[0])
    mensaje = thunder.readline().decode()
    print(mensaje)

    time.sleep(2)