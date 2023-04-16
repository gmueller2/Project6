import datetime
import unittest

from model.competition import Competition
from model.team import Team
from test.test_league import LeagueTests
from model.emailer import Emailer
from unittest.mock import patch



class CompetitionTests(unittest.TestCase):
    def test_create(self):
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "There", now)

        self.assertEqual("Here", c1.location)
        self.assertEqual(1, c1.oid)
        self.assertIsNone(c1.date_time)
        self.assertEqual(2, len(c1.teams_competing))
        self.assertIn(t1, c1.teams_competing)
        self.assertIn(t2, c1.teams_competing)
        self.assertNotIn(t3, c1.teams_competing)

        self.assertEqual("There", c2.location)
        self.assertEqual(2, c2.oid)
        self.assertEqual(now, c2.date_time)
        self.assertEqual(2, len(c2.teams_competing))
        self.assertNotIn(t1, c2.teams_competing)
        self.assertIn(t2, c2.teams_competing)
        self.assertIn(t3, c2.teams_competing)

    @patch('builtins.print')
    def test_send_email(self, mock_print):
        league = LeagueTests.build_league()
        c = league.competitions[1]
        c.send_email(Emailer.instance(), "S", "M")
        mock_print.assert_called_with('Email successfully sent!')


    def test_comp_string(self):
        league = LeagueTests.build_league()
        c = league.competitions[0]
        c2 = league.competitions[3]
        self.assertEqual("Competition at t1 vs t2 with 2 teams", str(c))
        self.assertEqual("Competition at t2 vs t3 with 2 teams", str(c2))

