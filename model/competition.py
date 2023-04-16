from model.identified_object import IdentifiedObject


class Competition (IdentifiedObject):

    def __init__(self, oid, teams, location, datetime):
        super().__init__(oid)
        self._teams_competing = teams
        self.date_time = datetime
        self.location = location

    @property   # means people don't have to put parentheses - you CAN access it directly as if it were a variable
    def teams_competing(self):
        return self._teams_competing

    def send_email(self, emailer, subject, message):
        emails = []
        for team in self._teams_competing:
            for member in team.members:
                emails.append(member.email)
        emailer.send_plain_email(emails, subject, message)

    def __str__(self):
        if self.date_time is None:
            return f"Competition at {self.location} with {len(self.teams_competing)} teams"
        else:
            return f"Competition at {self.location} on {self.date_time} with {len(self.teams_competing)} teams"

