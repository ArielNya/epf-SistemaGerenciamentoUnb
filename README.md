---
generator: Aspose.Words for Java 23.4.0;
---

**Sistema Acadêmico (Backend com Bottle, Frontend com React)**

Este projeto implementa um sistema acadêmico simples, composto por um
backend em Python usando o framework Bottle e um frontend em JavaScript
usando React.

**Estrutura do Projeto**

O projeto é dividido em duas partes principais, organizadas em
subdiretórios:

- **backend/**: Contém a aplicação Python (Bottle), responsável pela
  lógica de negócios, manipulação de dados e exposição da API REST.

- **frontend/**: Contém a aplicação React, que fornece a interface de
  usuário para interagir com o backend.

A estrutura de pastas na raiz do projeto deve ser a seguinte:

.  
├──run_app.py \<\-- Script para iniciar a aplicação completa  
├──frontend/ \<\-- Pasta da aplicação React  
│ ├──public/  
│ ├──src/  
│ ├──package.json  
│ └──\...  
└──backend/ \<\-- Pasta da aplicação Python (Bottle)  
├──app.py  
├──main.py  
├──controllers/  
├──data/  
├──models/  
├──services/  
└──views/

**Como Usar a Aplicação**

Siga os passos abaixo para configurar e executar a aplicação.

**1. Configuração do Backend (Python - Bottle)**

O backend é a espinha dorsal da aplicação, responsável por gerenciar os
dados dos alunos, disciplinas, turmas e notas/frequências.

**Pré-requisitos do Backend**

Certifique-se de ter o Python 3 instalado na sua máquina.

**Instalação das Dependências**

1.  **Navegue até a pasta do backend** (./backend) no seu terminal.  
    cd backend

2.  Instale as dependências Python necessárias. Para este projeto, o
    principal é o bottle:  
    pip install bottle  
    pip install bottle-cors \# Se estiver a usar o middleware CORS
    explicitamente  
      
    (Se houver outras bibliotecas como sqlite3 para o banco de dados,
    geralmente já vêm com Python ou não precisam de instalação via pip.)

**Inicialização do Banco de Dados**

O banco de dados (SQLite) será inicializado automaticamente na primeira
execução do main.py. Ele criará um ficheiro de banco de dados (.db)
dentro da pasta backend/data/.

**Executando o Backend Manualmente (Apenas para referência)**

Para executar apenas o backend, faria (após cd backend):

python main.py

O servidor Bottle será iniciado e ficará disponível em
http://localhost:8080.

**2. Configuração do Frontend (React)**

O frontend é a interface de utilizador que permite interagir com o
backend.

**Pré-requisitos do Frontend**

Certifique-se de ter o Node.js e o npm (ou Yarn) instalados na sua
máquina.

**Instalação das Dependências**

1.  **Navegue até a pasta do frontend** (./frontend) no seu terminal.  
    cd frontend

2.  Instale as dependências JavaScript:  
    npm install  
    \# ou  
    \# yarn install

**Executando o Frontend Manualmente (Apenas para referência)**

Para executar apenas o frontend, faria (após cd frontend):

npm start  
\# ou  
\# yarn start

O servidor de desenvolvimento React será iniciado, geralmente em
http://localhost:3000.

**3. Executando a Aplicação Completa (Recomendado)**

Para sua conveniência, criei um script Python (run_app.py) que inicia
ambos os servidores (backend e frontend) em paralelo.

1.  **Certifique-se de que todas as dependências foram instaladas** para
    o backend e o frontend (passos 1.2 e 2.2).

2.  **Navegue de volta para a raiz do seu projeto** (onde run_app.py
    está localizado).  
    \# Se estava em ./frontend ou ./backend, volte para a raiz do
    projeto  
    cd ..

3.  Execute o script:  
    python run_app.py

Este script irá:

- Iniciar o servidor Bottle em http://localhost:8080.

- Iniciar o servidor de desenvolvimento React (geralmente em
  http://localhost:3000).

Pode aceder à aplicação pelo seu navegador em http://localhost:3000.

**Para parar a aplicação**: Pressione Ctrl+C no terminal onde o
run_app.py está a ser executado. Ele irá encerrar ambos os servidores.

**Uso da API (Backend)**

O backend expõe uma API RESTful para gerenciar as entidades do sistema.
Pode interagir com esta API usando ferramentas como **curl** (linha de
comando) ou **Postman** (interface gráfica).

A URL base para todas as requisições da API é http://localhost:8080.

**Alunos**

- **POST /alunos - Adicionar um novo aluno**  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"nome\": \"João Silva\",  
  \"matricula\": 2023001,  
  \"curso\": \"Engenharia de Software\",  
  \"dataNascimento\": \"2000-01-15\"  
  }\' http://localhost:8080/alunos

- **GET /alunos - Listar todos os alunos**  
  curl http://localhost:8080/alunos

- **GET /alunos/\<matricula:int\> - Buscar um aluno por matrícula**  
  curl http://localhost:8080/alunos/2023001

- **DELETE /alunos/\<matricula:int\> - Eliminar um aluno por
  matrícula**  
  curl -X DELETE http://localhost:8080/alunos/2023001

- POST /alunos/concluir - Registar uma disciplina concluída por um
  aluno  
  (Note que o backend espera alunoId e codigoDiciplina aqui.
  Certifique-se de que o alunoId é a matrícula do aluno e o
  codigoDiciplina é o código da disciplina.)  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"alunoId\": 2023001,  
  \"codigoDiciplina\": 101  
  }\' http://localhost:8080/alunos/concluir

- **GET /alunos/\<matricula:int\>/concluidas - Listar disciplinas
  concluídas por um aluno**  
  curl http://localhost:8080/alunos/2023001/concluidas

- **DELETE /alunos/limpar - Limpar todos os alunos (CUIDADO!)**  
  curl -X DELETE http://localhost:8080/alunos/limpar

**Disciplinas**

- **POST /diciplinas - Adicionar uma nova disciplina**  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"nome\": \"Algoritmos e Estruturas de Dados\",  
  \"cargaHoraria\": 60,  
  \"descricao\": \"Estudo de algoritmos fundamentais e estruturas de
  dados.\"  
  }\' http://localhost:8080/diciplinas

- **GET /diciplinas - Listar todas as disciplinas**  
  curl http://localhost:8080/diciplinas

- **GET /diciplinas/\<codigo:int\> - Buscar uma disciplina por
  código**  
  curl http://localhost:8080/diciplinas/101 \# Use o código retornado na
  criação

- **DELETE /diciplinas/\<codigo:int\> - Eliminar uma disciplina por
  código**  
  curl -X DELETE http://localhost:8080/diciplinas/101

- POST /diciplinas/\<codigo:int\>/prerequisitos - Adicionar um
  pré-requisito a uma disciplina  
  (O codigo na URL é da disciplina que receberá o pré-requisito. No
  corpo, codigo é do pré-requisito.)  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"codigo\": 101  
  }\' http://localhost:8080/diciplinas/102/prerequisitos

- **GET /diciplinas/\<codigo:int\>/prerequisitos - Listar pré-requisitos
  de uma disciplina**  
  curl http://localhost:8080/diciplinas/102/prerequisitos

- **DELETE
  /diciplinas/\<diciplinaCodigo:int\>/prerequisitos/\<prereqCodigo:int\> -
  Remover um pré-requisito de uma disciplina**  
  curl -X DELETE http://localhost:8080/diciplinas/102/prerequisitos/101

- **GET /diciplinas/\<diciplinaCodigo:int\>/turmas - Listar turmas de
  uma disciplina**  
  curl http://localhost:8080/diciplinas/101/turmas

**Observação sobre Disciplinas:** Atualmente, o backend não possui um
endpoint PUT para atualizar disciplinas. Para modificar os dados de uma
disciplina existente, precisaria implementar um novo endpoint no
DiciplinaView.py e DiciplinaController.py.

**Turmas**

- **POST /turmas - Criar uma nova turma**  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"nome\": \"Turma A - AED\",  
  \"disciplinaId\": 101,  
  \"anoSemestre\": \"2023.2\",  
  \"horarioInicio\": \"08:00:00\",  
  \"horarioFim\": \"10:00:00\",  
  \"diasSemana\": \"Seg,Qua,Sex\",  
  \"sala\": \"B-201\",  
  \"capacidade\": 30  
  }\' http://localhost:8080/turmas

- **GET /turmas - Listar todas as turmas**  
  curl http://localhost:8080/turmas

- **GET /turmas/\<turmaId:int\> - Buscar uma turma por ID**  
  curl http://localhost:8080/turmas/1

- **PUT /turmas/\<turmaId:int\> - Atualizar os dados de uma turma**  
  curl -X PUT -H \"Content-Type: application/json\" -d \'{  
  \"nome\": \"Turma B - AED\",  
  \"disciplinaId\": 101,  
  \"anoSemestre\": \"2023.2\",  
  \"horarioInicio\": \"10:00:00\",  
  \"horarioFim\": \"12:00:00\",  
  \"diasSemana\": \"Ter,Qui\",  
  \"sala\": \"B-202\",  
  \"capacidade\": 25  
  }\' http://localhost:8080/turmas/1

- **DELETE /turmas/\<turmaId:int\> - Eliminar uma turma**  
  curl -X DELETE http://localhost:8080/turmas/1

- **POST /turmas/\<turmaId:int\>/matricular - Matricular um aluno numa
  turma**  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"alunoId\": 2023001  
  }\' http://localhost:8080/turmas/1/matricular

- **POST /turmas/\<turmaId:int\>/desmatricular - Desmatricular um aluno
  de uma turma**  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"alunoId\": 2023001  
  }\' http://localhost:8080/turmas/1/desmatricular

- **GET /turmas/\<turmaId:int\>/alunos - Listar alunos matriculados numa
  turma**  
  curl http://localhost:8080/turmas/1/alunos

- **GET /turmas/\<alunoId:int\>/turmas - Listar turmas de um aluno**  
  curl http://localhost:8080/turmas/2023001/turmas

**Notas e Frequências**

- **POST /notas-frequencias - Atribuir nota e frequência a um aluno numa
  turma**  
  curl -X POST -H \"Content-Type: application/json\" -d \'{  
  \"alunoId\": 2023001,  
  \"turmaId\": 1,  
  \"nota\": 8.5,  
  \"frequencia\": 0.90  
  }\' http://localhost:8080/notas-frequencias

- **GET /notas-frequencias/\<alunoId:int\>/turmaId:int - Buscar nota e
  frequência de um aluno numa turma específica**  
  curl http://localhost:8080/notas-frequencias/2023001/1

- **GET /alunos/\<alunoId:int\>/notas-frequencias - Listar notas e
  frequências de um aluno em todas as turmas**  
  curl http://localhost:8080/alunos/2023001/notas-frequencias

- **GET /turmas/\<turmaId:int\>/notas-frequencias - Listar notas e
  frequências de todos os alunos numa turma específica**  
  curl http://localhost:8080/turmas/1/notas-frequencias

**Usando Postman (ou ferramentas similares)**

Para quem prefere uma interface gráfica, o **Postman** (ou Insomnia,
Thunder Client para VS Code) é altamente recomendado.

1.  **Importe coleções**: Pode criar uma nova coleção e adicionar
    requisições HTTP (GET, POST, PUT, DELETE) para cada um dos endpoints
    listados acima.

2.  **Defina Headers**: Para requisições POST e PUT que enviam dados
    JSON, certifique-se de definir o header Content-Type como
    application/json.

3.  **Corpo da Requisição**: Para POST e PUT, selecione a opção raw e o
    tipo JSON para inserir os dados no formato JSON.
