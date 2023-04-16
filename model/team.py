from model.identified_object import IdentifiedObject
from model.exceptions import DuplicateOid
from model.exceptions import DuplicateEmail


class Team (IdentifiedObject):

    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._members = []

    @property
    def members(self):
        return self._members

    def add_member(self, member):
        oid_list = [member.oid for member in self._members]
        email_list = [member.email for member in self._members]
        if member.oid in oid_list:
            raise DuplicateOid(f"Duplicate member in team for object ID: {member.oid}", member.oid)
        elif member.email in email_list:
            raise DuplicateEmail(f"Duplicate email for team member: {member.email}", member.email)
        else:
            self._members.append(member)

    def member_named(self, member_name):
        s = [member for member in self._members if member.name == member_name]
        if bool(s) is True:
            return s[0]
        else:
            return None

    def remove_member(self, member):
        self._members.remove(member)

    def send_email(self, emailer, subject, message):
        # each of the send email methods can only send ONE email, hence the second choice is a little better. We don't
        # want to DDOS our email server with a hundred requests, we want one email with several recipients.
        emails = [member.email for member in self._members if member.email is not None]
        emailer.send_plain_email(emails, subject, message)

    def __str__(self):
        return f"{self.name}: {len(self._members)} members"

