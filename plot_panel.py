import argparse
import pandas as pd  # type: ignore
import pickle
from panelart.data.soc_distrust.utils import load_soc_distrust
from panelart.utils.plot import plot_results
from panelart.postprocess import parse_party
from panelart.postprocess.one_party import parse_text
from panelart.postprocess.proba import parse_text as parse_text_proba
import seaborn as sns  # type: ignore


def count_votes(v):
    res = {}

    for party in v:
        if party in res:
            res[party] += 1
        else:
            res[party] = 1
    return res


def get_text(response, model):
    if model == 'command-r-plus':
        return response.text
    elif model in ['gpt-4o', 'gpt-4o-mini', 'gpt-3.5-turbo']:
        return response.choices[0].message.content
    elif 'claude' in model:
        return response.content[0].text
    else:
        raise ValueError(f"Unknown model {model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot panel art")
    parser.add_argument("results_path", type=str, help="Path to the results file")
    parser.add_argument("orig_path", type=str, help="Path to the original file")
    parser.add_argument("--plot_type", type=str, default="proba", choices=["one_party", "proba"], help="Type of plot to generate")
    parser.add_argument("--n_sample", type=int, default=1, help="Number of samples to plot")
    parser.add_argument("--model_name", type=str, default="command-r-plus", help="Name of the model to use")
    parser.add_argument("--title", type=str, default="Votes distribution", help="Title of the plot")
    args = parser.parse_args()

    sns.set()

    with open(args.results_path, "rb") as f:
        results = pickle.load(f)

    df = load_soc_distrust(args.orig_path)
    orig = [parse_party(t) for t in df.loc[results.keys()]['Q21']]
    m = args.model_name

    if args.plot_type == "proba":
        results = [[parse_text_proba(get_text(r, m)) for r in results.values()] for _ in range(args.n_sample)]
    elif args.plot_type == "one_party":
        results = [[parse_text(get_text(r, m)) for r in results.values()]]
    else:
        raise ValueError("Unknown plot type")
    
    data = []
    orig_counts = count_votes(orig)
    res_counts = [count_votes(r) for r in results]
    for i, r in enumerate(res_counts):
        for k, o in orig_counts.items():
            if i == 0:
                data.append({'id': i, 'party': k, 'count': o, 'output': 'voted'})
        for k, o in r.items():
            data.append({'id': i, 'party': k, 'count': o, 'output': 'predicted'})
    plot_df = pd.DataFrame(data)
    plot_df['party'] = pd.Categorical(plot_df['party'], ['ANO', 'SPOLU', 'PirátiSTAN', 'SPD', 'KSČM', 'PŘÍSAHA', 'jiná strana', 'neuvedeno', 'nevolil'])

    plot_results(plot_df, title=args.title, figsize=(10, 6))
