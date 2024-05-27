from chatgpt import chatgpt
# from mistral import call_mistral
from tqdm import tqdm
import json

INSTRUCTION = "Please work as an expert regex translator. I'll give you a natural language description which corresponds to some regex.\nPlease answer with a single line of regex consistent to the description and tries to keep it succinct and simple."

PLAIN = """[Task]
Please work as an expert regex translator. I'll give you a natural language description which corresponds to some regex.
Please answer with a single line of regex consistent to the description and tries to keep it succinct and simple.
[Input: natural language description]
{nl}
"""

def test_chatgpt():
    print(chatgpt("what's the capital of japan?"))

def plain_prompt(description):
    prompt = PLAIN.format(nl=description)
    messages = [{"role": "user", "content": prompt}]
    return messages

def in_context_prompt(model_name, description):
    if model_name == "chatgpt":
        messages=[
            {"role": "system", "content": "You are a helpful, pattern following assistant"},
            {"role": "user", "content": INSTRUCTION},
            {"role": "user", "content": "lines that do not contain numerical characters"},
            {"role": "assistant", "content": "~(.*[0-9].*)"},
            {"role": "user", "content": description},
        ]
        return messages
    else:
        messages=[
            {"role": "user", "content": INSTRUCTION + " Task: lines that do not contain numerical characters"},
            {"role": "assistant", "content": "~(.*[0-9].*)"},
            {"role": "user", "content": "Task: " + description},
        ]
        return messages

def generate_regex_for_KB13(model_name, mode):
    if model_name == "mistral":
        from mistral import call_mistral
    responses = []
    with open(f"datasets/KB13/src.txt", "r") as fnl:
        nls = [l.strip() for l in fnl.readlines() if l.strip()]
    with open(f"datasets/KB13/targ.txt", "r") as fgt:
        gts = [l.strip() for l in fgt.readlines() if l.strip()]

    for nl, gt in tqdm(zip(nls, gts)):
        if mode == "plain":
            messages = plain_prompt(nl)
        elif mode == "in-context":
            messages = in_context_prompt(model_name, nl)
        
        if model_name == "mistral":
            output = call_mistral(messages).strip()
        elif model_name == "chatgpt":
            output = chatgpt(messages).strip()
        responses += [{
            "description": nl,
            # "prompt": prompt,
            "ground_truth": gt,
            "chatgpt_output": output
        }]
        # print(nl)
        # print(gt, responses[-1]["chatgpt_output"])
    
    with open(f"outputs/KB13/{model_name}_{mode}.json", "w") as fout:
        json.dump(responses, fout)
        

generate_regex_for_KB13("chatgpt", "plain")