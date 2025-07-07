
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from data.database import Base
from typing import List
from datetime import date
from .AlunoTurmaModel import AlunoTurma

class AlunoModel(Base):
    __tablename__ = 'alunos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    dataNascimento: Mapped[date] = mapped_column()
    matricula: Mapped[int] = mapped_column(nullable=False)
    curso: Mapped[str] = mapped_column(nullable=False)
    concluidas: Mapped[List['Completas']] = relationship(back_populates='aluno')

    matriculas = relationship('AlunoTurma', back_populates='aluno')
    notas_frequencias = relationship('NotaFrequencia', back_populates='aluno')

    def __repr__(self):
        return f"Aluno: {self.nome}; Matricula: {self.matricula}; Curso: {self.curso}; Concluidas: {self.concluidas}"
    
    
class Completas(Base):
    __tablename__ = 'completas'
    id: Mapped[int] = mapped_column(primary_key=True)
    alunoId: Mapped[int] = mapped_column(ForeignKey('alunos.id'))
    codigo: Mapped[int] = mapped_column(nullable=False)
    aluno: Mapped['AlunoModel'] = relationship(back_populates='concluidas')

    def __repr__(self):
        return f"{self.codigo}"