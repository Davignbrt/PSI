from flask import Flask, request, render_template, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = 'superdificil'

# Configurando o Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Classe base do usuário
class User(UserMixin):
    def __init__(self, id, nome, email, password_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.password_hash = password_hash

# Conexão com o banco de dados
def get_conexao():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Adiciona o usuário ao banco
def add_user(nome, email, senha):
    password_hash = generate_password_hash(senha)
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (nome, email, password_hash) VALUES (?, ?, ?)', (nome, email, password_hash))
    conn.commit()
    conn.close()

# Função para encontrar um usuário pelo e-mail
def find_user_by_email(email):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    return user

# Função para encontrar um usuário pelo ID
def find_user_by_id(user_id):
    conn = get_conexao()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# Função usada pelo Flask-Login para carregar o usuário a partir do ID
@login_manager.user_loader
def load_user(user_id):
    user = find_user_by_id(user_id)
    if user:
        return User(id=user['id'], nome=user['nome'], email=user['email'], password_hash=user['password_hash'])
    return None

# Página base
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dash():
    return render_template('dashboard.html', nome=current_user.nome)

# Rota de login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form['email']
        senha = request.form['senha']

        user = find_user_by_email(email)
        if user and check_password_hash(user['password_hash'], senha):
            user_obj = User(id=user['id'], nome=user['nome'], email=user['email'], password_hash=user['password_hash'])
            login_user(user_obj)
            return redirect(url_for('dash'))
        else:
            flash('E-mail ou senha incorretos.')
            return redirect(url_for('login'))

# Rota de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        if find_user_by_email(email):
            flash('O e-mail já está registrado.')
            return redirect(url_for('register'))

        add_user(nome, email, senha)
        return redirect(url_for('login'))

# Rota de logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
