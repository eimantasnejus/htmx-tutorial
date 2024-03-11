from django.core.management import BaseCommand

from scores.models import Fixture, Team, Tournament

TEAMS = [
    "Arsenal",
    "Aston Villa",
    "Bournemouth",
    "Brighton",
    "Burnley",
    "Chelsea",
    "Crystal Palace",
    "Everton",
    "Leicester",
    "Liverpool, Manchester City",
    "Manchester United",
    "Newcastle",
    "Norwich",
    "Sheffield United",
    "Southampton",
    "Tottenham",
    "Watford",
    "West Ham",
    "Wolves",
    "Willows",
]


class Command(BaseCommand):
    help = "Load EPL teams and fixtures"

    def handle(self, *args, **kwargs):
        # Create the tournament
        tournament = Tournament.objects.get_or_create(name="Premier League")[0]

        # Create the teams
        for team in TEAMS:
            Team.objects.get_or_create(name=team)
        teams = Team.objects.all()

        # Create a set of fixtures from the teams list
        fixtures = []
        for i in range(0, len(teams), 2):
            fixtures.append(Fixture(home_team=teams[i], away_team=teams[i + 1], tournament=tournament))
        if Fixture.objects.count() == 0:
            Fixture.objects.bulk_create(fixtures)
