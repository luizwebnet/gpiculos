from ia.agent import AgenteVeiculo
from tabulate import tabulate
import logging
import os
from dotenv import load_dotenv    

load_dotenv()

def exibir_titulo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print()
    print("=" * 80)
    print("   ██████╗ ██╗  ")
    print("  ██╔═══██╗██║  ")
    print("  ██║   ██║██║  ")
    print("  ██║   ██║██║  ")
    print("  ╚██████╔╝██║  ")
    print("  ╚═════╝ ╚═╝  ")
    print("\n GPículos - Tão natural quanto dirigir")
    print("=" * 80)
    print()

def exibir_instrucoes():
    print("🧑‍🏭 Olá! Sou seu assistente para encontrar o seu tão sonhado veículo.")
    print("💬 Fale comigo como se estivesse falando com um vendedor de loja. Por exemplo:")
    print()
    print('   - "O que você tem aí de Toyota no ano 2011?"')
    print('   - "Busco um carro automático e econômico"')
    print('   - "Veículos até 50000 reais"')
    print('   - "Carros novos em SP"')
    print()
    print("❌ Para sair, digite: bye")
    print()

def main():
    logging.basicConfig(level=logging.WARNING)

    agent = AgenteVeiculo(
        api_key=os.getenv("API_KEY"),        
        base_db=os.getenv("BASE_DB")
    )

    exibir_titulo()
    exibir_instrucoes()

    while True:
        mensagem = input("📝 Sua mensagem: ").strip()
        if mensagem.lower() in ("bye", "sair", "exit", "quit"):
            print("\n👋 Obrigado por usar o GPículos! Até logo!\n")
            break

        print("\n⏳ Consultando...\n")
        resposta = agent.consultar_veiculos(mensagem, excluir=["id", "blobImagem"])
        print(resposta)
        print("\n" + "-" * 80 + "\n")

if __name__ == "__main__":
    main()
