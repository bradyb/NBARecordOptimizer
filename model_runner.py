import csv
import itertools
import json
import pprint as pp
import requests

import nba_site_constants
import rating_loader

_DAYS_IN_WEEK = 7
_MAX_WEEKS = 24
_SEASON = '2019'
_BRANCH_SIZE = 3
_CARMELO_PROB1 = 20
_CARMELO_PROB2 = 21

class PlanFinder:

	def __init__(self):
		with open('dates-dash.txt', 'r') as dates_file:
			day_list = dates_file.read().splitlines()
		self.week_list = list()
		for day in range(0, len(day_list), _DAYS_IN_WEEK):
			self.week_list.append(day_list[day:day + _DAYS_IN_WEEK])

		# Unused since win percentages are being pulled from 538
		self.offensive_ratings = self._LoadJSONFile(nba_site_constants.
										OFFENSIVE_TEAM_RATINGS_FILE)
		self.defensive_ratings = self._LoadJSONFile(nba_site_constants.
										DEFENSIVE_TEAM_RATINGS_FILE)
		# The number of wins and losses accrued through WEEKS_PLAYED
		self.total_wins, self.total_losses = self._GetCurrentScore()
		# Only needed for interacting with stats.nba.com
		self.team_to_id = nba_site_constants.TEAM_TO_ID_MAP
		self.id_to_team = nba_site_constants.ID_TO_TEAM_MAP
		# This is only needed when using _TeamScoreForWeek
		# TODO(bradyb): Create base class with children implementing
		# the scoring function.
		self.week_schedules = dict()
		# Memoizing a team's expected score for a particular week.
		self.team_week_score = dict()
		# Used for memoizing branches we've aleady traversed.
		self.set_to_best = dict()
		# Map of dates to list of game objects from 538. 
		self.date_to_elo = dict()
		self._Load538EloScores()
		pp.pprint(self.date_to_elo)

	def _FormScheduleUrl(self, date):
		return nba_site_constants.PROD_URL + date.replace('-', '') + '/scoreboard.json'

	def _Load538EloScores(self):
		"""Fills self.date_to_elo"""
		matched_row = None
		with open("538_stats/nba_elo.csv", "r") as elo_csv:
			reader = csv.reader(elo_csv, delimiter=',')
			for row in reader:
				if row[1] == _SEASON:
					if row[0] in self.date_to_elo:
						self.date_to_elo[row[0]].append(row)
					else:
						self.date_to_elo[row[0]] = [row]

	def _UpdateOpponents(self, teams_opponents, hteam_id, vteam_id):
		"""For a game, updates each team's opponent lists for that week."""
		if hteam_id in teams_opponents:
			teams_opponents[hteam_id].append(vteam_id)
		else:
			teams_opponents[hteam_id] = [vteam_id]
		if vteam_id in teams_opponents:
			teams_opponents[vteam_id].append(hteam_id)
		else:
			teams_opponents[vteam_id] = [hteam_id]		

	def _GetSchedule(self, date):
		"""Returns a dict from team ids to lists of opponents."""
		url = self._FormScheduleUrl(date)
		response = requests.get(url)
		response.raise_for_status()
		teams_opponents = dict()
		for game in response.json()['games']:
			self._UpdateOpponents(teams_opponents, game['hTeam']['teamId'], game['vTeam']['teamId'])
		return teams_opponents

	def _ProbAWinsVsB(self, team, opponent):
		a_ortg = self.offensive_ratings[team]
		a_drtg = self.defensive_ratings[team]
		b_ortg = self.offensive_ratings[opponent]
		b_drtg = self.defensive_ratings[opponent]

		a_win_pct = a_ortg**16.5/(a_ortg**16.5 + a_drtg**16.5)
		b_win_pct = b_ortg**16.5/(b_ortg**16.5 + b_drtg**16.5)
		return a_win_pct * (1 - b_win_pct)/(a_win_pct * (1 - b_win_pct) + b_win_pct * (1 - a_win_pct))

	def _GetCurrentScore(self):
		total_wins = 0
		total_losses = 0
		for pick_info in nba_site_constants.PICKS.values():
			total_wins += pick_info['wins']
			total_losses += pick_info['losses']
		return total_wins, total_losses

	def _LoadJSONFile(self, file_name):
		with open(file_name) as file:
			data = json.load(file)
		return data

	def _TeamScoreForWeek(self, team_name, week, opponents):
		"""Computes the expected number of wins for a team in a given week
		using _ProbAWinsVsB to compute the probability of Team A beating
		Team B.
		"""
		init_team = True
		if team_name in self.team_week_score:
			if week in self.team_week_score[team_name]:
				return self.team_week_score[team_name][week]
			init_team = False

		if init_team:
			self.team_week_score[team_name] = dict()
		expected_wins = 0
		for opponent in opponents:
			opponent_name = self.id_to_team[opponent]
			expected_wins = expected_wins + self._ProbAWinsVsB(team_name, opponent_name)
		self.team_week_score[team_name][week] = expected_wins
		return expected_wins

	def _TeamEloScoreForWeek(self, week, team_name):
		"""Computes the expected number of wins for a team in a given week
		using CARMELO win probability pulled from 
		https://data.fivethirtyeight.com/. The data is stored locally in 
		date_to_elo.
		"""
		team_abbrv = nba_site_constants.NAME_TO_ABBRV_MAP[team_name]
		total_wins = 0.0
		total_losses = 0.0
		for day in self.week_list[week - 1]:
			if day not in self.date_to_elo:
				continue
			day_games = self.date_to_elo[day]
			for game in day_games:
				# If team_name is home or away.
				if game[4] == team_abbrv:
					total_wins += float(game[_CARMELO_PROB1])
					total_losses += float(game[_CARMELO_PROB2])
				elif game[5] == team_abbrv:
					total_wins += float(game[_CARMELO_PROB2])
					total_losses += float(game[_CARMELO_PROB1])
		return total_wins, total_losses

	def _GetWeekSchedule(self, week):
		"""IP may have been throttled.
		TODO(bradyb): test this.
		"""
		if week in self.week_schedules:
			return self.week_schedules[week]

		games_dict = dict()
		for day in self.week_list[week - 1]:
			for team, opponents in self._GetSchedule(day).items():
				if team in games_dict:
					games_dict[team].extend(opponents)
				else:
					games_dict[team] = opponents
		self.week_schedules[week] = games_dict
		return games_dict


	def _GetNextWeek(self, week, picks):
		week_expectation = dict()
		# Don't need if we're going to use 538 data
		# schedule = self._GetWeekSchedule(week)
		for team in nba_site_constants.TEAMS:
			if team in picks:
				continue
			# same reason as above
			wins, losses = self._TeamEloScoreForWeek(week, team)
			week_expectation[team] = {'wins': wins,
									  'losses': losses}
		return week_expectation

	def _GetBestPlans(self, week, picks):
		remaining_teams_set = frozenset(self._GetRemainingTeams(picks))
		if remaining_teams_set in self.set_to_best:
			return self.set_to_best[remaining_teams_set]

		week_expectation = self._GetNextWeek(week, picks)
		total_games = self.total_wins + self.total_losses

		value_dict = dict() 
		for team, scores in week_expectation.items():
			week_value = (scores['wins'] + self.total_wins) / (total_games + scores['wins'] + scores['losses'])
			value_dict[team] = week_value

		sorted_week = sorted(value_dict.items(), key=lambda kv: kv[1], reverse=True)
		if week < 24:
			top_plans = list()
			for next_week in range(min(_BRANCH_SIZE, 24 - week)):
				updated_picks = picks.copy()
				next_team = sorted_week[next_week][0]
				updated_picks[next_team] = {'week': week, 
											'wins': week_expectation[next_team]['wins'],
											'losses': week_expectation[next_team]['losses']}
				top_plans.append(self._GetBestPlans(week + 1, updated_picks))
			best_plan = self._BestPlan(top_plans)
			self.set_to_best[remaining_teams_set] = best_plan
			return best_plan
		else:
			updated_picks = picks.copy()
			next_team = sorted_week[0][0]
			updated_picks[next_team] = {'week': week, 
										'wins': week_expectation[next_team]['wins'],
										'losses': week_expectation[next_team]['losses']}
			return updated_picks

	def _BestPlan(self, picks_list):
		best_score = 0
		best_plan = None
		for picks in picks_list:
			score = self._ComputePlanScore(picks)

			if score > best_score:
				best_score = score
				best_plan = picks.copy()

		return best_plan

	def _ComputePlanScore(self, plan):
		total_wins = 0
		total_games = 0
		for scores in plan.values():
			total_wins += scores['wins']
			total_games += scores['wins'] + scores['losses']

		return (total_wins / total_games)

	def _GetRemainingTeams(self, picks):
		return [team for team in nba_site_constants.TEAMS if team not in picks]

	def FindBestPlan(self):
		plans = self._GetBestPlans(nba_site_constants.WEEKS_PLAYED + 1, 
								   nba_site_constants.PICKS.copy())

		return plans



	def FormatPlan(self, plan):
		return sorted( ((value, key) for key, value in plan.items()), reverse=True)

if __name__ == "__main__":
	plan_finder = PlanFinder()
	best_plan = plan_finder.FindBestPlan() 
	pp.pprint(best_plan)
	print("Plan score: ", plan_finder._ComputePlanScore(best_plan))
	pp.pprint([team for team in nba_site_constants.TEAMS if team not in best_plan])
