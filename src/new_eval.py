import subprocess, json
from tqdm import tqdm
from xeger import Xeger
import re
import random
import string

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

def generate_sample(gt, n=5):
    generator = Xeger(limit=15, seed=6)
    generated = []
    for i in range(n):
        ps = generator.xeger(gt)
        generated.append((ps, 1))
    for i in range(n):
        res = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        matched = re.match(gt, res)
        if matched == None:
            generated.append((ps, 0))
        else:
            span = matched.span()
            if span[0] != 0 or span[1] != len(res):
                generated.append((ps, 0))
            else:
                generated.append((ps, 1))
    return generated


def evaluate(gt, pred):
    samples = generate_sample(gt, 5)
    try:
        pattern = re.compile(pred)
        valid = True
    except:
        valid = False

    tp, fp, fn = 0, 0, 0
    for sample, label in samples:
        if not valid:
            if label == 1: 
                fp += 1
            else:
                fn += 1
        else:
            result = re.match(pred, sample)
            matched = bool(result) and result.span() == (0, len(sample))
            if matched:
                if label == 1:
                    tp += 1
                else:
                    fp += 1
            else:
                if label == 1:
                    fn += 1
    return tp, fp, fn, valid

    


f = open("outputs/KB13/chatgpt_in-context.json", "r")
instances = json.load(f)
count_dfa_equiv = 0

tp, fp, fn = 0, 0, 0
valid = 0
length = []

for instance in tqdm(instances):
    ground_truth = instance["ground_truth"]
    chatgpt_output = instance["chatgpt_output"]

    length.append(len(chatgpt_output))
    
    a, b, c, v = evaluate(ground_truth, chatgpt_output)
    tp += a
    fp += b
    fn += c
    valid = valid + 1 if v else valid

p = tp/(tp + fp)
r = tp/(tp + fn)
f1 = 2*p*r/(p+r)

print(p, r, f1)
print(valid)
print(sum(length)/len(length))