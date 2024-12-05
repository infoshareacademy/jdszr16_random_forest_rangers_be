import openai
import os

api_key = os.getenv("OPENAI_API_KEY")
api_org = os.getenv("OPENAI_API_ORG")


def get_illness_info(difficulty = 0, length = 10, subject = "cukrzyca"):
    openai.api_key = api_key

    print(difficulty, length, subject)
    taskContent = ''

    if difficulty == 1:
        taskContent = f"Jestes lekarzem. Profesorem medycyny i farmaceuta. Znasz nazwy lekow po lacine. W swoich tekstach podajesz nazwy nazwy chorob po lacinie. Piszesz teksty dla lekarzy w bardzo skomplikowany sposob"
    else:
        taskContent = f"Nie jestes lekarzem. Piszesz bardzo proste teksty dla osob bez znajomosci medycyny."

    print(taskContent)



    client = openai.OpenAI(api_key=api_key, organization=api_org)
    openAI_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": taskContent
            },
            {
                "role": "user",
                "content": f"napisz text o  {subject}. Zmiesc sie w {length} zdaniach.",
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