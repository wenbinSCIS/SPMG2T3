import unittest
from skills_required_by_role import SRBR

class TestRole(unittest.TestCase):
    def test_to_dict(self):
        r1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        self.assertEqual(r1.to_dict(), {
            "SRBR":1,
            "RoleID":1,
            "SkillsID":1}
        )
