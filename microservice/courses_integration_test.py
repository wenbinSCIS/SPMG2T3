import unittest
import flask_testing
import json
from freezegun import freeze_time
from courses import app, db, courses

class TestApp(flask_testing.TestCase):
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
    app.config['TESTING'] = True

    def create_app(self):
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TestGetAllCourses(TestApp):
    def test_get_all_courses_singular(self):
        c1 = courses(CourseID = 1,CourseName='Figma',CourseDescription="UI Creation and artistic vision")
        db.session.add(c1)
        db.session.commit()
        
        response = self.client.get("/courses/getAll")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["data"], [{
            'CourseID': c1.CourseID,
            'CourseName': c1.CourseName,
            "CourseDescription": c1.CourseDescription,
        }
        ])
    def test_get_all_courses_multiple(self):
        c2 = courses(CourseID = 2,CourseName='Canva',CourseDescription="UI Creation and artistic vision as well")
        c1 = courses(CourseID = 1,CourseName='Figma',CourseDescription="UI Creation and artistic vision")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        
        response = self.client.get("/courses/getAll")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["data"], [{
            'CourseID': c1.CourseID,
            'CourseName': c1.CourseName,
            "CourseDescription": c1.CourseDescription,
        },{
            'CourseID': c2.CourseID,
            'CourseName': c2.CourseName,
            "CourseDescription": c2.CourseDescription,
        }
        ])
    def test_get_all_no_courses(self):
        response = self.client.get("/courses/getAll")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": "No Courses Found." })

class TestGetCourseByID(TestApp):
    def test_get_course_by_ID(self):
        c1 = courses(CourseID = 1,CourseName='Figma',CourseDescription="UI Creation and artistic vision")
        c2 = courses(CourseID = 2,CourseName='Canva',CourseDescription="UI Creation and artistic vision as well")
        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()
        
        response = self.client.get("/getCoursebyId?cid=1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'CourseID': c1.CourseID,
            'CourseName': c1.CourseName,
            "CourseDescription": c1.CourseDescription,
        }])

    def test_get_course_by_ID_no_courses(self):
        response = self.client.get("/getCoursebyId?cid=3")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "CourseID is not valid." })

    def test_get_course_by_ID_no_ID(self):
        response = self.client.get("/getCoursebyId?cid=")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "No Course ID provided" })

