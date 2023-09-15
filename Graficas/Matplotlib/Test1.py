import random

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

import flet as ft
from flet.matplotlib_chart import MatplotlibChart
import time
matplotlib.use("svg")

def main(page: ft.Page):
    fig, ax = plt.subplots()
    datos_x = [0]
    datos_y = [0]
    page.add(MatplotlibChart(fig, expand=True, transparent=True))

    datos_x1 = [0]
    datos_y1 = [0]

    contador = 0
    while True:
        contador = contador + 1
        time.sleep(2)
        if len(datos_x) >= 15:
            datos_x.pop(0)
            datos_y.pop(0)
        datos_x.append(contador)
        datos_y.append(random.uniform(5, 15))
        ax.clear()
        ax.plot(datos_x,datos_y)
        ax.scatter(datos_x, datos_y, color='blue', marker='o', facecolors='blue', s=100)

        if len(datos_x1) >= 15:
            datos_x1.pop(0)
            datos_y1.pop(0)
        datos_x1.append(contador)
        datos_y1.append(random.uniform(5, 15))
        ax.plot(datos_x1, datos_y1, color='red')
        ax.scatter(datos_x1, datos_y1, color='red', marker='o', facecolors='red', s=100)

        ax.grid()
        page.update()

ft.app(target=main)