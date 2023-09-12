from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from pymongo import MongoClient
from redis import Redis

from config import Config

from .db import create_user, find_user, verify_user


# Criar uma função para criar a instância da aplicação
def create_app(config_class=Config):
    app = Flask(__name__)

    # Configurar as configurações globais da aplicação
    app.config.from_object(config_class)

    # Configurar conexão com o Redis para armazenamento em cache
    redis = Redis.from_url(app.config['REDIS_URL'])

    # Configurar conexão com o MongoDB usando as informações do arquivo de configuração
    client = MongoClient(app.config['MONGODB_SETTINGS']['host'])

    # Selecionar o banco de dados padrão (no caso, 'Cluster0')
    db = client.get_default_database('Cluster0')

    # Rotas da aplicação e outras lógicas de negócio

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/test-redis')
    def test_redis():
        try:
            # Testar conexão com o Redis
            redis.ping()
            flash('Conexão com o Redis bem-sucedida!', 'success')
        except Exception as e:
            error_message = f'Erro na conexão com o Redis: {str(e)}'
            flash(error_message, 'danger')
        return redirect(url_for('index'))

    @app.route('/test-mongodb')
    def test_mongodb():
        try:
            # Testar conexão com o MongoDB
            collections = db.list_collection_names()
            flash('Conexão com o MongoDB bem-sucedida!', 'success')
        except Exception as e:
            error_message = f'Erro na conexão com o MongoDB: {str(e)}'
            flash(error_message, 'danger')
        return redirect(url_for('index'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Implemente a função de verificação de login (verifique se o usuário e a senha correspondem)
            if verify_user(username, password):
                flash('Login bem-sucedido!', 'success')

                # Armazene o nome do usuário na sessão para rastrear a autenticação
                session['username'] = username

                return redirect(url_for('user_profile', username=username))
            else:
                flash('Credenciais inválidas. Tente novamente.', 'danger')

        return render_template('login.html')

    @app.route('/logout')
    def logout():
        # Remova o nome do usuário da sessão para fazer logout
        session.pop('username', None)
        flash('Logout bem-sucedido!', 'success')
        return redirect(url_for('index'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if not username or not password:
                flash('Por favor, preencha todos os campos.', 'danger')
            elif create_user(username, password):
                flash('Cadastro realizado com sucesso!', 'success')
                return redirect(url_for('index'))
            else:
                flash(
                    'Usuário já existe. Escolha um nome de usuário diferente.',
                    'danger',
                )
        return render_template('register.html')

    @app.route('/user/<username>')
    def user_profile(username):
        # Implemente a função para buscar os detalhes do usuário no banco de dados
        user_data = find_user(username)
        if user_data:
            return render_template('user_profile.html', user=user_data)
        else:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('login'))

    return app
