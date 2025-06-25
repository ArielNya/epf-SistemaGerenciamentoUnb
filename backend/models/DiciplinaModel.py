from data.database import Base
from sqlalchemy import String, Date
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List


class DiciplinaModel(Base):
    __tablename__ = 'diciplina'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    codigo: Mapped[int] = mapped_column(nullable=False)
    carga: Mapped[int] = mapped_column(nullable=False)

    prereq: Mapped[List['Prerequisitos']] = relationship(back_populates='listaPrereq', overlaps=True)