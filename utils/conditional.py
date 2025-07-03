from typing import Callable, Type, TypeVar
T = TypeVar('T')

def verificar_parametro(parametro:str,funcao:Callable[[],None]):
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == parametro:                
        funcao()
        sys.exit()
        
