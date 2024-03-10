import random
import time

from django.core.management import BaseCommand

from scores.models import Fixture

ITERATIONS = 10

class Command(BaseCommand):
    help = 'Generate a results for the games'

    def handle(self, *args, **options):

        for i in range(ITERATIONS):
            time.sleep(random.randint(1, 6))

            # Select how many fixtures we're going to update
            update_count = random.randint(1, 6)

            # Order by ("?") to get random records
            fixtures = Fixture.objects.filter(game_finished=False).order_by('?')

            # Get the fixtures to update
            fixtures = fixtures[:update_count]

            self.update_fixtures(fixtures)

            self.is_game_finished(fixtures)

    @staticmethod
    def update_fixtures(fixtures):
        """Add 1 or 2 goals to the home and away teams"""
        for fixture in fixtures:
            if fixture.game_finished:
                continue
            fixture.home_goals += random.randint(0, 2)
            fixture.away_goals += random.randint(0, 2)
        Fixture.objects.bulk_update(fixtures, ['home_goals', 'away_goals'])


    def is_game_finished(self, fixtures):
        """Mark the game as finished with a 30% chance"""
        for fixture in fixtures:
            if random.randint(1, 100) > 70:
                fixture.game_finished = True
                fixture.save()
