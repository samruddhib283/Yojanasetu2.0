import openai

openai.api_key = "your-openai-api-key"

def format_schemes_for_prompt(schemes):
    prompt = "Summarize the following government schemes in a simple way for users:\n\n"
    for scheme in schemes:
        prompt += f"Name: {scheme.name}\nMinistry: {scheme.ministry}\nYear: {scheme.launch_year}\nSector: {scheme.sector}\nSummary: {scheme.summary}\n\n"
    prompt += "Now provide a brief overall summary that explains these schemes clearly."
    return prompt

def generate_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=400
    )
    return response.choices[0].message['content']
