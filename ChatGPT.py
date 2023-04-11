import openai

openai.api_key = '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'

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "語頭には「あーはいはい、それね。」、すべての語尾に「らしいのぉ。」か「わい。」をつけて質問に短く答えてください"},
        {"role": "user", "content": "この時期に関東で釣れる魚ってなに？"},
    ],
    max_tokens=150
)
print(f"ChatGPT: {response['choices'][0]['message']['content']}")
print(response['usage'])
