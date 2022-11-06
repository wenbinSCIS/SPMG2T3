import unittest
import flask_testing
import json
from skills_acquired_by_course import app, db, SABC

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

class TestGetAllBySkillId(TestApp):
    def test_get_all_by_skillid(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=2,SkillsID=1)
        sabc3 = SABC(SABC=3,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.add(sabc3)
        db.session.commit()
        
        response = self.client.get("/getSABCbySkillID?sid="+str(sabc1.SkillsID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'SABC': sabc1.SABC,
            'CourseID': sabc1.CourseID,
            'SkillsID': sabc1.SkillsID},
            {'SABC': sabc2.SABC,
            'CourseID': sabc2.CourseID,
            'SkillsID': sabc2.SkillsID}])

    def test_get_all_by_skillid_invalid_skill_id(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=2,SkillsID=1)
        sabc3 = SABC(SABC=3,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.add(sabc3)
        db.session.commit()
        
        response = self.client.get("/getSABCbySkillID?sid=99")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": "There are no SABC." })

    def test_get_all_by_skillid_no_skill_id(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=2,SkillsID=1)
        sabc3 = SABC(SABC=3,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.add(sabc3)
        db.session.commit()
        
        response = self.client.get("/getSABCbySkillID?sid=")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

class TestGetAllByCourseId(TestApp):
    def test_get_all_by_courseid(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=2,SkillsID=1)
        sabc3 = SABC(SABC=3,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.add(sabc3)
        db.session.commit()
        
        response = self.client.get("/getSABCbyCourseID?CourseID="+str(sabc1.CourseID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'SABC': sabc1.SABC,
            'CourseID': sabc1.CourseID,
            'SkillsID': sabc1.SkillsID},
            {'SABC': sabc3.SABC,
            'CourseID': sabc3.CourseID,
            'SkillsID': sabc3.SkillsID}])

    def test_get_all_by_courseid_invalid_course_id(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=2,SkillsID=1)
        sabc3 = SABC(SABC=3,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.add(sabc3)
        db.session.commit()
        
        response = self.client.get("/getSABCbyCourseID?CourseID=99")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": "There are no SABC." })

    def test_get_all_by_courseid_no_course_id(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=2,SkillsID=1)
        sabc3 = SABC(SABC=3,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.add(sabc3)
        db.session.commit()
        
        response = self.client.get("/getSABCbyCourseID?CourseID=")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

class TestAddSkillCourse(TestApp):
    def test_add_skill_course(self):
        request_body = {
            'CourseID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":1},{"SkillName":"HTML","SkillsID":2}]
        }
        
        response = self.client.post("/addskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["course data"],
            {'SABC': 2,
            'CourseID': 1,
            'SkillsID': 2})

    def test_add_skill_course_no_course_id(self):
        request_body = {
            "Skills":[{"SkillName":"Python","SkillsID":1},{"SkillName":"HTML","SkillsID":2}]
        }
        
        response = self.client.post("/addskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })

    def test_add_skill_course_no_skill(self):
        request_body = {
            "CourseID":1
        }
        
        response = self.client.post("/addskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })

    def test_add_skill_course_already_added_skill(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        db.session.add(sabc1)
        db.session.commit()

        request_body = {
            'CourseID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":1}]
        }
        
        response = self.client.post("/addskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Error Occured. Skill already tied to Course." })

    def test_add_skill_course_no_skill_in_list(self):
        request_body = {
            'CourseID': 1,
            "Skills":[]
        }
        
        response = self.client.post("/addskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "CourseID": 1,
                                        "message":"No Skills to add to course.", 
                                        "code": 500 })

class TestDeleteSkillCourse(TestApp):
    def test_delete_skill_course(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.commit()

        request_body = {
            'CourseID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":1}]
        }
        
        response = self.client.post("/deletebyskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{ "CourseID": 1,"Success":True, "code": 201 })

    def test_delete_skill_course_no_skill_in_list(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.commit()

        request_body = {
            'CourseID': 1,
            "Skills":[]
        }
        
        response = self.client.post("/deletebyskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        { "CourseID": 1,"message":"No Skills to add to role.", "code": 500 })

    def test_delete_skill_course_invalid_course_id(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.commit()

        request_body = {
            'CourseID': 99,
            "Skills":[{"SkillName":"Python","SkillsID":1}]
        }
        
        response = self.client.post("/deletebyskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        {'message': 'Course did not exist or Course does not has skill with id 1'})

    def test_delete_skill_course_invalid_skill_id(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.commit()

        request_body = {
            'CourseID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":3}]
        }
        
        response = self.client.post("/deletebyskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        {'message': 'Course did not exist or Course does not has skill with id 3'})

    def test_delete_skill_course_no_course_id(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.commit()

        request_body = {
            "Skills":[{"SkillName":"Python","SkillsID":3}]
        }
        
        response = self.client.post("/deletebyskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        { "message": "Incorrect JSON object provided." })

    def test_delete_skill_course_no_skill_list(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.commit()

        request_body = {
            "CourseID":1
        }
        
        response = self.client.post("/deletebyskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        { "message": "Incorrect JSON object provided." })

    def test_delete_skill_course_one_invalid_skill(self):
        sabc1 = SABC(SABC=1,CourseID=1,SkillsID=1)
        sabc2 = SABC(SABC=2,CourseID=1,SkillsID=2)
        db.session.add(sabc1)
        db.session.add(sabc2)
        db.session.commit()

        request_body = {
            "CourseID":1,
            "Skills":[{"SkillName":"Python","SkillsID":1},{"SkillName":"HTML","SkillsID":99}]
        }
        
        response = self.client.post("/deletebyskillcourse",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        {'message': 'Course did not exist or Course does not has skill with id 99. The rest of the skills are deleted'})