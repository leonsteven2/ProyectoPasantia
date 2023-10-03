list = ["1","2","3","4"]
comando_sql = "insert into rhpc values "
for i in range(0,len(list)):
    separator = "," if i<(len(list)-1) else ";"
    comando_sql = comando_sql + f"\n('{list[i]}','{list[i]}'){separator}"

print(comando_sql)