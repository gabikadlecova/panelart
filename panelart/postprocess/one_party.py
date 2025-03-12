def parse_text(t):
    try:
        if "2021 jsem volila, ale stranu neuvádím." in t or 'ale neřeknu' in t or 'ale neřekla pro' in t or 'strana neuvedena' in t or 'Dobrý den' in t or 'ale nepamatuji' in t or 'ale neřekl' in t or 'ano, STRANA' in t or 'yes, PARTY' in t:
            return None

        if "Pardon, ale" in t or 'ale neuvedl jsem' in t or 'Zde je odpověď ve správném formátu:' in t or 'Omlouvám se, ale' in t or 'nechtěla bych uvést' in t or 'soukromí nemohu uvést' in t:
            return None
        
        if 'ale nebudu uvádět, kterou stranu jsem volil' in t or 'Did not vote:' in t:
            return None

        if 'Ve volbách do poslanecké sněmovny 2021 jsem NEVOLIL/A' in t:
            return 'nevolil'

        if t == 'no':
            return 'nevolil'

        t = t.replace('volila', 'volil')
        if 'jsem volil ' in t:
            t = t.split('jsem volil ')[-1]

        if 'SPOLU' in t or 'TOP 09' in t or 'ODS' in t or 'Spolu' in t:
            return 'SPOLU'
        elif 'irátsk' in t or 'irátská' in t or 'iráty' in t or 'STAN' in t or 'iráti' in t or 'PirStan' in t:
            return 'PirátiSTAN'
        elif 'ANO' in t:
            return 'ANO'
        elif 'SPD' in t:
            return 'SPD'
        elif 'KSČM' in t:
            return 'KSČM'
        elif 'ČSSD' in t:
            return "jiná strana"
        elif 'nevol' in t or 'nehlas' in t or 'ne,' in t or 'ne.' in t or 'nezú' in t:
            return 'nevolil'
        #else:
        #    return None

        raise ValueError(f"Unknown party: {t}")

    except Exception as e:
        print(f"Unknown: {t}")
