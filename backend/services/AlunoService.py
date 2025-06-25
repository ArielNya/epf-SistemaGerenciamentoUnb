from models.AlunoModel import AlunoModel, Completas
from sqlalchemy.orm import Session
from sqlalchemy import select, update, JSON


class AlunoService:
    def __init__(self, db: Session):
        self.db: Session = db
        

    def criarAluno(self, nome: str, matricula: int, curso: str) -> AlunoModel | None:
        #if not nome: return None
        temp = self.buscarAlunoMatricula(matricula)
        if not temp:
            newAluno = AlunoModel(nome=nome, matricula=matricula, curso=curso)
            self.db.add(newAluno)
            self.db.commit()
            self.db.refresh(newAluno)
            return newAluno
        else:
            return None

    def concluir(self, codigo, matricula):
        aluno = self.buscarAlunoMatricula(matricula=matricula)
        temp = self.db.query(Completas).filter(Completas.codigo == codigo).first()
        if temp: return None
        if aluno:
            done = Completas(codigo=codigo, aluno=aluno)
            self.db.add(done)
            self.db.commit()
            return done
        else:
            return None

    def listarConcluidas(self, matricula: int):
        aluno = self.buscarAlunoMatricula(matricula=matricula)
        return self.db.query(Completas).filter(Completas.aluno == aluno).all()

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

