import openai

openai.api_key = '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'

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "語頭には「あーはいはい、それね。」、すべての語尾に「らしいのぉ。」か「わい。」をつけて質問に短く答えてください"},
        {"role": "user", "content": "APIってなに？"},
    ],
    max_tokens=150
)
print(f"ChatGPT: {response['choices'][0]['message']['content']}")
print(response['usage'])
