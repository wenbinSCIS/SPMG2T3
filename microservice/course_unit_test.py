import unittest
from freezegun import freeze_time
from courses import courses

class TestCourses(unittest.TestCase):
    @freeze_time("2022-10-05 09:19:17")
    def test_to_dict(self):
        c1 = courses(CourseID = 1,CourseName='Figma',CourseDescription="UI Creation and artistic vision")
        self.assertEqual(c1.to_dict(), {
            'CourseID': 1,
            'CourseName':'Figma',
            "CourseDescription":"UI Creation and artistic vision"}
        )