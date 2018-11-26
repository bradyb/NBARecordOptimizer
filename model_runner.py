import csv
import itertools
import pprint as pp
import requests

import fivethirtyeight_reader as reader
import nba_site_constants

_DAYS_IN_WEEK = 7
_MAX_WEEKS = 24
_BRANCH_SIZE = 4
_CARMELO_PROB1 = 20
_CARMELO_PROB2 = 21

class PlanFinder:

	def __init__(self):
		with open('dates-dash.txt', 'r') as dates_file:
			day_list = dates_file.read().splitlines()
		self.week_list = list()
		for day in range(0, len(day_list), _DAYS_IN_WEEK):
			self.week_list.append(day_list[day:day + _DAYS_IN_WEEK])

		# The number of wins and losses accrued through WEEKS_PLAYED
		self.total_wins, self.total_losses = self._GetCurrentScore()
		# Memoizing a team's expected score for a particular week.
		self.team_week_score = dict()
		# Used for memoizing branches we've aleady traversed.
		self.set_to_best = dict()
		# Map of dates to list of game objects from 538.
		self.date_to_elo = reader.FiveThirtyEightReader().GetMap()

	def _GetCurrentScore(self):
		total_wins = 0
		total_losses = 0
		for pick_info in nba_site_constants.PICKS.values():
			total_wins += pick_info['wins']
			total_losses += pick_info['losses']
		return total_wins, total_losses

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

if __name__ == "__main__":
	plan_finder = PlanFinder()
	best_plan = plan_finder.FindBestPlan()
	pp.pprint(best_plan)
	print("Plan score: ", plan_finder._ComputePlanScore(best_plan))
	pp.pprint([team for team in nba_site_constants.TEAMS if team not in best_plan])
