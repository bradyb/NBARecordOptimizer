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

def _GetNextWeek(week, off_ratings, def_ratings, picks):
	week_expectation = dict()
	for team in nba_site_constants.TEAMS
		if team in picks:
			continue
		wins, losses, team = _TeamForWeek(nba_site_constants.TEAMS[team], 
										  week, 
										  off_ratings, 
										  def_ratings)
		week_expectation[team] = (wins, losses)
	return week_expectation

def _GetBestPlans(offensive_ratings, def_ratings, week,
				 total_wins, total_losses, picks):
	# Return Top 3 of Next Week
	week_expectation = _GetNextWeek(week, off_ratings, def_ratings, picks)

	if week < 24:
		# Return the top 3 of these list
	else:
		# Return the best plans continuing the with top 3


def FindBestPlan():
	offensive_ratings = _LoadJSONFile(nba_site_constants.
										OFFENSIVE_TEAM_RATINGS_FILE)
	defensive_ratings = _LoadJSONFile(nba_site_constants.
										DEFENSIVE_TEAM_RATINGS_FILE)

	total_wins, total_losses = _GetCurrentScore()

	plans = _GetBestPlans(offensive_ratings, def_ratings, 
						nba_site_constants.WEEKS_PLAYED,
						total_wins, total_losses, nba_site_constants.PICKS.copy())

	return _BestPlan(plans)



def FormatPlan(plan):
    return sorted( ((value, key) for key, value in plan.items()), reverse=True)


def ComputeNextPick():
	rating_loader.LoadRatings()
	plan = FindBestPlan()
	print FormatPlan(plan)

if __name__ == "__main__":
	ComputeNextPick()