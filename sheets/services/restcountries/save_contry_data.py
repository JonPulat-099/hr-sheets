import requests
from django.core.files.base import ContentFile
from sheets.models import Country


def save_data(data):
    name_ru = data.get("translations", {}).get("rus", {}).get("common", "Unknown")
    flag_url = data.get("flags", {}).get("png", "")

    if flag_url:
        flag_response = requests.get(flag_url)
        if flag_response.status_code == 200:
            country, created = Country.objects.get_or_create(iso_code=data.get("cca3"))
            country.name_ru = name_ru
            country.flag.save(
                f"{data.get("cca3").lower()}.png",
                ContentFile(flag_response.content),
                save=True,
            )
            print(f"Saved {data.get("cca3")}: {name_ru}")
