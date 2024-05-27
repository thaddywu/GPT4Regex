from chatgpt import chatgpt
from tqdm import tqdm
import json

def test_chatgpt():
    print(chatgpt("what's the capital of japan?"))

def plain_prompt(nl):
    return f"""[Task] Please give me a regular expression with the language description I give to you.
Please response with one line of a regular expression but nothing else.
[Example]
Description: lines using words that begin with 'z'.
Answer: .*\\bz[A-Za-z]*\\b.*
[Description]
{nl}
"""

def generate_regex_for_KB13():
    responses = []
    with open(f"datasets/KB13/src.txt", "r") as fnl:
        nls = [l.strip() for l in fnl.readlines() if l.strip()]
    with open(f"datasets/KB13/targ.txt", "r") as fgt:
        gts = [l.strip() for l in fgt.readlines() if l.strip()]

    for nl, gt in tqdm(zip(nls[:10], gts[:10])):
        prompt = plain_prompt(nl)
        responses += [{
            "description": nl,
            "prompt": prompt,
            "ground_truth": gt,
            "chatgpt_output": chatgpt(prompt).strip()
        }]
        print(nl)
        print(prompt)
        print(responses[-1]["chatgpt_output"])
    
    with open(f"outputs/KB13/test.txt", "w") as fout:
        json.dump(responses, fout)
        

generate_regex_for_KB13()