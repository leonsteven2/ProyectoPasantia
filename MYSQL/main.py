import pandas as pd
import pymysql
from credenciales import password

# Crea un DataFrame con algunos datos
df = pd.DataFrame({
    "nombre": ["Juan", "Pedro", "María"],
    "edad": [20, 25, 30]
})

# Configura la conexión a la base de datos
db = pymysql.connect(
    host="localhost",
    user="root",
    password=password,
    database="test",
)

# print(db)
#
# cursor = db.cursor()
# comando_sql = "insert into cliente (CI, NOMBRE, APELLIDO) value ('1105134132','HANS','LEON')"
# cursor.execute(comando_sql)
# db.commit()
# print("Insertado via normal")

# Crear un DataFrame de ejemplo
data = {
    'CI': [1, 2, 3, 4, 5],
    'NOMBRE': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'APELLIDO': ['AliceS', 'BobS', 'CharlieS', 'DavidS', 'EveS']
}
df = pd.DataFrame(data)
print(df)
df.to_sql('cliente', con=db, if_exists='replace', index=False)




