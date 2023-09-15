import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Crear datos ficticios
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Crear un DataFrame
data = pd.DataFrame({'x': x, 'y': y})

# Crear una paleta de colores estilo neon
color_scale = [
    [0, 'rgba(0, 255, 150, 1.0)'],  # Color inicial (verde neon)
    [1, 'rgba(0, 255, 150, 0.2)']   # Color final con opacidad reducida
]

# Crear un gráfico de línea interactivo estilo neon
fig = go.Figure()

# Agregar círculos rellenos y líneas
fig.add_trace(
    go.Scatter(
        x=data['x'],
        y=data['y'],
        mode='lines+markers',
        marker=dict(size=10, color=data['y'], colorscale=color_scale, showscale=True),
        line=dict(width=3, color='white'),
    )
)

# Personalizar el diseño del gráfico
fig.update_layout(
    title='Gráfico de Línea Neon Interactivo',
    xaxis_title='Eje X',
    yaxis_title='Eje Y',
    font=dict(family='Arial', size=14, color='white'),
    xaxis=dict(showline=True, linewidth=2, linecolor='white', mirror=True),
    yaxis=dict(showline=True, linewidth=2, linecolor='white', mirror=True),
    plot_bgcolor='black',  # Fondo negro
    paper_bgcolor='black',  # Color de fondo del papel
    showlegend=False,
)

# Mostrar el gráfico interactivo estilo neon
fig.show()
