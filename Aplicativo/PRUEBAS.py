import csv

# Datos que quieres guardar en el archivo CSV
datos = [
    ["Nombre", "Edad", "Ciudad"],
    ["Juan", 25, "Madrid"],
    ["María", 30, "Barcelona"],
    ["Carlos", 22, "Valencia"],
]

# Nombre del archivo CSV en el que quieres guardar los datos
nombre_archivo = "datos.csv"

# Abre el archivo CSV en modo de escritura
with open(nombre_archivo, mode="w", newline="") as archivo_csv:
    # Crea un objeto escritor de CSV
    escritor_csv = csv.writer(archivo_csv)

    # Escribe los datos en el archivo CSV
    for fila in datos:
        escritor_csv.writerow(fila)

print(f"Los datos se han guardado en {nombre_archivo}")