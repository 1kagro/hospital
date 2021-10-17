from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
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
        return render_template('register.html')

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