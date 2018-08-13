import cassiopeia as cass
import os
from cassiopeia import Summoner
import datetime
import pycurl
import certifi
import arrow

curl = pycurl.Curl()
curl.setopt(pycurl.CAINFO, certifi.where())
#curl.setopt(pycurl.URL, 'https://www.quora.com')
#curl.perform()

API_KEY = os.environ.get("RIOT_API_KEY")
cass.set_riot_api_key(API_KEY)
cass.set_default_region("NA")

person = "snowcola"
summoner = Summoner(name=person, region="NA")


last_week = datetime.datetime.now() - datetime.timedelta(weeks=1)
year = last_week.year
month = last_week.month
day = last_week.day
matchhistory = cass.MatchHistory(summoner=summoner, 
                                    begin_time=arrow.Arrow(year, month, day), 
                                    end_time=arrow.now())

wins = 0
total_games = len(matchhistory)
for match in matchhistory:
    if match.participants[summoner].team.win:
        wins += 1

print(f"{wins}   {total_games}  {wins/total_games*100}")