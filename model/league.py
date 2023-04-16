from model.identified_object import IdentifiedObject
from model.exceptions import DuplicateOid


class League (IdentifiedObject):

    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    def add_team(self, team):
        oid_list = [t.oid for t in self._teams]
        if team.oid not in oid_list:
            self.teams.append(team)
        else:
            raise DuplicateOid(f"{team.name} already in {self.name}", team.oid)

    def remove_team(self, team):
        if team in self._teams:
            if len(self.competitions_for_team(team)) == 0:
                self.teams.remove(team)
            else:
                raise ValueError("Team currently active in competitions!")
        else:
            raise ValueError("Team not found!")

    def team_named(self, team_name):
        s = [team for team in self.teams if team.name == team_name]
        if bool(s) is True:
            return s[0]
        else:
            return None

    # working is more important than clean, which is more important than efficient.
    def add_competition(self, competition):
        oid_list = [c.oid for c in self._competitions]
        if competition.oid in oid_list:
            raise DuplicateOid(f"Competition:{competition.oid} already exists", competition.oid)
        not_in_league = [t for t in competition.teams_competing if t not in self._teams]
        if len(not_in_league) > 0:
            raise ValueError("Team in competition is not part of the league")
        else:
            self._competitions.append(competition)

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def teams_for_member(self, member):

        member_teams = []
        for t in self._teams:
            members = t.members
            for m in members:
                if m == member:
                    member_teams.append(t)

        return member_teams

    def competitions_for_team(self, team):

        team_competitions = []
        for c in self._competitions:
            teams = c.teams_competing
            for t in teams:
                if t == team:
                    team_competitions.append(c)

        return team_competitions

    def competitions_for_member(self, member):

        member_competitions = []
        for c in self._competitions:
            teams = c.teams_competing
            for t in teams:
                members = t.members
                for m in members:
                    if m == member:
                        member_competitions.append(c)

        return member_competitions

    def __str__(self):
        return f"{self.name}: {len(self._teams)} teams, {len(self._competitions)} competitions"

