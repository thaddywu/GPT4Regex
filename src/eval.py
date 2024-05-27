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
    
    return '\\n1' in str(out)
    # regex_dfa_equals.jar would return "[regex1]\n[regex2]\n[equivalent?1:0]"

def dfa_equiv_count(outputpath):
    count = 0
    with open(outputpath, "r") as f:
        instances = json.load(f)
        for instance in instances:
            ground_truth = instance["ground_truth"]
            chatgpt_output = instance["chatgpt_output"]
            print(instance["description"])
            print(ground_truth)
            print(chatgpt_output)
            print(dfa_equiv(ground_truth, chatgpt_output))
            print()
            if dfa_equiv(ground_truth, chatgpt_output):
                count += 1
    return count

print(dfa_equiv_count("outputs/KB13/test.txt"))