from models.DiciplinaModel import DiciplinaModel, Prerequisitos
from sqlalchemy.orm import Session
from models.Turmas import Turma
from typing import List, Optional

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
            self.db.flush() # Use flush para obter o ID antes do commit final

            if prerequisitos:
                # Chame addPrereq para cada pré-requisito
                # addPrereq agora retorna True/False e processa todos os itens da lista
                if not self.addPrereq(newDiciplina.codigo, prerequisitos=prerequisitos):
                    self.db.rollback() # Se a adição de prereq falhar, desfaz tudo
                    print("Erro: Falha ao adicionar um ou mais pré-requisitos durante a criação da disciplina.")
                    return None
                
            self.db.commit() # Commit final depois de tudo
            self.db.refresh(newDiciplina)
                
            print(f'Diciplina {newDiciplina.nome} criada com sucesso')
            return newDiciplina

        except Exception as e:
            self.db.rollback()
            print(f'Erro ao criar disciplina ou adicionar pré-requisitos: {e}')
            return None

    
    def buscarDiciplina(self, codigo: int) -> DiciplinaModel | None:
        print(f"DEBUG_BUSCAR_DICIPLINA: Chamado com codigo={codigo}")
        print(f"DEBUG_BUSCAR_DICIPLINA: Estado da sessão (is active): {self.db.is_active}")
        print(f"DEBUG_BUSCAR_DICIPLINA: ID da sessão (endereço de memória): {id(self.db)}")
        diciplina = self.db.query(DiciplinaModel).filter(DiciplinaModel.codigo == codigo).first()
        print(f"DEBUG_BUSCAR_DICIPLINA: Resultado da busca para {codigo}: {diciplina}")
        return diciplina # Retorna a variável diciplina já buscada
    
    # Este método agora processa todos os pré-requisitos na lista e retorna um booleano de sucesso
    def addPrereq(self, diciplinaCodigo: int, prerequisitos: List[int]) -> bool:
        diciplina = self.buscarDiciplina(diciplinaCodigo)
        if not diciplina:
            print(f"Erro: Disciplina principal {diciplinaCodigo} não encontrada.")
            return False

        all_succeeded = True
        for pCodigo in prerequisitos:
            prereqDiciplina = self.buscarDiciplina(codigo=pCodigo)
            if not prereqDiciplina:
                print(f"Erro: Pré-requisito {pCodigo} não encontrado para a disciplina {diciplinaCodigo}. Pulando este.")
                all_succeeded = False
                continue # Continua para o próximo pré-requisito

            existingPrereq = self.db.query(Prerequisitos).filter(
                Prerequisitos.disciplinaId == diciplina.id,
                Prerequisitos.codigo == prereqDiciplina.codigo
            ).first()

            if not existingPrereq:
                try:
                    newReq = Prerequisitos(codigo=prereqDiciplina.codigo, disciplinaId=diciplina.id)
                    self.db.add(newReq)
                    # O commit será feito uma única vez no final
                    print(f"Pré-requisito {pCodigo} adicionado à disciplina {diciplina.nome}.")
                except Exception as e:
                    print(f'Erro ao adicionar pré-requisito {pCodigo}: {e}')
                    all_succeeded = False
            else:
                print(f"Pré-requisito {pCodigo} já existe para a disciplina {diciplina.nome}.")
        
        try:
            self.db.commit() # Commit de todas as adições de pré-requisitos de uma vez
        except Exception as e:
            self.db.rollback()
            print(f"Erro final de commit ao adicionar pré-requisitos: {e}")
            all_succeeded = False # Marca como falha se o commit final der erro
        
        return all_succeeded
        
    def listarDiciplinas(self) -> List[DiciplinaModel]:
        return self.db.query(DiciplinaModel).all()
        
    def listarPrereq(self, codigo: int) -> List[DiciplinaModel] | None: # Adicionado tipo de retorno
        print(f"DEBUG_LISTAR_PREREQ: Iniciando busca de prerequisitos para diciplina com codigo={codigo}")
        diciplina = self.buscarDiciplina(codigo=codigo) 
        print(f"DEBUG_LISTAR_PREREQ: Resultado de buscarDiciplina dentro de listarPrereq: {diciplina}")
        if not diciplina:
            print(f"DEBUG_LISTAR_PREREQ: Diciplina com codigo {codigo} NÃO ENCONTRADA por buscarDiciplina.")
            return None
        try:
            print(f"DEBUG_LISTAR_PREREQ: Diciplina encontrada (ID: {diciplina.id}). Buscando associações de pré-requisitos...")

            prereq_associations = self.db.query(Prerequisitos).filter(Prerequisitos.disciplinaId == diciplina.id).all()
            print(f"DEBUG_LISTAR_PREREQ: Associações encontradas: {len(prereq_associations)}")

            preReqList = []
            for req in prereq_associations: # Iterar sobre as associações de pré-requisitos
                preDiciplina = self.buscarDiciplina(codigo=req.codigo)
                if preDiciplina:
                    preReqList.append(preDiciplina)
                    print(f"DEBUG_LISTAR_PREREQ: Adicionado pré-requisito: {preDiciplina.nome} ({req.codigo})")
                else:
                    print(f"DEBUG_LISTAR_PREREQ: ERRO: Disciplina pré-requisito com CÓDIGO {req.codigo} não encontrada no banco.")

                # Prints de depuração (movidos e corrigidos para usar preReqList)
                print(f"DEBUG_LISTAR_PREREQ: Tipo de preReqList ANTES do len(): {type(preReqList)}")
                print(f"DEBUG_LISTAR_PREREQ: Conteúdo de preReqList ANTES do len(): {preReqList}")
                num_prereqs_current = len(preReqList)
                print(f"DEBUG_LISTAR_PREREQ: Número atual de pré-requisitos na lista: {num_prereqs_current}.")
            
            # REMOVIDA A LINHA INCORRETA QUE CAUSAVA O ERRO:
            # print(f"DEBUG_LISTAR_PREREQ: Retornando {len(preDiciplina)} pré-requisitos.") 

            print(f"DEBUG_LISTAR_PREREQ: Finalizando busca. Total de pré-requisitos encontrados: {len(preReqList)}.")
            return preReqList
        except Exception as e:
            print(f"DEBUG_LISTAR_PREREQ: EXCEÇÃO CAPTURADA APÓS ENCONTRAR DISCIPLINA: {type(e).__name__} - {e}")
            self.db.rollback() 
            return None

    def deleteDiciplina(self, codigo: int) -> bool:
        diciplina = self.buscarDiciplina(codigo=codigo)
        if not diciplina: # Adicionado verificação se a disciplina existe
            return False

        try:
            # Corrigido o operador OR e a variável diciplina
            self.db.query(Prerequisitos).filter(
                (Prerequisitos.disciplinaId == diciplina.id) |
                (Prerequisitos.codigo == diciplina.codigo)
            ).delete(synchronize_session=False)
            
            self.db.delete(diciplina)
            self.db.commit()
            print(f'Disciplina {codigo} e seus pré-requisitos/associações deletados com sucesso.')
            return True
        except Exception as e:
            self.db.rollback()
            print(f'Erro ao deletar disciplina {codigo}: {e}')
            return False

    def deletePrereq(self, diciplinaCodigo: int, prereqCodigo: int) -> bool: # Adicionado tipo de retorno
        diciplina = self.buscarDiciplina(diciplinaCodigo)
        if not diciplina:
            print(f"Erro: Disciplina {diciplinaCodigo} não encontrada.")
            return False
            
        prereq_disciplina_obj = self.buscarDiciplina(prereqCodigo) # Buscar o objeto da disciplina pré-requisito
        if not prereq_disciplina_obj:
            print(f"Erro: Pré-requisito com código {prereqCodigo} não encontrado como disciplina.")
            return False

        # Usar o ID da disciplina principal e o CÓDIGO da disciplina pré-requisito
        pDelete = self.db.query(Prerequisitos).filter(
            Prerequisitos.disciplinaId == diciplina.id,
            Prerequisitos.codigo == prereq_disciplina_obj.codigo
        ).first()

        if pDelete:
            try:
                self.db.delete(pDelete)
                self.db.commit()
                print(f'Prerequisito {prereqCodigo} removido da diciplina {diciplina.nome}.')
                return True
            except Exception as e:
                self.db.rollback()
                print(f'Erro ao deletar pré-requisito {prereqCodigo}: {e}')
                return False
        else:
            print(f"Pré-requisito {prereqCodigo} não encontrado para a disciplina {diciplinaCodigo}.")
            return False
        
    def listarTurmasPorDiciplina(self, diciplinaCodigo: int) -> List[Turma]:
        diciplina = self.buscarDiciplina(diciplinaCodigo)
        if not diciplina:
            print(f'Erro: Diciplina com codigo {diciplinaCodigo} não foi encontrada')
            return []
        return diciplina.turmas # Assumindo que 'turmas' é um relationship carregado