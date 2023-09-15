import plotly.express as px
import plotly.graph_objs as go
import flet as ft
from flet import ElevatedButton
from plotly.subplots import make_subplots
import pandas as pd
from flet.plotly_chart import PlotlyChart
import random

def main(page: ft.Page):
    datos_x = [0]
    datos_y = [0]
    fig = make_subplots(rows=1, cols=1)
    fig.update_layout(title='Gráfica en Tiempo Real')

    def add_point_to_graphic(e):
        datos_x.append(len(datos_x)+1)
        print(datos_x)
        datos_y.append(random.randint(0,10))
        print(datos_y)
        fig.data = []  # Limpiar los datos existentes
        fig.add_trace(go.Scatter(x=datos_x, y=datos_y, mode='lines+markers', name='Puntos en tiempo real'))
        fig.update_traces()
        page.update()
        print("Sale de la funcion")



    page.add(PlotlyChart(fig, expand=True))
    page.add(ElevatedButton("Agregar", on_click=add_point_to_graphic))

ft.app(target=main)