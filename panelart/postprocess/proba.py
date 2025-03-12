import numpy as np


def parse_resp(r):
    # incorrect format fixing, separate vote section and party section
    r = r.replace('volila', 'volil')
    r = r.replace('volil, 0.65 a]', '[volil, 0.65]').replace('volil, 0.55 a]', '[volil, 0.55]').strip('*').strip(';').replace(']]', ']').strip()
    r = r.replace(' a]', ']').replace(' b]', ']')
    voted, parties = r.split(']; [')

    # vote section
    volil, nevolil = voted.split('], [')
    volil = volil.strip('[')
    nevolil = nevolil.strip(']')
    res_volil = {}
    
    def get_pb_name(v):
        name, pb = v.split(', ')
        name = name.strip('"')
        pb = float(pb)
        res_volil[name] = pb

    get_pb_name(volil)
    get_pb_name(nevolil)
    assert len(res_volil) == 2
    
    # party section
    ps, pbs = [], []
    for val in parties.split('], ['):
        val = val.replace('proba ', '')
        val = val.replace('[', '').replace(']', '')
        p, pb = val.split(', ')
        p = p.strip('"')
        ps.append(p)
        pbs.append(float(pb))

    return res_volil, ps, pbs


val = {
    'i': 0
}


def parse_text(pred):
    try:

        if "ODS, 0.30, ANO, 0.20" in pred or 'Omlouvám se, ale nemohu' in pred or 'Je mi líto, ale' in pred or '*[], []' in pred or 'Promiň, ale nemohu' in pred or "I'm sorry, but I can't assist with that request" in pred or 'olil' not in pred:
            return None
        
        if "Ve volbách do poslanecké sněmovny 2021 jsem" in pred or 'Ve volbách do Poslanecké sněmovny 2021 jsem' in pred or 'Volila jsem ve volbách do Poslanecké sněmovny v roce 2021' in pred:
            return None
        
        if "Zde je můj odhad," in pred or 'poměrně vysoká, odhadem 80%' in pred or 'jsem s pravděpodobností 65 % volila hnutí ANO 2011' in pred:
            return None

        if 'že respondent volil, velmi vysoká, odhadem 85 %.' in pred:
            return None
        
        if 'že respondentka volila ve volbách do Poslanecké sněmovny' in pred:
            return None

        if 'Pokud volila, je pravděpodobné, že volila stranu SPD' in pred or ' nejpravděpodobnější je, že volil hnutí ANO' in pred:
            return None
        
        if 'Pravděpodobnost, že respondent volil ve volbách do Poslanecké sněmovny' in pred:
            return None
        
        if 'Ve volbách do poslanecké sněmovny v roce 2021 jsem s pravděpodobností' in pred or 'Ve volbách do poslanecké sněmovny 2021 je pravděpodobnost' in pred or 'Podle poskytnutých informací o respondentovi odhaduji následující:' in pred:
            return None

        if 'Šance, že tato žena volila ve' in pred or 'Šance, že respondent volil ve volbách do Poslanecké sněmovny' in pred or 'Šance, že respondentka volila' in pred:
            return None
        
        if 'Poslanecké sněmovny v roce 2021 jsem s pravděpodobností' in pred or 'Pravděpodobnost, že respondentka volila ve' in pred or 'Šance, že tato respondentka volila' in pred:
            return None
        
        if 'Pravděpodobnost, že respondent volil ve "Volby do poslanecké sněmovny 2021", je 70 %' in pred or 'Šance, že respondent volil' in pred or 'Šance, že respondent ve volbách' in pred or 'Ve volbách do poslanecké ' in pred:
            return None
        
        if 'Ve volbách do Poslanecké sněmovny v roce 2021 jsem pravděpodobně nehlasoval.' in pred or 'Šance, že respondentka volila' in pred or 'Ve volbách do poslanecké sněmovny v roce 2021 jsem' in pred or 'Pravděpodobnost, že respondent' in pred:
            return None

        for l in pred.split('\n'):
            if l.startswith('* [') or (l.startswith('*') and not l.startswith('*Pokud') and not l.startswith('* ')):
                pred = l
                break

        if 'Pro určení' in pred:
            pred = pred.split('\n')[2]
    
        ppred = pred
    
        pred = pred.split('Here is the output: ')[-1]
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.3, Piráti a STAN, 0.2, SPOLU, 0.2, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.3], [Piráti a STAN, 0.2], [SPOLU, 0.2], [jiná strana, 0.3]')
        pred = pred.replace('[jiná strana, 0.15]; [nevolil, 0.2]', '[jiná strana, 0.15]').replace('[volil, 0.8], [A', '[volil, 0.8], [nevolil, 0.2]; [A')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPD, 0.50, ANO, 0.30, jiná strana, 0.20', '[volil, 0.85], [nevolil, 0.15]; [SPD, 0.50], [ANO, 0.30], [jiná strana, 0.20]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; SPOLU, 0.4, ANO 2011, 0.3, Piráti a STAN, 0.2, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.4], [ANO 2011, 0.3], [Piráti a STAN, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; SPOLU, 0.4, ANO, 0.3, Piráti a STAN, 0.2, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.4], [ANO, 0.3], [Piráti a STAN, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.8], [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]; [nevolil, 0.2]', '[volil, 0.8], [nevolil, 0.2]; [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; ANO, 0.40, SPD, 0.25, ODS, 0.15, jiná strana, 0.20', '[volil, 0.85], [nevolil, 0.15]; [ANO, 0.40], [SPD, 0.25], [ODS, 0.15], [jiná strana, 0.20]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.3, Piráti a STAN, 0.2, SPOLU, 0.2, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.3], [Piráti a STAN, 0.2], [SPOLU, 0.2], [jiná strana, 0.3]')
        pred = pred.replace('volil, 0.7, nevolil, 0.3; ANO, 0.4, SPD, 0.2, Piráti a STAN, 0.15, ODS, 0.15, jiná strana, 0.1', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.2], [Piráti a STAN, 0.15], [ODS, 0.15], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.8], [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]; [nevolil, 0.2]', '[volil, 0.8], [nevolil, 0.2]; [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]')
        pred = pred.replace('volil, 0.8, [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]; nevolil, 0.2', '[volil, 0.8], [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]; [nevolil, 0.2]')
        pred = pred.replace('volil, 0.65 a], [nevolil, 0.35]; [SPD, 0.25], [ANO, 0.2], [KSČM, 0.15], [jiná strana, 0.05]', '[volil, 0.65], [nevolil, 0.35]; [SPD, 0.25], [ANO, 0.2], [KSČM, 0.15], [jiná strana, 0.05]')
        pred = pred.replace('volil, 0.6, 0.4; ANO, 0.35], [SPD, 0.2], [KSČM, 0.15], [jiná strana, 0.15], [Přísaha, 0.1], [Piráti, 0.05]', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.35], [SPD, 0.2], [KSČM, 0.15], [jiná strana, 0.15], [Přísaha, 0.1], [Piráti, 0.05]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; ANO, 0.4, SPD, 0.3, ODS, 0.1, jiná strana, 0.2', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.4], [SPD, 0.3], [ODS, 0.1], [jiná strana, 0.2]')
        pred = pred.replace('volil, 0.7, nevolil, 0.3; ANO, 0.25], [SPD, 0.25], [KSČM, 0.15], [Piráti, 0.1], [jiná strana, 0.2]', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.25], [SPD, 0.25], [KSČM, 0.15], [Piráti, 0.1], [jiná strana, 0.2]')
        pred = pred.replace('volil, 0.7, nevolil, 0.3; SPD, 0.4, ANO, 0.3, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [SPD, 0.4], [ANO, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('volil, 0.8; nevolil, 0.2; ANO, 0.5, SPD, 0.3, jiná strana, 0.2', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.5], [SPD, 0.3], [jiná strana, 0.2]')
        pred = pred.replace('volil, 0.8; nevolil, 0.2; Piráti a STAN, 0.3, SPOLU (ODS, KDU-ČSL, TOP 09), 0.3, ANO 2011, 0.15, PŘÍSAHA, 0.1, Česká pirátská strana, 0.05, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [Piráti a STAN, 0.3], [SPOLU, 0.3], [ANO 2011, 0.15], [PŘÍSAHA, 0.1], [Česká pirátská strana, 0.05], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.6; nevolil, 0.4; ANO 2011, 0.3, SPD, 0.2, Česká pirátská strana, 0.1', '[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.3], [SPD, 0.2], [Česká pirátská strana, 0.1]')
        pred = pred.replace('volil, 0.6, nevolil, 0.4;', '[volil, 0.6], [nevolil, 0.4];')
        pred = pred.replace('volil, 0.3, nevolil, 0.7;', '[volil, 0.3], [nevolil, 0.7];')
        pred = pred.replace('Spíše volil, 0.7, spíše nevolil, 0.3; SPD, 0.5, ANO, 0.3, jiná strana, 0.2', '[volil, 0.7], [nevolil, 0.3]; [SPD, 0.5], [ANO, 0.3], [jiná strana, 0.2]')
        pred = pred.replace('Volil, 0.6', '[volil, 0.6], [nevolil, 0.4]')
        pred = pred.replace('ANO, 0.5, SPD, 0.3, jiná strana, 0.2', '[ANO, 0.5], [SPD, 0.3], [jiná strana, 0.2]')
        pred = pred.replace('[\n', '[')
        pred = pred.replace('*[-', '*[')
        pred = pred.replace('volil, 0.7, nevolil, 0.3; ANO, 0.4, SPD, 0.2, Koalice SPOLU, 0.15, Piráti a STAN, 0.15, jiná strana, 0.1', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.2], [SPOLU, 0.15], [Piráti a STAN, 0.15], [jiná strana, 0.1]')
        pred = pred.replace('* ', '*')
        pred = pred.replace('],[', '], [')
        pred = pred.replace('volil, 0.4*,', '[volil, 0.4],')
        pred = pred.replace('volil, 0.7;', '[volil, 0.7], [nevolil, 0.3];')
        pred = pred.replace('SPOLU (ODS, KDU-ČSL, TOP 09)', 'SPOLU')
        pred = pred.replace('SPOLU (ODS, KDU-ČSL a TOP 09)', 'SPOLU')
        pred = pred.replace('Spolu (ODS, KDU-ČSL, TOP 09)', 'SPOLU')
        pred = pred.replace('Spolu - ODS, KDU-ČSL, TOP 09', 'SPOLU')
        pred = pred.replace('(', '[').replace(')', ']')
        pred = pred.replace('*; ', '*')
        pred = pred.replace('Piráti a STAN, 0.3, SPOLU, 0.3, ANO 2011, 0.15, PŘÍSAHA, 0.1, Česká pirátská strana, 0.05, jiná strana, 0.1', '[Piráti a STAN, 0.3], [SPOLU, 0.3], [ANO 2011, 0.15], [PŘÍSAHA, 0.1], [Česká pirátská strana, 0.05], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.65, nevolil, 0.35; SPD, 0.40, ANO, 0.25, Trikolóra Svobodní Soukromníci, 0.20, jiná strana, 0.15', '[volil, 0.65], [nevolil, 0.35]; [SPD, 0.40], [ANO, 0.25], [Trikolóra Svobodní Soukromníci, 0.20], [jiná strana, 0.15]')
        pred = pred.replace('volil, 0.7, nevolil, 0.3; SPOLU, 0.4, ANO, 0.3, Piráti a STAN, 0.2, jiná strana, 0.1', '[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.4], [ANO, 0.3], [Piráti a STAN, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; SPOLU, 0.4, Piráti a STAN, 0.3, ANO, 0.2, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('ANO 2011, 0.3, SPD, 0.2, Česká pirátská strana, 0.1', '[ANO 2011, 0.3], [SPD, 0.2], [Česká pirátská strana, 0.1]')
        pred = pred.replace('volil, 0.65;', '[volil, 0.65], [nevolil, 0.35];')
        pred = pred.replace('volil, 0.85;', '[volil, 0.85], [nevolil, 0.15];')
        pred = pred.replace('volil, 0.6;', '[volil, 0.6], [nevolil, 0.4];')
        pred = pred.replace('volil, 0.6; nevolil, 0.4; ANO 2011, 0.3, SPD, 0.2, Česká pirátská strana, 0.1', '[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.3], [SPD, 0.2], [Česká pirátská strana, 0.1]')
        pred = pred.replace('[[', '[').replace(']]', ']').replace('volil, 0.8;', '[volil, 0.8], [nevolil, 0.2];')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4], [nevolil, 0.4];', '[volil, 0.6], [nevolil, 0.4];')
        pred = pred.replace('SPD, 0.4, ANO, 0.3, jiná strana, 0.3', '[SPD, 0.4], [ANO, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; ANO, 0.4, SPD, 0.3, jiná strana, 0.3', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.4], [SPD, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; [ANO, 0.5], [SPD, 0.3], [jiná strana, 0.2]', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.5], [SPD, 0.3], [jiná strana, 0.2]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.4, SPD, 0.3, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.4], [SPD, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; SPD, 0.4, ANO, 0.3, Trikolóra, 0.2, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [SPD, 0.4], [ANO, 0.3], [Trikolóra, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; SPOLU, 0.3, ANO, 0.25, Piráti a STAN, 0.2, jiná strana, 0.25', '[volil, 0.6], [nevolil, 0.4]; [SPOLU, 0.3], [ANO, 0.25], [Piráti a STAN, 0.2], [jiná strana, 0.25]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; ANO, 0.4, SPD, 0.2, ODS, 0.15, KDU-ČSL, 0.15, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.4], [SPD, 0.2], [ODS, 0.15], [KDU-ČSL, 0.15], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; SPOLU, 0.4, Piráti a STAN, 0.3, ANO 2011, 0.2, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO 2011, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.4, ANO 2011, 0.3, Piráti a STAN, 0.15, jiná strana, 0.15', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.4], [ANO 2011, 0.3], [Piráti a STAN, 0.15], [jiná strana, 0.15]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.40, ANO 2011, 0.30, Piráti a STAN, 0.15, jiná strana, 0.15', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.40], [ANO 2011, 0.30], [Piráti a STAN, 0.15], [jiná strana, 0.15]')
        pred = pred.replace('volil, 0.75, nevolil, 0.25; ANO, 0.40, SPD, 0.30, KSČM, 0.15, jiná strana, 0.15', '[volil, 0.75], [nevolil, 0.25]; [ANO, 0.40], [SPD, 0.30], [KSČM, 0.15], [jiná strana, 0.15]')
        pred = pred.replace('*volil, 0.3, nevolil, 0.7; ANO, 0.4, SPD, 0.3, jiná strana, 0.3*', '')
        pred = pred.replace('Volil, 0.55; Nevolil, 0.45; ANO, 0.25; SPOLU, 0.2; Piráti a STAN, 0.15; Přísaha, 0.1; KSČM, 0.05; ČSSD, 0.05; SPD, 0.05; Trikolora, 0.05', '[volil, 0.55], [nevolil, 0.45]; [ANO, 0.25], [SPOLU, 0.2], [Piráti a STAN, 0.15], [Přísaha, 0.1], [KSČM, 0.05], [ČSSD, 0.05], [SPD, 0.05], [Trikolora, 0.05]')

        pred = pred.replace('[volil, 0.8], [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]; [nevolil, 0.2]', '[volil, 0.8], [nevolil, 0.2]; [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.15], [jiná strana, 0.15]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.25], [Piráti, 0.15], [SPOLU, 0.1], [PŘÍSAHA, 0.1], [SPD, 0.05], [KSČM, 0.05], [jiná strana, 0.05]', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.25], [Piráti, 0.15], [SPOLU, 0.1], [PŘÍSAHA, 0.1], [SPD, 0.05], [KSČM, 0.05], [jiná strana, 0.05]')
        
        pred = pred.replace('volil, 0.6, 0.4; ', '[volil, 0.6], [nevolil, 0.4]; [')
        pred = pred.replace('volil, 0.7, 0.3; ', '[volil, 0.7], [nevolil, 0.3]; [')
        pred = pred.replace('volil, 0.8, 0.2; ', '[volil, 0.8], [nevolil, 0.2]; [')
        pred = pred.replace('volil, 0.8, nevolil, 0.2; ', '[volil, 0.8], [nevolil, 0.2]; [')
        pred = pred.replace('volil, 0.7, nevolil, 0.3; ', '[volil, 0.7], [nevolil, 0.3]; [')

        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; Piráti, 0.25, SPOLU, 0.2, ANO, 0.1, STAN, 0.05, jiná strana, 0.05', '[volil, 0.6], [nevolil, 0.4]; [Piráti, 0.25], [SPOLU, 0.2], [ANO, 0.1], [STAN, 0.05], [jiná strana, 0.05]')

        pred = pred.replace('volil, 0.7, [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.1], [jiná strana, 0.1]; nevolil, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.1], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; Piráti, 0.25], [STAN, 0.2], [SPOLU, 0.15], [ANO, 0.1], [jiná strana, 0.1]', '[volil, 0.6], [nevolil, 0.4]; [Piráti, 0.25], [STAN, 0.2], [SPOLU, 0.15], [ANO, 0.1], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.9, 0.1; ANO, 0.45], [Piráti, 0.25], [SPOLU, 0.15], [PŘÍSAHA, 0.05], [jiná strana, 0.1]', '[volil, 0.9], [nevolil, 0.1]; [ANO, 0.45], [Piráti, 0.25], [SPOLU, 0.15], [PŘÍSAHA, 0.05], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.25], [SPD, 0.15], [Piráti, 0.1], [ODS, 0.05], [STAN, 0.03], [jiná strana, 0.02]', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.25], [SPD, 0.15], [Piráti, 0.1], [ODS, 0.05], [STAN, 0.03], [jiná strana, 0.02]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.25], [Piráti, 0.15], [SPOLU, 0.1], [SPD, 0.05], [KSČM, 0.05], [jiná strana, 0.05]', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.25], [Piráti, 0.15], [SPOLU, 0.1], [SPD, 0.05], [KSČM, 0.05], [jiná strana, 0.05]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.25, Piráti, 0.2, SPD, 0.15, KSČM, 0.1, ČSSD, 0.05, jiná strana, 0.05', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.25], [Piráti, 0.2], [SPD, 0.15], [KSČM, 0.1], [ČSSD, 0.05], [jiná strana, 0.05]')
        pred = pred.replace('volil, 0.8, [SPD, 0.3], [ANO, 0.25], [Piráti, 0.15], [KSČM, 0.1]; nevolil, 0.2', '[volil, 0.8], [nevolil, 0.2]; [SPD, 0.3], [ANO, 0.25], [Piráti, 0.15], [KSČM, 0.1]')
        pred = pred.replace('volil, 0.9, nevolil, 0.1; Piráti, 0.45], [STAN, 0.25], [SPOLU, 0.15], [jiná strana, 0.1]', '[volil, 0.9], [nevolil, 0.1]; [Piráti, 0.45], [STAN, 0.25], [SPOLU, 0.15], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.97, 0.03; ANO, 0.55, SPD, 0.25, KSČM, 0.1, ČSSD, 0.05, jiná strana, 0.05', '[volil, 0.97], [nevolil, 0.03]; [ANO, 0.55], [SPD, 0.25], [KSČM, 0.1], [ČSSD, 0.05], [jiná strana, 0.05]')
        pred = pred.replace('volil, 0.6, [SPOLU, 0.2], [ANO, 0.15], [PirátiSTAN, 0.15], [SPD, 0.05], [jiná strana, 0.05]; nevolil, 0.4', '[volil, 0.6], [nevolil, 0.4]; [SPOLU, 0.2], [ANO, 0.15], [PirátiSTAN, 0.15], [SPD, 0.05], [jiná strana, 0.05]')
        pred = pred.replace('volil, 0.7, [ANO 2011, 0.3], [Piráti, 0.2], [SPD, 0.1], [jiná strana, 0.1]; nevolil, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO 2011, 0.3], [Piráti, 0.2], [SPD, 0.1], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.6, [ANO 2011, 0.2], [Piráti, 0.1], [SPOLU, 0.1], [jiná strana, 0.2]; nevolil, 0.4', '[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.2], [Piráti, 0.1], [SPOLU, 0.1], [jiná strana, 0.2]')
        pred = pred.replace('volil, 0.6, [ANO 2011, 0.3], [Piráti, 0.2], [SPD, 0.1]; nevolil, 0.4', '[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.3], [Piráti, 0.2], [SPD, 0.1]')
        pred = pred.replace('[volil, 0.8], [nevolil, 0.2]; [ANO, 0.25, Piráti, 0.2, SPD, 0.15, STAN, 0.1, ČSSD, 0.05, KSČM, 0.05, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.25], [Piráti, 0.2], [SPD, 0.15], [STAN, 0.1], [ČSSD, 0.05], [KSČM, 0.05], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.95, 0.05], [Piráti, 0.45, SPD, 0.3, ANO, 0.15, KSČM, 0.1]; ', '[volil, 0.95], [nevolil, 0.05]; [Piráti, 0.45], [SPD, 0.3], [ANO, 0.15], [KSČM, 0.1]; ')
        pred = pred.replace('volil, 0.65, 0.35; ANO, 0.25, SPD, 0.2, KSČM, 0.15, ČSSD, 0.1, jiná strana, 0.05', '[volil, 0.65], [nevolil, 0.35]; [ANO, 0.25], [SPD, 0.2], [KSČM, 0.15], [ČSSD, 0.1], [jiná strana, 0.05]')
        pred = pred.replace('volil, 0.6, [SPOLU, 0.2], [ANO, 0.15], [Piráti, 0.1], [STAN, 0.05], [jiná strana, 0.1]; nevolil, 0.4', '[volil, 0.6], [nevolil, 0.4]; [SPOLU, 0.2], [ANO, 0.15], [Piráti, 0.1], [STAN, 0.05], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.7, [SPOLU, 0.35], [Piráti, 0.25], [STAN, 0.1]; nevolil, 0.3', '[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.35], [Piráti, 0.25], [STAN, 0.1]')
        pred = pred.replace('volil, 0.95, 0.05; Piráti, 0.45, STAN, 0.25, SPOLU, 0.2, ANO, 0.05, jiná strana, 0.05', '[volil, 0.95], [nevolil, 0.05]; [Piráti, 0.45], [STAN, 0.25], [SPOLU, 0.2], [ANO, 0.05], [jiná strana, 0.05]')
        pred = pred.replace('[volil, 0.7, PirSTAN, 0.7]], [nevolil, 0.3]; ANO, 0.15], [SPOLU, 0.15], [Piráti, 0.1], [STAN, 0.1], [jiná strana, 0.1]', '[volil, 0.7], [nevolil, 0.3]; [PirSTAN, 0.7], [ANO, 0.15], [SPOLU, 0.15], [Piráti, 0.1], [STAN, 0.1], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.6, [ANO 2011, 0.3], [Piráti, 0.15], [SPD, 0.1], [jiná strana, 0.05]; nevolil, 0.4', '[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.3], [Piráti, 0.15], [SPD, 0.1], [jiná strana, 0.05]')
        pred = pred.replace('volil, 0.95, 0.05; Piráti, 0.35], [SPOLU, 0.3], [PŘÍSAHA, 0.2], [STAN, 0.1], [jiná strana, 0.05]', '[volil, 0.95], [nevolil, 0.05]; [Piráti, 0.35], [SPOLU, 0.3], [PŘÍSAHA, 0.2], [STAN, 0.1], [jiná strana, 0.05]')
        pred = pred.replace('volil, 0.6, [ANO 2011, 0.2], [Piráti, 0.15], [SPOLU, 0.15], [jiná strana, 0.1]; nevolil, 0.4', '[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.2], [Piráti, 0.15], [SPOLU, 0.15], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.6, [SPOLU, 0.3], [ANO, 0.2], [Piráti, 0.1], [jiná strana, 0.0]; nevolil, 0.4', '[volil, 0.6], [nevolil, 0.4]; [SPOLU, 0.3], [ANO, 0.2], [Piráti, 0.1], [jiná strana, 0.0]')
        pred = pred.replace('volil, 0.7, [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.1], [jiná strana, 0.1]; nevolil, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO 2011, 0.3], [Piráti, 0.2], [SPOLU, 0.1], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.7, [SPOLU, 0.3], [Piráti, 0.2], [STAN, 0.1], [PŘÍSAHA, 0.1]; nevolil, 0.3', '[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.3], [Piráti, 0.2], [STAN, 0.1], [PŘÍSAHA, 0.1]')
        pred = pred.replace('volil, 0.7, [ANO 2011, 0.3], [SPOLU, 0.2], [Piráti a STAN, 0.1], [PŘÍSAHA, 0.1]; nevolil, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO 2011, 0.3], [SPOLU, 0.2], [Piráti a STAN, 0.1], [PŘÍSAHA, 0.1]')
        pred = pred.replace('volil, 0.7, [SPOLU, 0.3], [ANO, 0.2], [Piráti, 0.1], [jiná strana, 0.1]; nevolil, 0.3', '[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.3], [ANO, 0.2], [Piráti, 0.1], [jiná strana, 0.1]')

        pred = pred.replace('[volil, 0.3], [nevolil, 0.7]; ANO, 0.4, SPD, 0.3, jiná strana, 0.3', '[volil, 0.3], [nevolil, 0.7]; [ANO, 0.4], [SPD, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [SPD, 0.5, ANO, 0.3, jiná strana, 0.2', '[volil, 0.7], [nevolil, 0.3]; [SPD, 0.5], [ANO, 0.3], [jiná strana, 0.2]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.40, ANO 2011, 0.30, Piráti a STAN, 0.20, jiná strana, 0.10', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.40], [ANO 2011, 0.30], [Piráti a STAN, 0.20], [jiná strana, 0.10]')
        pred = pred.replace('volil, 0.75, nevolil, 0.25; SPD, 0.40, ANO, 0.30, Trikolóra, 0.20, jiná strana, 0.10', '[volil, 0.75], [nevolil, 0.25]; [SPD, 0.40], [ANO, 0.30], [Trikolóra, 0.20], [jiná strana, 0.10]')
        pred = pred.replace('[volil, 0.8], [nevolil, 0.2]; [ANO, 0.4, SPD, 0.3, ODS, 0.2, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.4], [SPD, 0.3], [ODS, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; SPOLU, 0.3, ANO, 0.25, Piráti a STAN, 0.15, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [SPOLU, 0.3], [ANO, 0.25], [Piráti a STAN, 0.15], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.4, SPD, 0.2, jiná strana, 0.4', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.4], [SPD, 0.2], [jiná strana, 0.4]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPD, 0.2, ODS, 0.1, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.2], [ODS, 0.1], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; Piráti a STAN, 0.3, SPOLU, 0.25, ANO 2011, 0.15, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [Piráti a STAN, 0.3], [SPOLU, 0.25], [ANO 2011, 0.15], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.8], [nevolil, 0.2]; [SPD, 0.5, ANO, 0.3, jiná strana, 0.2', '[volil, 0.8], [nevolil, 0.2]; [SPD, 0.5], [ANO, 0.3], [jiná strana, 0.2]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPD, 0.2, ČSSD, 0.1, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.2], [ČSSD, 0.1], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.3, ANO 2011, 0.25, Piráti a STAN, 0.2, jiná strana, 0.25', '[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.3], [ANO 2011, 0.25], [Piráti a STAN, 0.2], [jiná strana, 0.25]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPD, 0.3, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [Piráti a STAN, 0.4, SPOLU, 0.3, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [Piráti a STAN, 0.4], [SPOLU, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.35, ANO 2011, 0.25, Piráti a STAN, 0.20, jiná strana, 0.20', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.35], [ANO 2011, 0.25], [Piráti a STAN, 0.20], [jiná strana, 0.20]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.35, Piráti a STAN, 0.30, ANO 2011, 0.20, jiná strana, 0.15', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.35], [Piráti a STAN, 0.30], [ANO 2011, 0.20], [jiná strana, 0.15]')
        pred = pred.replace('[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.3, ANO, 0.25, Piráti a STAN, 0.2, ČSSD, 0.15, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.3], [ANO, 0.25], [Piráti a STAN, 0.2], [ČSSD, 0.15], [jiná strana, 0.1]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.35, ANO, 0.25, Piráti a STAN, 0.20, jiná strana, 0.20', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.35], [ANO, 0.25], [Piráti a STAN, 0.20], [jiná strana, 0.20]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPD, 0.2, ODS, 0.1, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.2], [ODS, 0.1], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.4, Piráti a STAN, 0.3, ANO 2011, 0.2, jiná strana, 0.1', '[volil, 0.7], [nevolil, 0.3]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO 2011, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; Piráti a STAN, 0.3, SPOLU, 0.25, ANO, 0.15, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [Piráti a STAN, 0.3], [SPOLU, 0.25], [ANO, 0.15], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPD, 0.2, Piráti, 0.1, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.2], [Piráti, 0.1], [jiná strana, 0.3]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.35, ANO, 0.30, Piráti a STAN, 0.15, jiná strana, 0.20', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.35], [ANO, 0.30], [Piráti a STAN, 0.15], [jiná strana, 0.20]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPD, 0.40, ANO, 0.30, Trikolóra, 0.15, jiná strana, 0.15', '[volil, 0.85], [nevolil, 0.15]; [SPD, 0.40], [ANO, 0.30], [Trikolóra, 0.15], [jiná strana, 0.15]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; SPOLU, 0.3, Piráti a STAN, 0.25, ANO 2011, 0.2, jiná strana, 0.15, ČSSD, 0.1', '[volil, 0.6], [nevolil, 0.4]; [SPOLU, 0.3], [Piráti a STAN, 0.25], [ANO 2011, 0.2], [jiná strana, 0.15], [ČSSD, 0.1]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; ANO, 0.35, ODS, 0.25, Piráti a STAN, 0.15, SPD, 0.10, jiná strana, 0.15', '[volil, 0.85], [nevolil, 0.15]; [ANO, 0.35], [ODS, 0.25], [Piráti a STAN, 0.15], [SPD, 0.10], [jiná strana, 0.15]')
        pred = pred.replace('volil, 0.85, nevolil, 0.15; SPOLU, 0.40, ANO 2011, 0.25, Piráti a STAN, 0.20, jiná strana, 0.15', '[volil, 0.85], [nevolil, 0.15]; [SPOLU, 0.40], [ANO 2011, 0.25], [Piráti a STAN, 0.20], [jiná strana, 0.15]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPD, 0.3, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.3], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; SPD, 0.3, ANO, 0.25, Trikolora, 0.15, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [SPD, 0.3], [ANO, 0.25], [Trikolora, 0.15], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPD, 0.2, ČSSD, 0.1, jiná strana, 0.3', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPD, 0.2], [ČSSD, 0.1], [jiná strana, 0.3]')
        pred = pred.replace('[[volil, 0.8], [nevolil, 0.2]], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO, 0.2], [jiná strana, 0.1]', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4, SPOLU, 0.3, Piráti a STAN, 0.2, jiná strana, 0.1', '[volil, 0.7], [nevolil, 0.3]; [ANO, 0.4], [SPOLU, 0.3], [Piráti a STAN, 0.2], [jiná strana, 0.1]')
        pred = pred.replace('[volil, 0.7], [nevolil, 0.3]; [SPD, 0.4, ANO, 0.3, jiná strana, 0.2, KSČM, 0.1', '[volil, 0.7], [nevolil, 0.3]; [SPD, 0.4], [ANO, 0.3], [jiná strana, 0.2], [KSČM, 0.1]')
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; SPOLU, 0.3, ANO, 0.25, Piráti a STAN, 0.15, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [SPOLU, 0.3], [ANO, 0.25], [Piráti a STAN, 0.15], [jiná strana, 0.3]')
        pred = pred.replace('[volil, 0.8], [nevolil, 0.2]; [ANO, 0.4, SPD, 0.3, ODS, 0.2, jiná strana, 0.1', '[volil, 0.8], [nevolil, 0.2]; [ANO, 0.4], [SPD, 0.3], [ODS, 0.2], [jiná strana, 0.1]')

        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.2], [SPOLU, 0.15], [Piráti a STAN, 0.1], [Piráti, 0.05], [jiná strana, 0.05], [SPD, 0.05], [KSČM, 0.05], [ČSSD, 0.05], [Přísaha, 0.05], [Trikolora, 0.05], [DSSS, 0.05], [Volte Pravý Blok, 0.05], [Nezávislí, 0.05], [Moravané, 0.05]', '[volil, 0.6], [nevolil, 0.4]; [ANO 2011, 0.2], [SPOLU, 0.15], [Piráti a STAN, 0.1], [Piráti, 0.05], [jiná strana, 0.05], [SPD, 0.05], [KSČM, 0.05], [ČSSD, 0.05], [Přísaha, 0.05], [Trikolora, 0.05], [DSSS, 0.05], [Volte Pravý Blok, 0.05], [Nezávislí, 0.05], [Moravané, 0.05]')

        pred = pred.replace('[[volil, 0.8], [nevolil, 0.2]], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO, 0.2], [jiná strana, 0.1]', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO, 0.2], [jiná strana, 0.1]')
        
        pred = pred.replace('[volil, 0.95, 0.05], [Piráti, 0.45, SPD, 0.3, ANO, 0.15, KSČM, 0.1]; ', '[volil, 0.95], [nevolil, 0.05]; [Piráti, 0.45], [SPD, 0.3], [ANO, 0.15], [KSČM, 0.1]')
        pred = pred.replace('[volil, 0.7, PirSTAN, 0.7]], [nevolil, 0.3]; ANO, 0.15], [SPOLU, 0.15], [Piráti, 0.1], [STAN, 0.1], [jiná strana, 0.1]', '[volil, 0.7], [nevolil, 0.3]; [Piráti a STAN, 0.7], [ANO, 0.15], [SPOLU, 0.15], [Piráti, 0.1], [STAN, 0.1], [jiná strana, 0.1]')
        
        pred = pred.replace('[[volil, 0.8], [nevolil, 0.2]], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO, 0.2], [jiná strana, 0.1]', '[volil, 0.8], [nevolil, 0.2]; [SPOLU, 0.4], [Piráti a STAN, 0.3], [ANO, 0.2], [jiná strana, 0.1]')

        pred = pred.strip(';: ')
        pred = pred.strip('.,')

        if 'January 2023' in pred or '<EOS_TOKEN>' in pred:
            pred = pred.split('<EOS_TOKEN>')[0].replace(';\n', '')
        
        pred = pred.replace('[volil, 0.6], [nevolil, 0.4]; ANO, 0.3, Piráti a STAN, 0.2, SPOLU, 0.2, jiná strana, 0.3', '[volil, 0.6], [nevolil, 0.4]; [ANO, 0.3], [Piráti a STAN, 0.2], [SPOLU, 0.2], [jiná strana, 0.3]')

        pred = pred.split('; ')
        if len(pred) == 3:
            pred = [*pred]
            pred = f"[{pred[0]}], [{pred[1]}]; {pred[2]}"
        else:
            pred = '; '.join(pred)
        pred = pred.replace('[*', '*[')

        failures = ['[nevolil, 1.0];',
                    '[nevolila, 1.0]; [], []',
                    '[volil, 0.0], [nevolil, 1.0];',
                    '[nevolila, 1.0], ;',
                '[nevolil, 1.0]; [], []',
                '[nevolil, 1.0], []; []']
        if pred.strip('*') in failures:
            volil = False
            raise ValueError("Invalid")
        else:
            res_volil, parts, pbs = parse_resp(pred)
            return res_volil, parts, pbs
    except Exception as e:
        print(pred)
        raise e
    

