import cohere
import time


class CommandRPlus:
    def __init__(self, api_key: str, model: str = 'command-r-plus', sleep_if_timeout=True):
        self.client = cohere.Client(api_key)
        self.model = model
        self.sleep_if_timeout = sleep_if_timeout

    def generate(self, prompt: str, **kwargs):
        try:
            res = self.client.chat(
                message=prompt,
                model=self.model,
                **kwargs
            )
        except cohere.errors.too_many_requests_error.TooManyRequestsError as e:
            if self.sleep_if_timeout:
                # out of free api calls
                if 'month' in str(e):
                    raise e

                print('Sleeping during 1 minute timeout...')
                time.sleep(60)
                res = self.generate(prompt, **kwargs)
            else:
                raise e

        return res
