from openai import OpenAI

# 直接传入 API Key（注意：不要用 os.environ.get）
client = OpenAI(
    api_key="sk-a910aacb624644af9b4b32f474336baf",  # 直接写字符串，不要用 os.environ.get
    base_url="https://api.deepseek.com"
)

# 测试调用
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "user", "content": "你好"}
    ]
)

print(response.choices[0].message.content)