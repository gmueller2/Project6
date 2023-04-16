import pickle
import os
import csv
from model.team import Team
from model.team_member import TeamMember


class LeagueDatabase:

    _sole_instance = None

    def __init__(self):
        self._leagues = []
        self._last_oid = 0
        # https://stackoverflow.com/questions/25040834/prevent-other-classes-methods-from-calling-my-constructor

    @property
    def leagues(self):
        return self._leagues

    @classmethod
    def instance(cls):  # this is a typical, if simple, singleton - will have problems with multithreading
        if cls._sole_instance is None:
            cls._sole_instance = LeagueDatabase()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        if os.path.exists(f'{file_name}'):
            f = open(f'{file_name}', mode='rb')
            cls._sole_instance = pickle.load(f)
            f.close()
        else:
            print("File not found, trying to load backup...")
            if os.path.exists(f'{file_name}.backup'):
                f = open(f'{file_name}.backup', mode='rb')
                cls._sole_instance = pickle.load(f)
                f.close()

    def add_league(self, league):
        self._leagues.append(league)

    def remove_league(self, league):
        self._leagues.remove(league)

    def league_named(self, name):
        for league in self._leagues:
            if league.name == name:
                return league
        return None

    def next_oid(self):
        self._last_oid += 1
        return self._last_oid

    def reset_oid(self):
        self._last_oid = 0
        return self._last_oid

    def save(self, file_name):  # if file exists rename to .backup // and THEN save it. use the OS module here.
        if os.path.exists(f'{file_name}'):
            os.rename(f'{file_name}', f'{file_name}.backup')
        f = open(f'{file_name}', mode='wb')
        pickle.dump(self, f)
        f.close()

    def import_league_teams(self, league, file_name):

        if league not in self.leagues:
            print(f'Cannot find league {league}.')
        else:
            with open(f'{file_name}', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # skip header
                for team, name, email in reader:
                    if league.team_named(team) is None:
                        new_team = Team(self.next_oid(), team)
                        league.add_team(new_team)
                    if league.team_named(team).member_named(name) is None:
                        target_team = league.team_named(team)
                        new_member = TeamMember(self.next_oid(), name, email)
                        target_team.add_member(new_member)
        # https://stackoverflow.com/questions/47128105/how-to-get-data-from-csv-into-a-python-object

    def export_league_teams(self, league, file_name):
        if league not in self.leagues:
            print(f'Cannot find league {league}.')
        else:
            if os.path.isfile(f'{file_name}') is False:
                open(f'{file_name}', 'x')
            with open(f'{file_name}', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Team name', 'Member name', 'Member email'])
                for team in league.teams:
                    for member in team.members:
                        target_row = [team.name, member.name, member.email]
                        writer.writerow(target_row)
