import unittest
from freezegun import freeze_time
from skills import skills

class Testskills(unittest.TestCase):
    @freeze_time("2022-10-05 09:19:17")
    def test_to_dict(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        self.assertEqual(sk1.to_dict(), {
            'SkillsID': sk1.SkillsID,
            "Skillname":sk1.Skillname
        }
        )