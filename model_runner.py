import itertools
import json
import pprint as pp
import requests

import nba_site_constants
import rating_loader


class PlanFinder:

	def _FormScheduleUrl(self, date):
		return nba_site_constants.PROD_URL + str(date) + '/scoreboard.json'

	def _UpdateOpponents(self, teams_opponents, hteam_id, vteam_id):
		if hteam_id in teams_opponents:
			teams_opponents[hteam_id].append(vteam_id)
		else:
			teams_opponents[hteam_id] = [vteam_id]
		if vteam_id in teams_opponents:
			teams_opponents[vteam_id].append(hteam_id)
		else:
			teams_opponents[vteam_id] = [hteam_id]		

	def _GetSchedule(self, date):
		url = self._FormScheduleUrl(date)
		response = requests.get(url)
		response.raise_for_status()
		teams_opponents = dict()
		for game in response.json()['games']:
			self._UpdateOpponents(teams_opponents, game['hTeam']['teamId'], game['vTeam']['teamId'])
		return teams_opponents

	def _ProbAWinsVsB(self, a_ortg, a_drtg, b_ortg, b_drtg):
		a_win_pct = a_ortg**16.5/(a_ortg**16.5 + a_drtg**16.5)
		b_win_pct = b_ortg**16.5/(b_ortg**16.5 + b_drtg**16.5)
		return a_win_pct * (1 - b_win_pct)/(a_win_pct * (1 - b_win_pct) + b_win_pct * (1 - a_win_pct))

	def _GetCurrentScore(self):
		total_wins = 0
		total_losses = 0
		for pick_info in nba_site_constants.PICKS.itervalues():
			total_wins += pick_info['wins']
			total_losses += pick_info['losses']
		return total_wins, total_losses

	def _LoadJSONFile(self, file_name):
		with open(file_name) as file:
			data = json.load(file)
		return data

	def _TeamScoreForWeek(self, team_name, opponents, oratings, dratings):
		expected_wins = 0
		for opponent in opponents:
			expected_wins = expected_wins + _ProbAWinsVsB(oratings[team_name],
	    		dratings[team_name],
	    		oratings[opponent],
	    		dratings[opponent])
		return expected_wins

	def _GetWeekSchedule(self, week, weeks_list):
		games_dict = dict()
		for day in weeks_list[week]:
			for team, opponents in self._GetSchedule(date):
				games_dict[team].extend(opponents)


	def _GetNextWeek(self, week, off_ratings, def_ratings, picks):
		# Get Schedule for the week here
		week_expectation = dict()
		for team in nba_site_constants.TEAMS:
			if team in picks:
				continue
			wins, losses, team = _TeamScoreForWeek(nba_site_constants.TEAMS[team], 
											  week, 
											  off_ratings, 
											  def_ratings)
			week_expectation[team] = {'wins': wins,
									  'losses': losses}
		return week_expectation

	def _GetBestPlans(self, off_ratings, def_ratings, week,
					 total_wins, total_losses, picks):
		# Return Top 3 of Next Week
		week_expectation = _GetNextWeek(week, off_ratings, def_ratings, picks)
		total_games = total_wins + total_losses
		#compare = lambda (key, value): (value['wins'] + total_wins) / (total_games + value['wins'] + value['losses'])
		#sorted_week = sorted(week_expectation.iteritems(), key=compare, reverse=True)
		#if week < 24:
		#	return _BestPlan(_GetBestPlans(off_ratings, def_ratings, week + 1, total_wins))
		#else:
		#	return 


	def FindBestPlan(self):
		offensive_ratings = _LoadJSONFile(nba_site_constants.
										OFFENSIVE_TEAM_RATINGS_FILE)
		defensive_ratings = _LoadJSONFile(nba_site_constants.
										DEFENSIVE_TEAM_RATINGS_FILE)

		total_wins, total_losses = _GetCurrentScore()

		plans = _GetBestPlans(offensive_ratings, defensive_ratings, 
						nba_site_constants.WEEKS_PLAYED,
						total_wins, total_losses, nba_site_constants.PICKS.copy())

		return _BestPlan(plans)



	def FormatPlan(self, plan):
		return sorted( ((value, key) for key, value in plan.items()), reverse=True)


def ComputeNextPick():
	rating_loader.LoadRatings()

if __name__ == "__main__":
	plan_finder = PlanFinder()
	plan_finder._GetSchedule(20181028)