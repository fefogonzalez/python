import os
import platform

#FG: verificar si es necesario importarla
#import psutil #instalar previamente con -->  "pip install psutil"

import paramiko #instalar previamente con --> pip install paramiko
import socket

def Verificar_disponibilidad(ip,port):
    #Ejemplo tomado de https://www.youtube.com/watch?v=HQR67_suo-E
    socket.setdefaulttimeout(.5)

    DEVICE_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result_of_check = DEVICE_SOCKET.connect_ex((ip,port))

    if result_of_check == 0:
       Disponible = 1
       DEVICE_SOCKET.close()
    else:
       Disponible = 0
    
    return (Disponible)

def getHostInformation():
    print(f"El equipo {platform.node()} esta corriendo sobre un SO {platform.system()} version {platform.release()} ")
    print(f"La arquitectura del procesador es: {platform.processor()}")
    return (" ")
    #print(f"Informacion del procesador: {platform.processor()}")


def ObtenerProcesosActivos(host, port, usuario_ssh, password_ssh):
    # Muestro solo las columnas pid y command
    command = "ps -eo pid,comm"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, usuario_ssh, password_ssh)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()

    #FG: Parsear la salida antes de mostrar
    #contar cantidad de procesos

    print(lines)

def ObtenerUsuariosConectados(host, port, usuario_ssh, password_ssh):
    command = "who"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, usuario_ssh, password_ssh)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
        
    #FG: parsear la salida antes de mostrarla, ya que muestra todos los usuarios en una misma linea
    
    print(lines)





def ObtenerInfoDelSistema(host, port, usuario_ssh, password_ssh):
    command = "uname -n"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, usuario_ssh, password_ssh)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    
    
    #FG: parsear la salida antes de mostrarla, ya que muestra todos los usuarios en una misma linea
    
    print(lines)


def main():

    input_file_name = 'inventario.csv'

    file_in = open(input_file_name)

    #Saltear encabezado
    row = next(file_in)

    equipos = []

    for line in file_in:
    
        line  = line.strip('\n')
        line = line.split(',')
    
        host = line[0]
        port = int(line[1])
        usuario_ssh = line[2]
        password_ssh = line[3]
    
        print('host:', host,'port:', port,'usuario:',usuario_ssh,'password:',password_ssh)
    
        Disponibilidad  = Verificar_disponibilidad(host,port)

        print("***** Inicio de la informacion obtenida para el equipo " + host + " *****")
        
        if (Disponibilidad) :
            #print(getHostInformation())
            print(ObtenerProcesosActivos(host,port,usuario_ssh,password_ssh))
            print(ObtenerInfoDelSistema(host,port,usuario_ssh,password_ssh))
            print(ObtenerUsuariosConectados(host,port,usuario_ssh,password_ssh))
        else:
            print("No hay conectividad con el target " + host)
                    
        print("***** Fin de la informacion obtenida para el equipo " + host + " *****")

    file_in.close()


if __name__ == '__main__':
   main()