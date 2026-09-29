import os
from .algo import line_hash

def read_hashline_file(path: str, start_line: int = 1, end_line: int = None) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        
    output = []
    limit = end_line if end_line else len(lines)
    for i in range(start_line - 1, min(limit, len(lines))):
        num = i + 1
        text = lines[i]
        h = line_hash(text)
        output.append(f"{num}:{h}|{text}")
        
    return "\n".join(output)

def apply_hashline_operations(path: str, operations: list) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
        
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        
    def parse_anchor(anchor):
        parts = anchor.split(':')
        return int(parts[0]), parts[1]
        
    ops = []
    for op in operations:
        start_num, start_hash = parse_anchor(op['start'])
        end_num, end_hash = parse_anchor(op.get('end', op['start']))
        ops.append({
            'start_num': start_num,
            'start_hash': start_hash,
            'end_num': end_num,
            'end_hash': end_hash,
            'action': op['action'],
            'content': op.get('new_content', '').splitlines() if op.get('new_content') is not None else []
        })
        
    ops.sort(key=lambda x: x['start_num'], reverse=True)
    
    for op in ops:
        s_idx = op['start_num'] - 1
        e_idx = op['end_num'] - 1
        
        if s_idx >= len(lines) or line_hash(lines[s_idx]) != op['start_hash']:
            found = line_hash(lines[s_idx]) if s_idx < len(lines) else 'EOF'
            raise ValueError(f"Hash mismatch na linha {op['start_num']}. Esperado {op['start_hash']}, encontrado {found}. Leia o arquivo novamente.")
        if e_idx >= len(lines) or line_hash(lines[e_idx]) != op['end_hash']:
            found = line_hash(lines[e_idx]) if e_idx < len(lines) else 'EOF'
            raise ValueError(f"Hash mismatch na linha {op['end_num']}. Esperado {op['end_hash']}, encontrado {found}. Leia o arquivo novamente.")
            
        if op['action'] == 'replace':
            lines = lines[:s_idx] + op['content'] + lines[e_idx + 1:]
        elif op['action'] == 'insert_after':
            lines = lines[:e_idx + 1] + op['content'] + lines[e_idx + 1:]
        elif op['action'] == 'insert_before':
            lines = lines[:s_idx] + op['content'] + lines[s_idx:]
        elif op['action'] == 'delete':
            lines = lines[:s_idx] + lines[e_idx + 1:]
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")
        
    return "Edição Hashline aplicada com sucesso. Arquivo atualizado."
