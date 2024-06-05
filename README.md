# Evaluating LLMs' Performance on Regex Generation

This is a course project for CS263

## Running Guide

### Generation

The last line of `query.py` is 
```
generate_regex_for_KB13("mistral", "in-context")
```
Change the model name (choose from `mistral` and `chatgpt`) and method (choose from `plain` and `in-context`) as expected. You can also edit the demonstrations in `in_context_prompt()` when choosing in context learning. We provide sample output of GPT-4 and GPT-3.5 in `outputs/KB13`

### Evaluation

For equivalence, change the parameter in last line of `eval.py` to the path to desired output and run `python src/eqv.py`

For other scores, follow a similar procedure to change the path to prediction and then run `python src/eval.py`
