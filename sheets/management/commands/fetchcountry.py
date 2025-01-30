import requests
from django.core.management.base import BaseCommand, CommandError
from sheets.services.restcountries.save_contry_data import save_data


class Command(BaseCommand):
    help = "Fetch & save country data"

    def handle(self, *args, **options):
        self.stdout.write("🟢 Command runned successfully")
        try:
            url = f"https://restcountries.com/v3.1/all"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                print(f"Fetched {len(data)} countries")
                save_data(data)

            else:
                self.stdout.write(
                    f"❌ Failed to fetch data, status code: {response.status_code}"
                )

        except Exception as e:
            self.stdout.write(f"❌ Failed to fetch data: {e}")

        self.stdout.write("🔵 Command completed")
