def parse_text(t):
    if 'SPOLU' in t:
        return 'SPOLU'
    if 'Pir' in t:
        return 'PirátiSTAN'
    if 'ANO' in t:
        return 'ANO'
    if 'SPD' in t:
        return 'SPD'
    if 'nevol' in t or 'nehlas' in t or 'ne,' in t or 'ne.' in t or 'nezú' in t:
        return 'nevolil'

    raise ValueError(f"Unknown party: {t}")
