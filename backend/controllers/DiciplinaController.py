from services.DiciplinaService import DiciplinaService
from models.DiciplinaModel import DiciplinaModel, Prerequisitos
from models.Turmas import Turma
from typing import List, Optional

class DiciplinaController:
    def __init__(self, diciplinaService: DiciplinaService):
        self.diciplinaService: DiciplinaService = diciplinaService

    def criarDiciplina(
            self,
            nome: str,
            codigo: int,
            carga: int,
            prereq: Optional[List[int]] = None
    ) -> Optional[DiciplinaModel]:
        
        try:
            return self.diciplinaService.criarDiciplina(nome=nome, codigo=codigo, prerequisitos=prereq, carga=carga)
        except Exception as e:
            print(f'Erro: {e}')
            return None
        
    def listarDiciplina(self) -> List[DiciplinaModel]:
        return self.diciplinaService.listarDiciplinas()
    
    def buscarDiciplinaPorCodigo(self, codigo: int) -> Optional[DiciplinaModel]:
        return self.diciplinaService.buscarDiciplina(codigo=codigo)
    
    def addPrereq(
            self,
            diciplinaCodigo: int,
            prereqCodigo: int,
    ) -> Optional[Prerequisitos]:
        try:
            return self.diciplinaService.addPrereq(diciplinaCodigo, [prereqCodigo])
        except Exception as e:
            print(f'Erro: {e}')
            return None
        
    def listarPrereq(self, codigo: int):
        return self.diciplinaService.listarPrereq(codigo)
    
    def deleteDiciplina(self, codigo: int) -> bool:
        return self.diciplinaService.deleteDiciplina(codigo)
    
    def deletarPrereq(
            self,
            diciplinaCodigo: int,
            prereqCodigo: int
    ) -> bool:
        
        return self.diciplinaService.deletePrereq(diciplinaCodigo, prereqCodigo)
    
    def listarTurmasDiciplina(self, diciplinaCodigo: int) -> List[Turma]:
        return self.diciplinaService.listarTurmasPorDiciplina(diciplinaCodigo)