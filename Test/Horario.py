import pandas as pd

# Crear un diccionario con los datos del horario
horarios = {
    'Inicio': [
        '07:00',
        '08:00',
        '09:00',
        '10:00',
        '11:00',
        '12:00',
        '13:30',
        '14:30'
    ],
    'Final': [
            '08:00',
            '09:00',
            '10:00',
            '11:00',
            '12:00',
            '13:00',
            '14:30',
            '15:30'
        ],
}
horario_clases = pd.DataFrame(horarios)

dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']

# Agregamos los días al dataframe
for i in range(0, len(dias_semana)):
    horario_clases[dias_semana[i]] = ["-","-","-","-","-","-","-","-"]

# Agregar una materia
nombre_materia1 = "Mantenimiento"
hora_inicio_materia1 = "09:00"
hora_final_materia1 = "11:00"
nrc_materia1 = 14045
materia1 = {
    'Nombre': "Mant",
    'NRC': "14045",
    'NRC-LAB': None,
    'Teo 1': ["Martes", "09:00", "11:00"],
    'Teo 2': ["Jueves", "09:00", "11:00"]
}
materia2 = {
    'Nombre': "Prod",
    'NRC': "14367",
    'NRC-LAB': "15472",
    'Teo 1': ["Martes", "11:00", "13:00"],
    'Teo 2': ["Jueves", "11:00", "13:00"],
    'Lab': ["Martes", "13:30", "15:30"],
}

materia3 = {
    'Nombre': "Empr",
    'NRC': "16573",
    'NRC-LAB': None,
    'Teo 1': ["Lunes", "13:30", "15:30"],
    'Teo 2': ["Miercoles", "13:30", "15:30"],
}

materia4 = {
    'Nombre': "Rob",
    'NRC': "14374",
    'NRC-LAB': "15482",
    'Teo 1': ["Lunes", "11:00", "13:00"],
    'Teo 2': ["Miercoles", "11:00", "13:00"],
    'Lab': ["Miercoles", "09:00", "11:00"],
}

materias = [materia1, materia2, materia3, materia4]

contador = 0

while True:
    contador = contador + 1
    print(f"Intento: {contador}")
    for i in range(0,len(materias)):
        materia_actual = materias[i]
        for i in range(3, len(materia_actual)):
            horario_actual = list(materia_actual.keys())[i]
            for i in range(1, len(materia_actual[horario_actual])):
                # Si i=1 accedemos al string "Hora Inicio", Si i=2 accedemos al string "Hora Final"
                estado_horario = list(horarios.keys())[i - 1]
                # Accedemos al indice que contiene el horario de inicio y fin de la materia
                indice_hora = horario_clases.index[horario_clases[estado_horario] == materia_actual[horario_actual][i]]
                item = horario_clases.at[indice_hora[0], materia_actual[horario_actual][0]]
                if item == "-":
                    if horario_actual == "Lab":
                        nrc = materia_actual['NRC-LAB']
                    else:
                        nrc = materia_actual['NRC']
                    horario_clases.at[indice_hora[0], materia_actual[horario_actual][0]] = f"{materia_actual['Nombre']} / {nrc}" #materia_actual['Nombre']
                else:
                    print("No es posible crear el horario")
                    break

    break

print(horario_clases)
horario_clases.to_csv('horario.csv', index=False)




