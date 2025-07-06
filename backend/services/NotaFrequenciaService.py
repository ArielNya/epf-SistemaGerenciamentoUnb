from sqlalchemy.orm import Session
from models.NotaFrequenciaModel import NotaFrequencia
from models.AlunoModel import AlunoModel
from models.AlunoTurmaModel import AlunoTurma
from models.Turmas import Turma
from typing import Optional, List

class NotaFrequenciaService:
    def __init__(self, db: Session):
        self.db = db
    
    def atribuirFrequencia(self, alunoId: int, turmaId: int, nota: Optional[float] = None, frequencia: Optional[int] = None) -> Optional[NotaFrequencia]:
        aluno = self.db.query(AlunoModel).filter(AlunoModel.id == alunoId).first()
        turma = self.db.query(Turma).filter(Turma.id == turmaId).first()
        matricula = self.db.query(AlunoTurma).filter(AlunoTurma.alunoId == alunoId, AlunoTurma.turmaId == turmaId).first()
        if not aluno:
            print(f'Erro: Aluno com ID {alunoId} não foi encontrado')
            return None
        if not turma:
            print(f'Erro: Turma com ID {turmaId} não foi encontrada')
            return None
        if not matricula:
            print(f'Erro: Aluno não está matriculado na turma com ID {turmaId}')
            return None
        
        nf = self.db.query(NotaFrequencia).filter(
            NotaFrequencia.alunoId == alunoId,
            NotaFrequencia.turmaId == turmaId
        ).first()
        try:
            if nf:
                if nota is not None:
                    nf.nota = nota
                if frequencia is not None:
                    nf.frequencia = frequencia
                print(f'Nota/Frequencia atualizada para o aluno {aluno.nome} na turma {turma.nome}')
            else:
                nf = NotaFrequencia(
                    alunoId=alunoId,
                    turmaId=turmaId,
                    nota=nota,
                    frequencia=frequencia
                )
                self.db.add(nf)
                print(f'Nota/Frequencia criada para o aluno {aluno.nome} na turma {turma.nome}')
            
            self.db.commit()
            self.db.refresh(nf)
            return nf
        
        except Exception as e:
            self.db.rollback()
            print(f'Erro ao atualizar/criar notas e frequencias: {e}')
            return None
        
    def buscarNotaFrequencia(self, alunoId: int, turmaId: int) -> Optional[NotaFrequencia]:
        return self.db.query(NotaFrequencia).filter(
            NotaFrequencia.alunoId == alunoId,
            NotaFrequencia.turmaId == turmaId
        ).first()
    
    def listarNotasFrequenciasAluno(self, alunoId: int) -> List[NotaFrequencia]:
        return self.db.query(NotaFrequencia).filter(NotaFrequencia.alunoId == alunoId).all()
    
    def listarNotasFrequenciasTurma(self, turmaId: int) -> List[NotaFrequencia]:
        return self.db.query(NotaFrequencia).filter(NotaFrequencia.turmaId == turmaId).all()
    
    