# main.py
# Este é o ponto de entrada principal para executar o servidor web.

import os
# Certifique-se de que response, request e abort estão importados aqui
from bottle import run, response, request, abort
import json # Certifique-se de que json está importado aqui

# Importa o objeto 'app' totalmente configurado do nosso arquivo app.py.
# Este objeto contém todas as rotas e configurações mescladas.
from app import app

# Importa a função de inicialização do banco de dados.
from data.database import initDb

# É uma boa prática executar o servidor em uma porta definida por uma variável de ambiente,
# com um padrão razoável se não estiver definida. Isso é útil para deploy.
port = int(os.environ.get('PORT', 8080))



if __name__ == '__main__':
    print("--------------------------------------------------")
    print("Iniciando a configuração do servidor...")

    # Garante que o diretório para o banco de dados SQLite exista.
    if not os.path.exists('./data'):
        print("Diretório './data' não encontrado. Criando...")
        os.makedirs('./data')

    # Inicializa o banco de dados, criando as tabelas se elas não existirem.
    print("Inicializando o banco de dados (initDb)...")
    initDb()
    print("Banco de dados pronto.")

    # --- APLICA O MIDDLEWARE CORS AO SEU APLICATIVO BOTTLE PRINCIPAL ---
    # Esta é a LINHA CHAVE: envolve o seu objeto 'app' com a função de middleware CORS.


    print("--------------------------------------------------")
    print(f"Iniciando o servidor de desenvolvimento Bottle...")
    print(f"Servidor rodando em http://0.0.0.0:{port}")
    print(f"Acesse pelo seu navegador em http://localhost:{port}")
    print("Pressione Ctrl+C para parar o servidor.")
    print("--------------------------------------------------")

    # Agora, execute o aplicativo ENVOLVIDO pelo middleware CORS.
    run(app=app, host='0.0.0.0', port=port, debug=True, reloader=True)