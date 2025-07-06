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
        self.app.route('/diciplinas/<diciplinaCodigo:int>/prerequisitos/<prereqCodigo:int>', method='DELETE', callback=self.deleteDiciplina)
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
            prereq = data.get('prerequisitos')

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
                    'prerequisitos': [p.codigo for p in diciplina.prereq] if diciplina.prereq else []
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
            for _, diciplinaObj in diciplinas:
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
            prereqCodigo = data.get('prerequisitoCodigo')
            if not prereqCodigo:
                response.status = '400'
                return json.dumps({'message': 'Dados incompletos'})
            prereqAdicionado = self.diciplinaController.addPrereq(codigo, prereqCodigo)
            if prereqAdicionado:
                response.status = 200
                return json.dumps({
                    'id': prereqAdicionado.id,
                    'codigoPrerequisito': prereqAdicionado.codigo,
                    'diciplinaId': prereqAdicionado.diciplinaId
                })
            else:
                response.status = 400
                return json.dumps({'message': f'Não foi possivel adicionar o prerequisito {prereqCodigo} a diciplina {codigo}'})
        except Exception as e:
            response.status = 500
            return json.dumps({'message': f'Erro interno do servidor {e}'})
        
    