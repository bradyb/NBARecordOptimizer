import json
import nba_site_constants
import rating_loader

def _LoadJSONFile(file_name):
	with open(file_name) as file:
		data = json.load(file)
	return data

def FindOptimalPlan():
	offensive_ratings = _LoadJSONFile(nba_site_constants.OFFENSIVE_TEAM_RATINGS_FILE)
	defensive_ratings = _LoadJSONFile(nba_site_constants.DEFENSIVE_TEAM_RATINGS_FILE)

	max_score = 0
	permutation = None

def FormatPlan(plan):
	pass

def ComputeNextPick():
	rating_loader.LoadRatings()
	plan = FindOptimalPlan()
	print FormatPlan(plan)

if __name__ == "__main__":
	ComputeNextPick()