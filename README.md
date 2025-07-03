
# GPículos 🚗  
*Tão natural quanto dirigir*

---

## 📖 Sobre o Projeto

Este é um assistente inteligente de busca de veículos, *via terminal*, capaz de interpretar comandos em linguagem natural como:

- "O que você tem aí de Toyota no ano 2011?"
- "Busco um carro automático e econômico"
- "Veículos até 50000 reais"
- "Carros novos em SP"

O sistema interpreta a intenção, converte em filtros, consulta o banco e retorna uma resposta amigável.

---

## 🗂️ Estrutura de Pastas

```bash
C2S/
├── data/                     # Banco de dados SQLite
│   └── database.sqlite
├── ia/                       # Camada de inteligência artificial
│   └── agent.py              # Agente principal que consulta IA e orquestra tudo
├── integracao/              # Repositório e acesso ao banco
│   └── integration_db.py
├── modelo/                  # Modelo de dados (SQLAlchemy)
│   └── veiculo.py
├── test/                    # Testes de banco e IA
│   ├── test_db.py
│   └── test_ia.py
├── utils/                   # Funções auxiliares, helpers e mixins
│   ├── conditional.py
│   ├── imports.py
│   ├── mix_in.py
│   └── ui.py
└── .env                     # Variáveis de ambiente (API key, DB, etc)
```

---

## 🚀 Como Executar (produção)

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Crie o arquivo `.env` com as seguintes variáveis:

```
API_KEY=your-api-key-here
API_KEY_DEEP=your-api-key-here
BASE_URL=https://api.deepseek.com
BASE_DB=sqlite:///data/database.sqlite
```

3. Execute o sistema:

```bash
python -main.py
```

---

## 🧪 Testes

### Teste com o banco:

```bash
python -m test.test_db
```

Para apagar os dados fake do banco:

```bash
python -m test.test_db 0
```

### Teste com IA:

```bash
python -m test.test_ia
```

---

## 💡 Observações Técnicas

- O projeto foi construído com uma arquitetura **simples**, mas baseada em princípios do **SOLID**, como responsabilidade única e separação de camadas.
- Foi aplicado um padrão de **singleton inteligente** no agente, em diálogo com os conceitos do **MCP**.
- Optou-se por engenharia de prompt e métodos estruturados ao invés de aplicar um MCP completo nesta fase.
- Toda lógica de filtro foi feita de forma robusta para lidar com dados simples ou em lista tal qual corrigir erros ou expressões .
- O projeto está pronto para receber melhorias e sugestões — **sinta-se à vontade para contribuir!**

---

## 🤖 LLMs testadas

- [x] OpenAI (via `openai` SDK) - nativo no projeto
- [x] DeepSeek


---

## 📦 Bibliotecas utilizadas

| Biblioteca       | Nativa? | Função principal                        |
|------------------|---------|-----------------------------------------|
| `os`             | ✅       | Variáveis de ambiente                   |
| `re`             | ✅       | Regex para parsing de strings           |
| `json`           | ✅       | Serialização e manipulação de dados     |
| `random`         | ✅       | Geração de dados fake                   |
| `logging`        | ✅       | Logging estruturado                     |
| `typing`         | ✅       | Tipagem genérica                        |
| `contextlib`     | ✅       | Gerenciamento de sessão com contextos   |
| `sqlalchemy`     | ❌       | ORM para banco SQLite                   |
| `faker`          | ❌       | Geração de dados fake                   |
| `python-dotenv`  | ❌       | Carregar variáveis do `.env`            |
| `tabulate`       | ❌       | Exibir tabelas formatadas no terminal   |
| `openai`         | ❌       | Acesso à API da OpenAI                  |

---

## 🐍 Versão do Python utilizada

```bash
python --version
```

> Testado com **Python 3.10.8**

---

## 🙏 Agradecimentos

Obrigado por considerar o projeto!  
Fique à vontade para enviar sugestões, críticas ou melhorias.  
Nos vemos na estrada! 🛣️🚗
