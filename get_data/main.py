from riotwatcher import LolWatcher
from collections import defaultdict
from pprint import pprint

# REGION constant can be set to any desired region code
REGION = 'NA1'

# QueueID value for Ranked
RANKED_QUEUE = 420


# Gets API key from a file in .gitignore, hiding the key.
def api_key():
    with open('api_key.txt', 'r') as key:
        return key.read().strip()


api = LolWatcher(api_key())


def get_challenger_players_ids():
    challenger_league = api.league.challenger_by_queue(region=REGION, queue='RANKED_SOLO_5x5')
    return challenger_league['entries']


def get_puuid_from_summoner(summoner):
    return api.summoner.by_id(region=REGION, encrypted_summoner_id=summoner['summonerId'])['puuid']


def get_matchlist_from_puuid(summoner_puuid):
    return api.match.matchlist_by_puuid(region=REGION, puuid=summoner_puuid)


def iterate_most_played_role_from_puuid(summoner_puuid, previous_role_frequency):
    summoner = api.summoner.by_puuid(region=REGION, encrypted_puuid=summoner_puuid)
    summoner_matchlist = api.match.matchlist_by_puuid(region=REGION, puuid=summoner_puuid)
    summoner_role_frequency = defaultdict(int)

    for match in summoner_matchlist[:7]:
        match_details = api.match.by_id(region=REGION, match_id=match)
        match_type = match_details['info']['queueId']
        match_info = match_details['info']

        if match_type != RANKED_QUEUE:
            continue

        for player in match_info['participants']:
            if summoner['puuid'] == player['puuid']:
                if player['individualPosition'] != 'Invalid':
                    summoner_role_frequency[player['individualPosition']] += 1

    if len(summoner_role_frequency) != 0:
        role = max(summoner_role_frequency, key=summoner_role_frequency.get)
        previous_role_frequency[role] += 1
        print('Summoner ' + summoner['name'] + "'s main role is " + role)
    else:
        print('Summoner ' + summoner['name'] + "'s has not played ranked in 6 games")


def get_most_mained_role_in_challenger():
    summoners = get_challenger_players_ids()
    main_role_frequency = defaultdict(int)

    for summoner in summoners:
        summoner_puuid = get_puuid_from_summoner(summoner)
        iterate_most_played_role_from_puuid(summoner_puuid, main_role_frequency)
        pprint(dict(main_role_frequency))

    return max(main_role_frequency, key=main_role_frequency.get)


print('The most mained role in challenger is ' + get_most_mained_role_in_challenger())
