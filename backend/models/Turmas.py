from data.database import Base
from sqlalchemy import String, Time, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import time
from .DiciplinaModel import DiciplinaModel

class Turma(Base):
    __tablename__ = 'turmas'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[int] = mapped_column(index=True)
    anoSemestre: Mapped[str] = mapped_column(String(50))

    diciplinaId: Mapped[int] = mapped_column(ForeignKey('disciplina.codigo'))
    diciplina = relationship('DiciplinaModel', back_populates='turmas')

    horarioInicio: Mapped[time] = mapped_column(nullable=False)
    horarioFim: Mapped[time] = mapped_column(nullable=False)
    diasSemana: Mapped[str] = mapped_column(nullable=False)
    sala: Mapped[str] = mapped_column(nullable=False)
    capacidade: Mapped[int] = mapped_column(nullable=False)

    matriculas = relationship('AlunoTurma', back_populates='turma')
    notaFrequencia = relationship('NotaFrequencia', back_populates='turma')

    def __repr__(self):
        return f"<Turma(id={self.id}, nome='{self.nome}', disciplina_id={self.disciplina_id}, horario='{self.horario_inicio}-{self.horario_fim} {self.dias_semana}', sala='{self.sala}')>"
