import openai
import os

api_key = os.getenv("OPENAI_API_KEY")
api_org = os.getenv("OPENAI_API_ORG")


def get_illness_treatment_plan(disease = "cukrzyca"):
    openai.api_key = api_key

    client = openai.OpenAI(api_key=api_key, organization=api_org)
    openAI_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Jestes farmaceutą i lekarzem. Znasz sie na medycynie"
            },
            {
                "role": "user",
                "content": f"Napisz text o  sposobach leczenia choroby o nazwie {disease}. Tekst powinien byc przystepny dla pacjentow. Zmiesc sie w 20 zdaniach. Nie opisuj choroby, tylko leczenie.",
                "response_format": {
                    "type": "tekst"
                }
            }
        ],
        response_format={
            "type": "text"
        },
        temperature=1,
        max_tokens=1048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return openAI_response.choices[0].message.content
