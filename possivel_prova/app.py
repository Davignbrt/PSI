from flask import Flask, render_template
from auth.auth import bp_auth
from tasks.tasks import bp_task  # Certifique-se de importar o blueprint de tasks corretamente

app = Flask(__name__)

# Configuração da chave secreta para sessões
app.config['SECRET_KEY'] = 'secreto'

# Registrando os Blueprints
app.register_blueprint(bp_auth, url_prefix='/auth')  # Corrigido: Passando o objeto do blueprint
app.register_blueprint(bp_task, url_prefix='/task')  # Corrigido: Passando o objeto do blueprint

# Rota inicial
@app.route('/')
def index():
    return render_template('index.html')  # Corrigido: Agora retorna o template