def make_choice(pred):
    try:
        res_volil, parts, pbs = pred
        volil = np.random.choice([True, False], size=1, p=[res_volil['volil'], res_volil['nevolil']])

        if volil:        
            pbs = np.array(pbs)
            pbs /= sum(pbs)
            choice = np.random.choice(parts, size=1, p=pbs)[0]
            if 'Pirates' in choice or 'PirStan' in choice or 'STAROS' in choice or 'Starost' in choice or 'pirát' in choice or 'Piráti' in choice or 'Pirati' in choice or 'STAN' in choice or 'PIR' in choice or 'Pirá' in choice:
                choice = 'PirátiSTAN'
            elif 'Občanská' in choice or 'ODS' in choice or 'TOP' in choice or 'KDU' in choice or 'SPOLU' in choice.upper() or 'Koalice 3' in choice:
                choice = 'SPOLU'
            elif choice == 'NEVÍM':
                choice = 'nevím'    
            elif 'vobodn' in choice or choice == 'TSS':
                return None
            elif 'PŘÍS' in choice.upper() or 'PRISAHA' in choice:
                choice = 'PŘÍSAHA'
            elif choice == 'NEVOLIL' or 'nešel volit' in choice or 'nehlasoval' in choice or 'nešel' in choice:
                choice = 'nevolil'
            elif 'sociálně' in choice or 'ociální' in choice or 'SSD' in choice or 'statní' in choice or 'Trikolora' in choice or 'JIN' in choice.upper() or 'DSSS' in choice or 'TSS' in choice or 'risaha' in choice:
                choice = 'jiná strana'
            elif 'elení' in choice or 'ELENÍ' in choice or 'zelen' in choice or choice == 'j 红á strana' or 'Trikol' in choice or 'eleni' in choice or 'ČSSD' in choice or 'Volný blok' in choice or 'VOLNÝ' in choice:
                choice = 'jiná strana'
            elif 'ANO' in choice or 'Ano' in choice or 'ano' in choice:
                choice = 'ANO'
            elif 'KSČM' in choice or 'omunist' in choice or 'KSCM' in choice:
                choice = 'KSČM'
            elif 'SPD' in choice or 'Svoboda a p' in choice or 'SVOBODA A P' in choice or 'Tomia Okamury' in choice:
                #print(choice)
                choice = 'SPD'
            elif 'kandidát Ne' in choice or 'Svobodomyslní' in choice or 'Desired' in choice or choice == 'Typ00' or choice == 'PCH' \
                or choice == 'neznámá strana' or 'Koalice pro svobo' in choice or 'Paroubek' in choice or 'nehlasuji' in choice or 'nevolil' in choice or 'nevím' in choice or 'Moravané' in choice \
                or 'SSOZS' in choice or 'odmítám' in choice:
                choice = None
            else:
                raise ValueError(f"Unknown party: {choice}")
        else:
            choice = 'nevolil'

        return choice
    except Exception as e:
        print(pred)
        #print(e)
        #raise e

