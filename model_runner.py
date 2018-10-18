import itertools
import json
import nba_site_constants
import rating_loader

def _ProbAWinsVsB(a_ortg, a_drtg, b_ortg, b_drtg):
	a_win_pct = a_ortg**16.5/(a_ortg**16.5 + a_drtg**16.5)
	b_win_pct = b_ortg**16.5/(b_ortg**16.5 + b_drtg**16.5)
	return a_win_pct * (1 - b_win_pct)/(a_win_pct * (1 - b_win_pct) + b_win_pct * (1 - a_win_pct))


def _LoadJSONFile(file_name):
	with open(file_name) as file:
		data = json.load(file)
	return data

def FindOptimalPlan():
	offensive_ratings = _LoadJSONFile(nba_site_constants.OFFENSIVE_TEAM_RATINGS_FILE)
	defensive_ratings = _LoadJSONFile(nba_site_constants.DEFENSIVE_TEAM_RATINGS_FILE)

	max_score = 0
	permutation = None

	for team_index in itertools.permutations(range(0,30), 24):
		pass


def FormatPlan(plan):
	pass

def ComputeNextPick():
	rating_loader.LoadRatings()
	plan = FindOptimalPlan()
	print FormatPlan(plan)

if __name__ == "__main__":
	ComputeNextPick()