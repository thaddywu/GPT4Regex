from chatgpt import chatgpt
from tqdm import tqdm
import json

def test_chatgpt():
    print(chatgpt("what's the capital of japan?"))

def plain_prompt(nl):
    return f"""[Task]
Please work as an expert regex translator. I'll give you a natural language description which corresponds to some regex.
Please answer with a single line of regex consistent to the description and tries to keep it succinct and simple.
[Input: natural language description]
{nl}
"""

def generate_regex_for_KB13():
    responses = []
    with open(f"datasets/KB13/src.txt", "r") as fnl:
        nls = [l.strip() for l in fnl.readlines() if l.strip()]
    with open(f"datasets/KB13/targ.txt", "r") as fgt:
        gts = [l.strip() for l in fgt.readlines() if l.strip()]

    for nl, gt in tqdm(zip(nls, gts)):
        prompt = plain_prompt(nl)
        responses += [{
            "description": nl,
            "prompt": prompt,
            "ground_truth": gt,
            "chatgpt_output": chatgpt(prompt).strip()
        }]
        print(nl)
        print(responses[-1]["chatgpt_output"])
    
    with open(f"outputs/KB13/plain.txt", "w") as fout:
        json.dump(responses, fout)
        

generate_regex_for_KB13()