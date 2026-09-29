"""
Ponto de entrada do plugin hermes-hashline-editor.
Registra as ferramentas de leitura e edição baseadas em hash no contexto do Hermes.
"""
from typing import List, Dict, Any
from .hermes_hashline.patcher import read_hashline_file, apply_hashline_operations

def register(ctx):
    # O contexto Hermes deve fornecer uma API para registrar ferramentas para o LLM.
    
    @ctx.tool(name="read_hashline", description="Lê um arquivo convertendo-o para o formato Hashline (NUM:HASH|CONTEUDO) para edição precisa.")
    def read_hashline(path: str, start_line: int = 1, end_line: int = None) -> str:
        return read_hashline_file(path, start_line, end_line)

    @ctx.tool(name="patch_hashline", description="Aplica edições estruturadas no arquivo usando âncoras de Hashline. Ações: replace, insert_after, insert_before, delete.")
    def patch_hashline(path: str, operations: List[Dict[str, Any]]) -> str:
        """
        operations deve ser uma lista de dicionários:
        [{ "action": "replace", "start": "2:f7", "end": "3:a1", "new_content": "texto..." }]
        """
        return apply_hashline_operations(path, operations)
