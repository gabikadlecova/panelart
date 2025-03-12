def base_prompt_proba():
    prompt_start = """
    In place of [INSERT], fill in (in Czech) whether the respondent voted in \"Volby do poslanecké sněmovny 2021\" and if yes, then for what party.
    List the probable parties with probabilities (always output whether the respondent voted and for what party). List as many parties as necessary.
    You can also answer "jiná strana" if the voter voted for a small unpopular party. The probabilities must sum up to 1.0.

    The output format is:
    *[volil, proba a], [nevolil, proba b]; [PARTY1, proba 1], [PARTY2, proba 2],... , [PARTYN, proba n]]*
    where PARTY1, PARTY2,... are the names of the parties, proba a, proba b, proba 1,... should be replaced by float probabilities. Do not print anything else after the second star sign.
    Always list both [volil, proba a], [nevolil, proba b] with the respective probabilities. The probabilities should sum up to 1. (i.e. proba of volil + nevolil = 1.0,
    proba 1 + proba 2 + ... + proba n = 1.0) 
    Be sure to keep the correct separators (';' between the volil/nevolil section and party section, ',' anywhere else).

    """
    prompt_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"

    return prompt_start, prompt_end


def choice_proba():
    prompt_start = """
    In place of [INSERT], fill in (in Czech) whether the respondent voted in \"Volby do poslanecké sněmovny 2021\" and if yes, then for what party.
    Choices: ANO, SPOLU, PirátiSTAN, SPD, KSČM, PŘÍSAHA, jiná strana.

    List the probable parties with probabilities (always output whether the respondent voted and for what party). List as many parties as necessary.
    You can also answer "jiná strana" if the voter voted for a small unpopular party. The probabilities must sum up to 1.0.

    The output format is:
    *[volil, proba a], [nevolil, proba b]; [PARTY1, proba 1], [PARTY2, proba 2],... , [PARTYN, proba n]]*
    where PARTY1, PARTY2,... are the names of the parties, proba a, proba b, proba 1,... should be replaced by float probabilities. Do not print anything else after the second star sign.
    Always list both [volil, proba a], [nevolil, proba b] with the respective probabilities. The probabilities should sum up to 1. (i.e. proba of volil + nevolil = 1.0,
    proba 1 + proba 2 + ... + proba n = 1.0) 
    Be sure to keep the correct separators (';' between the volil/nevolil section and party section, ',' anywhere else).

    """
    prompt_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"

    return prompt_start, prompt_end


def choice_long_proba():
    prompt_start = """
    In place of [INSERT], fill in (in Czech) whether the respondent voted in \"Volby do poslanecké sněmovny 2021\" and if yes, then for what party.
    Choices: ANO, SPOLU, PirátiSTAN, Svoboda a přímá demokracie, KSČM, PŘÍSAHA, jiná strana.

    List the probable parties with probabilities (always output whether the respondent voted and for what party). List as many parties as necessary.
    You can also answer "jiná strana" if the voter voted for a small unpopular party. The probabilities must sum up to 1.0.

    The output format is:
    *[volil, proba a], [nevolil, proba b]; [PARTY1, proba 1], [PARTY2, proba 2],... , [PARTYN, proba n]]*
    where PARTY1, PARTY2,... are the names of the parties, proba a, proba b, proba 1,... should be replaced by float probabilities. Do not print anything else after the second star sign.
    Always list both [volil, proba a], [nevolil, proba b] with the respective probabilities. The probabilities should sum up to 1. (i.e. proba of volil + nevolil = 1.0,
    proba 1 + proba 2 + ... + proba n = 1.0) 
    Be sure to keep the correct separators (';' between the volil/nevolil section and party section, ',' anywhere else).

    """
    prompt_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"

    return prompt_start, prompt_end


def choice_tomio():
    prompt_start = """
    In place of [INSERT], fill in (in Czech) whether the respondent voted in \"Volby do poslanecké sněmovny 2021\" and if yes, then for what party.
    Choices: ANO, SPOLU, PirátiSTAN, Svoboda a přímá demokracie Tomia Okamury, KSČM, PŘÍSAHA, jiná strana.

    List the probable parties with probabilities (always output whether the respondent voted and for what party). List as many parties as necessary.
    You can also answer "jiná strana" if the voter voted for a small unpopular party. The probabilities must sum up to 1.0.

    The output format is:
    *[volil, proba a], [nevolil, proba b]; [PARTY1, proba 1], [PARTY2, proba 2],... , [PARTYN, proba n]]*
    where PARTY1, PARTY2,... are the names of the parties, proba a, proba b, proba 1,... should be replaced by float probabilities. Do not print anything else after the second star sign.
    Always list both [volil, proba a], [nevolil, proba b] with the respective probabilities. The probabilities should sum up to 1. (i.e. proba of volil + nevolil = 1.0,
    proba 1 + proba 2 + ... + proba n = 1.0) 
    Be sure to keep the correct separators (';' between the volil/nevolil section and party section, ',' anywhere else).

    """
    prompt_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"

    return prompt_start, prompt_end


