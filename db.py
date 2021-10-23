from flask import session, flash
import sqlite3
from sqlite3 import Error
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import date

def conectar():
    try:
        conexion = sqlite3.connect('db/basedatos.db')
        return conexion
    except Error:
        print(Error)

def consultarTabla(nombre, condicion):
    conexion = conectar()
    cursor = conexion.cursor()
    
    if condicion is None:
        query = 'SELECT * FROM {}'.format(nombre)
    else:
        query = 'SELECT * FROM {} WHERE {}'.format(nombre, condicion)
    
    cursor.execute(query)
    
    datos = cursor.fetchall()
    conexion.close
    
    return datos

def consularColumna(columna, tabla, condicion):
    conexion = conectar()
    cursor = conexion.cursor()
    
    if condicion is None:
        query = 'SELECT {} FROM {}'.format(columna, tabla)
    else:
        query = 'SELECT {} FROM {} WHERE {}'.format(columna, tabla, condicion)
    
    cursor.execute(query)
    
    datos = cursor.fetchall()
    conexion.close
    
    return datos

def age(born):
    listxd2 = born.split("-")
    listxd = [[], [], []]
    listxd[0] = listxd2[2]
    listxd[1] = listxd2[1]
    listxd[2] = listxd2[0]

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

    
def registrarP(nombre, t_id, n_id, birthday, email, phone_number, passw):
    conexion = conectar()
    cursor = conexion.cursor()
    
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
    
    passhash = generate_password_hash(passw, method='pbkdf2:sha256', salt_length=8)
    
    edad = age(birthday)
    print(consultarTabla("pacientes", "IDp = {}".format(n_id)))
    if consultarTabla("pacientes", "IDp = {}".format(n_id)) == []:
        query = 'INSERT INTO pacientes (nombres, apellidos, tipoID, IDp, "password", edad, sexo, email) VALUES ("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}")'.format(nombres, apellidos, t_id, n_id, passhash, edad, "NA", email)
        cursor.execute(query)
        conexion.commit()
        session['id'] = query["IDp"]
        session['email'] = query["email"]
    else:
        print("error, cedula registrada")
    conexion.close()

""" def checkpass(id, password):
    passwordbd = consularColumna("password", "pacientes", "IDp = {}".format(id))
    if check_password_hash() """