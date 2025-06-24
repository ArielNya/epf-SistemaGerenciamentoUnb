import os
from sqlalchemy import create_engine

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Configurações do servidor
    HOST = 'localhost'
    PORT = 8080
    DEBUG = True
    RELOADER = True

    # Paths
    #EMPLATE_PATH = os.path.join(BASE_DIR, 'views')
    #STATIC_PATH = os.path.join(BASE_DIR, 'static')
    #DATA_PATH = os.path.join(BASE_DIR, 'data')

    # Outras configurações
    #SECRET_KEY = 'sua-chave-secreta-aqui'

