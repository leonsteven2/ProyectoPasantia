import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import flet as ft
from flet.matplotlib_chart import MatplotlibChart
from flet import ElevatedButton
import random

matplotlib.use("svg")

def main(page: ft.Page):

    datos_x = [0,4]
    datos_y = [0,10]
    fig, ax = plt.subplots()
    grafica = ax.plot(datos_x,datos_y,label="Hola")

    def agregar_datos_plot(e):
        datos_x.append(len(datos_x) + 1)
        print(datos_x)
        datos_y.append(random.randint(0, 10))
        print(datos_y)
        grafica.update()
        page.update()



    page.add(MatplotlibChart(fig, expand=True))
    page.add(ElevatedButton("Iniciar", on_click=agregar_datos_plot))

ft.app(target=main)