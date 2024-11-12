import numpy as np


def create_gender_age_education_text(r, split_up=False):
    if split_up:
        return [f"Jsem {r['gender'].lower()}.", f"Je mi {r['age']} let.", f"Mé vzdělání je {r['education']}."]

    return f"Jsem {r['gender'].lower()}, je mi {r['age']} let, mé vzdělání je {r['education']}."

def create_location_text(r, split_up=False):
    kraj_name = r['kraj'].replace('raj', 'raji')
    if 'ý' in r['kraj']:
        kraj_name = kraj_name.replace('ý', 'ém')
    elif 'Praha' in kraj_name:
        kraj_name = 'Praze'

    if split_up:
        return [f"Žiji v {kraj_name}.", f"Žiji v okresu {r['okres']}.", f"Žiji v obci o velikosti {r['townsize']}."]
    
    return f"Žiji v {kraj_name}, v okresu {r['okres']} a obci o velikosti {r['townsize']}."

def create_employment_income_text(r, split_up=False):
    if split_up:
        text = [f"Z hlediska zaměstnání jsem {r['employment']}."]
        if r['income'] is not None:
            text.append(f"Příjem naší domácnosti je {r['income']}.")
        return text
    
    text = f"Z hlediska zaměstnání jsem {r['employment']}"
    text += f" a příjem naší domácnosti je {r['income']}." if r['income'] is not None else '.'
    
    return text

def create_eu_text(r):
    if r['eu'] != 'Nevím':
        eu = r['eu'][:-3]
        eu += 'ý' if r['gender'] == 'Muž' else 'á'
        return f"Jsem {eu.lower()}, že je česká republika členským státem EU."
    return ''

def create_nato_text(r):
    if r['nato'] != 'Nevím':
        nato = r['nato'][:-3]
        nato += 'ý' if r['gender'] == 'Muž' else 'á'
        return f"Jsem {nato.lower()}, že je česká republika členským státem NATO."
    return ''

def create_zivotni_uroven_text(r):
    if r['zivotni_uroven'] != 'Nevím':
        zivu = r['zivotni_uroven']
        return f"{'Mám' if 'ani' not in zivu else 'Nemám'} {zivu.lower()} životní úroveň."
    return ''

def create_zajem_politika_text(r):
    if r['zajem_politika'] != 'Nevím':
        return f"{r['zajem_politika']} o politiku."
    return ''

def create_covid_vacc_text(r):
    gender_a = '' if r['gender'] == 'Muž' else 'a'
    if r['covid_vacc'] == 'Ano':
        return f"Jsem očkován{gender_a} proti covidu."
    elif r['covid_vacc'] == 'Ne':
        return f"Nejsem očkován{gender_a} proti covidu."
    return ''


prompt_function_map = {
    'gender_age_edu': create_gender_age_education_text,
    'location': create_location_text,
    'employment_income': create_employment_income_text,
    'eu': create_eu_text,
    'nato': create_nato_text,
    'zivotni_uroven': create_zivotni_uroven_text,
    'zajem_politika': create_zajem_politika_text,
    'covid_vacc': create_covid_vacc_text
}


def try_split_up(func, r):
    try:
        return func(r, split_up=True)
    except TypeError:
        return [func(r)]


def create_prompt(r, keys=None):
    if keys is None:
        keys = prompt_function_map.keys()
    return ' '.join(prompt_function_map[key](r) for key in keys)


def create_prompt_shuffled(r, keys=None, split_up=False, seed=42):
    if keys is None:
        keys = list(prompt_function_map.keys())
    
    random = np.random.RandomState(seed)

    if split_up:
        parts = [try_split_up(prompt_function_map[key], r) for key in keys]
        parts = [part for sublist in parts for part in sublist]
    else:
        parts = [prompt_function_map[key](r) for key in keys]

    random.shuffle(parts)
    return ' '.join(parts)
