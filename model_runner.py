import itertools
import json

import nba_site_constants
import rating_loader

def _ProbAWinsVsB(a_ortg, a_drtg, b_ortg, b_drtg):
	a_win_pct = a_ortg**16.5/(a_ortg**16.5 + a_drtg**16.5)
	b_win_pct = b_ortg**16.5/(b_ortg**16.5 + b_drtg**16.5)
	return a_win_pct * (1 - b_win_pct)/(a_win_pct * (1 - b_win_pct) + b_win_pct * (1 - a_win_pct))

def _GetCurrentScore():
	total_wins = 0
	total_losses = 0
	for wins, losses in nba_site_constants.PAST_SCORES:
		total_wins += wins
		total_losses += losses
	return total_wins, total_losses



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

def _GetNextteam(week, off_ratings, def_ratings, current_plan):
	week_expectation = dict()
	best_team = None
	best_wins = 0
	best_losses = 0
	for team in nba_site_constants.TEAMS
		wins, losses, team = _TeamForWeek(nba_site_constants.TEAMS[team], 
										  week, 
										  off_ratings, 
										  def_ratings)
	return best_wins, best_losses, best_team

def FindBestPlan():
	offensive_ratings = _LoadJSONFile(nba_site_constants.
										OFFENSIVE_TEAM_RATINGS_FILE)
	defensive_ratings = _LoadJSONFile(nba_site_constants.
										DEFENSIVE_TEAM_RATINGS_FILE)

	total_wins, total_losses = _GetCurrentScore()
	next_team = None
	current_plan = dict()

	scores = _GetNextWeek(week, 
						  offensive_ratings, 
						  defensive_ratings, 
						  current_plan)

	return current_plan



def FormatPlan(plan):
    return sorted( ((value, key) for key, value in plan.items()), reverse=True)


def ComputeNextPick():
	rating_loader.LoadRatings()
	plan = FindBestPlan()
	print FormatPlan(plan)

if __name__ == "__main__":
	ComputeNextPick()