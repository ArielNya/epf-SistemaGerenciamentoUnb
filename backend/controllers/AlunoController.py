from services.AlunoService import AlunoService
from models.AlunoModel import AlunoModel, Completas
from typing import List, Dict, Optional
from datetime import date

class AlunoController:
    def __init__(self, alunoService: AlunoService):
        self.alunoService = alunoService

    def addAluno(self, nome: str, matricula: int, curso: str, dataNascimento: date) -> AlunoModel | None:
            try:
                aluno = self.alunoService.criarAluno(nome=nome, matricula=matricula, curso=curso, dataNasimento=dataNascimento)
                return aluno
            except Exception as e:
                print(f"Erro {e}")
                return None

    def buscarAlunoMatricula(self, matricula: int) -> Optional[AlunoModel]:
        return self.alunoService.buscarAlunoMatricula(matricula=matricula)

    def deleteAluno(self, matricula: int) -> bool:
        return self.alunoService.deleteAluno(matricula=matricula)
        
    def listarAlunos(self) -> list[AlunoModel]:
        return self.alunoService.listarAlunos()
    
    def concluirDiciplina(self, codigoDiciplina: int, matricula: int) -> Optional[Completas]:
         try:
              return self.alunoService.concluir(codigo=codigoDiciplina, matricula=matricula)
         except Exception as e:
              print(f'Erro: {e}')
              return None
         
    def listarDiciplinasConcluidas(self, matricula: int) -> List[Completas]:
        self.alunoService.listarConcluidas(matricula=matricula)

    def limparListaDeAlunos(self) -> bool:
         try:
              self.alunoService.limparLista()
              return True
         except Exception as e:
              print(f'Erro: {e}')
              return False