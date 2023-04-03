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
