import openai
import os

# from api_cals.translate_values import translate_values_to_polish
from api_calls.translate_values import translate_values_to_polish
api_key = os.getenv("OPENAI_API_KEY")
api_org = os.getenv("OPENAI_API_ORG")



def get_illness_all_data(is_doctor=False, probability_value  = "", input_values = ''):
    openai.api_key = api_key


    input_values = input_values.model_dump()
    translated_data = translate_values_to_polish(data = input_values)
    translated_data.pop("education", None)

    # Tworzenie czytelnego opisu pacjenta na podstawie przetworzonych danych
    patient_summary = ", ".join([f"{key}: {value}" for key, value in translated_data.items()])
    probability_value_txt = round(probability_value * 100, 2).astype(str) + " %"


    if is_doctor:
        taskContent = (
            "Jesteś lekarzem, profesorem medycyny i farmaceutą. "
            "Znasz nazwy leków po łacinie i używasz skomplikowanego języka medycznego. "
            "W tekstach stosujesz terminologię fachową, opisujesz choroby po łacinie "
            "i koncentrujesz się na szczegółowych metodach leczenia i diagnostyki. "
            f"Jesli {probability_value} jest wieksze od 0.5 badz bardzo surowy w ocenie pacjenta. "
        )
    else:
        taskContent = (
            "Nie jesteś lekarzem. Twój styl jest bardzo prosty, przystępny i skierowany "
            "do osób, które nie mają wiedzy medycznej. Unikasz trudnych terminów, "
            "podajesz proste wyjaśnienia i wskazówki dotyczące zdrowia."
        )


    if is_doctor:
        user_content = (
            f"Zawsze zaczynaj zdaniem: Na podstawie podanych informacji, ryzyko zachorowania pacjenta na choroby serca w ciągu nastepnych dziesięciu lat wynosi {probability_value_txt}. Rob pozniej jedna linijke przerwy.  "
            f"Zawsze pisz w 3 osobie. Zrob opis stanu zdrowia pacjenta na podstawie tych informacji: {patient_summary}. Jesli jakis wynik nie jest w normie zawsze podawaj zakresy normy"
            f"Unikaj trudnych terminów, podaj proste zalecenia dotyczące zdrowia i stylu życia. W opisie odwoluj sie do wyslanych wartosci"
            f"Jesli zobaczysz ze pewne parametry sa powyzej normy podawaj zalecenia na dalsze badania. Badzi szczegolowy. Zaproponuj jak sie leczyc i odrzywiac "
            f"W woich odpowiedziach nie uzywaj gwiazdek. Jesli tworzysz nowe wiersze, nie zostawiaj duzych przerw miedzy nimi. Najwyzej jedna linijka przerwy"

        )
    else:
        user_content = (
            f"Zawsze zaczynaj zdaniem: Na podstawie podanych informacji, Twoje ryzyko zachorowania na choroby serca w ciągu nastepnych dziesieciu lat wynosi {probability_value_txt}. Rob pozniej jedna linijke przerwy.  "
            f"Zrob opis stanu zdrowia pacjenta na podstawie tych informacji: {patient_summary}. Jesli jakis wynik nie jest w normie zawsze podawaj zakresy normy"
            f"Unikaj trudnych terminów, podaj proste zalecenia dotyczące zdrowia i stylu życia. W opisie odwoluj sie do wyslanych wartosci"
            f"Jesli zobaczysz ze pewne parametry sa powyzej normy to zalecaj wizyte u lekarza. Zaproponuj jak sie leczyc i odrzywiac "
            f"W woich odpowiedziach nie uzywaj gwiazdek. Jesli tworzysz nowe wiersze, nie zostawiaj duzych przerw miedzy nimi. Najwyzej jedna linijka przerwy"

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

