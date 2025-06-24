from services.AlunoService import AlunoService
from models.AlunoModel import AlunoModel
from typing import List, Dict

class AlunoController:
    def __init__(self, alunoService: AlunoService):
        self.alunoService = alunoService

    def addAluno(self, nome: str, matricula: int) -> AlunoModel | None:
            try:
                aluno = self.alunoService.criarAluno(nome=nome, matricula=matricula)
                return aluno
            except Exception as e:
                print(f"Erro {e}")
                return None



    def deleteAluno(self, matricula: int) -> bool:
        if self.alunoService.deleteAluno(matricula):
            print(f"Aluno deletado com sucesso")
            return True
        else:
            print(f"aluno não encontrado com essa matricula: {matricula}")
            return False
        
    def listarAlunos(self) -> list[AlunoModel]:
        return self.alunoService.listarAlunos()