from __future__ import annotations

import argparse
import numpy as np
import pickle
import os
from panelart.data.soc_distrust.utils import load_soc_distrust, process_soc_distrust_short, create_respondent_prompt, create_respondent_prompt_shuffled
from panelart.models import get_model
from panelart.panel.generate import generate_panel
from jsonargparse import CLI


def create_soc_distrust_panel(
        out_dir: str,
        api_key: str,
        model_name: str = 'command-r-plus',
        seed: int = 42,
        sample_size: int | None = None,
        data_path: str = 'data/soc_distrust.sav',
        prompt_type: str = 'base',
        shuffle: bool | None = False,
        split_up: bool | None = False,
        out_prefix: str | None = None
):
    """
    Create a panel for the social distrust dataset.

    Args:
        out_dir: Output directory for the generated panel
        api_key: API key for the model
        model_name: Name of the model to use
            Default: 'command-r-plus'
        seed: Random seed for sampling
            Default: 42
        sample_size: Sample size (when using a subset of the data) or the full dataset if None
        data_path: Path to the data file
            Default: 'data/soc_distrust.sav'
        prompt_type: Type of prompt to create
            Default: 'base'
        shuffle: Whether to shuffle the prompt parts
            Default: False
        split_up: Whether to split up the prompt parts when shuffling
            Default: False   
        out_prefix: Prefix for the output file name
            Default: None     
    """

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    out_path = f"{model_name}_{prompt_type}_{sample_size}_{seed}_shuffle-{shuffle}_split_up-{split_up}.pkl"
    out_path = f"{out_prefix}_{out_path}" if out_prefix is not None else out_path
    out_path = os.path.join(out_dir, out_path)

    shuffle = False if shuffle is None else shuffle
    split_up = False if split_up is None else split_up

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
    if os.path.exists(out_path):
        with open(out_path, 'rb') as f:
            results = pickle.load(f)

    model_cls = get_model(model_name)
    model = model_cls(api_key=api_key)

    panel = generate_panel(model, prompts, results=results)
    with open(out_path, 'wb') as f:
        pickle.dump(panel, f)


if __name__ == '__main__':
    CLI(create_soc_distrust_panel)
