import subprocess, json
from tqdm import tqdm

def dfa_equiv(gold, predicted):
    # This function uses the regex_dfa_equals.jar to check the equivalence of two given regexes.
    try:
        out = subprocess.check_output(['java', '-jar', 
                                       'deep-regex/deep-regex-model/regex_dfa_equals.jar', 
                                       '{}'.format(gold), '{}'.format(predicted)])
    except Exception as e:
        return False
    
    return '\n1' in str(out)
    # regex_dfa_equals.jar would return "[regex1]\n[regex2]\n[equivalent?1:0]"

with open("outputs/KB13/plain.txt", "r") as f:
    instances = json.load(f)
    count_dfa_equiv = 0
    for instance in tqdm(instances):
        ground_truth = instance["ground_truth"]
        chatgpt_output = instance["chatgpt_output"]
        if dfa_equiv(ground_truth, chatgpt_output):
            count_dfa_equiv += 1

print(count_dfa_equiv)