from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from data.database import Base

class AlunoModel(Base):
    __tablename__ = 'alunos'
    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(50))
    matricula: Mapped[int] = mapped_column(nullable=False)

    def __repr__(self):
        return f"Aluno: {self.nome}; Matricula: {self.matricula}"
    
    