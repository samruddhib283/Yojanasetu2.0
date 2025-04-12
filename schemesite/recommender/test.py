import openai

openai.api_key = "your_key_here"

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Tell me 3 Indian government schemes for farmers."}
    ]
)

print(response['choices'][0]['message']['content'])
