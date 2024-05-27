from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch

import os

os.environ["HF_HOME"] = "/data/jkx/.cache"
device = "cuda" # the device to load the model onto

model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
model.to(device)

def call_mistral(messages):
    encodeds = tokenizer.apply_chat_template(messages, return_tensors="pt")
    model_inputs = encodeds.to(device)
    generated_ids = model.generate(model_inputs, max_new_tokens=1000, do_sample=True)[0][model_inputs.shape[1]:]
    # print(generated_ids)
    decoded:str = tokenizer.decode(generated_ids)
    if decoded.endswith("</s>"):
        decoded = decoded[:-4]
    decoded_list = decoded.split("\n")
    decoded = decoded_list[0]
    return decoded


# call_mistral()
