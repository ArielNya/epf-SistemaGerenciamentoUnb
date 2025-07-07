from bottle import Bottle, response, request
from controllers.TurmaController import TurmaController
from datetime import time
import json

class TurmaView:
    def __init__(self, turmaController: TurmaController):
        self.turmaController = turmaController
        self.app = Bottle()
        self.setupRoutes()


    def setupRoutes(self):
        self.app.route('/turmas', method='POST', callback=self.criarTurma)
        self.app.route('/turmas', method='GET', callback=self.listarTurmas)
        self.app.route('/turmas/<turmaId:int>', method='GET', callback=self.buscarId)
        self.app.route('/turmas/<turmaId:int>', method='PUT', callback=self.atualizarTurma)
        self.app.route('/turmas/<turmaId:int>', method='DELETE', callback=self.deleteTurma)
        self.app.route('/turmas/<turmaId:int>/matricular', method='POST', callback=self.matricularAluno)
        self.app.route('/turmas/<turmaId:int>/desmatricular', method='POST', callback=self.desmatricularAluno)
        self.app.route('/turmas/<turmaId:int>/alunos', method='GET', callback=self.listarAlunos)
        self.app.route('/turmas/<alunoId:int>/turmas', method='GET', callback=self.listarTurmasAluno)

    def _getJson(self):
        response.content_type = 'application/json'
        data = request.json
        if data is None or not isinstance(data, dict):
            response.status = 400
            return None, json.dumps({'message': 'Corpo da requisição invalido'})
        return data, None
    
    def criarTurma(self):
        data, errorResponse = self._getJson()
        if errorResponse: 
            return errorResponse
        
        try:
            nome = data.get('nome')
            disciplinaId = data.get('disciplinaId')
            anoSemestre = data.get('anoSemestre')
            horarioInicioStr = data.get('horarioInicio')
            horarioFimStr = data.get('horarioFim')
            diasSemana = data.get('diasSemana')
            sala = data.get('sala')
            capacidade = data.get('capacidade')

            if not all([nome, diasSemana, disciplinaId, anoSemestre, horarioFimStr, horarioInicioStr, sala, capacidade is not None]):
                response.status = 400
                return json.dumps({'message', 'Dados incompletos'})
            
            try:
                horarioInicio = time.fromisoformat(horarioInicioStr)
                horarioFim = time.fromisoformat(horarioFimStr)
            except ValueError:
                response.status = 400
                return json.dumps({'message': 'Formato de data invallido, use HH:MM:SS'})
            turma = self.turmaController.criarTurma(
                nome=nome,
                disciplinaId=disciplinaId,
                anoSemestre=anoSemestre,
                horarioInicio=horarioInicio,
                horarioFim=horarioFim,
                diasSemana=diasSemana,
                sala=sala,
                capacidade=capacidade
            )
            if turma:
                response.status = 201
                return json.dumps({
                    "id": turma.id,
                    "nome": turma.nome,
                    "disciplinaId": turma.diciplinaId,
                    "anoSemestre": turma.anoSemestre,
                    "horarioInicio": turma.horarioInicio.isoformat(),
                    "horarioFim": turma.horarioFim.isoformat(),
                    "diasSemana": turma.diasSemana,
                    "sala": turma.sala,
                    "capacidade": turma.capacidade
                })
            else:
                response.status = 400
                return json.dumps({'message': 'Não foi possivel criar a turma, verifique os dados fornecidos'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def listarTurmas(self):
        response.content_type = 'application/json'
        try:
            turmas = self.turmaController.listarTurmas()
            turmasJson = []
            for turma in turmas:
                turmasJson.append({
                    "id": turma.id,
                    "nome": turma.nome,
                    "disciplinaId": turma.diciplinaId,
                    "anoSemestre": turma.anoSemestre,
                    "horarioInicio": turma.horarioInicio.isoformat(),
                    "horarioFim": turma.horarioFim.isoformat(),
                    "diasSemana": turma.diasSemana,
                    "sala": turma.sala,
                    "capacidade": turma.capacidade
                })
            return json.dumps(turmasJson)
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor'})
        
    def buscarId(self, turmaId):
        response.content_type = 'application/json'
        try:
            turma = self.turmaController.buscarTurmaId(turmaId)
            if turma:
                return json.dumps({
                    "nome": turma.nome,
                    "disciplinaId": turma.diciplinaId,
                    "anoSemestre": turma.anoSemestre,
                    "horarioInicio": turma.horarioInicio.isoformat(),
                    "horarioFim": turma.horarioFim.isoformat(),
                    "diasSemana": turma.diasSemana,
                    "sala": turma.sala,
                    "capacidade": turma.capacidade
                })
            else:
                response.status = 404
                return json.dumps({'message': f'Erro: turma com id {turmaId} não foi encontrada'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def atualizarTurma(self, turmaId):
        dadosAtualizar, errorResponse = self._getJson()
        if errorResponse: return errorResponse

        try:
            if 'horarioInicio' in dadosAtualizar:
                try:
                    dadosAtualizar['horarioInicio'] = time.fromisoformat(dadosAtualizar['horarioInicio'])
                except ValueError:
                    response.status = 400
                    return json.dumps({'message': 'Erro: Formato de horarioInicio invalido, use HH:MM:SS'})
                
            if 'horarioFim' in dadosAtualizar:
                try:
                    dadosAtualizar['horarioFim'] = time.fromisoformat(dadosAtualizar['horarioFim'])
                except ValueError:
                    response.status = 400
                    return json.dumps({'message': 'Erro: Formato de horarioFim invalido, use HH:MM:SS'})
            turmaAtualizada = self.turmaController.atualizarTurma(turmaId, dadosAtualizar)
            if turmaAtualizada:
                response.status = 200
                return json.dumps({
                    "id": turmaAtualizada.id,
                    "nome": turmaAtualizada.nome,
                    "disciplinaId": turmaAtualizada.diciplinaId,
                    "anoSemestre": turmaAtualizada.anoSemestre,
                    "horarioInicio": turmaAtualizada.horarioInicio.isoformat(),
                    "horarioFim": turmaAtualizada.horarioFim.isoformat(),
                    "diasSemana": turmaAtualizada.diasSemana,
                    "sala": turmaAtualizada.sala,
                    "capacidade": turmaAtualizada.capacidade
                })
            else:
                response.status = 400
                return json.dumps({'message': f'Não foi possivel atualizar a turma {turmaId}'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def deleteTurma(self, turmaId):
        try:
            if self.turmaController.deletarTurma(turmaId):
                response.status = 200
                return json.dumps({'message': 'turma deletada com sucesso'})
            else:
                response.status = 404
                return json.dumps({'message': f'Erro: turma com id {turmaId} não foi encontrada'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def desmatricularAluno(self, turmaId):
            data, errorResponse = self._getJson()
            if errorResponse: return errorResponse


            try:
                alunoId = data.get('alunoId')
                if not alunoId:
                    response.status = 400
                    return json.dumps({'message': 'Erro: Dados incompletos, alunoId é obrigatório'})
                if self.turmaController.desmatricularAluno(alunoId, turmaId):
                    response.status = 200
                    return json.dumps({'message': f'Aluno {alunoId} foi desmatriculado com sucesso'})
                else:
                    response.status = 404
                    return json.dumps({'message': f'Matricula do aluno {alunoId} não foi encontrada'})
            except Exception as e:
                response.status = 500
                return json.dumps({'message': f'Erro interno do servidor {e}'})
            
    def matricularAluno(self, turmaId):
        data, errorResponse = self._getJson()
        if errorResponse: return errorResponse

        try:
            alunoId = data.get('alunoId')
            if not alunoId:
                response.status = 400
                return json.dumps({'message': 'Dados incompletos, alunoId é obrigatório'})
            
            matricula = self.turmaController.matricularAlunoTurma(alunoId, turmaId)
            if matricula:
                response.status = 200
                return json.dumps({
                    'alunoId': matricula.alunoId,
                    'turmaId': matricula.turmaId
                })
            else:
                response.status = 400
                return json.dumps({'message': f'Não foi possivel matricular aluno {alunoId} na turma {turmaId}'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})


    def listarAlunos(self, turmaId):
        response.content_type = 'application/json'
        try:
            alunos = self.turmaController.listarAlunosMatriculadosTurma(turmaId)
            if alunos is None:
                response.status = 404
                return json.dumps({'message': f'Turma com id {turmaId} não foi encontrada'})
            alunosJson = []
            for alunoObj in alunos:
                alunosJson.append({
                    "id": alunoObj.id,
                    "nome": alunoObj.nome,
                    "matricula": alunoObj.matricula,
                    "curso": alunoObj.curso,
                    "dataNascimento": alunoObj.dataNascimento.isoformat()
                })
            return json.dumps(alunosJson)
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def listarTurmasAluno(self, alunoId):
        response.content_type = 'application/json'
        try:
            turmas = self.turmaController.listarTurmasDoAluno(alunoId)
            if turmas is None:
                response.status = 404
                return json.dumps({'message': f'Aluno com id {alunoId} não foi encontrado'})
            turmasJson = []
            for turma in turmas:
                turmasJson.append({
                    "id": turma.id,
                    "nome": turma.nome,
                    "disciplinaId": turma.diciplinaId,
                    "anoSemestre": turma.anoSemestre,
                    "horarioInicio": turma.horarioInicio.isoformat(),
                    "horarioFim": turma.horarioFim.isoformat(),
                    "diasSemana": turma.diasSemana,
                    "sala": turma.sala,
                    "capacidade": turma.capacidade
                })
            return json.dumps(turmasJson)
        except Exception as e:
            response.stauts = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
