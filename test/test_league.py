import unittest

from model.competition import Competition
from model.league import League
from model.team import Team
from model.team_member import TeamMember
from model.exceptions import DuplicateOid


class LeagueTests(unittest.TestCase):
    def test_create(self):
        league = League(1, "AL State Curling League")
        self.assertEqual(1, league.oid)
        self.assertEqual("AL State Curling League", league.name)
        self.assertEqual([], league.teams)
        self.assertEqual([], league.competitions)

    def test_adding_team_adds_to_teams(self):
        t = Team(1, "Ice Maniacs")
        league = League(1, "AL State Curling League")
        self.assertNotIn(t, league.teams)
        league.add_team(t)
        self.assertIn(t, league.teams)

    def test_adding_competition_adds_to_competitions(self):
        c = Competition(1, [], "Local tourney", None)
        league = League(13, "AL State Curling League")
        self.assertNotIn(c, league.competitions)
        league.add_competition(c)
        self.assertIn(c, league.competitions)

    @staticmethod
    def build_league():
        league = League(1, "Bedrock League")
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        t3 = Team(3, "t3")
        all_teams = [t1, t2, t3]
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        tm1 = TeamMember(1, "Fred", "fred@bedrock.com")
        tm2 = TeamMember(2, "Barney", "barney@bedrock.com")
        tm3 = TeamMember(3, "Wilma", "wilma@bedrock.com")
        tm4 = TeamMember(4, "Betty", "betty@bedrock.com")
        tm5 = TeamMember(5, "Pebbles", "pebbles@bedrock.com")
        tm6 = TeamMember(6, "Bamm-Bamm", "bam-bam@bedrock.com")
        tm7 = TeamMember(7, "Dino", "dino@bedrock.com")
        tm8 = TeamMember(8, "Mr. Slate", "mrslate@bedrock.com")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t2.add_member(tm3)
        t2.add_member(tm4)
        t2.add_member(tm5)
        t3.add_member(tm6)
        t3.add_member(tm7)
        t3.add_member(tm8)
        # every team plays every other team twice
        oid = 1
        for c in [Competition(oid := oid + 1, [team1, team2], team1.name + " vs " + team2.name, None)
                  for team1 in all_teams
                  for team2 in all_teams
                  if team1 != team2]:
            league.add_competition(c)
        return league

    def test_team_named(self):
        league = self.build_league()
        t = league.team_named("t1")
        self.assertEqual(league.teams[0], t)
        t = league.team_named("t3")
        self.assertEqual(league.teams[2], t)
        t = league.team_named("bogus")
        self.assertIsNone(t)

    def test_big_league(self):  # this is something we'll need to talk to Dr. Shaffer about.
        league = self.build_league()
        t = league.teams[0]
        cs = league.competitions_for_team(t)
        # matchups are (t1, t2), (t1, t3), (t2, t1), (t3, t1) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehension
        self.assertEqual({"t1 vs t2", "t1 vs t3", "t2 vs t1", "t3 vs t1"}, cs_names)

        self.assertEqual([league.teams[2]], league.teams_for_member(league.teams[2].members[0]))

        # Grab a player from the third team
        cs = league.competitions_for_member(league.teams[2].members[0])
        # matchups are (t3, t1), (t3, t2), (t2, t3), (t1, t3) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehension
        self.assertEqual({"t3 vs t1", "t3 vs t2", "t2 vs t3", "t1 vs t3"}, cs_names)

    def test_remove_something(self):
        t = Team(1, "Ice Maniacs")
        league = League(1, "AL State Curling League")
        league.add_team(t)
        self.assertIn(t, league.teams)
        league.remove_team(t)
        self.assertNotIn(t, league.teams)

    def test_teams_for_member(self):
        league = LeagueTests.build_league()
        t = league.teams[0]
        m = t.member_named("Fred")
        self.assertEqual([t], league.teams_for_member(m))
        t2 = league.teams[1]
        m2 = t2.member_named("Betty")
        self.assertEqual([t2], league.teams_for_member(m2))

    def test_league_str(self):
        league = LeagueTests.build_league()
        self.assertEqual("Bedrock League: 3 teams, 6 competitions", str(league))

    def test_league_comp_team_not_in_league(self):
        league = LeagueTests.build_league()
        expected = [c for c in league.competitions]  # we add the 'new' comp later in the test
        t42 = Team(42, "t42")
        t17 = Team(17, "t17")
        league.add_team(t17)
        comp = Competition(42, [t42, t17], "Fake Game", None)
        expected.append(comp)
        with self.assertRaises(ValueError):
            league.add_competition(comp)
        self.assertNotEqual(expected, league.competitions) # make sure the comp isn't added by accident
        league.add_team(t42)  # now check if we can add it if we add the team to the league
        league.add_competition(comp)
        self.assertEqual(expected, league.competitions)

    def test_league_add_team_dup_oid(self):
        league = LeagueTests.build_league()
        tm1 = Team(1, "Bad Team")
        with self.assertRaises(DuplicateOid):
            league.add_team(tm1)

    def test_league_add_comp_dup_oid(self):
        league = LeagueTests.build_league()
        c1 = Competition(42, [], "Fake Game", None)
        c2 = Competition(42, [], "False Game", None)
        league.add_competition(c1)
        self.assertIn(c1, league.competitions)
        with self.assertRaises(DuplicateOid):
            league.add_competition(c2)

    def test_remove_team_in_comp(self):
        league = LeagueTests.build_league()
        t33 = Team(33, "Hello")
        t34 = Team(34, "There")
        t35 = Team(35, "World")
        league.add_team(t33)
        league.add_team(t34)
        league.add_team(t35)
        self.assertIn(t33, league.teams)
        self.assertIn(t34, league.teams)
        self.assertIn(t35, league.teams)
        c1 = Competition(89, [t33, t34], "Crash Game", None)
        league.add_competition(c1)
        self.assertIn(c1, league.competitions)
        with self.assertRaises(ValueError):
            league.remove_team(t34)
        league.remove_team(t35)
        self.assertIn(t34, league.teams)
        self.assertNotIn(t35, league.teams)
