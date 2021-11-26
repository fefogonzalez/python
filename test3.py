import os
import platform
import psutil #instalar previamente con -->  "pip install psutil"


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




def main():

    inventario = open('myfile.txt', 'r')
    lista_equipos = inventario.readlines()
 
    count = 0
    # Strips the newline character
    for equipo in lista_equipos:
        count += 1
        #MyServer 
        print(equipo.strip())

        HOST_UP  = True if os.system("ping -c 1 " + equipo.strip()) is 0 else False
        #print(HOST_UP)

        if (HOST_UP) :
            print(getListOfProcessActive())
            print(getHostInformation())
            print(getLoggedUsers())
        else:
            print("No hay conectividad con el target " + equipo.strip())


if __name__ == '__main__':
   main()