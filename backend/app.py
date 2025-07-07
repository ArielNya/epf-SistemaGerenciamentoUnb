# app.py
# Este arquivo é responsável por configurar a aplicação, inicializando
# e conectando todos os diferentes componentes (Views, Controllers, Services, Database).

import os
from bottle import Bottle, response, request, abort, hook, HTTPResponse

# --- Estrutura de Projeto Assumida ---
# Assume-se que a estrutura do seu projeto é a seguinte:
# /
# |- app.py (Este arquivo)
# |- main.py
# |- controllers/
# |  - AlunoController.py
# |  - ...
# |- services/
# |  - AlunoService.py
# |  - ...
# |- views/
# |  - AlunoView.py
# |  - ...
# |- data/
# |  - database.py
# |- models/
# |  - AlunoModel.py
# |  - ...

# --- Importando Componentes da Aplicação ---

# Import Views: Lidam com as requisições e respostas HTTP.
from views.AlunoView import AlunoView
from views.DiciplinaView import DiciplinaView
from views.NotaFrequenciaView import NotaFrequenciaView
from views.TurmasView import TurmaView

# Import Controllers: Contêm a lógica principal da aplicação.
from controllers.AlunoController import AlunoController
from controllers.DiciplinaController import DiciplinaController
from controllers.NotaFrequenciaController import NotaFrequenciaController
from controllers.TurmaController import TurmaController

# Import Services: Lidam com a lógica de negócios e interações com o banco.
# NOTA: A implementação real desses arquivos de serviço deve existir no diretório 'services'.
from services.AlunoService import AlunoService
from services.DiciplinaService import DiciplinaService
from services.NotaFrequenciaService import NotaFrequenciaService
from services.TurmaService import TurmaService

# Importa o sessionmaker do SQLAlchemy do seu arquivo de banco de dados.
from data.database import session as Session


# --- Injeção de Dependência e Configuração da Aplicação ---

# 1. Cria o objeto principal da aplicação
# Esta instância 'app' será a aplicação central do Bottle.
app = Bottle()
cors_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    # 'Access-Control-Allow-Headers': 'X-Token, ...',
    # 'Access-Control-Expose-Headers': 'X-My-Custom-Header, ...',
    # 'Access-Control-Max-Age': '86400',
    # 'Access-Control-Allow-Credentials': 'true',
}

@hook('after_request')
def handle_options():
    if request.method == 'OPTIONS':
        # Bypass request routing and immediately return a response
        raise HTTPResponse(headers=cors_headers)

@hook('after_request')
def enable_cors():
    for key, value in cors_headers.items():
       response.set_header(key, value)
# 2. Prepara a Sessão do Banco de Dados
print("Configurando a sessão do banco de dados...")
try:
    # Cria uma instância da sessão do banco de dados que será passada para os serviços.
    # Esta sessão será usada durante o ciclo de vida da aplicação.
    db_session = Session()
    print("Sessão do banco de dados pronta.")
except Exception as e:
    print(f"FATAL: Não foi possível criar a sessão do banco de dados: {e}")
    # A aplicação não pode rodar sem uma sessão de banco de dados.
    exit(1)

# 3. Inicializa os Serviços
# Os serviços são instanciados com a sessão do banco de dados, permitindo que eles façam queries.
print("Inicializando os serviços...")
try:
    aluno_service = AlunoService(db_session)
    diciplina_service = DiciplinaService(db_session)
    nota_frequencia_service = NotaFrequenciaService(db_session)
    turma_service = TurmaService(db_session)
    print("Serviços inicializados com sucesso.")
except NameError as e:
    print(f"FATAL: Erro ao inicializar os serviços. Verifique se todos os arquivos de serviço existem: {e}")
    exit(1)
except Exception as e:
    print(f"FATAL: Ocorreu um erro inesperado ao inicializar os serviços: {e}")
    exit(1)


# 4. Inicializa os Controllers
# Os controllers são instanciados com os serviços dos quais dependem.
print("Inicializando os controllers...")
aluno_controller = AlunoController(aluno_service)
diciplina_controller = DiciplinaController(diciplina_service)
nota_frequencia_controller = NotaFrequenciaController(nota_frequencia_service)
turma_controller = TurmaController(turma_service)
print("Controllers inicializados com sucesso.")


# 5. Inicializa as Views
# As views são instanciadas com os controllers dos quais dependem.
# IMPORTANTE: Um erro de digitação foi detectado em 'AlunoView.py'. O método `setupRouetes`
# deve ser renomeado para `setupRoutes` para que as rotas de aluno funcionem corretamente.
print("Inicializando as views...")
aluno_view = AlunoView(aluno_controller)
diciplina_view = DiciplinaView(diciplina_controller)
nota_frequencia_view = NotaFrequenciaView(nota_frequencia_controller)
turma_view = TurmaView(turma_controller)
print("Views inicializadas com sucesso.")


# 6. Mescla as Rotas
# Cada classe de view cria sua própria mini-aplicação ('sub-app') com suas próprias rotas.
# Nós mesclamos as rotas de cada uma dessas sub-apps em nosso objeto 'app' principal.
print("Mesclando as rotas...")
app.merge(aluno_view.app)
app.merge(diciplina_view.app)
app.merge(nota_frequencia_view.app)
app.merge(turma_view.app)
print("Rotas mescladas com sucesso.")
print("Configuração da aplicação concluída.")

# O objeto 'app' agora está totalmente configurado e pronto para ser executado por um servidor.
