from openai import OpenAI

def chatgpt(prompt):
    client = OpenAI()
    stream = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    answer = ""
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            answer += chunk.choices[0].delta.content
    return answer