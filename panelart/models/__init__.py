from panelart.models.cohere import CommandRPlus
from panelart.models.openai_models import GPTModel
from panelart.models.anthropic import ClaudeModel


def get_model(key):
    if key not in model_map:
        raise ValueError(f"Model {key} not found. Available models: {model_map.keys()}")
    return model_map[key]


model_map = {
    'claude': lambda api_key: ClaudeModel(api_key, model='claude-3-opus-20240229'),
    'command-r-plus': CommandRPlus,
    'gpt-4o': lambda api_key: GPTModel(api_key, model='gpt-4o'),
    'gpt-4o-mini': lambda api_key: GPTModel(api_key, model='gpt-4o-mini'),
    'gpt-3.5-turbo': lambda api_key: GPTModel(api_key, model='gpt-3.5-turbo')
}
