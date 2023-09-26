from riotwatcher import LolWatcher, ApiError
from collections import defaultdict

LAN = 'LA1'

NA = 'NA1'

# REGION constant can be set to any of the above regions
REGION = NA


# Gets API key from a file in .gitignore, hiding the key.
def api_key():
    with open('api_key.txt', 'r') as key:
        return key.read().strip()


api = LolWatcher(api_key())


# Returns an array of all challenger players on NA
def challenger_players():
    challenger_league = api.league.challenger_by_queue(region=REGION, queue='RANKED_SOLO_5x5')
    return challenger_league['entries']


# Takes in a summoner and returns its PUUID
def puuid(summoner):
    return api.summoner.by_id(region=REGION, encrypted_summoner_id=summoner['summonerId'])['puuid']


# Takes in a PUUID and returns its matchlist (an array of match IDs)
def matchlist(summoner_puuid):
    return api.match.matchlist_by_puuid(region=REGION, puuid=summoner_puuid)


# Takes in a match and returns the names of the players in the game
def names_of_participants(match):
    for player in match['metadata']['participants']:
        print(api.summoner.by_puuid(region=REGION, encrypted_puuid=player)['name'])

dd = defaultdict(int)
# Takes in either a puuid or a name and returns a dict of their role frequency in their last 20 games
def most_played_role(puuid=None, name=None, counter_dict=None):
    if name:
        summoner = api.summoner.by_name(region=REGION, summoner_name=name)
    elif puuid:
        summoner = api.summoner.by_puuid(region=REGION, encrypted_puuid=puuid)
    else:
        raise ValueError("You must provide either a PUUID or a name.")
    print(summoner)
    summoner_matchlist = matchlist(summoner['puuid'])
    if counter_dict:
        role_frequency = counter_dict
    else:
        role_frequency = defaultdict(int)

    for match in summoner_matchlist[:3]:
        match_details = api.match.by_id(region=REGION, match_id=match)
        print(match_details)
        matchid = match_details['info']['queueId']
        if match_details['info']['queueId'] != 420:
            print('skipped')
            continue
        match_info = match_details['info']
        for player in match_info['participants']:
            if summoner['puuid'] == player['puuid']:
                if player['individualPosition'] != 'Invalid':
                    # print('THE DICT IS')
                    # print(role_frequency)
                    role_frequency[player['individualPosition']] += 1
    if role_frequency:
        role = max(role_frequency, key=role_frequency.get)
        return role


def most_mained_role_in_challenger():
    summoners = challenger_players()
    main_role_frequency = defaultdict(int)
    for summoner in summoners:
        summoner_puuid = puuid(summoner)
        main_role_frequency[most_played_role(puuid=summoner_puuid)] += 1
        print(main_role_frequency)
    return max(main_role_frequency, key=main_role_frequency.get)


# challenger_players = challenger_players()
# print(challenger_players)

# summoner1_matchlist = matchlist(puuid(challenger_players[0]))


print(most_mained_role_in_challenger())

# most_played_roles(puuid='tWaCuoPkUPuqJIPvDeGkSVp1MFsVaJ1ukNJjVSZVif3cBGo9KZPsvbWRga9Mmo6cZYjxUgXWbBIutw')

# first_match = api.match.by_id(region=REGION, match_id=summoner1_matchlist[0])


# print(first_match)

# print(api.match.timeline_by_match(REGION, matchlist[0]))


# names_of_participants(first_match)

# for player in challenger_players['entries']:
# print(player['summonerName'])