def base_prompt_one_party():
    prompt_start = """
    In place of [INSERT], fill in (in Czech) whether the respondent voted in \"Volby do poslanecké sněmovny 2021\" and if yes, then for what party.

    The output format:
    Did not vote:
    no
    Voted:
    yes, PARTY
    where PARTY is the name of the party.
    """
    prompt_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"

    return prompt_start, prompt_end


def base_prompt_one_party_simple():
    prompt_start = """
    In place of [INSERT], fill in (in Czech) whether the respondent voted in \"Volby do poslanecké sněmovny 2021\" and if yes, then for what party.

    """
    prompt_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"

    return prompt_start, prompt_end


def czech_prompt_proba():
    czech_prompt_start = """Po značce [INSERT] doplň, zda respondent volil ve volbách do poslanecké sněmovny 2021 a pokud ano, pro jakou stranu hlasoval.
    Možné strany, kterým nejspíše dal hlas, vypiš s pravděpodobností že pro danou stranu hlasoval. Vypiš kolik stran je potřeba.
    Případně můžeš vypsat i "jiná strana", což představuje hlas pro málo populární stranu. Součet pravděpodobností musí být 1.0.

    Formát výstupu je:
    *[volil, proba a], [nevolil, proba b]; [PARTY1, proba 1], [PARTY2, proba 2],... , [PARTYN, proba n]*
    kde PARTY1, PARTY2,... jsou jména stram, proba a, proba b, proba 1,... je třeba nahradit desetinnými čísly (pravděpodobnost). Za druhý znak "*" už nic nevypisuj.
    
    Zachovej správné oddělovače (';' mezi sekcí volil/nevolil a sekcí stran, všude jinde ','). Volil/nevolil je první, pak následují strany.
    """

    czech_prompt_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"
    return czech_prompt_start, czech_prompt_end


def act_as_prompt_proba():
    act_prompt_start = """
    You are a Czech respondent that voted in parliamentary elections in 2021. You will get a question about who you voted in some elections. List whether you voted or not, and what party you voted for if yes. The output format is:
    *[volil, proba a], [nevolil, proba b]; [PARTY1, proba 1], [PARTY2, proba 2],... , [PARTYN, proba n]]*
    where PARTY1, PARTY2,... are the names of the parties, proba a, proba b, proba 1,... should be replaced by float probabilities. Do not print anything else after the second star sign.
    Always list both [volil, proba a], [nevolil, proba b] with the respective probabilities. The probabilities should sum up to 1. (i.e. proba of volil + nevolil = 1.0,
    proba 1 + proba 2 + ... + proba n = 1.0) 
    Be sure to keep the correct separators (';' between the volil/nevolil section and party section, ',' anywhere else).

    Act like a Czech respondent of the following group:
    """

    act_prompt_end = """
    Koho jsi volil ve volbách do poslanecké sněmovny 2021?
    """
    return act_prompt_start, act_prompt_end


def prompt_simple_instructions_proba():
    prompt_simple_start = """
    In place of [INSERT], fill in (in Czech) the probability that the respondent voted in \"Volby do poslanecké sněmovny 2021\" and for what party they voted.
    List probability of voting and the probable parties with probabilities (always output whether the respondent voted and for what party). List as many parties as necessary.
    You can also answer "jiná strana" if the voter voted for a small unpopular party.

    The respondent bio:
    """

    prompt_simple_end = " Ve volbách do poslanecké sněmovny 2021 jsem [INSERT]"
    return prompt_simple_start, prompt_simple_end


prompt_functions = {
    "base": base_prompt_proba,
    "choice": choice_proba,
    "choice_long": choice_long_proba,
    "choice_tomio": choice_tomio,
    "one_party": base_prompt_one_party,
    "one_party_simple": base_prompt_one_party_simple,
    "czech": czech_prompt_proba,
    "act_as": act_as_prompt_proba,
    "simple": prompt_simple_instructions_proba
}
