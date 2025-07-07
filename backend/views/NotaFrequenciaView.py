from bottle import Bottle, response, request
from controllers.NotaFrequenciaController import NotaFrequenciaController
import json

class NotaFrequenciaView:
    def __init__(self, notaFrequenciaController: NotaFrequenciaController):
        self.app = Bottle()
        self.notaFrequenciaController = notaFrequenciaController
        self.setupRoutes()

    def setupRoutes(self):
        self.app.route('/notas-frequencias', method='POST', callback=self.atribuir)
        self.app.route('/notas-frequencias/<alunoId:int>/turmaId:int', method='GET', callback=self.buscarNotaFrequencia)
        self.app.route('/alunos/<alunoId:int>/notas-frequencias', method='GET', callback=self.listarNotasFrequenciaAluno)
        self.app.route('/turmas/<turmaId:int>/notas-frequencias', method='GET', callback=self.listarNotasFrequenciaTurma)
    
    def _getJsonData(self):
        response.content_type = 'application/json'
        data = request.json
        if data is None or not isinstance(data, dict):
            response.status = 400
            return None, json.dumps({'message': 'Corpo da requisição invalido'})
        return data, None
    

    def atribuir(self):
        data, errorResponse = self._getJsonData()
        if errorResponse:
            return errorResponse
        try:
            alunoId = data.get('alunoId')
            turmaId = data.get('turmaId')
            nota = data.get('nota')
            frequencia = data.get('frequencia')

            if not all([alunoId, turmaId]):
                response.status = 400
                return json.dumps({'message': 'Dados incompletos: alunoId e turmaId são obrigatórios'})

            if nota is not None and not isinstance(nota, (int, float)):
                response.status = 400
                return json.dumps({'message': 'Nota deve ser um numero'})
            if frequencia is not None and not isinstance(frequencia, (int, float)):
                response.status = 400
                return json.dumps({'message': 'Frequencia deve ser um numero'})
            
            nf = self.notaFrequenciaController.atribuirNotaFrequencia(alunoId, turmaId, nota, frequencia)
            if nf:
                response.status = 200
                return json.dumps({
                    "id": nf.id,
                    "alunoId": nf.alunoId,
                    "turmaId": nf.turmaId,
                    "nota": nf.nota,
                    "frequencia": nf.frequencia
                })
            else:
                response.status = 400
                return json.dumps({'message': 'Não foi possível atribuir nota/frequência. Verifique os IDs ou se o aluno está matriculado na turma'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def buscarNotaFrequencia(self, alunoId, turmaId):
        response.content_type = 'application/json'
        try:
            nf = self.notaFrequenciaController.buscarNotaFrequencia(alunoId, turmaId)
            if nf:
                response.status = 200
                return json.dumps({
                    "id": nf.id,
                    "alunoId": nf.alunoId,
                    "turmaId": nf.turmaId,
                    "nota": nf.nota,
                    "frequencia": nf.frequencia
                })
            else:
                response.status = 404
                return json.dumps({'message':'Não foi possivel encontrar aluno e/ou turma'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def listarNotasFrequenciaAluno(self, alunoId):
        response.content_type = 'application/json'
        try:
            nfs = self.notaFrequenciaController.listarNotasFrequenciaAluno(alunoId)
            nfsJson = []
            for nf in nfs:
                nfsJson.append({
                    "id": nf.id,
                    "alunoId": nf.alunoId,
                    "turmaId": nf.turmaId,
                    "nota": nf.nota,
                    "frequencia": nf.frequencia                    
                })

            return json.dumps(nfsJson)
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def listarNotasFrequenciaTurma(self, turmaId):
        response.content_type = 'application/json'
        try:
            nfs = self.notaFrequenciaController.listarNotasFrequenciaTurma(turmaId)
            nfsJson = []
            for nf in nfs:
                nfsJson.append({
                    "id": nf.id,
                    "alunoId": nf.alunoId,
                    "turmaId": nf.turmaId,
                    "nota": nf.nota,
                    "frequencia": nf.frequencia
                })
            return json.dumps(nfsJson)
        except Exception as e:
            response.status = 500
            return json.dumps({"message": f"Erro interno do servidor: {e}"})
    