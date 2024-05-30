from chatgpt import chatgpt
from tqdm import tqdm
import json

def test_chatgpt():
    print(chatgpt("what's the capital of japan?"))

def zeroshot(nl):
    return f"""[Task] Please give me a regular expression with the language description I give to you.
Please response with one line of a regular expression but nothing else.
Don't use ^ and $. You can use ~ for complement, & for intersection.
[Description]
{nl}
"""

def oneshot(nl):
    return f"""[Task] Please give me a regular expression with the language description I give to you.
Please response with one line of a regular expression but nothing else.
Don't use ^ and $. You can use ~ for complement, & for intersection.
[Example]
Description: lines using words that begin with 'z'.
Answer: .*\\bz[A-Za-z]*\\b.*
[Description]
{nl}
"""

def twoshot(nl):
    constant = "(.*254.*){2}"
    return f"""[Task] Please give me a regular expression with the language description I give to you.
Please response with one line of a regular expression but nothing else.
Don't use ^ and $. You can use ~ for complement, & for intersection.
[Example]
Description: lines using words that begin with 'z'.
Answer: .*\\bz[A-Za-z]*\\b.*
Description: lines that contain the number '254' at least twice.
Answer: {constant}
[Description]
{nl}
"""

def generate_regex_for_KB13():
    responses = []
    with open(f"datasets/KB13/src.txt", "r") as fnl:
        nls = [l.strip() for l in fnl.readlines() if l.strip()]
    with open(f"datasets/KB13/targ.txt", "r") as fgt:
        gts = [l.strip() for l in fgt.readlines() if l.strip()]

    for nl, gt in tqdm(zip(nls, gts)):
        prompt = twoshot(nl)
        responses += [{
            "description": nl,
            "prompt": prompt,
            "ground_truth": gt,
            "chatgpt_output": chatgpt(prompt).strip()
        }]
        print(nl)
        print(prompt)
        print(responses[-1]["chatgpt_output"])
    
    with open(f"outputs/KB13/chatgpt4-two-shot.txt", "w") as fout:
        json.dump(responses, fout)
        

generate_regex_for_KB13()