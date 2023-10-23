import pandas as pd
table_name = "lab_humedad"

df = pd.read_csv("datosPrueba.csv")

datos_mysql_thunder = [
    'fecha', 'hora',
    'rh_pc_sp', 'rh_pc', 'unit_rh_pc',
    'rh_pctc_sp', 'rh_pctc', 'unit_pctc',
    'satur_pressure_sp', 'satur_pressure', 'unit_satur_pressure',
    'chmbr_pressure', 'unit_chmbr_pressure',
    'satur_temp_sp', 'satur_temp', 'unit_satur_temp',
    'chmbr_temp', 'unit_chmbr_temp',
    'flow_sp', 'flow', 'unit_flow',
    'id_equipo'
]

comando_mysql_inicio = f"INSERT INTO {table_name}\n("
for dato in datos_mysql_thunder:
    comando_mysql_inicio += dato + ","
comando_mysql_inicio = comando_mysql_inicio[:-1] + ")\n"

comando_mysql_final = f"VALUES\n"
for i in range(0, len(df)):
    comando_mysql_final = comando_mysql_final + "("
    for dato in datos_mysql_thunder:
        comando_mysql_final += f"'{df[dato].iloc[i]}'" + ","
    comando_mysql_final = comando_mysql_final[:-1] + ""
    comando_mysql_final += "),\n"

comando_mysql_final = comando_mysql_final[:-2] + ";"

comando = comando_mysql_inicio + comando_mysql_final

print(comando)



