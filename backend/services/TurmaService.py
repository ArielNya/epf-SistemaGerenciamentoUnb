from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, select
from models.Turmas import Turma
from models.DiciplinaModel import DiciplinaModel
from models.AlunoTurmaModel import AlunoTurma
from models.NotaFrequenciaModel import NotaFrequencia
from models.AlunoModel import AlunoModel
from datetime import time, date
from typing import List, Dict, Optional


class TurmaService:
    def __init__(self, db: Session) :
        self.db = db

    def criarTurma(self, nome: str, diciplinaId: int, anoSemestre: str,
                 horarioInicio: time, horarioFim: time, diaSemana: str,
                 sala: str, capacidade: int) -> Optional[Turma]:
        diciplina = self.db.query(DiciplinaModel).filter(DiciplinaModel.id == diciplinaId).first()
        if not diciplina:
            print(f'Erro, diciplina com Id {diciplinaId} não foi encontrada')
            return False
        if self._existeConflitoTurma(diciplinaId, horarioInicio, horarioFim, diaSemana, sala):
            print(f'Erro: Conflito de horario e/ou sala para a diciplina {diciplina.nome} na sala {sala} nos dias {diaSemana}')
            return None
        if capacidade <= 0:
            print(f'Erro: capacidade deve ser maior que 0')
            return None
        try:
            novaTurma = Turma(
                nome=nome,
                diciplinaId=diciplinaId,
                anoSemestre=anoSemestre,
                horarioInicio=horarioInicio,
                horarioFim=horarioFim,
                diasSemana=diaSemana,
                sala=sala,
                capacidade=capacidade
            )
            self.db.add(novaTurma)
            self.db.commit()
            self.db.refresh(novaTurma)
            print(f"Turma '{novaTurma.nome}' para '{diciplina.nome}' criada com sucesso!")
            return novaTurma
        
        except Exception as e:
            print(f'Erro ao criar turma: {e}')
            return None




    def _existeConflitoTurma(self, disciplinaId: int, horarioInicio: time, horarioFim: time, diasSemana: str, sala: str, turmaIdExcluir: Optional[int] = None) -> bool:

        diasSemanaLista = [d.strip() for d in diasSemana.split(',') if d.strip()]


        query = self.db.query(Turma).filter(Turma.sala == sala)

        if turmaIdExcluir:
            query = query.filter(Turma.id != turmaIdExcluir)

        turmasExistentesNaSala = query.all()

        for turma in turmasExistentesNaSala:
            turmaDiasSemanaLista = [d.strip() for d in turma.diasSemana.split(',') if d.strip()]


            diasComuns = set(diasSemanaLista).intersection(turmaDiasSemanaLista)
            if not diasComuns:
                continue 


            if not (horarioInicio >= turma.horarioFim or horarioFim <= turma.horarioInicio):
                return True 

        return False 

    def buscarTurmaId(self, turmaId: int) -> Optional[Turma]:
        return self.db.query(Turma).filter(Turma.id==turmaId).first()
    
    def listarTurmas(self, diciplinaId: Optional[int] = None) -> List[Turma]:
        query = self.db.query(Turma)
        if diciplinaId:
            query = query.filter(Turma.diciplinaId == diciplinaId)
        return query.all()
    
    def atualizarTurma(self, turmaId: id, novosDados: Dict) -> Optional[Turma]:
        turma = self.buscarTurmaId(turmaId=turmaId)
        if not turma:
            print(f'Erro: Turma com ID {turmaId} não encontrada')
            return None
        novoHorarioInicio = novosDados.get('horarioInicio', turma.horarioInicio)
        novoHorarioFim = novosDados.get('horarioFim', turma.horarioFim)
        novosDiasSemana = novosDados.get('diasSemana', turma.diasSemana)
        novaSala = novosDados.get('sala', turma.sala)

        horarioOuSalaAlterado = (
            novoHorarioInicio != turma.horarioInicio or
            novoHorarioFim != turma.horarioFim or
            novosDiasSemana != turma.diasSemana or
            novaSala != turma.sala
        )

        if horarioOuSalaAlterado:
            if self._existeConflitoTurma(turma.disciplinaId, novoHorarioInicio, novoHorarioFim, novosDiasSemana, novaSala, turmaIdExcluir=turmaId):
                print(f"Erro: Conflito de horário ou sala detectado ao tentar atualizar a turma {turma.nome}.")
                return None

        try:
            for key, value in novosDados.items():
                setattr(turma, key, value)
            self.db.commit()
            self.db.refresh(turma)
            print(f"Turma '{turma.nome}' atualizada com sucesso!")
            return turma
        except Exception as e:
            self.db.rollback()
            print(f"Erro ao atualizar turma: {e}")
            return None 
        
    def deletarTurma(self, turmaId: int) -> bool:
        turma = self.buscarTurmaId(turmaId)
        if not turma:
            print(f'Erro: Turma com ID {turmaId} não foi encontrada')
            return False
        try:
            self.db.query(AlunoTurma).filter(AlunoTurma.turmaId == turmaId).delete()
            self.db.query(NotaFrequencia).filter(NotaFrequencia.turmaId == turmaId).delete()
            self.db.delete(turma)
            self.db.commit()
            print(f'Turma {turma.nome} foi deletada')
            return True
        except Exception as e:
            self.db.rollback()
            print(f'Erro ao deletar turma: {e}')
            return False
        
    def matricularAluno(self, alunoId: int, turmaId: int) -> Optional[AlunoTurma]:
        aluno = self.db.query(AlunoModel).filter(AlunoModel.id == alunoId).first()
        turma = self.db.query(Turma).filter(Turma.id == turmaId).first()
        if not aluno:
            print(f'Erro: Aluno com ID {alunoId} não foi encontrado')
            return None
        if not turma:
            print(f'Erro: Turma com ID {turmaId} não foi encontrada')
            return None
        matriculaExistente = self.db.query(AlunoTurma).filter(
            AlunoTurma.alunoId == alunoId,
            AlunoTurma.turmaId == turmaId
        ).first()
        if matriculaExistente:
            print(f'Aluno {aluno.nome} já esta matriculado na turma {turma.nome}')
            return None
        alunosNaTurma = self.db.query(AlunoTurma).filter(AlunoTurma.turmaId == turmaId).count
        if alunosNaTurma >= turma.capacidade:
            print(f'Turma {turma.nome} atingiu sua capacidade maxima')
            return None
        try:
            novaMatricula = AlunoTurma(alunoId=alunoId, turmaId=turmaId)
            self.db.add(novaMatricula)
            self.db.commit()
            self.db.refresh(novaMatricula)
            print(f'Aluno {aluno.nome} matriculado na turma {turma.nome} da diciplina {turma.diciplina}')
            return novaMatricula

        except Exception as e:
            self.db.rollback()
            print(f'Erro {e}')
            return None
    
    def desmatricularAluno(self, alunoid: int, turmaId: int):
        matricula = self.db.query(AlunoTurma).filter(
            AlunoTurma.alunoId == alunoid,
            AlunoTurma.turmaId == turmaId
        ).first()

        if not matricula:
            print(f'Erro: Matricula do aluno {alunoid} não foi encontrada')
            return False
        try:
            self.db.delete(matricula)
            self.db.commit()
            print(f'Aluno {alunoid} desmatriculado da turma {turmaId} com sucesso')
            return True

        except Exception as e:
            self.db.rollback()
            print(f'Erro: {e}')
            return False
        
    def listarAlunosMatriculados(self, turmaId: int) -> List[AlunoModel]:
        turma = self.buscarTurmaId(turmaId)
        if not turma:
            print(f'Erro: Turma com ID {turmaId} não existe')
            return []
        return [matricula.aluno for matricula in turma.matriculas]
    
    def listarTurmasDoAluno(self, alunoId: int) -> List[Turma]:
        aluno = self.db.query(AlunoModel).filter(AlunoModel.id == alunoId).first()
        if not aluno:
            print(f'Erro: Aluno com ID {alunoId} não foi encontrado')
            return []
        return [matricula.turma for matricula in aluno.matriculas]
    