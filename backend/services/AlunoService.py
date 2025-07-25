from models.AlunoModel import AlunoModel, Completas
from sqlalchemy.orm import Session
from sqlalchemy import select, update, JSON
from datetime import date
from models.DiciplinaModel import DiciplinaModel

class AlunoService:
    def __init__(self, db: Session):
        self.db: Session = db

    def criarAluno(self, nome: str, matricula: int, curso: str, dataNasimento: date) -> AlunoModel | None:
        #if not nome: return None
        temp = self.buscarAlunoMatricula(matricula)
        if not temp:
            newAluno = AlunoModel(nome=nome, matricula=matricula, curso=curso, dataNascimento=dataNasimento)
            self.db.add(newAluno)
            self.db.commit()
            self.db.refresh(newAluno)
            return newAluno
        else:
            print(f"Erro: Aluno com matrícula {matricula} já existe.")
            return None

    def concluir(self, codigo: int, matricula: int) -> Completas | None:
        aluno = self.buscarAlunoMatricula(matricula=matricula)
        temp = self.db.query(Completas).filter(Completas.codigo == codigo).first()
        if temp: return None
        if aluno:
            done = Completas(codigo=codigo, aluno=aluno)
            self.db.add(done)
            self.db.commit()
            self.db.refresh(done)
            print(f'Diciplina {codigo} marcada como concluida para o aluno {aluno.nome}')
            return done
        else:
            return None

    def listarConcluidas(self, matricula: int):
        aluno = self.buscarAlunoMatricula(matricula=matricula)
        if not aluno:
            print(f'Erro: Aluno com matricula {matricula} não foi encontrado')
            return []
        concluidas = self.db.query(Completas).filter(Completas.alunoId == aluno.id).all()
        concluidasList = []
        for concluida in concluidas:
            concluidasList.append(concluida)

        return concluidasList

    def buscarAlunoMatricula(self, matricula: int) -> AlunoModel | None:
        aluno = self.db.query(AlunoModel).filter(AlunoModel.matricula == matricula).first()
        if aluno:
            return aluno
        else:
            return None
    
    def listarAlunos(self) -> list[AlunoModel]:
        #return self.db.query(AlunoModel).all()
        try:
            alunos = self.db.query(AlunoModel).all()
            return alunos
        except Exception as e:
            print(f"Erro no AlunoService.listarAlunos: {e}")
            self.db_session.rollback()
            return []

    def deleteAluno(self, matricula: int) -> bool:
        aluno = self.buscarAlunoMatricula(matricula)
        if aluno:
            try:
                self.db.delete(aluno)
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                print(f'Erro: {e}')
                return False
        else:
            return False
        
    def limparLista(self):
        try:
            self.db.query(AlunoModel).delete()
            self.db.commit()
            print('Todos os alunos foram deletados')
        except Exception as e:
            self.db.rollback()
            print(f'Erro: {e}')
