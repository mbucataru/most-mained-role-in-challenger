from riotwatcher import LolWatcher, ApiError
from collections import defaultdict

LAN = 'LA1'

NA = 'NA1'

# REGION constant can be set to any of the above regions
REGION = LAN


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

# Takes in either a puuid or a name and returns a dict of their role frequency in their last 20 games
def most_played_roles(puuid=None, name=None):
    if name:
        summoner = api.summoner.by_name(region=REGION, summoner_name=name)
    elif puuid:
        summoner = api.summoner.by_puuid(region=REGION, encrypted_puuid=puuid)
    else:
        raise ValueError("You must provide either a PUUID or a name.")
    print(summoner)
    summoner_matchlist = matchlist(summoner['puuid'])
    role_frequency = defaultdict(int)

    for match in summoner_matchlist:
        match_details = api.match.by_id(region=REGION, match_id=match)
        match_info = match_details['info']
        for player in match_info['participants']:
            if summoner['puuid'] == player['puuid']:
                role_frequency[player['individualPosition']] += 1

    print(role_frequency)

challenger_players = challenger_players()

summoner1_matchlist = matchlist(puuid(challenger_players[0]))

most_played_roles(puuid='tWaCuoPkUPuqJIPvDeGkSVp1MFsVaJ1ukNJjVSZVif3cBGo9KZPsvbWRga9Mmo6cZYjxUgXWbBIutw')

#first_match = api.match.by_id(region=REGION, match_id=matchlist[0])


#print(first_match)

#print(api.match.timeline_by_match(REGION, matchlist[0]))



#names_of_participants(first_match)

# for player in challenger_players['entries']:
# print(player['summonerName'])
