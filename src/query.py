from chatgpt import chatgpt
from tqdm import tqdm

def test_chatgpt():
    print(chatgpt("what's the capital of japan?"))

def plain_prompt(nl):
    return f"""[Task]
Please work as a expert regex generator. I'll give you a natural language description which corresponds to some regex.
Please answer with a single line of regex consistent to the description and tries to keep it succinct and simple.
[Input: natural language description]
{nl}
"""

def generate_regex_for_KB13():
    with open(f"datasets/KB13/src.txt", "r") as fin:
        with open(f"outputs/KB13/plain.txt", "w") as fout:
            for l in tqdm(fin.readlines()):
                if not l.strip(): continue
                response = chatgpt(plain_prompt(l.strip())).strip()
                print(response, file=fout)

generate_regex_for_KB13()