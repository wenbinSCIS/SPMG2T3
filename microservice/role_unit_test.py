import unittest
from freezegun import freeze_time
from roles import Roles

class TestRole(unittest.TestCase):
    @freeze_time("2022-10-05 09:19:17")
    def test_to_dict(self):
        r1 = Roles(RoleName='Programmer', CreatedBy='Ryan Tan', Fulfilled="",
                    Description="To programme the newest project",
                    TimeAdded="2022-10-05 09:19:17")
        self.assertEqual(r1.to_dict(), {
            'RoleID': None,
            'RoleName': 'Programmer',
            'CreatedBy': 'Ryan Tan',
            "Fulfilled":"",
            "Description":"To programme the newest project",
            "TimeAdded":"2022-10-05 09:19:17"}
        )