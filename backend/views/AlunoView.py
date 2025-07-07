from bottle import Bottle, request, response, abort, HTTPResponse
from controllers.AlunoController import AlunoController
from data.database import getDb
import json
from datetime import date

class AlunoView:
    def __init__(self, alunoController: AlunoController):
        self.alunoController = alunoController
        self.app = Bottle()
        self.setupRoutes()

    def setupRoutes(self):
        self.app.route('/alunos', method='POST', callback=self.adicionarAluno)
        self.app.route('/alunos/<matricula:int>', method='GET', callback=self.buscarAlunoMatricula)
        self.app.route('/alunos/<matricula:int>', method='DELETE', callback=self.deleteAluno)
        self.app.route('/alunos', method='GET', callback=self.listarAlunos)
        self.app.route('/alunos/concluir', method='POST', callback=self.concluirDiciplina)
        self.app.route('/alunos/<matricula:int>/concluidas', method='GET', callback=self.listarConcluidas)
        self.app.route('/alunos/limpar', method='DELETE', callback=self.limparLista)

    def _getJson(self):
        response.content_type = 'application/json'
        # --- NOVAS LINHAS PARA DEBUG ---
        print("DEBUG: Entrando em _getJson()")
        print(f"DEBUG: Headers da Requisição: {request.headers}")
        print(f"DEBUG: Content-Type recebido: {request.headers.get('Content-Type')}")
        
        try:
            # Tenta ler o corpo bruto da requisição
            raw_body = request.body.read().decode('utf-8')
            print(f"DEBUG: Corpo bruto da requisição: '{raw_body}'")
            # Reseta o ponteiro do corpo para que request.json possa lê-lo
            request.body.seek(0) 
        except Exception as e:
            raw_body = f"Erro ao ler corpo bruto: {e}"
            print(f"DEBUG: {raw_body}")

        data = request.json
        print(f"DEBUG: Valor de request.json: {data}")
        print(f"DEBUG: Tipo de request.json: {type(data)}")
        if data is None or not isinstance(data, dict):
            response.status = 400
            return None, json.dumps({'message': 'Corpo da requisição invalido'})
        
        return data, None
    
    def adicionarAluno(self):
        data, errorResponse = self._getJson()
        if errorResponse:
            return errorResponse
        
        try:
            nome = data.get('nome')
            matricula = data.get('matricula')
            curso = data.get('curso')
            dataNascimentoStr = data.get('dataNascimento')

            if not all([nome, matricula, curso, dataNascimentoStr]):
                response.status = 400
                return json.dumps({'message': 'Dados incompletos'})
            
            try:
                dataNascimento = date.fromisoformat(dataNascimentoStr)
            except ValueError:
                response.status = 400
                return json.dumps({'message': 'Formato de data invalido'})
            aluno = self.alunoController.addAluno(nome, matricula, curso, dataNascimento)
            if aluno:
                response.status = 201
                return json.dumps({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'matricula': aluno.matricula,
                    'curso': aluno.curso,
                    'dataNascimento': aluno.dataNascimento.isoformat()
                })
            else:
                response.status = 409
                return json.dumps({'message': f'Erro: Não foi possivel adicionar aluno com matricula {matricula}. Verifique se o aluno já está matricula'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def buscarAlunoMatricula(self, matricula):
        response.content_type = 'application/json'
        try:
            aluno = self.alunoController.buscarAlunoMatricula(matricula)
            if aluno:
                return json.dumps({
                    'id': aluno.id,
                    'nome': aluno.nome,
                    'matricula': aluno.matricula,
                    'curso': aluno.curso,
                    'dataNascimento': aluno.dataNascimento.isoformat()
                })
            else:
                response.status = 404
                return json.dumps({'message': f'Erro: aluno com matricula {matricula} não foi encontrado'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
    
    def deleteAluno(self, matricula):
        response.content_type = 'application/json'
        try:
            if self.alunoController.deleteAluno(matricula):
                response.status = 200
                return json.dumps({'message': f'Aluno com matricula {matricula} deletado com sucesso'})
            else:
                response.status = 404
                return json.dumps({'message': f'Aluno com matricula {matricula} não foi encontrado'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def listarAlunos(self):
        response.content_type = 'application/json'
        try:
            alunos = self.alunoController.listarAlunos()
            alunosJson = []
            for alunoObj in alunos:
                data_nascimento_formatada = None
                if alunoObj.dataNascimento:
                    try:
                        data_nascimento_formatada = alunoObj.dataNascimento.isoformat()
                    except AttributeError:
                        print(f"DEBUG: dataNascimento do aluno {alunoObj.matricula} não é um objeto de data válido.")
                        # Trate o erro, talvez defina como None ou uma string vazia
                        data_nascimento_formatada = None # ou ''

                alunosJson.append({
                    'id': alunoObj.id,
                    'nome': alunoObj.nome,
                    'matricula': alunoObj.matricula,
                    'curso': alunoObj.curso,
                    'dataNascimento': data_nascimento_formatada
                })
            return json.dumps(alunosJson)
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {type(e).__name__}'})
        
    def concluirDiciplina(self):
        data, errorResponse = self._getJson()
        if errorResponse:
            return errorResponse
        
        try:
            codigoDiciplina = data.get('codigoDiciplina')
            matriculaAluno = data.get('matriculaAluno')
            if not all([codigoDiciplina, matriculaAluno]):
                response.status = 400
                return json.dumps({'message': 'Dados incompletos'})
            
            concluida = self.alunoController.concluirDiciplina(codigoDiciplina, matriculaAluno)
            if concluida:
                response.status = 200
                return json.dumps({
                    'id': concluida.id,
                    'codigoDiciplina': concluida.codigo,
                    'alunoId': concluida.alunoId
                })
            else:
                response.status = 400
                return json.dumps({'message', 'Não foi possivel concluir diciplina, verifique o código e a matricula'})

        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def listarConcluidas(self, matricula):
        response.content_type = 'application/json'
        try:
            concluidas = self.alunoController.listarDiciplinasConcluidas(matricula)
            if concluidas is None:
                response.status = 404
                return json.dumps({'message': f'Aluno com matricula {matricula} não foi encontrado'})
            concluidasJson = []
            for concluida in concluidas:
                concluidasJson.append({
                    'id': concluida.id,
                    'codigoDiciplina': concluida.codigo,
                    'alunoId': concluida.alunoId
                })
            return json.dumps(concluidasJson)
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def limparLista(self):
        response.content_type = 'application/json'
        try:
            if self.alunoController.limparListaDeAlunos():
                response.status = 200
                return json.dumps({'message': 'Todos os alunos foram excluidos da lista'})
            else:
                response.status = 500
                return json.dumps({'message': 'Não foi possivel limpar a lista'})
            
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno no servidor {e}'})