# app/db.py

from bson.objectid import ObjectId
from flask import current_app, g
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash


def get_db():
    """
    Obtém uma conexão com o banco de dados MongoDB configurada no contexto do aplicativo Flask.

    Parameters:
        Nenhum

    Returns:
        pymongo.database.Database: Uma instância de banco de dados MongoDB.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost:27017/'}
        >>> with app.app_context():
        ...     db = get_db()
        ...     assert db is not None
    """
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGODB_SETTINGS']['host'])
        g.db = client.get_database('Cluster0')
    return g.db


def close_db(e=None):
    """
    Fecha a conexão com o banco de dados MongoDB configurada no contexto do aplicativo Flask.

    Parameters:
        Nenhum.

    Returns:
        Nenhum.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost:27017/'}
        >>> with app.app_context():
        ...     db = get_db()
        ...     close_db()
        ...     assert 'db' not in g
    """
    db = g.pop('db', None)
    if db is not None:
        db.client.close()


def init_db():
    """
    Inicializa o banco de dados MongoDB no contexto do aplicativo Flask, criando uma coleção de usuários se ela não existir.

    Parameters:
        Nenhum.

    Returns:
        Nenhum.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost:27017/'}
        >>> with app.app_context():
        ...     init_db()
        ...     db = get_db()
        ...     assert 'users' not in db.list_collection_names()
    """

    # Adicione suas operações de inicialização do banco de dados aqui
    db = get_db()

    # Crie uma coleção de usuários se ela não existir
    if 'users' not in db.list_collection_names():
        db.create_collection('users')
        users_collection = db['users']

        # Adicione um usuário de exemplo (substitua por seus próprios usuários)
        user_data = {
            'username': 'exemplo',
            'password': 'senha_de_exemplo',
        }
        users_collection.insert_one(user_data)


def find_user(username):
    """
    Encontra um usuário pelo nome de usuário no banco de dados.

    Parameters:
        username (str): O nome de usuário a ser pesquisado.

    Returns:
        dict: Um dicionário representando o usuário encontrado ou None se o usuário não existir.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost:27017/'}
        >>> with app.app_context():
        ...     init_db()
        ...     user = find_user('Tales')
        ...     assert user is not None
    """
    db = get_db()
    users_collection = db['users']
    return users_collection.find_one({'username': username})


def find_password(password):
    """
    Encontra um usuário pelo senha no banco de dados.

    Parameters:
        password (str): A senha do usuário a ser pesquisada.

    Returns:
        dict: Um dicionário representando o usuário encontrado ou None se o usuário não existir.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost:27017/'}
        >>> with app.app_context():
        ...     init_db()
        ...     user = find_password('senha_de_exemplo')
        ...     assert user is not None
    """
    db = get_db()
    users_collection = db['users']
    return users_collection.find_one({'password': password})


def create_user(username, password):
    """
    Cria um novo usuário no banco de dados com o nome de usuário e senha fornecidos.

    Parameters:
        username (str): O nome de usuário do novo usuário.
        password (str): A senha do novo usuário.

    Returns:
        bool: True se o usuário foi criado com sucesso, False se o usuário com o mesmo nome de usuário já existir.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost:27017/'}
        >>> with app.app_context():
        ...     init_db()
        ...     result = create_user('dsfds', 'nova_seddnha')
        ...     assert result is True
        >>> with app.app_context():
        ...     init_db()
        ...     created = create_user('Tales', 'senha_de_exemplo')
        ...     assert created is False
    """
    db = get_db()
    users_collection = db['users']
    if find_user(username) is None:
        users_collection.insert_one(
            {'username': username, 'password': password}
        )
        return True
    return False


def verify_user(username, password):
    """
    Verifica as credenciais de um usuário no banco de dados.

    Parameters:
        username (str): O nome de usuário a ser verificado.
        password (str): A senha a ser verificada.

    Returns:
        dict or None: Um dicionário representando o usuário se as credenciais estiverem corretas, None se as credenciais estiverem incorretas ou o usuário não existir.

    Examples:
        >>> from flask import Flask
        >>> app = Flask(__name__)
        >>> app.config['MONGODB_SETTINGS'] = {'host': 'mongodb://localhost:27017/'}
        >>> with app.app_context():
        ...     init_db()
        ...     result = verify_user('exemplo', 'senha_de_exemplo')
        ...     assert result is not None
        ...     result = verify_user('exemplo', 'senha_incorreta')
        ...     assert result is None
        ...     result = verify_user('usuario_inexistente', 'senha_qualquer')
        ...     assert result is None
    """
    user = find_user(username)
    pswd = find_password(password)
    if user and pswd:
        return user, pswd
    return None
