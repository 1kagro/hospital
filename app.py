from flask import Flask, render_template, url_for, request, redirect, session, g, flash
from werkzeug.security import check_password_hash, generate_password_hash

import db

app = Flask(__name__)

# settings
app.secret_key = 'mykey'

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        n_id = int(request.form['id'])
        password = request.form['password']
        
        passwordbd = db.consularColumna("password", "pacientes", "IDp = {}".format(n_id))
        query = db.consultarTabla("pacientes", "IDp = {}".format(n_id))
        
        error = 'Usuario y/o contraseña inválida'
        
        if query != []:
            if passwordbd != []:
                if check_password_hash(passwordbd[0][0], password):
                    session['loggedin'] = True
                    session['id'] = query[0][3]
                    session['email'] = query[0][7]
                    print(query)
                    query2 = db.consultarTabla("medicos", "IDp = {}".format(n_id))
                    print(query2)
                    dato = db.consultarTabla("citas", "paciente = {} ".format(n_id))
                    especialidad = db.consultarTabla("medicos", None)
                    print(":", dato)
                    print("::", especialidad)
                    #return redirect(url_for('user', info = query))
                    return render_template('perfil.html', info = query, info2 = query2, datos = dato, esp = especialidad)
                else:
                    flash(error)
        else:
            query = db.consultarTabla("superadministradores", "IDsp = {}".format(n_id))
            
            if query != []:
                passwordbd = query[0][4]
                if passwordbd != []:
                    if check_password_hash(passwordbd, password):
                        session['loggedin'] = True
                        session['id'] = query[0][3]
                        print(query[0][4])
                        return render_template('dashboard.html', info = query)
                    else:
                        flash(error)
            else:
                query = db.consultarTabla("medicos", "IDm = {}".format(n_id))
                if query != []:
                    passwordbd = query[0][4]
                    if check_password_hash(passwordbd, password):
                        session['loggedin'] = True
                        session['id'] = query[0][3]
                        print(query[0][4])
                        print("MEDICO INCIÓ SESIÓN")
                        #return render_template('medicos.html', info = query)
                    else:
                        flash(error)
                else:
                    flash('El usuario no existe')

        return render_template('login.html')
         
        """ if((n_id == 12345678) and (password == "Usuario1")):
            return redirect(url_for('user'))
        elif((n_id == 99999999) and (password == "Administrador1")):
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html') """
    else:
        if 'loggedin' in session:
            n_id = session['id']
            query = db.consultarTabla("pacientes", "IDp = {}".format(n_id))
            query2 = db.consultarTabla("medicos", "IDm = {}".format(n_id))
            query3 = db.consultarTabla("superadministradores", "IDsp = {}".format(n_id))
            
            if query != []:
                query2 = db.consultarTabla("medicos", "IDp = {}".format(n_id))
                return render_template('perfil.html', info = query, info2 = query2)
            elif query2 != []:
                return render_template('perfil.html', info = query)
            else:
                return render_template('dashboard.html', info = query3)
                
        return render_template('login.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if(request.method == "GET"):
        return render_template('register.html')

    else:
        name = request.form['name']
        t_id = request.form['tipo-id']
        n_id = request.form['n-id']
        birthday = request.form['birthday']
        genero = request.form['genero']
        email = request.form['email']
        phone_number = request.form['celular']
        password = request.form['pass']
        password2 = request.form['pass2']
        
        db.registrarP(name, t_id, n_id, birthday, email, phone_number, password, genero)
        
        return render_template('login.html')

@app.route('/register_M', methods=['GET', 'POST'])
def registerM():
    if(request.method == "GET"):
        return render_template('registerM.html')

    else:
        error = ""
        name = request.form['name']
        t_id = request.form['tipo-id']
        n_id = request.form['n-id']
        birthday = request.form['birthday']
        genero = request.form['genero']
        email = request.form['email']
        phone_number = request.form['celular']
        password = request.form['pass']
        password2 = request.form['pass2']
        especialidad = request.form['especialidad']
        db.registrarM(name, t_id, n_id, password, especialidad, birthday, email, genero, phone_number, error)
        
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect( url_for('home'))

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = db.consultarTabla("paciente", "IDp = {}".format(user_id))

def login_requered(view):
    @functools.wraps(view)
    def wrappend_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))


@app.route('/usuario', methods=['GET', 'POST'])
def user():
    n_id = session['id']
    query = db.consultarTabla("pacientes", "IDp = {}".format(n_id))
    dato = db.consultarTabla("citas", "paciente = {} ".format(n_id))
    especialidad = db.consultarTabla("medicos", None)
    #user_id = request.form['id']
    return render_template('perfil.html',info=query, datos = dato, esp = especialidad)

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if "loggedin" in session:
        n_id = session['id']
        print(n_id)
        query = db.consultarTabla("pacientes", "IDp = '{}'".format(n_id))
        query2 = ""
        if request.method == "POST":
            
            esp = request.form.get("tipo-cita")
            
            if esp != "":
                query2 = db.consultarTabla("medicos", "especialidad = '{}'".format(str(esp)))
                print(query2)
            
            print(query)
            if query != []:
                nombre = request.form.get('medico')
                date = request.form.get("datetime-local")
                if nombre != None:
                    print(nombre)
                    db.agendarCita(nombre, esp, date, n_id)
                return render_template('agendar.html', info = query, medicos = query2)
        else:
            return render_template('agendar.html', info = query)
    return render_template('login.html')

    #user_id = request.form['id']
    #return render_template('agendar.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "loggedin" in session:
        n_id = session['id']
        query3 = db.consultarTabla("superadministradores", "IDsp = {}".format(n_id))
        if query3 != []:
            return render_template('dashboard.html', info = query3)
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)