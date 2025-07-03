from integracao.integration_db import VeiculoRepositorio,DatabaseManager
from typing import Dict, Any, Optional, List,TypeVar,Type
from openai import OpenAI
from sqlalchemy import String, Integer, Float, Boolean
import json
import re
import logging
from tabulate import tabulate

T = TypeVar('T')


class AgenteVeiculo:
    def __init__(self, base_db:str, modelo:Optional[Type[T]]=None, api_key: Optional[str] = None, base_url: Optional[str] = None ):
        
        self.db = base_db
        self.repositorio = self._conecta_repositorio()
        self.modelo = modelo or self.repositorio.modelo
        self.campos = [col.name for col in self.modelo.__table__.columns]
        self.camposDescricao = self._obter_campos_descricao()
        self.prompt_system = self._gerar_prompt_system()                       
        self.client = OpenAI(api_key=api_key, timeout=20) if not base_url else OpenAI(api_key=api_key,base_url=base_url, timeout=20)
        self.llmModel = "gpt-4" if not base_url else "deepseek-chat"
                
        self.logger = logging.getLogger(__name__)
    
    def _conecta_repositorio (self) -> Type[T]:                
        objDatabaseManager = DatabaseManager(self.db,None,False)
        objDatabaseManager.iniciar_tabela()
        return VeiculoRepositorio(objDatabaseManager)    
     
    def _obter_campos_descricao(self) -> Dict[str, Dict[str, Any]]:        
        dicInfoCampos = {}
        for col in self.modelo.__table__.columns:
            if col.name in self.campos:
                dicInfoCampos[col.name] = {
                    'tipo': str(col.type),
                    'nullable': col.nullable,
                    'descricao': col.info.get("descricao", ""),
                    'exemplos': col.info.get("exemplos", ""),
                }
        return dicInfoCampos
    
    def _gerar_prompt_system(self) -> str:        
        listCamposDetalhados = []
        strShot  = "\nExemplo(s):\n"        
        for chave, valor in self.camposDescricao.items():
            linha = f"- {chave}: {valor['descricao']}\n"
            if valor.get('exemplos'):
                linha += f"Termos corretos: {', '.join(str(ex) for ex in valor['exemplos'])}\n"  
            if valor.get('shot'):
                for shot in valor["shot"][:3]:                    
                    for chave_1,valor_1 in shot.items():
                        strShot += f"{chave_1} = {valor_1}\n"
            listCamposDetalhados.append(linha)
        
        campos_str = "\n".join(listCamposDetalhados) + strShot 
        
        return f"""
        Você é um assistente especializado em busca de veículos automotivos.

        O usuário irá descrever o tipo de carro que deseja ou fazer perguntas sobre veículos.
        Sua tarefa é extrair informações relevantes e convertê-las em filtros de busca.        

        INSTRUÇÕES:
        1. Analise a mensagem do usuário e identifique quais campos podem ser extraídos
        2. Para campos de texto (str*): use valores exatos quando mencionados
        3. Para campos booleanos (bool*): use true/false baseado na intenção do usuário
        4. Para campos numéricos: extraia valores específicos ou ranges quando possível
        5. Se o usuário mencionar faixa de preços, use apenas o valor máximo em numValor
        6. Para anos, aceite tanto formato "2020" quanto 2020, mas sempre retorne como string
        7. Ignore informações irrelevantes para busca de veículos
        8. O nome da marca pode estar incorreto. Averigue em "Termos corretos" e corrija se precisar.

        FORMATO DE RESPOSTA:
        Retorne APENAS um JSON válido, sem explicações adicionais.
        Se nenhum filtro puder ser extraído, retorne um objeto vazio {{}}.

       CAMPOS DISPONÍVEIS COM DESCRIÇÃO, TERMOS CORRETOS E EXEMPLOS:
       {campos_str}
        """
    
    def _interpretar_mensagem(self, mensagem_usuario: str) -> Dict[str, Any]:        
                                
        try:
            resposta = self.client.chat.completions.create(
                model=self.llmModel, 
                messages=[
                    {"role": "system", "content": self.prompt_system},
                    {"role": "user", "content": mensagem_usuario}
                ],
                temperature=0.2, 
                max_tokens=500
            )            
            
            conteudo = resposta.choices[0].message.content.strip()
            self.logger.debug(f"Resposta da IA: {conteudo}")
            
            conteudo = re.sub(r"^```(?:json)?|```$", "", conteudo, flags=re.IGNORECASE).strip()
            
            return json.loads(conteudo)            
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Erro ao fazer parse do JSON: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Erro ao interpretar mensagem: {e}")
            return {}
    
    def _validar_filtros(self, filtros: Dict[str, Any]) -> Dict[str, Any]:                        
        dictFiltrosValidados = {}

        for campo, valor in filtros.items():
            strInfo = self.camposDescricao.get(campo)
            if not strInfo:
                continue

            tipo_coluna = strInfo["tipo"]
            valores_validados = []

            #Lista
            valores = valor if isinstance(valor, list) else [valor]

            for item in valores:
                if "FLOAT" in tipo_coluna and isinstance(item, (int, float)):
                    valores_validados.append(float(item))
                elif "INTEGER" in tipo_coluna and isinstance(item, (int, float)):
                    valores_validados.append(int(item))
                elif "BOOLEAN" in tipo_coluna and isinstance(item, bool):
                    valores_validados.append(item)
                elif "CHAR" in tipo_coluna or "TEXT" in tipo_coluna:
                    if isinstance(item, str):
                        valores_validados.append(item.strip())

            if valores_validados:
                # Apenas 1- ùnico
                dictFiltrosValidados[campo] = valores_validados if len(valores_validados) > 1 else valores_validados[0]

        return dictFiltrosValidados
        
    def _gerar_resposta_amigavel(self, resultados: List, excluir:List[str] = None) -> str:        
        if not resultados:
            return "Não encontrei veículos que correspondam aos critérios especificados. Tente ajustar sua busca."
        
        dadosDict = [dado.to_dict(excluir=excluir) for dado in resultados ]        
        quantidade = len(resultados)

        if quantidade == 1:
            return f"Encontrei 1 veículo que atende seus critérios!\n {tabulate(dadosDict, headers='keys', tablefmt='fancy_grid')}"
        else:
            return f"Encontrei {quantidade} veículos que atendem seus critérios! \n {tabulate(dadosDict, headers='keys', tablefmt='pretty')} \n Vamos realizar outra consulta? Caso deseje sair, digite 'bye' :)"
                
    def consultar_veiculos(self, mensagem_usuario: str, excluir:List[str] = None) -> List:        
        try:            
            self.logger.info(f"Enter!")
            
            strFiltroBruto = self._interpretar_mensagem(mensagem_usuario)
            self.logger.info(f"Filtros extraído(s): {strFiltroBruto}")
                    
            objFiltros = self._validar_filtros(strFiltroBruto)
            self.logger.info(f"Filtros validado(s): {objFiltros}")            

            self.logger.info(f"Encontrado(s) {len(objFiltros)} filtro(s) , {objFiltros}")

            if objFiltros:
                resultados = self.repositorio.buscar_veiculos(objFiltros,1)
                self.logger.info(f"Encontrado(s) {len(resultados)} veículo(s)")
                return self._gerar_resposta_amigavel(resultados,excluir)
            else:
                # Sem filtro,  busca padrão
                return  self.repositorio.buscar_veiculos({},1)
                
        except Exception as e:
            self.logger.error(f"Erro na busca de veículos: {e}")
            return []    
