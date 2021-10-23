from flask import Flask, render_template, url_for, request, redirect, session, g
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
        
        if passwordbd != []:
            if check_password_hash(passwordbd[0][0], password):
                session['loggedin'] = True
                session['id'] = query[0][3]
                session['email'] = query[0][7]
                print(query)
                #return redirect(url_for('user', info = query))
                return render_template('perfil.html', info = query)
        else:
            error = 'Usuario y/o contraseña inválida'
            query = db.consultarTabla("superadministradores", "IDsp = {}".format(n_id))
            if query != []:
                session['loggedin'] = True
                session['id'] = query[0][3]
                print(query[0][4])
                return redirect(url_for('dashboard'))
        return render_template('login.html', error=error)
        
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
            return render_template('perfil.html', info = query)
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
        email = request.form['email']
        phone_number = request.form['celular']
        password = request.form['pass']
        password2 = request.form['pass2']
        
        db.registrarP(name, t_id, n_id, birthday, email, phone_number, password)
        
        return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return render_template('login.html')

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
    #user_id = request.form['id']
    return render_template('perfil.html')

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    #user_id = request.form['id']
    return render_template('agendar.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)