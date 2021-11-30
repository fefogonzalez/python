import os
import platform
import socket
from datetime import datetime

# Instalar el modulo previamente con --> "pip install paramiko"
import paramiko

#instalar previamente con --> pip install pymysql
import pymysql 


'''
Funcion que recibe como parametros algunos de los datos recolectados y los inserta en una base MySql
La base MySql se encuentra levantada en un hosting personal
'''
def EscribirBD (host, cpu, so, login, procesos):
    # FG: punto a mejorar 1
    conexion = pymysql.connect(
                                host='sql532.main-hosting.eu',
                                user='u561475971_dbadmin',
                                password='Pa$$w0rd',
                                db='u561475971_db_inventario',
                                port=3306
                            )

    cursor = conexion.cursor()

    now = datetime.now()
    sql = "INSERT INTO relevamiento (conexion, host, cpu, so, login, procesos) VALUES (%s,%s,%s,%s,%s,%s)"
    valores = (now, host, cpu, so, login, procesos)

    cursor.execute(sql,valores)
    conexion.commit()


'''
Funcion que recibe como parametros host/ip y puerto ssh para verificar si el cliente a relevar se encuentra disponible
La funcion, devuelve 1 (Disponible) o 0 (No disponible), dependiendo de si se puedo establecer la conexion
'''
def Verificar_disponibilidad(ip,port):
    socket.setdefaulttimeout(.5)

    DEVICE_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result_of_check = DEVICE_SOCKET.connect_ex((ip,port))

    if result_of_check == 0:
       Disponible = 1
       DEVICE_SOCKET.close()
    else:
       Disponible = 0
    
    return (Disponible)


'''
Funcion que recibe como parametros la informacion definida en el inventario
Mediante una conexion ssh, se envian comandos de Sistema Operativo para recibir informacion que luego sera guardada en la bbdd
En este caso, muestra por pantalla los procesos corriendo y guarda en la bbdd la cantidad de procesos corriendo
'''
def ObtenerProcesosActivos(host, port, usuario_ssh, password_ssh,ssh_cred):
    command  = "ps -eo pid,comm"             # Muestro solo las columnas pid y command
    command2 = "ps -eo pid,comm | wc -l"     # Cuento los procesos

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if (ssh_cred) :
        ssh.connect(host, port, usuario_ssh, password_ssh)
    else:
        ssh.connect(host, port, usuario_ssh)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()

    # FG: punto a mejorar 2
    print(lines)

    stdin, stdout, stderr = ssh.exec_command(command2)
    CantProc = stdout.readlines()

    return(CantProc)


'''
Funcion que recibe como parametros la informacion definida en el inventario
Mediante una conexion ssh, se envian comandos de Sistema Operativo para recibir informacion que luego sera guardada en la bbdd
En este caso, muestra por pantalla los procesos corriendo y guarda en la bbdd la cantidad de procesos corriendo
'''
def ObtenerUsuariosConectados(host, port, usuario_ssh, password_ssh,ssh_cred):
    command  = "who"             # Lista los usuarios conectods
    command2 = "who | wc -l"     # Cuenta los usuarios conectados

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if (ssh_cred) :
        ssh.connect(host, port, usuario_ssh, password_ssh)
    else:
        ssh.connect(host, port, usuario_ssh)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()

    # FG: punto a mejorar 3
    print(lines) # Muestra por pantalla los usuarios conectados

    #Se cuentan la cantidad de usuarios conectados y se guarda en la bbdd
    stdin, stdout, stderr = ssh.exec_command(command2)
    lines = stdout.readlines()

    return(lines)

'''
Funcion que recibe como parametros la informacion definida en el inventario
Mediante una conexion ssh, se envian comandos de Sistema Operativo para recibir informacion que luego sera guardada en la bbdd
En este caso, muestra por pantalla los procesos corriendo y guarda en la bbdd la cantidad de procesos corriendo
'''
def ObtenerInfoDelSistema(host, port, usuario_ssh, password_ssh,ssh_cred):
    command  = "uname -n" #Obtengo el hostname del equipo
    command2 = "cat /proc/cpuinfo  | grep -i 'model name' | uniq " # Obtengo el modelo de CPU
    #command3 = "hostnamectl | grep Opera*" # Obtengo el Sistema Operativo
    command3 = "uname -o" # Obtengo el Sistema Operativo

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if (ssh_cred) :
        ssh.connect(host, port, usuario_ssh, password_ssh)
    else:
        ssh.connect(host, port, usuario_ssh)

    stdin, stdout, stderr = ssh.exec_command(command)
    resultadohost = stdout.readlines()
    
    stdin, stdout, stderr = ssh.exec_command(command2)
    resultadoprocesador = stdout.readlines()
    # FG: punto a mejorar 4
    #resultadoprocesador = resultadoprocesador.replace("model name : ","")

    stdin, stdout, stderr = ssh.exec_command(command3)
    resultadoso = stdout.readlines()
    # FG: punto a mejorar 4
    #resultadoso = resultadoso.replace("Operating System: ","")

    #Muestro por pantalla la info obtenida
    print("El equipo: " + resultadohost[0] + " esta corriendo sobre un: " + resultadoso[0])
    print("El procesador es: "+resultadoprocesador[0])

    return(resultadohost,resultadoprocesador,resultadoso)

def main():

    input_file_name = 'inventario.csv'

    file_in = open(input_file_name)

    row = next(file_in) # Avanzo a la siguiente linea del inventario para descartar el encabezado del archivo

    equipos = []

    for line in file_in:
    
        line  = line.strip('\n')
        line = line.split(',')
    
        host = line[0]
        port = int(line[1])
        usuario_ssh = line[2]
        password_ssh = line[3]
        ssh_cred = line[4]
    
        Disponibilidad  = Verificar_disponibilidad(host,port)

        print("***** Inicio de recoleccion de datos para el equipo " + host + " *****")
        
        if (Disponibilidad) :
            login = ObtenerUsuariosConectados(host,port,usuario_ssh,password_ssh,ssh_cred)
            procesos = ObtenerProcesosActivos(host,port,usuario_ssh,password_ssh,ssh_cred)
            InfoSistema = ObtenerInfoDelSistema(host,port,usuario_ssh,password_ssh,ssh_cred)

            # Como resultado de llamar a la funcion ObtenerInfoDelSistema obtengo una lista con datos es necesario separarlos para guarda en la bbdd
            hostname = InfoSistema[0]
            cpu = InfoSistema[1]
            so = InfoSistema[2]

            # Envio la informacion recolectada a la bbdd
            EscribirBD (hostname, cpu, so, login, procesos)
        else:
            print("No hay conectividad con el target " + host)
                    
        print("***** Fin de recoleccion de datos para el equipo " + host + " *****")

    file_in.close()


if __name__ == '__main__':
   main()