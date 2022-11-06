import unittest
from skills_acquired_by_course import SABC

class TestRole(unittest.TestCase):
    def test_to_dict(self):
        r1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        self.assertEqual(r1.to_dict(), {
            "SABC":1,
            "CourseID":1,
            "SkillsID":1}
        )
