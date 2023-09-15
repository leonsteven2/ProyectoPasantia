import plotly.graph_objs as go
from plotly.subplots import make_subplots
import time
import random

# Crear una figura de subgráficos
fig = make_subplots(rows=1, cols=1)
fig.update_layout(title='Gráfica en Tiempo Real')

# Listas para almacenar los datos
datos_x = []
datos_y = []

# Función para agregar un punto a la gráfica
def agregar_punto():
    datos_x.append(len(datos_x) + 1)
    datos_y.append(random.randint(1, 100))

# Bucle para agregar nuevos puntos cada 2 segundos
while True:
    agregar_punto()

    # Actualizar la gráfica
    fig.data = []  # Limpiar los datos existentes
    fig.add_trace(go.Scatter(x=datos_x, y=datos_y, mode='lines+markers', name='Puntos en tiempo real'))

    # Mostrar la gráfica
    fig.show()

    time.sleep(2)  # Esperar 2 segundos antes de agregar el próximo punto
