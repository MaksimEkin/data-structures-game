"""
Run: python manage.py test home_page.api.tests_api
Reference: https://www.django-rest-framework.org/api-guide/testing/
"""
from django.test import TestCase

class BColors:
    """Colors for printing"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class APIOverview(TestCase):
    """Tests calls related to the overview of the API."""

    def test_index_loads_properly(self):
        """The index page loads properly"""

        response = self.client.get('')
        self.assertEqual(response.status_code, 200, msg=f'{BColors.FAIL}\t[-]\tResponse was not 200!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass return code api_overview.{BColors.ENDC}")


class Rankings(TestCase):
    """Tests the API call for getting top n ranking players"""

    def test_invalid_api_request(self):
        """Invalid API request. Too many or too few players requested"""

        # Test accessing to many players
        response = self.client.get('/api/rankings/55')

        self.assertEqual(response.status_code, 400, msg=f'{BColors.FAIL}\t[-]\tResponse was not 400 for too large numbers!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning the correct response code for too many players.{BColors.ENDC}")

        # Test accessing to less players
        response2 = self.client.get('/api/rankings/-1')

        self.assertEqual(response2.status_code, 400, msg=f'{BColors.FAIL}\t[-]\tResponse was not 400 for negative numers!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning the correct response code for negative number of players.{BColors.ENDC}")

    def test_top_n(self):
        """Test getting top n players"""

        # Test accessing to many players
        response = self.client.get('/api/rankings/2')

        self.assertEqual(response.status_code, 200, msg=f'{BColors.FAIL}\t[-]\tResponse was not 200!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning correct response code for requesting top n players.{BColors.ENDC}")

        top_n_players = response.data['top_ranking_players']
        n = response.data['n']

        self.assertEqual(n, 2, msg=f'{BColors.FAIL}\t[-]\tWrong number of players returned!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning correct number of players{BColors.ENDC}")

        first_player = top_n_players[0]['points']
        second_player = top_n_players[1]['points']

        self.assertEquals(first_player >= second_player, True,  msg=f'{BColors.FAIL}\t[-]\tWrong ordering!{BColors.ENDC}')
        print(f"{BColors.OKGREEN}\t[+]\tPass returning correct ordering of players{BColors.ENDC}")
