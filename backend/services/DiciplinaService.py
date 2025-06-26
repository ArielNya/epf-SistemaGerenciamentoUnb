from models.DiciplinaModel import DiciplinaModel, Prerequisitos
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List

class DiciplinaService:
    def __init__(self, db: Session):
        self.db: Session = db

    def criarDiciplina(self, nome: str, codigo: int, prerequisitos: List[int] | None, carga: int) -> DiciplinaModel | None:
        if self.buscarDiciplina(codigo=codigo):
            return None
        
        newDiciplina = DiciplinaModel(nome=nome, codigo=codigo, carga=carga)
        self.db.add(newDiciplina)
        self.db.commit()
        self.db.refresh(newDiciplina)
        
        if prerequisitos:
            self.addPrereq(codigo, prerequisitos=prerequisitos)
        return newDiciplina
    
    def buscarDiciplina(self, codigo: int):
        return self.db.query(DiciplinaModel).filter(DiciplinaModel.codigo == codigo).first()
    
    def addPrereq(self, diciplina: int, prerequisitos: List[int]):
        diciplina = self.buscarDiciplina(diciplina)
        if not diciplina: return None

        for p in prerequisitos:
            temp = self.db.query(Prerequisitos).filter(Prerequisitos.codigo == p).first()
            temp2 = self.db.query(DiciplinaModel).filter(DiciplinaModel.codigo==p).first()
            if not temp2: continue
            if temp: continue
            
            newReq = Prerequisitos(codigo=p, diciplina=diciplina)
            self.db.add(newReq)
            self.db.commit()
            self.db.refresh(newReq)
            return newReq
        
    def listarDiciplinas(self):
        return self.db.execute(select(DiciplinaModel)).all()
        
    def listarPrereq(self, codigo: int):
        diciplina = self.db.query(DiciplinaModel).filter(DiciplinaModel.codigo==codigo).first()
        if diciplina: return diciplina.prereq
        else: return None

    def deleteDiciplina(self, codigo: int) -> bool:
        diciplina = self.buscarDiciplina(codigo=codigo)
        if diciplina:
            self.db.delete(diciplina)
            self.db.commit()
            return True
        else:
            return False

    def deletePrereq(self, diciplina: int, prereq: int):
        d = self.buscarDiciplina(diciplina)
        if not diciplina: return False
        for p in d.prereq:
            if p == prereq:
                self.db.delete(p)
                self.db.commit()
                return True
    
