import json
import pandas as pd
import requests
import os

import nba_site_constants

def ScrapeURL(base_url, parameters):
    response = requests.get(base_url, params=parameters, headers={
	'Accept': 'application/json, text/plain, */*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Connection': 'keep-alive',
	'Host': 'stats.nba.com',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	'x-nba-stats-origin': 'stats',
	'x-nba-stats-token': 'true',
	'X-NewRelic-ID': 'VQECWF5UChAHUlNTBwgBVw=='
})
    response.raise_for_status()
    headers = response.json()['resultSets'][0]['headers']
    stats = response.json()['resultSets'][0]['rowSet']
    stats_df = pd.DataFrame(stats, columns=headers)
    stats_df['Season'] = parameters['Season']
    return stats_df

def LoadRatings():
 	data_frame = ScrapeURL(nba_site_constants.TEAM_STATS_URL, 
 						   nba_site_constants.TEAM_PARAMETERS)

 	# map of team name to respective team ratings
 	offensive_rating = dict()
 	defensive_rating = dict()

 	for index, row in data_frame.iterrows():
 		offensive_rating[row[nba_site_constants.TEAM_INDEX]] = row[nba_site_constants.OFFENSIVE_RATING_INDEX]
 		defensive_rating[row[nba_site_constants.TEAM_INDEX]] = row[nba_site_constants.DEFENSIVE_RATING_INDEX]
 	with open(nba_site_constants.OFFENSIVE_TEAM_RATINGS_FILE, 'w') as offensive_file:
 		offensive_file.write(json.dumps(offensive_rating))
 	with open(nba_site_constants.DEFENSIVE_TEAM_RATINGS_FILE, 'w') as defensive_file:
 		defensive_file.write(json.dumps(defensive_rating))

if __name__ == "__main__":
    LoadRatings()