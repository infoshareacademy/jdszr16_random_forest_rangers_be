import openai
import os

api_key = os.getenv("OPENAI_API_KEY")
api_org = os.getenv("OPENAI_API_ORG")

def get_illness_info(is_doctor=False, length=10, disease="cukrzyca", value=""):
    openai.api_key = api_key

    if is_doctor:
        taskContent = (
            "Jesteś lekarzem, profesorem medycyny i farmaceutą. "
            "Znasz nazwy leków po łacinie i używasz skomplikowanego języka medycznego. "
            "W tekstach stosujesz terminologię fachową, opisujesz choroby po łacinie "
            "i koncentrujesz się na szczegółowych metodach leczenia i diagnostyki."
        )
    else:
        taskContent = (
            "Nie jesteś lekarzem. Twój styl jest bardzo prosty, przystępny i skierowany "
            "do osób, które nie mają wiedzy medycznej. Unikasz trudnych terminów, "
            "podajesz proste wyjaśnienia i wskazówki dotyczące zdrowia."
        )


    if is_doctor:
        user_content = (
            f"Napisz tekst o {disease}. Zmiesc się w {length} zdaniach. "
            f"Sprawdź, czy wartość {value} mieści się w przyjętym zakresie i koniecznie to oceń. Jesli wartosci sie nie mieszcze to podawaj wartosci normy i zaproponuj medykamenty"
            f"Podaj nazwę leku po łacinie oraz sposób leczenia. "
            f"Zalec dodatkowe badania diagnostyczne. Pisz w trzeciej osobie liczby pojedynczej jako o pacjencie. "
            f"W pewnych przypdkach {value} moze byc Tak lub Nie. Oznacza to ze pacjent moze miec {disease} lub nie."
        )
    else:
        user_content = (
            f"Napisz tekst o {disease}. Zmieszcz się w {length+4} zdaniach. "
            f"Sprawdź, czy wartość {value} mieści się w przyjętym zakresie i oceń to w prostych słowach. "
            f"Unikaj trudnych terminów i podaj proste zalecenia dotyczące zdrowia. Sproboj czytelnika rozsmieszyc "
            f"W pewnych przypdkach {value} moze byc Tak lub Nie. Oznacza to ze pacjent moze miec {disease} lub nie."
        )

    client = openai.OpenAI(api_key=api_key, organization=api_org)

    openAI_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": taskContent},
            {"role": "user", "content": user_content}
        ],
        temperature=1,
        max_tokens=1048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return openAI_response.choices[0].message.content