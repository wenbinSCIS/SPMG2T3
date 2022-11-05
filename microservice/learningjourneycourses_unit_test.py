import unittest
from learningjourneycourses import learningjourneycourses

class TestLearningJourneyCourses(unittest.TestCase):
 
    def test_to_dict(self):
        c1 = learningjourneycourses(LJCID = 1,LJID=2,CourseID = 3)
        self.assertEqual(c1.to_dict(), {
            'LJCID': 1,
            'LJID':2,
            "CourseID":3}
        )