import itertools
import json

from django.conf import settings
from django.core.management import BaseCommand

from gdp.models import GDP


class Command(BaseCommand):
    help = "Load GDP data"

    def handle(self, *args, **kwargs):
        if not GDP.objects.exists():
            datafile = settings.BASE_DIR / "gdp" / "data" / "gdp.json"
            with open(datafile) as f:
                data = json.load(f)

            # Clean regional data and leave country data only
            data = itertools.dropwhile(lambda x: x["Country Name"] != "Afghanistan", data)

            gdps = []
            for item in data:
                gdps.append(
                    GDP(
                        country=item["Country Name"],
                        country_code=item["Country Code"],
                        year=item["Year"],
                        gdp=item["Value"],
                    )
                )
            GDP.objects.bulk_create(gdps)
