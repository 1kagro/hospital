from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date
password = "1234"
passhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

print(passhash)
print(check_password_hash("pbkdf2:sha256:260000$O8jZFkhF$9d11deed81fecf44e89021a995a44f859463528819f779d2e0b5815a3a0694b4", "hola"))



""" nombre = "Fabian"
nombre_v = nombre.split(" ")
if len(nombre_v) == 4:
    nombres = nombre_v[0] + " " + nombre_v[1]
    apellidos = nombre_v[2] + " " +nombre_v[3]
elif len(nombre_v) == 3:
    nombres = nombre_v[0]
    apellidos = nombre_v[1] + " " +nombre_v[2]
elif len(nombre_v) == 2:
    nombres = nombre_v[0]
    apellidos = nombre_v[1]
else:
    nombres = nombre_v[0]
    apellidos = ""
print(len(nombre_v))
print("Nombres: " + nombres, "apellidos: " + apellidos)

def age(born):
    listxd2 = born.split("-")
    listxd = [[], [], []]
    listxd[0] = listxd2[2]
    listxd[1] = listxd2[1]
    listxd[2] = listxd2[0]
    print(listxd)
    listTemp = []
    
    listTemp.append([date.today().day, date.today().month, date.today().year])
    
    if int(listxd[1]) < listTemp[0][1]:
        return listTemp[0][2] - int(listxd[2])
    elif(int(listxd[1]) == listTemp[0][1]):
        if(int(listxd[0]) <= listTemp[0][0]): 
            return listTemp[0][2] - int(listxd[2])
        elif(int(listxd[0]) > listTemp[0][0]): 
            return listTemp[0][2] - int(listxd[2])-1
    elif(int(listxd[1]) > listTemp[0][1]): 
        return listTemp[0][2] - int(listxd[2])-1

print(age("2002-05-04")) """