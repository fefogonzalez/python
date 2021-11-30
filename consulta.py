import pymysql #instalar previamente con --> pip install pymysql, agregar al dockerfile


print("Ingrese el hostname a buscar")
hostname = input()
#validar que se haya ingresado algo

#FG: Punto a mejorar 5
hostname = hostname+'%'

#FG: Punto a mejorar
conexion = pymysql.connect(
                                host='SERVIDOR_BBDD',
                                user='USER_DB',
                                password='PASSWORD_DB',
                                db='MY_DB',
                                port=3306
                            )

cursor = conexion.cursor()

query = "SELECT conexion, host, cpu, so, login, procesos FROM u561475971_db_inventario.relevamiento WHERE host like %s order BY conexion DESC LIMIT 1"
    
cursor.execute(query,hostname)

for registro in cursor:
    
    linea = list(registro)
        # conexion = linea[0]
    host = linea[1]
    cpu = linea[2]
    so = linea[3]
    login = linea[4]
    procesos = linea[5]
    print(linea)

cursor.close()
conexion.close()
