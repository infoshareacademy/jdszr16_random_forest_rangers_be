import openai

# Twój klucz API OpenAI
api_key = os.getenv("OPENAI_API_KEY")
api_org = os.getenv("OPENAI_API_ORG")

openai.api_key = api_key

def process_chat(user_input):
    # Historia rozmowy
    messages = [
        {"role": "system", "content": "Jesteś pomocnym asystentem."},
        {"role": "user", "content": user_input}
    ]

    # Wywołanie OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    # Pobranie odpowiedzi modelu
    return response['choices'][0]['message']['content']