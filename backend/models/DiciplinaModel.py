from data.database import Base
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List


class DiciplinaModel(Base):
    __tablename__ = 'disciplina'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    codigo: Mapped[int] = mapped_column(nullable=False)
    carga: Mapped[int] = mapped_column(nullable=False)
    prereq: Mapped[List['Prerequisitos']] = relationship(back_populates='diciplina')

    turmas = relationship('Turma', back_populates='diciplina')

    def __repr__(self):
        return f'{self.nome}'

class Prerequisitos(Base):
    __tablename__ = 'prerequisitos'
    id: Mapped[int] = mapped_column(primary_key=True)
    codigo: Mapped[int] = mapped_column(nullable=False)
    disciplinaId: Mapped[int] = mapped_column(ForeignKey('disciplina.id'))
    diciplina: Mapped['DiciplinaModel'] = relationship(back_populates='prereq')

    def __repr__(self):
        return f'{self.codigo}'
