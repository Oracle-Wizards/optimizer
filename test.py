import openai

# Replace with your valid Llama API token
api_key = "<LL-2bYY14yB4vqT03qEXMqonIfIGXiPeSNdFgrmkoPRZkdRfKDEccmDXsTF94mVZ8Az>"
base_url = "https://api.llama-api.com"

client = openai.OpenAI(api_key=api_key, base_url=base_url)

response = client.chat.completions.create(
    model="llama-13b-chat",
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
)

print(response.model_dump_json(indent=2))
print(response.choices[0].message.content)
