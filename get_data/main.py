from riotwatcher import LolWatcher, ApiError


def get_api_key():
    with open('api_key.txt', 'r') as key:
        return key.read().strip()


# This API call returns a dict with a key called 'entries' that is an array of the players
def get_challenger_players():
    return api.league.challenger_by_queue(region='NA1', queue='RANKED_SOLO_5x5')


api = LolWatcher(get_api_key())

challenger_players = get_challenger_players()

for player in challenger_players['entries']:
    print(player['summonerName'])
