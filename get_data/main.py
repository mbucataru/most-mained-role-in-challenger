from riotwatcher import LolWatcher, ApiError

REGION = 'NA1'


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


# Takes in a summoner and returns its matchlist
def matchlist(summoner):
    return api.match.matchlist_by_puuid(region=REGION, puuid=puuid(summoner))

def names_of_participants(match):
    for player in match['metadata']['participants']:
        print(api.summoner.by_puuid(region=REGION, encrypted_puuid=player)['name'])



challenger_players = challenger_players()

matchlist = matchlist(challenger_players[0])


first_match = api.match.by_id(region=REGION, match_id=matchlist[0])


print(first_match)

print(api.match.timeline_by_match(REGION, matchlist[0]))



#names_of_participants(first_match)

# for player in challenger_players['entries']:
# print(player['summonerName'])
