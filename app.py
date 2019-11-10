import csv

from flask import Flask, request, render_template, redirect, url_for, Response, session

from flask_login import UserMixin, login_required, logout_user, login_user, LoginManager
from LoginForm import LoginForm

app = Flask(__name__)

app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_key!'
)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):

    def __init__(self, *args):
        self.id = args[0]
        self.username = args[1]
        self.password = args[2]

    def get(id):
        # Abrimos el CSV.
        with open('files/usuarios.csv') as csv_file:
            # Obtenemos todos los usuarios
            users = csv.reader(csv_file, delimiter=',')

            # Recorremos los usuarios
            for user in users:
                # Si el usuario es igual al username lo retornamos.
                if user[0] == id:
                    return User(*user)

    def get_by_username(username):
        # Abrimos el CSV.
        with open('files/usuarios.csv') as csv_file:
            # Obtenemos todos los usuarios
            users = csv.reader(csv_file, delimiter=',')

            # Recorremos los usuarios
            for user in users:
                # Si el usuario es igual al username lo retornamos.
                if user[1] == username:
                    return User(*user)


    def create(self):
        pass

    def save(self):
        pass


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
@login_required
def home():
    user_id = session['user_id']
    user = User.get(user_id)
    return render_template('home.html', user=user)
    return Response("Hola {}!".format(user.username))


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_by_username(username)
        if user and user.password == password:
            login_user(user)
        else:
            return Response('Usuario o password incorrectos.')
        return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')