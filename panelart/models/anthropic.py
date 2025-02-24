import anthropic


class ClaudeModel:
    def __init__(self, api_key: str, model: str = 'claude-3-opus-20240229', max_tokens=1024):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens

    def generate(self, prompt: str):
        res = self.client.messages.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=self.model,
            max_tokens=self.max_tokens
        )

        return res
