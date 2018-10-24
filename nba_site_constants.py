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

REQUEST_HEADERS_OLD = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
    'Host': 'stats.nba.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

REQUEST_HEADERS = {
	'Accept': 'application/json, text/plain, */*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'en-US,en;q=0.9',
	'Connection': 'keep-alive',
	'Cookie': '_ga=GA1.2.1377756853.1539757763; ug=5b51910b01e4710a3c09a42b88002f3d; __gads=ID=99e90ba2f2ea239e:T=1539757764:S=ALNI_MYcZxwVPl4osHwbiUbDDXbM2o2QSg; _omappvp=rZqdlzsHNW0SRqZMt2AzaicL4xdNOCWDoIcQXsTBgEgYJNPDOINyv6rIFNHjegFn5bzsN5wKYIiQHCAgncCJVtZC9QxizgUu; check=true; AMCVS_248F210755B762187F000101%40AdobeOrg=1; AMCV_248F210755B762187F000101%40AdobeOrg=1687686476%7CMCIDTS%7C17828%7CMCMID%7C68712475597671435332818477153219687279%7CMCAAMLH-1540873734%7C9%7CMCAAMB-1540873734%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1540276134s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0; _gid=GA1.2.1670959731.1540268935; s_cc=true; AMCVS_7FF852E2556756057F000101%40AdobeOrg=1; AMCV_7FF852E2556756057F000101%40AdobeOrg=1687686476%7CMCIDTS%7C17828%7CMCMID%7C68709941649562229942818129117327216912%7CMCAAMLH-1540873736%7C9%7CMCAAMB-1540873736%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1540276136s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.0.0; ugs=1; ak_bmsc=FB5C1ECFE8F2A2BBBD64921E6642371D409158EA761300009BA3CE5B87631921~pliptG3JddbHbgXO0V3uOHMXPs6ypun6AEaq8yHkPYW11KsYiXUtF7Ylh4mn22/5jIC0rYEM5e+Yax6RCbbahjqLoZfsWsCiPADZMJ2GyEPf2jyIrcmOXcu+aTrIIyQXUA+8ij7tjGYqKIV4uOijcKcr4n+3eUy8BkMiITBH5ifh30j9EDKPa7yZ4PzXeZeliACQuEsflY4lYqRTzZI4yekOYqBgdkJVtqgo66SM7DL4o=; s_sq=%5B%5BB%5D%5D; _gat=1; bm_sv=5A9F520871019C1B8849EBFF0AF13F38~/AxbKFekR5vR4V/S1ofZq/hcYxmkmv9GP0Rx9Wj1VmMwoBk3UUazC+LvNkjnQCnP0tuIgJIYfFYwENe/Kv0GeYr+WqQGRMootyuoO11+IeZaNGCxBq0vxrjhfabmqpcsnd4hyj1DD3Ee0lrg/QsGDQ==; mbox=PC#62c73d03aa7b417c929e547499f4c01e.28_3#1603002564|session#84992069b0ef4f6a8db8f56185c3cb40#1540270940',
	'Host': 'stats.nba.com',
	'Referer': 'https://stats.nba.com/teams/advanced/?sort=OFF_RATING&dir=-1&Season=2018-19&SeasonType=Regular%20Season',
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
	'x-nba-stats-origin': 'stats',
	'x-nba-stats-token': 'true',
	'X-NewRelic-ID': 'VQECWF5UChAHUlNTBwgBVw=='
}

TEAM_INDEX = 1
OFFENSIVE_RATING_INDEX = 8
DEFENSIVE_RATING_INDEX = 10

TEAMS = [
	"Boston Celtics",
	"Brooklyn Nets",
	"New York Knicks",
	"Philadelphia 76ers",
	"Toronto Raptors",
	"Chicago Bulls",
	"Cleveland Cavaliers",
	"Detroit Pistons",
	"Indiana Pacers",
	"Milwaukee Bucks",
	"Atlanta Hawks",
	"Charlotte Hornets",
	"Miami Heat",
	"Orlando Magic",
	"Washington Wizards",
	"Denver Nuggets",
	"Minnesota Timberwolves",
	"Oklahoma City Thunder",
	"Portland Trail Blazers",
	"Utah Jazz",
	"Golden State Warriors",
	"LA Clippers",
	"Los Angeles Lakers",
	"Phoenix Suns",
	"Sacramento Kings",
	"Dallas Mavericks",
	"Houston Rockets",
	"Memphis Grizzlies",
	"New Orleans Pelicans",
	"San Antonio Spurs"
]

PICKS = {
	"Philadelphia 76ers": {'week': 0, 'wins': 2, 'losses': 1}
}

TEAMNAME_MAP = {
	"ATL":	"Atlanta Hawks",
	"BKN":	"Brooklyn Nets",
	"BOS":	"Boston Celtics",
	"CHA":	"Charlotte Hornets",
	"CHI":	"Chicago Bulls",
	"CLE":	"Cleveland Cavaliers",
	"DAL":	"Dallas Mavericks",
	"DEN":	"Denver Nuggets",
	"DET":	"Detroit Pistons",
	"GSW":	"Golden State Warriors",
	"HOU":	"Houston Rockets",
	"IND":	"Indiana Pacers",
	"LAC":	"LA Clippers",
	"LAL":	"Los Angeles Lakers",
	"MEM":	"Memphis Grizzlies",
	"MIA":	"Miami Heat",
	"MIL":	"Milwaukee Bucks",
	"MIN":	"Minnesota Timberwolves",
	"NOP":	"New Orleans Pelicans",
	"NYK":	"New York Knicks",
	"OKC":	"Oklahoma City Thunder",
	"ORL":	"Orlando Magic",
	"PHI":	"Philadelphia 76ers",
	"PHX":	"Phoenix Suns",
	"POR":	"Portland Trail Blazers",
	"SAC":	"Sacramento Kings",
	"SAS":	"San Antonio Spurs",
	"TOR":	"Toronto Raptors",
	"UTA":	"Utah Jazz",
	"WAS":	"Washington Wizards",
}

TEAMID_MAP = {
	"Boston Celtics": 1610612738,
	"Brooklyn Nets": 1610612751,
	"New York Knicks": 1610612752,
	"Philadelphia 76ers": 1610612755,
	"Toronto Raptors": 1610612761,
	"Chicago Bulls": 1610612741,
	"Cleveland Cavaliers": 1610612739,
	"Detroit Pistons": 1610612765,
	"Indiana Pacers": 1610612754,
	"Milwaukee Bucks": 1610612749,
	"Atlanta Hawks": 1610612737,
	"Charlotte Hornets": 1610612766,
	"Miami Heat": 1610612748,
	"Orlando Magic": 1610612753,
	"Washington Wizards": 1610612764,
	"Denver Nuggets": 1610612743,
	"Minnesota Timberwolves": 1610612750,
	"Oklahoma City Thunder": 1610612760,
	"Portland Trail Blazers": 1610612757,
	"Utah Jazz": 1610612762,
	"Golden State Warriors": 1610612744,
	"LA Clippers": 1610612746,
	"Los Angeles Lakers": 1610612747,
	"Phoenix Suns": 1610612756,
	"Sacramento Kings": 1610612758,
	"Dallas Mavericks": 1610612742,
	"Houston Rockets": 1610612745,
	"Memphis Grizzlies": 1610612763,
	"New Orleans Pelicans": 1610612740,
	"San Antonio Spurs": 1610612759
}

WEEKS_PLAYED = 1
