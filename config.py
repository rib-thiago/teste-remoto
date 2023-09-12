import os

from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave_secreta_padrao'
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGO_URI', 'mongodb://localhost/meu_app')
    }
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    DEBUG = True
    SESSION_COOKIE_NAME = 'meu_app_session'
