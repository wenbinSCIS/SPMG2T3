import unittest
from learningjourney import learningjourney

class TestLearningJourney(unittest.TestCase):
 
    def test_to_dict(self):
        c1 = learningjourney(LJID = 1,UserID = 2,LJName = "Not Important", RoleID=3)
        self.assertEqual(c1.to_dict(), {
            'LJID': 1,
            'UserID':2,
            'LJName': "Not Important",
            "RoleID":3}
        )