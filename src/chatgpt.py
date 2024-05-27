import openai
from openai import OpenAI
import time

INSTRUCTION = "Please work as an expert regex translator. I'll give you a natural language description which corresponds to some regex.\nPlease answer with a single line of regex consistent to the description and tries to keep it succinct and simple."

PLAIN = """[Task]
Please work as an expert regex translator. I'll give you a natural language description which corresponds to some regex.
Please answer with a single line of regex consistent to the description and tries to keep it succinct and simple.
[Input: natural language description]
{nl}
"""

def chatgpt(messages):
    client = OpenAI(api_key="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")
    while True:
        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )
            break
        except openai.RateLimitError as e:
            print(e)
            time.sleep(5)
    answer = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer += chunk.choices[0].delta.content
    return answer