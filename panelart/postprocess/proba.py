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


def parse_text(pred):
    try:
        print(pred)
        if "ODS, 0.30, ANO, 0.20" in pred or 'Omlouvám se, ale nemohu' in pred or 'Je mi líto, ale' in pred or '*[], []' in pred or 'Promiň, ale nemohu' in pred or "I'm sorry, but I can't assist with that request" in pred or 'olil' not in pred:
            return None
        
        for l in pred.split('\n'):
            if l.startswith('* [') or (l.startswith('*') and not l.startswith('*Pokud') and not l.startswith('* ')):
                pred = l
                break
        
        if 'Pro určení' in pred:
            pred = pred.split('\n')[2]

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

        if 'January 2023' in pred or '<EOS_TOKEN>' in pred:
            pred = pred.split('<EOS_TOKEN>')[0].replace(';\n', '')
        
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
        else:
            res_volil, parts, pbs = parse_resp(pred)
            #print(res_volil, parts, pbs)
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
            elif 'PŘÍS' in choice.upper():
                choice = 'PŘÍSAHA'
            elif choice == 'NEVOLIL':
                choice = 'nevolil'
            elif 'sociálně' in choice or 'ociální' in choice or 'SSD' in choice or 'statní' in choice or 'Trikolora' in choice or 'JIN' in choice.upper() or 'DSSS' in choice or 'TSS' in choice:
                choice = 'jiná strana'
            elif 'elení' in choice or 'ELENÍ' in choice or 'zelen' in choice or choice == 'j 红á strana' or 'Trikol' in choice:
                choice = 'jiná strana'
            elif 'ANO' in choice or 'Ano' in choice:
                choice = 'ANO'
            elif 'KSČM' in choice or 'omunist' in choice or 'KSCM' in choice:
                choice = 'KSČM'
            elif 'SPD' in choice or 'Svoboda a p' in choice or 'SVOBODA A P' in choice:
                print(choice)
                choice = 'SPD'
            elif 'kandidát Ne' in choice or 'Svobodomyslní' in choice or 'Desired' in choice or choice == 'Typ00' or choice == 'PCH' \
                or choice == 'neznámá strana' or 'Koalice pro svobo' in choice or 'Paroubek' in choice or 'nehlasuji' in choice or 'nevolil' in choice or 'nevím' in choice:
                choice = None
            else:
                raise ValueError(f"Unknown party: {choice}")
        else:
            choice = 'nevolil'

        return choice
    except Exception as e:
        print(pred)
        raise e
