def line_hash(line: str) -> str:
    """Compute the FNV-1a 8-bit hash of a normalized line."""
    normalized = line.strip().encode('utf-8')
    hash_val = 2166136261
    for byte in normalized:
        hash_val ^= byte
        hash_val = (hash_val * 16777619) & 0xFFFFFFFF
    return f"{(hash_val & 0xFF):02x}"
