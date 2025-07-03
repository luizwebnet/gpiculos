from sqlalchemy import Column, Integer, String, Float, Boolean, LargeBinary
from utils.imports import retornar_base_veiculo
from utils.mix_in import MixModelo

Base = retornar_base_veiculo()

class Veiculo(Base,MixModelo):
    __tablename__ = 'veiculos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    strMarca = Column(String(50), nullable=False, info={
        "nome":"Marca",
        "descricao": "Marca do veículo (ex: Toyota, Honda, Ford)",
        "exemplos": ["Toyota", "Honda", "Ford", "Chevrolet", "Volkswagen", "Fiat"],
        "shot": [
            { "Quero um Toyota Commodi 2012 branco": {"strMarca": "Toyota", "strModelo": "Commodi", "numAno": "2020", "strCor": "Branco"}}
        ]
    })
    strModelo = Column(String(150), nullable=False, info={
        "nome":"Modelo",
        "descricao": "Modelo do veículo (ex: Corolla, Civic)"
    })
    numAno = Column(String(4), nullable=False, info={
        "nome":"Ano",
        "descricao": 'Ano do veículo como string (ex: "2020")'
    })
    strCor = Column(String(20), nullable=False, info={
        "nome":"Cor",
        "descricao": "Cor do veículo (ex: Branco, Preto, Azul)",
        "exemplos": ["Branco", "Preto", "Prata", "Azul", "Vermelho", "Cinza"]
    })
    numKm = Column(Integer, nullable=False, info={
        "nome":"Km",
        "descricao": "Quilometragem do veículo (número inteiro)"
    })
    strEstado = Column(String(2), nullable=False, info={
        "nome":"Estado",
        "descricao": 'Estado/UF onde está o veículo (ex: "SP", "RJ")'
    })
    boolNovo = Column(Boolean, nullable=False, info={
        "nome":"É novo?",
        "descricao": "Se o veículo é novo (true) ou usado (false)",
        "shot": [
             { "Carros novos em SP": {"boolNovo": True, "strEstado": "SP"} }
        ]
    })
    numValor = Column(Float, nullable=False, info={
        "nome":"Valor",
        "descricao": "Preço do veículo (número decimal)"
    })
    boolAutomatico = Column(Boolean, nullable=False, info={
        "nome":"É automático?",
        "descricao": "Se o câmbio é automático (true) ou manual (false)",
        "shot": [
            { "Busco um carro automático e econômico" : {"boolAutomatico": True, "boolEconomico": True}}
        ]
    })
    boolEconomico = Column(Boolean, nullable=False, info={
        "nome":"É econômico?",
        "descricao": "Se o veículo é econômico (true) ou não (false)",
        "shot": [
            {"Veículos até 50000 reais" : {"numValor": 50000} }
        ]
    })
    blobImagem = Column(LargeBinary, nullable=True, info={
        "nome":"Imagem",
        "descricao": "Imagem do veículo"
    })