from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import LoginManager, login_user, logout_user, UserMixin
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Configuração inicial
engine = create_engine('sqlite:///site.db')
login_manager = LoginManager()

bp_auth = Blueprint('auth', __name__, template_folder='templates')

# Modelo básico de usuário para integração com Flask-Login
class User(UserMixin):
    def __init__(self, id, email, password=None):
        self.id = id
        self.email = email
        self.password = password  # Adicionando o campo de senha (opcional)

# Callback do Flask-Login para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    with Session(engine) as session:
        user_data = session.execute(text('SELECT id, email, password FROM user WHERE id = :id'), {'id': user_id}).fetchone()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2])
        return None

@bp_auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Inserção no banco de dados
        insert = text('INSERT INTO user (email, password) VALUES (:email, :senha)')
        with Session(engine) as session:
            session.execute(insert, {'email': email, 'senha': senha})
            session.commit()

        return redirect(url_for('auth.login'))  # Corrigindo o redirecionamento para a rota de login

    return render_template('auth/register.html')

@bp_auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Consulta ao banco de dados
        select = text('SELECT * FROM user WHERE email = :email AND password = :senha')
        with Session(engine) as session:
            result = session.execute(select, {'email': email, 'senha': senha}).fetchone()

        if result:  # Verifica se um usuário foi encontrado
            user = User(result[0], result[1], result[2])
            login_user(user)
            return redirect(url_for('tasks.registro'))  # Redireciona para a página de tarefas após o login
        else:
            return "Usuário ou senha incorretos!"  # Mensagem simples, pode ser aprimorada

    return render_template('auth/login.html')

@bp_auth.route('/logout')
def logout():
    logout_user()  # Finaliza a sessão do usuário
    return redirect(url_for('auth.login'))  # Redireciona para a página de login
