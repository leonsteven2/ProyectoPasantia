import keyboard
from time import sleep
# Define una función para manejar la combinación de teclas
def detect_keyboard_command(e):
    #print(e)
    if e.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl') and keyboard.is_pressed('mayusculas') and keyboard.is_pressed('A'):
        print("Se presiono el comando")

# Registra la función para detectar las pulsaciones de teclas
keyboard.hook(detect_keyboard_command)

# Mantén el programa en ejecución para continuar detectando pulsaciones de teclas
while True:
    print("Este es el bucle")
    sleep(4)

print("Después de keyboard")