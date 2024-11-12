from tqdm import tqdm


def generate_panel(model, prompts, results=None, skip_existing=True, verbose=True, **kwargs):
    results = results if results is not None else {}
    
    pbar = tqdm(prompts.items(), disable=not verbose)

    try:
        for idx, prompt in pbar:
            if idx in results and skip_existing:
                continue
        
            response = model.generate(prompt, **kwargs)
            results[idx] = response
    except Exception as e:
        print(type(e))
        print('Interrupted response generation, returning all computed results.')
        return results
    
    return results
