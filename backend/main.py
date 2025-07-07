# main.py
# Este é o ponto de entrada principal para executar o servidor web.

import os
from bottle import run

# Importa o objeto 'app' totalmente configurado do nosso arquivo app.py.
# Este objeto contém todas as rotas e configurações mescladas.
from app import app

# Importa a função de inicialização do banco de dados.
from data.database import initDb

# É uma boa prática executar o servidor em uma porta definida por uma variável de ambiente,
# com um padrão razoável se não estiver definida. Isso é útil para deploy.
# Por exemplo, você pode executar `PORT=8000 python main.py` no seu terminal.
port = int(os.environ.get('PORT', 8080))

# O bloco `if __name__ == '__main__':` garante que o código dentro dele
# só seja executado quando este script é chamado diretamente (ex: `python main.py`).
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

    # A função run() inicia o servidor web de desenvolvimento embutido do Bottle.
    #
    # - app: O objeto de aplicação Bottle a ser executado.
    # - host: '0.0.0.0' torna o servidor acessível de qualquer máquina na
    #         rede, não apenas 'localhost'.
    # - port: O número da porta em que o servidor irá escutar.
    # - debug: Quando True, fornece páginas de erro detalhadas, o que é muito útil
    #          durante o desenvolvimento.
    # - reloader: Quando True, o servidor reiniciará automaticamente sempre que você
    #             salvar uma alteração em um arquivo do projeto. Isso evita
    #             ter que parar e iniciar o servidor manualmente.
    print("--------------------------------------------------")
    print(f"Iniciando o servidor de desenvolvimento Bottle...")
    print(f"Servidor rodando em http://0.0.0.0:{port}")
    print(f"Acesse pelo seu navegador em http://localhost:{port}")
    print("Pressione Ctrl+C para parar o servidor.")
    print("--------------------------------------------------")

    run(app, host='localhost', port=port, debug=True, reloader=True)
