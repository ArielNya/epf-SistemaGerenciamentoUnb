from models.DiciplinaModel import DiciplinaModel, Prerequisitos
from sqlalchemy.orm import Session
from models.Turmas import Turma
from sqlalchemy import select
from typing import List

class DiciplinaService:
    def __init__(self, db: Session):
        self.db: Session = db

    def criarDiciplina(self, nome: str, codigo: int, prerequisitos: List[int] | None, carga: int) -> DiciplinaModel | None:
        if self.buscarDiciplina(codigo=codigo):
            print(f'Erro: Diciplina com codigo {codigo} já existe')
            return None
        
        try:
            newDiciplina = DiciplinaModel(nome=nome, codigo=codigo, carga=carga)
            self.db.add(newDiciplina)
            self.db.commit()
            self.db.refresh(newDiciplina)
            if prerequisitos:
                self.addPrereq(codigo, prerequisitos=prerequisitos)
                
            print(f'Diciplina {newDiciplina.nome} criada com sucesso')
            return newDiciplina

        except Exception as e:
            self.db.rollback()
            print(f'Erro: {e}')
            return None

    
    def buscarDiciplina(self, codigo: int) -> DiciplinaModel | None:
        return self.db.query(DiciplinaModel).filter(DiciplinaModel.codigo == codigo).first()
    
    def addPrereq(self, diciplinaCodigo: int, prerequisitos: List[int]):
        diciplina = self.buscarDiciplina(diciplinaCodigo)
        if not diciplina: return None

        for pCodigo in prerequisitos:
            prereqDiciplina = self.buscarDiciplina(codigo=pCodigo)
            if not prereqDiciplina:
                continue

            existingPrereq = self.db.query(Prerequisitos).filter(
                Prerequisitos.diciplinaId == diciplina.id,
                Prerequisitos.codigo == pCodigo
            ).first()
            if existingPrereq:
                continue
            try:
                newReq = Prerequisitos(codigo=pCodigo, disciplinaId=diciplina.id) 
                self.db.add(newReq)
                self.db.commit()
                self.db.refresh(newReq)
                print(f"Pré-requisito {pCodigo} adicionado à disciplina {diciplina.nome}.")
                return newReq 
            except Exception as e:
                self.db.rollback()
                print(f'Erro: {e}')
                return None
        return None
        
    def listarDiciplinas(self):
        return self.db.execute(select(DiciplinaModel)).all()
        
    def listarPrereq(self, codigo: int):
        diciplina = self.db.query(DiciplinaModel).filter(DiciplinaModel.codigo==codigo).first()
        if diciplina: return diciplina.prereq
        else: return []

    def deleteDiciplina(self, codigo: int) -> bool:
        diciplina = self.buscarDiciplina(codigo=codigo)
        self.db.query(Prerequisitos).filter(Prerequisitos.diciplinaId == diciplina.id).delete()
        if diciplina:
            try:
                self.db.delete(diciplina)
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                print(f'Erro: {e}')
                return False
        else:
            return False

    def deletePrereq(self, diciplina: int, prereq: int):
        d = self.buscarDiciplina(diciplina)
        if not diciplina: return False
        pDelete = self.db.query(Prerequisitos).filter(
            Prerequisitos.diciplinaId == d.id,
            Prerequisitos.codigo == prereq
        ).first()

        if pDelete:
            try:
                self.db.delete(pDelete)
                self.db.commit()
                print(f'Prerequisito {prereq} removido da diciplina {diciplina.nome}')
                return True
            except Exception as e:
                self.db.rollback()
                print(f'Erro: {e}')
                return False
        else:
            return False
        
    def listarTurmasPorDiciplina(self, diciplinaCodigo: int) -> List[Turma]:
        diciplina = self.buscarDiciplina(diciplinaCodigo)
        if not diciplina:
            print(f'Erro: Diciplina com codigo {diciplinaCodigo} não foi encontrada')
            return []
        return diciplina.turmas
