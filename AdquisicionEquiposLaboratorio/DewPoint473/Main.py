import serial

# Configura los parámetros de comunicación
ser = serial.Serial(
    port='COM4',  # Reemplaza esto con el puerto COM correcto en Windows
    baudrate=9600,      # Velocidad de baudios
    bytesize=serial.EIGHTBITS, # 8 bits de datos
    parity=serial.PARITY_NONE, # Sin paridad
    stopbits=serial.STOPBITS_ONE, # 1 bit de parada
    timeout=1            # Tiempo de espera en segundos (ajusta según sea necesario)
)

# Abre la conexión serie
ser.open()

# Envía un comando al dispositivo
comando = "DP?\r"  # Asegúrate de incluir el retorno de carro \r al final
ser.write(comando.encode())

# Lee la respuesta
respuesta = ser.read(1024)  # Lee hasta 1024 bytes (ajusta según sea necesario)

# Cierra la conexión serie
ser.close()

# Imprime la respuesta
print("Respuesta del dispositivo:", respuesta.decode())