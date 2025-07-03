import json
from sqlalchemy import LargeBinary
from sqlalchemy.orm.exc import DetachedInstanceError
import re
import logging

class MixModelo:    
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def __repr__(self):
        try:
            nome_classe = self.__class__.__name__
            dados = {}
            
            for coluna in self.__table__.columns:
                nome_campo = coluna.name
                valor = getattr(self, nome_campo)
                
                # Tratamento especial para diferentes tipos
                if isinstance(coluna.type, LargeBinary):
                    if valor:
                        dados[nome_campo] = f"<{len(valor)} bytes>"
                    else:
                        dados[nome_campo] = None
                elif isinstance(valor, float):
                    # Limita casas decimais para float
                    dados[nome_campo] = round(valor, 2)
                else:
                    dados[nome_campo] = valor
            
            return f"<{nome_classe} {json.dumps(dados, ensure_ascii=False, default=str, indent=2)}>"
            
        except DetachedInstanceError:
            self.logger.error(f"detached instance: {e}")            
            return ""
        except Exception as e:
            self.logger.error(f"Exception: {e}")            
            return ""
    
    def to_dict(self,excluir:list) -> dict:        
        excluir = excluir or []        
        try:
            dados = {}
            for col in self.__table__.columns:
                if col.name in excluir:
                    continue
                chave = col.info.get("nome", col.name)
                valor = getattr(self, col.name)
                
                if isinstance(col.type, LargeBinary):
                    valor = f"<{len(valor)} bytes>" if valor else None
                
                elif isinstance(valor, float):
                    valor = round(valor, 2)
                
                elif isinstance(valor, bool):
                    valor = "Sim" if valor else "Não"

                dados[chave] = valor
            return dados
        except DetachedInstanceError:
            logging.getLogger(self.__class__.__name__).error("Instância desconectada (detached)")
            return {}
        except Exception as e:
            logging.getLogger(self.__class__.__name__).error(f"Erro ao gerar dict: {e}")
            return {}
