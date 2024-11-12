from openai import OpenAI


class GPTModel:
    def __init__(self, api_key: str, model: str = 'gpt-4o', temp: float = 0.0):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temp = temp

    def generate(self, prompt: str):
        res = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=self.model,
            temperature=self.temp
        )

        return res
