from riotwatcher import LolWatcher, ApiError


def get_api_key():
    with open('api_key.txt', 'r') as key:
        return key.read().strip()

api = LolWatcher(get_api_key())

my_region = 'NA'
v4 = api.league

summoners = v4.entries(region='NA1', queue='RANKED_SOLO_5x5', tier='DIAMOND', division='III', page=1)

print(summoners)

for summoner in summoners:
    try:
        response = api.summoner.by_id(region='NA1', encrypted_summoner_id=summoner['summonerId'])
        match_list = api.match.matchlist_by_puuid(region='NA1', puuid=response['puuid'], queue=420)
        for match in match_list:
            current_match = api.match.timeline_by_match(region='NA1', match_id=match)


    except ApiError as err:
        if err.response.status_code == 429:
            print('We should retry in {} seconds.'.format(err.response.headers['Retry-After']))
            print('this retry-after is handled by default by the RiotWatcher library')
            print('future requests wait until the retry-after time passes')
        elif err.response.status_code == 404:
            print('Summoner with that ridiculous name not found.')

# all objects are returned (by default) as a dict
# lets see if i got diamond yet (i probably didnt)
# my_ranked_stats = api.league.by_summoner(my_region, me['id'])
# print(my_ranked_stats)

# First we get the latest version of the game from data dragon
# versions = api.data_dragon.versions_for_region(my_region)
# champions_version = versions['n']['champion']

# Lets get some champions
# current_champ_list = api.data_dragon.champions(champions_version)
# print(current_champ_list)

# For Riot's API, the 404 status code indicates that the requested data wasn't found and
# should be expected to occur in normal operation, as in the case of a an
# invalid summoner name, match ID, etc.
#
# The 429 status code indicates that the user has sent too many requests
# in a given amount of time ("rate limiting").
