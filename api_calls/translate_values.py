def translate_values_to_polish(data: dict) -> dict:
    # Mapowanie wartości na opisy
    translations = {
        "sex": {1: "mężczyzna", 0: "kobieta"},
        "prevalentStroke": {1: "miał udar", 0: "nie miał udaru"},
        "BPMeds": {1: "bierze leki na nadciśnienie", 0: "nie bierze leków na nadciśnienie"},
        "prevalentHyp": {1: "ma nadciśnienie", 0: "nie ma nadciśnienia"},
        "diabetes": {1: "ma cukrzycę", 0: "nie ma cukrzycy"},
    }

    # Tworzenie nowego słownika, gdzie zmieniają się tylko wartości 0 i 1
    translated_data = {
        key: translations[key][value] if key in translations and value in translations[key] else value
        for key, value in data.items()
    }

    return translated_data
