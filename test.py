import cassiopeia as cass
import os
from cassiopeia import Summoner
import datetime
import pycurl
import certifi
import arrow

curl = pycurl.Curl()
curl.setopt(pycurl.CAINFO, certifi.where())

API_KEY = os.environ.get("RIOT_API_KEY")
cass.set_riot_api_key(API_KEY)
cass.set_default_region("NA")

person = "snowcola"
summoner = Summoner(name=person, region="NA")

positions = summoner.league_positions
print(f"{positions.fives.tier} {positions.fives.division}")
#print(f"{wins}   {total_games}  {wins/total_games*100}")
