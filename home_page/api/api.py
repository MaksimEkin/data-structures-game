"""
    API for Homepage.
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from home_page.database import home_page_db as db


@api_view(['GET'])
def api_overview(request):
    """
    Overview of the API calls exist.

    :param request:
    :return: Response, list of API URLs.
    """
    api_urls = {
        'Top Ranking Users': '/rankings/<int:top_n>',
    }
    return Response(api_urls)


@api_view(['GET'])
def rankings(request, top_n):
    """
    Creates a new game board.

    :param request:
    :param top_n: how many top players to return
    :return game JSON of list :
    """

    # Check if the number of players request is valid
    if int(top_n) > 50 or int(top_n) <= 0:
        return Response({'error': 'Invalid number of players requested',
                         'max': 50,
                         'min': 0},
                        status=status.HTTP_400_BAD_REQUEST)

    # get the top n players
    players_info = list()
    for ii, cursor in enumerate(db.get_rankings()):

        # done
        if ii > int(top_n):
            break

        temp = {'user_id': cursor['user_id'], 'points': round(cursor['points'], 2)}

        # get the user info from db
        players_info.append(temp)

    return Response({'top_ranking_players': players_info, 'n': int(top_n)})
