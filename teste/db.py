# app/db.py

from bson.objectid import ObjectId
from flask import current_app, g
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash


def get_db():
    if 'db' not in g:
        client = MongoClient(current_app.config['MONGODB_SETTINGS']['host'])
        g.db = client.get_database('Cluster0')
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.client.close()


def init_db():
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
    db = get_db()
    users_collection = db['users']
    return users_collection.find_one({'username': username})


def find_password(password):
    db = get_db()
    users_collection = db['users']
    return users_collection.find_one({'password': password})


def create_user(username, password):
    db = get_db()
    users_collection = db['users']
    if find_user(username) is None:
        users_collection.insert_one(
            {'username': username, 'password': password}
        )
        return True
    return False


def verify_user(username, password):
    user = find_user(username)
    pswd = find_password(password)
    if user and pswd:
        return user, pswd
    return None
