from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import List, Optional, Type, TypeVar, Dict, Any
import os
from utils.imports import retornar_class_veiculo, retornar_class_faker, retornar_class_random, retornar_base_veiculo
from utils.ui import exibir_mensagem
import logging

# Genérico
T = TypeVar('T')

class DatabaseManager:   
    
    def __init__(self, database_url: str, base_class:Optional[Type[T]]=None, echo: bool = True):
        self.engine = create_engine(database_url, echo=echo)
        self.SessionLocal = sessionmaker(bind=self.engine)
        self.verificar_dir()
        self.base = base_class or retornar_base_veiculo()
        

    def verificar_dir(self):        
        if 'data/' in str(self.engine.url):
            os.makedirs('data', exist_ok=True)
    
    @contextmanager    
    def _get_session(self):       
        #Dinamizar as conexões com banco
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def iniciar_tabela(self):        
        self.base.metadata.create_all(bind=self.engine)
    
    def remover_tabela(self):        
        self.base.metadata.drop_all(bind=self.engine)

class VeiculoRepositorio:    
    
    def __init__(self, db_manager: DatabaseManager, modelo_class:Optional[Type[T]]=None):
        self.db = db_manager
        self.modelo = modelo_class or retornar_class_veiculo()        
        self.logger = logging.getLogger("__name__")

    def criar_veiculos(self, veiculo) -> None:        
        with self.db._get_session() as session:
            session.add(veiculo)
    
    def criar_multiplos_veiculos(self, veiculos: List) -> None:        
        with self.db._get_session() as session:
            session.add_all(veiculos)

    def existir_veiculos(self) -> bool:
        with self.db._get_session() as session:
            return session.query(session.query(self.modelo).exists()).scalar()        
    
    def buscar_veiculos(self, filtros: Optional[Dict[str, Any]] = None,json:Optional[int] = 0) -> List:
        with self.db._get_session() as session:
            query = session.query(self.modelo)

            if filtros:
                for campo, valor in filtros.items():
                    coluna = getattr(self.modelo, campo, None)
                    if coluna is not None:
                        if isinstance(valor,list):
                            query = query.filter(coluna.in_(valor))
                        elif isinstance(valor, str):
                            if valor == "":
                                query = query.filter(coluna.isnot(None))
                            else:
                                query = query.filter(coluna.ilike(f"%{valor}%"))
                        else:
                            query = query.filter(coluna == valor)
             
            listData = query.all()    
                        
            if json:
                session.expunge_all()             
            return listData
    
    def atualizar(self, veiculo_id: int, **kwargs) -> bool:        
        with self.db._get_session() as session:            
            veiculo = session.query(self.modelo).filter(self.modelo.id == veiculo_id).first()
            if veiculo:
                for key, value in kwargs.items():
                    setattr(veiculo, key, value)
                return True
            return False
    
    def deletar(self, veiculo_id: int) -> bool:        
        with self.db._get_session() as session:            
            veiculo = session.query(self.modelo).filter(self.modelo.id == veiculo_id).first()
            if veiculo:
                session.delete(veiculo)
                return True
            return False
    
    def limpar_todos(self) -> None:        
        with self.db._get_session() as session:            
            session.query(self.modelo).delete()
            exibir_mensagem("Dados removidos.",tipo="ok")

class VeiculoFakeDado:    
    
    def __init__(self, veiculo_class: Type[T]):
        self.VeiculoRepositorio = veiculo_class                
        self.Veiculo = self.VeiculoRepositorio.modelo

    
    def criar_veiculo_fake(self):                
        fake = retornar_class_faker()('pt_BR')
        random = retornar_class_random()        
                
        listMarcas = self.Veiculo.__table__.columns["strMarca"].info.get("exemplos", "")
        listCores = self.Veiculo.__table__.columns["strCor"].info.get("exemplos", "")
        
        return self.Veiculo(
            strMarca=random.choice(listMarcas),
            strModelo=fake.word().capitalize(),
            numAno=str(random.randint(2010, 2024)),
            strCor=random.choice(listCores),
            numKm=random.randint(0, 200000),
            strEstado=fake.estado_sigla(),
            boolNovo=random.choice([True, False]),
            numValor=round(random.uniform(15000, 120000), 2),
            boolAutomatico=random.choice([True, False]),
            boolEconomico=random.choice([True, False]),
            blobImagem=None
        )
    
    def popular_banco(self, quantidade: int = 100):                
        if not self.VeiculoRepositorio.existir_veiculos():
            veiculos = [self.criar_veiculo_fake() for _ in range(quantidade)]
            self.VeiculoRepositorio.criar_multiplos_veiculos(veiculos)
        else:
            exibir_mensagem("Base já contém veículos. Inserção não realizada.",tipo="atencao")

    def repopular_banco(self, quantidade=50):
        self.VeiculoRepositorio.limpar_todos()
        self.popular_banco(quantidade)
