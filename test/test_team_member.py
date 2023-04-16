import unittest
from unittest.mock import patch
from model.team_member import TeamMember
from model.emailer import Emailer


class TeamMemberTests(unittest.TestCase):
    def test_create(self):
        oid = 1
        name = "Fred"
        email = "fred.flintstone@gmail.com"
        tm = TeamMember(oid, name, email)
        self.assertEqual(oid, tm.oid)
        self.assertEqual(name, tm.name)
        self.assertEqual(email, tm.email)

    def test_equality_based_on_id(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        tm_3 = TeamMember(2, "name", "email")

        # team members must be equal to themselves
        self.assertTrue(tm_1 == tm_1)
        self.assertTrue(tm_2 == tm_2)
        self.assertTrue(tm_3 == tm_3)

        # same id are equal, even if other fields different
        self.assertTrue(tm_1 == tm_2)

        # different ids are not equal, even if other fields the same
        self.assertTrue(tm_1 != tm_3)

    def test_hash_based_on_id(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        tm_3 = TeamMember(2, "name", "email")

        # hash depends only on id
        self.assertTrue(hash(tm_1) == hash(tm_2))

        # objects with different id's may have different hash codes
        # note: this is not a requirement of the hash function but
        # for the case of id == 1 and id == 2 we can verify that their
        # hash codes are different in a REPL (just print(hash(1)) etc).
        self.assertTrue(hash(tm_1) != hash(tm_3))

    def test_str(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        self.assertEqual("name<email>", str(tm_1))
        self.assertEqual("other name<other email>", str(tm_2))

    @patch('builtins.print')
    def test_sends_email(self, mock_print):
        tm_1 = TeamMember(1, "name", "email@email.com")
        tm_1.send_email(Emailer.instance(), "Foo", "Bar")
        mock_print.assert_called_with('Email successfully sent!')


if __name__ == '__main__':
    unittest.main()
