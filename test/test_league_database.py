import unittest
from model.league import League
from model.team import Team
from model.team_member import TeamMember
from test.test_league import LeagueTests
from model.league_database import LeagueDatabase
import os
from filecmp import cmp


class LeagueDatabaseTests(unittest.TestCase):
    def test_add_remove_league(self):
        league_data = LeagueDatabase.instance()
        new_league = LeagueTests.build_league()
        league_data.add_league(new_league)
        self.assertIn(new_league, league_data.leagues)
        league_data.remove_league(new_league)
        self.assertNotIn(new_league, league_data.leagues)

    def test_league_named(self):
        league_data = LeagueDatabase.instance()
        new_league = LeagueTests.build_league()
        league_data.add_league(new_league)
        league_found = league_data.league_named("Bedrock League")
        self.assertEqual(new_league, league_found)
        league_data.remove_league(new_league)

    def test_next_oid(self):
        league_data = LeagueDatabase.instance()
        league_data.reset_oid()
        first_number = league_data.next_oid()
        self.assertEqual(1, first_number)
        second_number = league_data.next_oid()
        self.assertEqual(2, second_number)

    def test_save_load(self):
        league_data = LeagueDatabase.instance()  # this seems to only point toward one 'instance'
        test_league = LeagueTests.build_league()
        league_data.add_league(test_league)
        league_data.save('my_leagues')
        league_data.save('my_leagues')
        self.assertTrue(os.path.isfile('my_leagues.league'))
        league_data.remove_league(test_league)
        self.assertNotIn(test_league, league_data.leagues)
        # test loading
        LeagueDatabase.load('my_leagues')
        second_db = LeagueDatabase.instance()  # needs to be reloaded
        self.assertIn(test_league, second_db.leagues)
        # test backup
        second_db.remove_league(test_league)
        os.remove('my_leagues.league')
        LeagueDatabase.load('my_leagues')
        third_db = LeagueDatabase.instance()  # final reload
        self.assertIn(test_league, third_db.leagues)
        third_db.remove_league(test_league)

    def test_import_export(self):
        league_data = LeagueDatabase.instance()
        my_league = League(league_data.next_oid(), 'My League')
        league_data.add_league(my_league)
        league_data.import_league_teams(my_league, 'teams')
        my_team = Team(league_data.next_oid(), 'Mueller')
        my_member = TeamMember(league_data.next_oid(), 'Gene', 'gene@gmail.com')
        my_team.add_member(my_member)
        my_league.add_team(my_team)
        league_data.export_league_teams(my_league, 'new_teams')
        test_league = League(league_data.next_oid(), 'Test League')
        league_data.add_league(test_league)
        league_data.import_league_teams(test_league, 'compare_teams')
        self.assertTrue(cmp('compare_teams.csv', 'new_teams.csv'))


if __name__ == '__main__':
    unittest.main()
