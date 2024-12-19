from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Configuração inicial
engine = create_engine('sqlite:///site.db')

bp_task = Blueprint('task', __name__, template_folder='templates')

@bp_task.route('/add', methods=['GET', 'POST'])
@login_required  # Garante que o usuário esteja logado
def add_task():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        user_id = current_user.id  # Obtém o ID do usuário logado

        # Inserção no banco de dados com o user_id
        insert = text('INSERT INTO task (titulo, descricao, user_id) VALUES (:titulo, :descricao, :user_id)')
        with Session(engine) as session:
            session.execute(insert, {'titulo': titulo, 'descricao': descricao, 'user_id': user_id})
            session.commit()

        return redirect(url_for('task.list_tasks'))  # Redireciona para a lista de tarefas (ou outra página)

    return render_template('add_task.html')

@bp_task.route('/tasks')
@login_required
def list_tasks():
    with Session(engine) as session:
        # Seleciona todas as tarefas vinculadas ao usuário atual
        query = text('SELECT id, titulo, descricao FROM task WHERE user_id = :user_id')
        tasks = session.execute(query, {'user_id': current_user.id}).fetchall()
    return render_template('task_list.html', tasks=tasks)