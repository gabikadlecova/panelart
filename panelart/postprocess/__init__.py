def parse_party(vote):
    if 'ANO' in vote:
        return 'ANO'
    if 'Komu' in vote:
        return 'KSČM'
    if 'Spolu' in vote:
        return 'SPOLU'
    if 'STAR' in vote:
        return 'PirátiSTAN'
    if 'SPD' in vote:
        return 'SPD'
    if 'Robert' in vote:
        return 'PŘÍSAHA'
    if 'SSD' in vote or 'Tri' in vote or 'iná' in vote:
        return 'jiná strana'
    if 'Nebyl' in vote:
        return 'nevolil'
    if 'Nechci' in vote or 'Nevím' in vote:
        return 'neuvedeno'
    raise ValueError()
