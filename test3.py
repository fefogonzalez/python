import os
import platform
import psutil #instalar previamente con -->  "pip install psutil"
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

def getListOfProcessActive():
    print('*** Create a list of all running processes ***')
    listOfProcessNames = list()
    # Iterate over all running processes
    for proc in psutil.process_iter():
         try:
            # Get process detail as dictionary
            pInfoDict = proc.as_dict(attrs=['pid', 'name'])
            # Append dict of process detail in list
            listOfProcessNames.append(pInfoDict)
            # Iterate over the list of dictionary and print each elem
         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
             pass
    for elem in listOfProcessNames:
        print(elem)
    
    return ('')

def getHostInformation():
    print(f"El equipo {platform.node()} esta corriendo sobre un SO {platform.system()} version {platform.release()} ")
    print(f"La arquitectura del procesador es: {platform.processor()}")
    return (" ")
    #print(f"Informacion del procesador: {platform.processor()}")

def getLoggedUsers():
    user_list = psutil.users()
    #cantidad = user_list.count
    #print (cantidad)
    #print(f"En este momento hay XXX loggeados en el equipo" )
    for user in user_list:
        #username = user.name
        print(f"el usuario {user.name} se encuentra loggeado en la terminal {user.terminal} ")

    return ('')


def ObtenerProcesosActivos():
    host = "IP-ADDR"
    port = 22
    username = "USUARIO"
    password = "PASSWORD"

    command = "pwd"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    print(lines)

def ObtenerUsuariosConectados():
    host = "IP-ADDR"
    port = 22
    username = "USUARIO"
    password = "PASSWORD"

    command = "who"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    stdin, stdout, stderr = ssh.exec_command(command)
    lines = stdout.readlines()
    print(lines)



def main():

    inventario = open('myfile.txt', 'r')
    lista_equipos = inventario.readlines()
 
    count = 0
    for equipo in lista_equipos:
        count += 1

        Disponibilidad  = Verificar_disponibilidad(equipo.strip(),22)

        if (Disponibilidad) :
            #print(getListOfProcessActive())
            #print(getHostInformation())
            #print(getLoggedUsers())
            print(ObtenerProcesosActivos())
            print(ObtenerUsuariosConectados())
        else:
            print("No hay conectividad con el target " + equipo.strip())


if __name__ == '__main__':
   main()
