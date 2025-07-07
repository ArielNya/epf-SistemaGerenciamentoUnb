from data.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

class NotaFrequencia(Base):
    __tablename__ = 'NotaFrequencia'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    alunoId: Mapped[int] = mapped_column(ForeignKey('alunos.id'))
    turmaId: Mapped[int] = mapped_column(ForeignKey('turmas.id'))

    nota: Mapped[float] = mapped_column(nullable=True)
    frequencia: Mapped[int] = mapped_column(nullable=True)

    aluno = relationship('AlunoModel', back_populates='notas_frequencias')
    turma = relationship('Turma', back_populates='notaFrequencia')

    def __repr__(self):
        return f"<NotaFrequencia(id={self.id}, aluno_id={self.aluno_id}, turma_id={self.turma_id}, nota={self.nota}, frequencia={self.frequencia})>"
    