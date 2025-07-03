_veiculo = _base = _faker = _random = None

def retornar_class_veiculo():
    global _veiculo
    if _veiculo is None:
        from modelo.veiculo import Veiculo
        _veiculo = Veiculo
    return _veiculo

def retornar_base_veiculo():
    global _base
    if _base is None:
        from sqlalchemy.ext.declarative import declarative_base            
        _base = declarative_base()
    return _base

def retornar_class_faker():
    global _faker
    if _faker is None:
        from faker import Faker
        _faker = Faker
    return _faker

def retornar_class_random():
    global _random
    if _random is None:
        import random
        _random = random
    return _random
