from services.NotaFrequenciaService import NotaFrequenciaService
from models.NotaFrequenciaModel import NotaFrequencia
from typing import List, Optional

class NotaFrequenciaController:
    def __init__(self, notaFrequenciaService: NotaFrequenciaService):
        self.notaFrequenciaService = notaFrequenciaService

    def atribuirNotaFrequencia(
            self,
            alunoId: int,
            turmaId: int,
            nota: Optional[float] = None,
            frequencia: Optional[float] = None
    ) -> Optional[NotaFrequencia]:
        try:
            return self.notaFrequenciaService.atribuirFrequencia(alunoId, turmaId, nota, frequencia)
        except Exception as e:
            print(f'Erro: {e}')
            return None
        
    def buscarNotaFrequencia(
            self,
            alunoId: int,
            turmaId: int
    ) -> Optional[NotaFrequencia]:
        return self.notaFrequenciaService.buscarNotaFrequencia(alunoId, turmaId)
    
    def listarNotasFrequenciaAluno(
            self,
            alunoId: int
    ) -> List[NotaFrequencia]:
        return self.notaFrequenciaService.listarNotasFrequenciasAluno(alunoId)
    
    def listarNotasFrequenciaTurma(
            self,
            turmaId: int
    ) -> List[NotaFrequencia]:
        return self.notaFrequenciaService.listarNotasFrequenciasTurma(turmaId)
    
    