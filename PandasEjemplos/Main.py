import pandas as pd

# Crear un DataFrame vacío
df = pd.DataFrame(columns=['Nombre', 'Edad'])

# Agregar datos al DataFrame
df.loc[0] = ['Juan', 25]
df.loc[1] = ['María', 30]
df.loc[2] = ['Pedro', 22]

longitud = df.shape[0]
print(df)