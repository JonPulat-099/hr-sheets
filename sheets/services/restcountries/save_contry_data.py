import requests
from django.core.files.base import ContentFile
from sheets.models import Country  # Change "myapp" to your actual app name


def fetch_country_data(iso_code):
    url = f"https://restcountries.com/v3.1/alpha/{iso_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]  # Extract first country object

        name_ru = data.get("translations", {}).get("rus", {}).get("common", "Unknown")
        flag_url = data.get("flags", {}).get("png", "")

        if flag_url:
            flag_response = requests.get(flag_url)
            if flag_response.status_code == 200:
                country, created = Country.objects.get_or_create(iso_code=iso_code)
                country.name_ru = name_ru
                country.flag.save(
                    f"{iso_code.lower()}.png",
                    ContentFile(flag_response.content),
                    save=True,
                )
                print(f"Saved {iso_code}: {name_ru}")
    else:
        print(f"Failed to fetch data for {iso_code}")
