from services.TurmaService import TurmaService
from models.Turmas import Turma
from typing import List, Optional
from datetime import time

class TurmaController:
    def __init__(self, turmaService: TurmaService):
        self.turmaService = turmaService

    def criarTurma(
        self,
        nome: str,
        disciplinaId: int,
        anoSemestre: str,
        horarioInicio: time,
        horarioFim: time,
        diasSemana: str,
        sala: str,
        capacidade: int
    ) -> Optional[Turma]:
        try:
            return self.turmaService.criarTurma(
                nome=nome, disciplinaId=disciplinaId, anoSemestre=anoSemestre,
                horarioInicio=horarioInicio, horarioFim=horarioFim,
                diasSemana=diasSemana, sala=sala, capacidade=capacidade
            )
        except Exception as e:
            print(f"Erro no TurmaController.criarTurma: {e}")
            return None
        
    def listarTurmas(self) -> List[Turma]:
        return self.turmaService.listarTurmas()
    
    def buscarTurmaId(self, turmaId: int) -> Optional[Turma]:
        return self.turmaService.buscarTurmaId(turmaId)
    
    def atualizarTurma(self, turmaId: int, dadosAtualizar: dict) -> Optional[Turma]:
        try:
            return self.turmaService.atualizarTurma(turmaId, dadosAtualizar)
        except Exception as e:
            print(f'Erro: {e}')
            return None
        
    def deletarTurma(self, turmaId: int) -> bool:
        return self.turmaService.deletarTurma(turmaId)
    
    def matricularAlunoTurma(self, alunoId: int, turmaId: int) -> bool:
        try:
            return self.turmaService.matricularAluno(alunoId, turmaId)
        except Exception as e:
            print(f'Erro: {e}')
            return False
        
    def desmatricularAluno(self, alunoId: int, turmaId: int) -> bool:
        return self.turmaService.desmatricularAluno(alunoId, turmaId)
    

    def listarAlunosMatriculadosTurma(self, turmaId) -> List[any]:
        return self.turmaService.listarAlunosMatriculados(turmaId)
    
    def listarTurmasDoAluno(self, alunoId: int) -> List[Turma]:
        return self.turmaService.listarTurmasDoAluno(alunoId)