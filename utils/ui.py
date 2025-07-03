def exibir_mensagem(dado, tipo="info"):
    icones = {
        "info": "ℹ️",
        "ok": "✅",
        "atencao": "⚠️",
        "erro": "❌"
    }

    cores = {
        "info": "\033[94m",     # azul claro
        "ok": "\033[92m",       # verde
        "atencao": "\033[93m",  # amarelo
        "erro": "\033[91m",     # vermelho
    }

    reset = "\033[0m"
    cor = cores.get(tipo, "\033[0m")
    icone = icones.get(tipo, "🔔")

    print(f"{cor}{icone} {dado}{reset}\n")
