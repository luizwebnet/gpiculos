def main():        
    from ia.agent import AgenteVeiculo
    import logging
    from dotenv import load_dotenv    
    import os

    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    

    agent = AgenteVeiculo(
        api_key=os.getenv("API_KEY_DEEP"),        
        base_db=os.getenv("BASE_DB"),
        base_url=os.getenv("BASE_URL")
    )
            
    mensagens_teste = [
        "O que você tem aí de Toyota no ano 2011 e 2022? na cor azul e preta? Ah traz os ford tb!",
        "Busco um carro automático e econômico",
        "Veículos até 50000 reais",
        "Carros novos em SP"
    ]
    
    for msg in mensagens_teste:
        strRetorno = agent.consultar_veiculos(msg,excluir=["id", "blobImagem"])
        print(f"Mensagem: {msg}")
        print(strRetorno)
        print("-" * 50)    

if __name__ == "__main__":
    main()