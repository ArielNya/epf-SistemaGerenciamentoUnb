from models.AlunoModel import AlunoModel
from sqlalchemy.orm import Session
from sqlalchemy import select

class AlunoService:
    def __init__(self, db: Session):
        self.db: Session = db

    def criarAluno(self, nome: str, matricula: int) -> AlunoModel | None:
        #if not nome: return None
        temp = self.buscarAlunoMatricula(matricula)
        if not temp:
            newAluno = AlunoModel(nome=nome, matricula=matricula)
            self.db.add(newAluno)
            self.db.commit()
            self.db.refresh(newAluno)
            return newAluno
        else:
            return None

    
    def buscarAlunoMatricula(self, matricula: int) -> AlunoModel | None:
        return self.db.query(AlunoModel).filter(AlunoModel.matricula == matricula).first()
    
    def listarAlunos(self) -> list[AlunoModel]:
        return self.db.execute(select(AlunoModel)).all()

    def deleteAluno(self, matricula: int) -> bool:
        aluno = self.buscarAlunoMatricula(matricula)
        if aluno:
            self.db.delete(aluno)
            self.db.commit()
            return True
        else:
            return False
        
    def limparLista(self):
        self.db.query(AlunoModel).delete()
        self.db.commit

