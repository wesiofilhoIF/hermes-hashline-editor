# Hermes Hashline Editor Plugin

Um plugin nativo para agentes Hermes (Zeta, Okarun, Ash, etc.) que introduz a primitiva de edição por **Hashline** (inspirada na engine do Oh-My-Pi).

## O Problema
Agentes LLM tradicionais usam operações de "Unified Diff" ou substituição de strings. Se o LLM erra um espaço em branco, o patch falha (`string-not-found`) ou corrompe a indentação (crítico em `.yaml` ou `.py`).

## A Solução: Hashline
Este plugin não edita buscando texto. Ele lê o arquivo e atribui um **Hash criptográfico (FNV-1a)** para cada linha baseado no seu conteúdo normalizado.
O LLM não reescreve blocos velhos de código; ele ancora a edição usando o Hash: `2:f7`. 
Se a linha `2` no disco não tiver mais o hash `f7` (alguém editou no meio tempo), o patch é rejeitado imediatamente antes de causar danos.

## Tools Injetadas no Hermes
- `read_hashline(path, start_line, end_line)`: Retorna o texto formatado `NUM:HASH| CONTEUDO`.
- `patch_hashline(path, operations)`: Aplica operações determinísticas de `replace`, `insert_after`, `insert_before` e `delete` baseadas no ID da linha e seu Hash.
