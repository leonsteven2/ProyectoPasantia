import serial

# Configura los parámetros de comunicación
ser = serial.Serial(
    port='COM1',  # Reemplaza 'COM1' con el puerto COM correcto en Windows
    baudrate=9600,      # Velocidad de baudios
    bytesize=serial.EIGHTBITS, # 8 bits de datos
    parity=serial.PARITY_NONE, # Sin paridad
    stopbits=serial.STOPBITS_ONE, # 1 bit de parada
    timeout=1            # Tiempo de espera en segundos (ajusta según sea necesario)
)

# Abre la conexión serie
ser.open()

# Envía el comando al dispositivo
comando = "?\r"
ser.write(comando.encode())

# Lee y muestra la respuesta del dispositivo (ajusta el tamaño del búfer según sea necesario)
respuesta = ser.read(1024).decode()
print("Respuesta del dispositivo:", respuesta)

# Cierra la conexión serie
ser.close()