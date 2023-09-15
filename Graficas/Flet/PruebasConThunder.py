import plotly.express as px
import plotly.graph_objs as go
import flet as ft
from flet import ElevatedButton
from plotly.subplots import make_subplots
import pandas as pd
from flet.plotly_chart import PlotlyChart
import random
import serial
import time

def main(page: ft.Page):
    datos_x = [0]
    datos_y = [0]
    fig = make_subplots(rows=1, cols=1)
    fig.add_trace(go.Line(x=datos_x, y=datos_y, name='Puntos en tiempo real'))
    fig.update_layout(title='Gráfica en Tiempo Real')
    thunder = serial.Serial(
        port='COM5',  # Reemplaza 'COM1' con el puerto COM correcto en Windows
        baudrate=2400,  # Velocidad de baudios
        bytesize=serial.EIGHTBITS,  # 8 bits de datos
        parity=serial.PARITY_NONE,  # Sin paridad
        stopbits=serial.STOPBITS_ONE,  # 1 bit de parada
        timeout=1  # Tiempo de espera en segundos (ajusta según sea necesario)
    )

    def add_point_to_graphic(e):

        while True:
            datos_x.append(len(datos_x) + 1)

            mensaje = "?\r"
            thunder.write(mensaje.encode())
            mensaje_desde_thunder = thunder.readline().decode().strip().split(",")
            datos_y.append(mensaje_desde_thunder[0])

            fig.data = []  # Limpiar los datos existentes
            fig.add_trace(go.Line(x=datos_x, y=datos_y, name='Puntos en tiempo real'))
            #fig.update_traces()
            page.update()
            print("Sale de la funcion")

            time.sleep(5)





    page.add(PlotlyChart(fig, expand=True))
    page.add(ElevatedButton("Agregar", on_click=add_point_to_graphic))

ft.app(target=main)