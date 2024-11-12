import pandas as pd
from panelart.data.soc_distrust.respondents import create_prompt, create_prompt_shuffled
from panelart.data.soc_distrust.prompts import prompt_functions

from typing import List


def load_soc_distrust(data_path: str) -> pd.DataFrame:
    return pd.read_spss(data_path)


def _parse_row(r):
    # kraj and okres are regional division units
    res = {'gender': r['GENDER'], 'age': int(r['AGE1']), 'education': r['EDU'].lower(), 'kraj': r['KRAJ'], 'okres': r['OKRES'], 'townsize': r['VMB']}
    res['employment'] = ', '.join([r[c] for c in r.index if 'EMPL' in c and r[c] != 'Ne']).lower()
    res['income'] = '' if 'Nev' in r['INCOMEP'] else r['INCOMEP']
    res['zivotni_uroven'] = r['Q19']  # living standard
    res['zajem_politika'] = r['Q20']  # interest in politics
    res['eu'] = r['Q18']  # is it good that Czechia is part of the EU?
    res['nato'] = r['Q17']  # ditto ... NATO
    res['covid_vacc'] = r['Q23']  # did you receive the covid vaccine?

    # case sensitivity for prompt integration
    if 'Do' in res['income']:
        res['income'] = 'do 15.000 Kč'
    elif 'než' in res['income']:
        res['income'] = 'více než 80.000 Kč'
    res['income'] = res['income'] if len(res['income']) else None
    
    return res


def process_soc_distrust_short(df: pd.DataFrame) -> pd.DataFrame:
    data = [_parse_row(df.loc[i]) for i in df.index]
    return pd.DataFrame(data, index=df.index)


def create_respondent_prompt(r, keys: List[str] | None = None, prompt_type: str = 'base') -> str:
    prompt_start, prompt_end = prompt_functions[prompt_type]()
    return prompt_start + create_prompt(r, keys=keys) + prompt_end


def create_respondent_prompt_shuffled(r, keys: List[str] | None = None, prompt_type: str = 'base',
                                      split_up: bool = False, seed: int = 42) -> str:
    prompt_start, prompt_end = prompt_functions[prompt_type]()
    return prompt_start + create_prompt_shuffled(r, keys=keys, split_up=split_up, seed=seed) + prompt_end
