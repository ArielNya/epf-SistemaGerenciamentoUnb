from data.database import Base
from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .Turmas import Turma

class AlunoTurma(Base):
    __tablename__ = 'alunos_turmas'

    alunoId: Mapped[int] = mapped_column(ForeignKey('alunos.matricula'), primary_key=True)
    turmaId: Mapped[int] = mapped_column(ForeignKey('turmas.id'), primary_key=True)
    
    aluno = relationship('AlunoModel', back_populates='matriculas')
    turma = relationship('Turma', back_populates='matriculas')

    def __repr__(self):
        return f"<AlunoTurma(aluno_id={self.aluno_id}, turma_id={self.turma_id})>"
