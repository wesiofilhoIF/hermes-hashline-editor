# Hermes Hashline Editor Plugin

*Read this in [English](#english-version) | Leia em [Português](#versão-em-português)*

---

<a id="english-version"></a>
## 🇺🇸 English Version

A native plugin for Hermes agents (Zeta, Okarun, Ash, etc.) that introduces the **Hashline** editing primitive (inspired by the Oh-My-Pi engine).

### The Problem
Traditional LLM agents use "Unified Diff" operations or fuzzy string replacement. If the LLM makes a typo with a whitespace or indentation, the patch fails (`string-not-found`) or corrupts the code format (critical in `.yaml` or `.py` files).

### The Solution: Hashline
This plugin does not search for text when editing. It reads the file and assigns a **Cryptographic Hash (FNV-1a)** to each line based on its normalized content. 
The LLM no longer rewrites large blocks of old code; it anchors the edit using the Hash identity: e.g., `2:f7`. 
If line `2` on the disk no longer has the `f7` hash (someone else edited it in the meantime), the patch is rejected immediately before causing any damage.

### Injected LLM Tools
- `read_hashline(path, start_line, end_line)`: Returns the formatted text as `NUM:HASH| CONTENT`.
- `patch_hashline(path, operations)`: Applies deterministic operations (`replace`, `insert_after`, `insert_before`, `delete`) based on the line ID and its Hash.

---

<a id="versão-em-português"></a>
## 🇧🇷 Versão em Português

Um plugin nativo para agentes Hermes (Zeta, Okarun, Ash, etc.) que introduz a primitiva de edição por **Hashline** (inspirada na engine do Oh-My-Pi).

### O Problema
Agentes LLM tradicionais usam operações de "Unified Diff" ou substituição de strings. Se o LLM erra um espaço em branco, o patch falha (`string-not-found`) ou corrompe a indentação (crítico em `.yaml` ou `.py`).

### A Solução: Hashline
Este plugin não edita buscando texto. Ele lê o arquivo e atribui um **Hash criptográfico (FNV-1a)** para cada linha baseado no seu conteúdo normalizado.
O LLM não reescreve blocos velhos de código; ele ancora a edição usando o Hash: `2:f7`. 
Se a linha `2` no disco não tiver mais o hash `f7` (alguém editou no meio tempo), o patch é rejeitado imediatamente antes de causar danos.

### Tools Injetadas no Hermes
- `read_hashline(path, start_line, end_line)`: Retorna o texto formatado `NUM:HASH| CONTEUDO`.
- `patch_hashline(path, operations)`: Aplica operações determinísticas de `replace`, `insert_after`, `insert_before` e `delete` baseadas no ID da linha e seu Hash.

---

## 🤖 Para Agentes de IA: Como Instalar (Prompt)
Se você é um agente LLM ajudando um usuário a instalar este plugin, copie e siga o fluxo abaixo.

```text
================================================================
INSTALAR PLUGIN HERMES HASHLINE EDITOR
================================================================
Contexto: O usuário quer instalar a funcionalidade de Hashline no Hermes.

PASSO 0 — DESCOBERTA
0.1. Identifique os perfis Hermes do usuário.
     Geralmente ficam em: `~/.hermes/profiles/`
     Pergunte em qual perfil (ex: zeta, ash, default) o plugin deve ser ativado.

PASSO 1 — CLONAR O REPOSITÓRIO
1.1. Baixe o código fonte para uma pasta de trabalho local:
     cd ~/workspace (ou diretório preferido do usuário)
     git clone https://github.com/wesiofilhoIF/hermes-hashline-editor.git

PASSO 2 — CRIAR O LINK NO PERFIL
2.1. Crie a pasta de plugins no perfil alvo (ex: zeta) se não existir:
     mkdir -p ~/.hermes/profiles/<PROFILE>/plugins
2.2. Faça o symlink:
     ln -snf ~/workspace/hermes-hashline-editor ~/.hermes/profiles/<PROFILE>/plugins/hermes-hashline-editor

PASSO 3 — ATIVAR NO CONFIG.YAML
3.1. Edite o arquivo `~/.hermes/profiles/<PROFILE>/config.yaml`.
3.2. Localize a seção `plugins:` -> `enabled:`.
3.3. Adicione `- hermes-hashline-editor` à lista.

PASSO 4 — REINICIAR E VALIDAR
4.1. Reinicie o gateway do Hermes:
     systemctl --user restart hermes-gateway-<PROFILE>.service
4.2. Confirme que as tools `read_hashline` e `patch_hashline` estão disponíveis.
```
