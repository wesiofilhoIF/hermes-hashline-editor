"""
Ponto de entrada do plugin hermes-hashline-editor.
Registra as ferramentas de leitura e edição baseadas em hash no contexto do Hermes.
"""
from typing import List, Dict, Any
from .hermes_hashline.patcher import read_hashline_file, apply_hashline_operations

READ_HASHLINE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "path": {
            "type": "STRING",
            "description": "Caminho absoluto para o arquivo que será lido em formato Hashline."
        },
        "start_line": {
            "type": "INTEGER",
            "description": "Linha inicial da leitura (opcional)."
        },
        "end_line": {
            "type": "INTEGER",
            "description": "Linha final da leitura (opcional)."
        }
    },
    "required": ["path"]
}

PATCH_HASHLINE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "path": {
            "type": "STRING",
            "description": "Caminho absoluto do arquivo a ser modificado."
        },
        "operations": {
            "type": "ARRAY",
            "description": "Lista de operações ancoradas em Hashline.",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "action": {
                        "type": "STRING",
                        "enum": ["replace", "insert_after", "insert_before", "delete"],
                        "description": "Ação a ser realizada na âncora."
                    },
                    "start": {
                        "type": "STRING",
                        "description": "Âncora inicial com formato NUM:HASH (ex: '2:f7')."
                    },
                    "end": {
                        "type": "STRING",
                        "description": "Âncora final com formato NUM:HASH (ex: '3:a1'). Omitir se a operação afetar apenas a linha inicial."
                    },
                    "new_content": {
                        "type": "STRING",
                        "description": "Novo código/texto a ser inserido (obrigatório para replace e insert)."
                    }
                },
                "required": ["action", "start"]
            }
        }
    },
    "required": ["path", "operations"]
}

def tool_read_hashline(arguments: Dict[str, Any]) -> str:
    path = arguments.get("path")
    start_line = arguments.get("start_line", 1)
    end_line = arguments.get("end_line", None)
    try:
        return read_hashline_file(path, start_line, end_line)
    except Exception as e:
        return f"Erro ao ler arquivo em Hashline: {str(e)}"

def tool_patch_hashline(arguments: Dict[str, Any]) -> str:
    path = arguments.get("path")
    operations = arguments.get("operations", [])
    try:
        return apply_hashline_operations(path, operations)
    except Exception as e:
        return f"Erro ao aplicar Hashline Patch: {str(e)}"

def register(ctx):
    ctx.register_tool(
        name="read_hashline",
        schema=READ_HASHLINE_SCHEMA,
        handler=tool_read_hashline,
        toolset="hashline",
        description="Lê um arquivo convertendo-o para o formato Hashline (NUM:HASH|CONTEUDO) para edição precisa. Use sempre antes de aplicar patches."
    )

    ctx.register_tool(
        name="patch_hashline",
        schema=PATCH_HASHLINE_SCHEMA,
        handler=tool_patch_hashline,
        toolset="hashline",
        description="Aplica edições estruturadas no arquivo usando âncoras de Hashline. Exige que a linha seja idêntica ao Hash da última leitura. Ações suportadas: replace, insert_after, insert_before, delete."
    )
