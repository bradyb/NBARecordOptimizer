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

def _ScoreForWeek(team_name, week, oratings, dratings):
    opponents = []
	# Get the teams that the team plays this week
	# Count the number of back to backs?
	expected_wins = 0
	for opponent in opponents:
	    expected_wins = expected_wins + _ProbAWinsVs(oratings[team_name],
	                                                 dratings[team_name],
	                                                 oratings[opponent],
	                                                 dratings[opponent])
    return expected_wins

def _ComputePlanScore(permutation):
	score = 0
	for team_index, week in itertools.izip(permutation,
										   range(0, 24-nba_site_constants.WEEKS_PLAYED)):
		score = score + _ScoreForWeek(nba_site_constants.TEAMS[team_index], week)
	return score

def FindOptimalPlan():
	offensive_ratings = _LoadJSONFile(nba_site_constants.OFFENSIVE_TEAM_RATINGS_FILE)
	defensive_ratings = _LoadJSONFile(nba_site_constants.DEFENSIVE_TEAM_RATINGS_FILE)

	max_score = 0
	opt_permutation = None

	for permutation in itertools.permutations(range(0,len(nba_site_constants.TEAMS) - nba_site_constants.WEEKS_PLAYED),
													24 - nba_site_constants.WEEKS_PLAYED):
		score = _ComputePlanScore(permutation)
		if score > max_score:
			max_score = score
			opt_permutation = permutation

	return permutation



def FormatPlan(plan):
    print nba_site_constants.TEAMS[plan[0]]


def ComputeNextPick():
	rating_loader.LoadRatings()
	plan = FindOptimalPlan()
	print FormatPlan(plan)

if __name__ == "__main__":
	ComputeNextPick()