TEAM_STATS_URL = 'http://stats.nba.com/stats/leaguedashteamstats?'

TEAM_PARAMETERS = {
	'Conference': '',
	'DateFrom': '',
	'DateTo': '',
	'Division': '',
	'GameScope': '',
	'GameSegment': '',
	'LastNGames': 0,
	'LeagueID': "00",
	'Location': '',
	'MeasureType': "Advanced",
	'Month': 0,
	'OpponentTeamID': 0,
	'Outcome': '',
	'PORound': 0,
	'PaceAdjust': "N",
	'PerMode': "PerGame",
	'Period': 0,
	'PlayerExperience': '',
	'PlayerPosition': '',
	'PlusMinus': "N",
	'Rank': "N",
	'Season': "2018-19",
	'SeasonSegment': '',
	'SeasonType': "Regular Season",
	'ShotClockRange': '',
	'StarterBench': '',
	'TeamID': 0,
	'VsConference': '',
	'VsDivision': '',
}

OFFENSIVE_TEAM_RATINGS_FILE = 'oteam_ratings.txt'
DEFENSIVE_TEAM_RATINGS_FILE = 'dteam_ratings.txt'

REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

TEAM_INDEX = 1
OFFENSIVE_RATING_INDEX = 8
DEFENSIVE_RATING_INDEX = 10