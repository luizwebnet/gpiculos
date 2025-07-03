def main():
    from integracao.integration_db import DatabaseManager,VeiculoRepositorio,VeiculoFakeDado
    from utils.ui import exibir_mensagem
    from utils.conditional import verificar_parametro        
    import logging
    from dotenv import load_dotenv    
    import os


    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )


    objDatabaseManager = DatabaseManager(os.getenv("BASE_DB"),None,False)
    objDatabaseManager.iniciar_tabela()

    objVeiculoRepositorio = VeiculoRepositorio(objDatabaseManager)    
        
    #python test_db.py 0
    #Para limpar dados fake na linha de comando
    verificar_parametro(parametro="0",funcao=objVeiculoRepositorio.limpar_todos)    

    objVeiculoFakeDado = VeiculoFakeDado(objVeiculoRepositorio)    

    objVeiculoFakeDado.popular_banco(100)

    setDataVeiculos = [objVeiculoRepositorio.buscar_veiculos({},1), objVeiculoRepositorio.buscar_veiculos({'strMarca':['Toyota','Volkswagen'],'numAno':2018},1)]

    exibir_mensagem(f"Total: {len(setDataVeiculos[0])}, Toyotas: {len(setDataVeiculos[1])}, {setDataVeiculos[1]}",tipo="info")    


if __name__ == "__main__":
    main()