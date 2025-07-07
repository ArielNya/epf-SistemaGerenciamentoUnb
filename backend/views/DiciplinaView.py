from bottle import request, response, Bottle
from controllers.DiciplinaController import DiciplinaController
import json

class DiciplinaView:
    def __init__(self, diciplinaController: DiciplinaController):
        self.diciplinaController = diciplinaController
        self.app = Bottle()
        self.setupRoutes()

    def setupRoutes(self):
        self.app.route('/diciplinas', method='POST', callback=self.criarDiciplina)
        self.app.route('/diciplinas', method='GET', callback=self.listarDiciplinas)
        self.app.route('/diciplinas/<codigo:int>', method='GET', callback=self.buscarDiciplina)
        self.app.route('/diciplinas/<codigo:int>/prerequisitos', method='POST', callback=self.addPrereq)
        self.app.route('/diciplinas/<codigo:int>/prerequisitos', method='GET', callback=self.listarPrereq)
        self.app.route('/diciplinas/<codigo:int>', method='DELETE', callback=self.deleteDiciplina)
        self.app.route('/diciplinas/<diciplinaCodigo:int>/prerequisitos/<prereqCodigo:int>', method='DELETE', callback=self.deletePrereq)
        self.app.route('/diciplinas/<diciplinaCodigo:int>/turmas', method='GET', callback=self.listarTurmas)

    def _getJsonData(self):
        response.content_type = 'application/json'
        data = request.json
        if data is None or not isinstance(data, dict):
            response.status = 400
            return None, json.dumps({'message': 'Corpo da requisição invalido'})
        return data, None
    
    def criarDiciplina(self):
        data, errorResponse = self._getJsonData()
        if errorResponse:
            return errorResponse
        try:
            nome = data.get('nome')
            codigo = data.get('codigo')
            carga = data.get('carga')
            prereq = data.get('prereq')

            if not all([nome, codigo, carga is not None]):
                response.status = 400
                return json.dumps({'message': 'Dados incompletos'})
            if not isinstance(prereq, list) and prereq is not None:
                response.status = 400
                return json.dumps({'message': 'prequisitos deve ser uma lista de codigos'})
            
            diciplina = self.diciplinaController.criarDiciplina(nome, codigo, carga, prereq)
            if diciplina:
                response.status = 201
                return json.dumps({
                    'id': diciplina.id,
                    'nome': diciplina.nome,
                    'codigo': diciplina.codigo,
                    'carga': diciplina.carga,
                    'prereq': [p.codigo for p in diciplina.prereq] if diciplina.prereq else []
                })
            else:
                response.status = 409
                return json.dumps({'message': f'Não foi possivel criar a diciplina'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': 'Erro interno no servidor {e}'})
        
    def listarDiciplinas(self):
        response.content_type = 'application/json'
        try:
            diciplinas = self.diciplinaController.listarDiciplina()
            diciplinasJson = []
            for diciplinaObj in diciplinas:
                diciplinasJson.append({
                    'id': diciplinaObj.id,
                    'nome': diciplinaObj.nome,
                    'codigo': diciplinaObj.codigo,
                    'carga': diciplinaObj.carga,
                    'prerequisitos': [p.codigo for p in diciplinaObj.prereq] if diciplinaObj.prereq else []
                })

            return json.dumps(diciplinasJson)
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def buscarDiciplina(self, codigo):
        response.content_type = 'application/json'
        try:
            diciplina = self.diciplinaController.buscarDiciplinaPorCodigo(codigo)
            if diciplina:
                return json.dumps({
                    'id': diciplina.id,
                    'nome': diciplina.nome,
                    'codigo': diciplina.codigo,
                    'carga': diciplina.carga,
                    'prerequisitos': [p.codigo for p in diciplina.prereq] if diciplina.prereq else []
                })
            else:
                response.status = 404
                return json.dumps({'message': f'Diciplina com codigo {codigo} não foi encontrada'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def addPrereq(self, codigo):
        data, errorResponse = self._getJsonData()
        if errorResponse:
            return errorResponse
        try:
            prereqCodigo = data.get('prereqCodigo')
            if not prereqCodigo:
                response.status = '400'
                return json.dumps({'message': 'Dados incompletos'})
            prereqAdicionado = self.diciplinaController.addPrereq(codigo, prereqCodigo)
            if prereqAdicionado:
                response.status = 200
                return json.dumps({
                    'id': prereqAdicionado.id,
                    'codigoPrerequisito': prereqAdicionado.codigo,
                    'disciplinaId': prereqAdicionado.disciplinaId
                })
            else:
                response.status = 400
                return json.dumps({'message': f'Não foi possivel adicionar o prerequisito {prereqCodigo} a diciplina {codigo}'})
        except Exception as e:
                        # --- NOVAS LINHAS PARA DEBUG ---
            print(f"DEBUG: Uma exceção ocorreu em DiciplinaView.addPrereq: {type(e).__name__}")
            print(f"DEBUG: Detalhes da exceção: {e}")
            # Opcional: para ver o traceback completo
            # import traceback
            # traceback.print_exc(file=sys.stdout)
            # --- FIM DAS NOVAS LINHAS PARA DEBUG ---
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    
    def listarPrereq(self, codigo):
        response.content_type = 'application/json'
        try:

            prereq = self.diciplinaController.listarPrereq(codigo)
            # --- NOVOS PRINTS AQUI ---
            print(f"DEBUG_VIEW: Chamando controller.listarPrereq para codigo={codigo}")
            print(f"DEBUG_VIEW: Resultado do controller.listarPrereq: {prereq}")
            print(f"DEBUG_VIEW: Tipo do resultado do controller: {type(prereq)}")
            # --- FIM DOS NOVOS PRINTS ---
            if prereq == None: 
                response.status = 404
                return json.dumps({'message': f'diciplina {codigo} não foi encontrada'})
            if prereq == []:
                response.status = 201
                return json.dumps({'message': f'diciplina {codigo} não possui prerequisitos'})
            prereqJson = []
            for prereqObj in prereq:
                prereqJson.append({
                    'id': prereqObj.id,
                    'codigo': prereqObj.codigo,
                    'nome': prereqObj.nome,
                    'carga': prereqObj.carga
                })
            return json.dumps(prereqJson)
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        

    def deleteDiciplina(self, codigo):
        response.content_type = 'application/json'
        try:
            if self.diciplinaController.deleteDiciplina(codigo):
                response.status = 200
                return json.dumps({'message': f'Diciplina com codigo {codigo} foi deletada com sucesso'})
            else:
                response.status = 404
                return json.dumps({'message': f'Erro, Diciplina {codigo} não foi encontrada'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servvidos {e}'})
    
    def deletePrereq(self, diciplinaCodigo, prereqCodigo):
        response.content_type = 'application/json'
        try:
            if self.diciplinaController.deletarPrereq(diciplinaCodigo, prereqCodigo):
                response.status = 200
                return json.dumps({'message': f'Prerequisito com codigo {prereqCodigo} foi excuido com sucesso'})
            else:
                response.status = 404
                return json.dumps({'message': f'Prerequisito {prereqCodigo} para a diciplina {diciplinaCodigo} não foi encontrado'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    def listarTurmas(self, diciplinaCodigo):
        response.content_type = 'application/json'
        try:
            turmas = self.diciplinaController.listarTurmasDiciplina(diciplinaCodigo)
            if turmas is None:
                response.status = 404
                return json.dumps({'message': f'Erro: Não foi encontrada diciplina {diciplinaCodigo}'})
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
            return json.dumps({'message': f'Erro interno do servidor: {e}'})
        
        