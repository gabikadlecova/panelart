import argparse
import numpy as np
import pickle
import os
from panelart.data.soc_distrust.utils import load_soc_distrust, process_soc_distrust_short, create_respondent_prompt, create_respondent_prompt_shuffled
from panelart.models import get_model
from panelart.panel.generate import generate_panel


def create_soc_distrust_panel(out_name, api_key, model_name='command-r-plus', seed=42, sample_size=None, data_path='data/soc_distrust.sav',
                              prompt_type='base', shuffle=False, split_up=False):
    assert os.path.exists(os.path.dirname(out_name)), f"Output directory {os.path.dirname(out_name)} does not exist."
    assert not os.path.isdir(out_name), f"Output file {out_name} is a directory." 

    df = load_soc_distrust(data_path)

    # todo - replace with other variants for feature selection
    df = process_soc_distrust_short(df)

    if sample_size is not None:
        np.random.seed(seed)
        df = df.sample(sample_size)

    # todo - optionally add other keys
    if shuffle:
        prompts = {idx: create_respondent_prompt_shuffled(df.loc[idx], prompt_type=prompt_type, seed=seed, split_up=split_up) for idx in df.index}
    else:
        prompts = {idx: create_respondent_prompt(df.loc[idx], prompt_type=prompt_type) for idx in df.index}

    results = {}
    if os.path.exists(out_name):
        with open(out_name, 'rb') as f:
            results = pickle.load(f)

    model_cls = get_model(model_name)
    model = model_cls(api_key=api_key)

    panel = generate_panel(model, prompts, results=results)
    with open(out_name, 'wb') as f:
        pickle.dump(panel, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a panel using a specified model.')
    parser.add_argument('out_name', type=str, help='Output file name for the generated panel')
    parser.add_argument('api_key', type=str, help='API key for the model')
    parser.add_argument('--model_name', type=str, default='command-r-plus', help='Name of the model to use')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for sampling')
    parser.add_argument('--sample_size', type=int, default=None, help='Sample size (when using a subset of the data)')
    parser.add_argument('--data_path', type=str, default='data/soc_distrust.sav', help='Path to the data file')
    parser.add_argument('--prompt_type', type=str, default='base', help='Type of prompt to create')
    parser.add_argument('--shuffle', action='store_true', help='Whether to shuffle the prompt parts')
    parser.add_argument('--split_up', action='store_true', help='Whether to split up the prompt parts when shuffling')

    args = parser.parse_args()
    create_soc_distrust_panel(args.out_name, args.api_key, model_name=args.model_name, seed=args.seed,
                              sample_size=args.sample_size, data_path=args.data_path, prompt_type=args.prompt_type,
                              shuffle=args.shuffle, split_up=args.split_up)
