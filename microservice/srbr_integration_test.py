import unittest
import flask_testing
import json
from skills_required_by_role import app, db, SRBR

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

class TestGetAllByRoleId(TestApp):
    def test_get_all_by_roleid(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getSRBRbyRoleID?RoleID="+str(srbr1.SRBR))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'SRBR': srbr1.SRBR,
            'RoleID': srbr1.RoleID,
            'SkillsID': srbr1.SkillsID},
            {'SRBR': srbr3.SRBR,
            'RoleID': srbr3.RoleID,
            'SkillsID': srbr3.SkillsID}])

    def test_get_all_by_roleid_invalid_role_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getSRBRbyRoleID?RoleID=99")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": "There are no SRBR." })

    def test_get_all_by_roleid_no_role_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getSRBRbyRoleID")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

class TestGetRoleIdSkillId(TestApp):
    def test_get_byRIDSID(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getByRIDSID?roleid="+str(srbr1.RoleID)+"&sid="+str(srbr1.SkillsID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{ "code": 201,"message": "Required." })

    def test_get_byRIDSID_invalid_role_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getByRIDSID?roleid="+str(99)+"&sid="+str(srbr1.SkillsID))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,{ "code": 404,"message": "Not required." })

    def test_get_byRIDSID_invalid_skill_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getByRIDSID?roleid="+str(srbr1.RoleID)+"&sid="+str(99))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json,{ "code": 404,"message": "Not required." })

    def test_get_byRIDSID_no_role_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getByRIDSID?sid="+str(srbr1.SkillsID))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })

    def test_get_byRIDSID_no_skill_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=2,SkillsID=1)
        srbr3 = SRBR(SRBR=3,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.add(srbr3)
        db.session.commit()
        
        response = self.client.get("/getByRIDSID?roleid="+str(srbr1.RoleID))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })

class TestAddSkillRole(TestApp):
    def test_add_skill_role(self):
        request_body = {
            'RoleID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":1},{"SkillName":"HTML","SkillsID":2}]
        }
        
        response = self.client.post("/addskillrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["role data"],
            {'SRBR': 2,
            'RoleID': 1,
            'SkillsID': 2})

    def test_add_skill_role_no_role_id(self):
        request_body = {
            "Skills":[{"SkillName":"Python","SkillsID":1},{"SkillName":"HTML","SkillsID":2}]
        }
        
        response = self.client.post("/addskillrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })

    def test_add_skill_role_no_skill(self):
        request_body = {
            "RoleID":1
        }
        
        response = self.client.post("/addskillrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })

    def test_add_skill_role_already_added_skill(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        db.session.add(srbr1)
        db.session.commit()

        request_body = {
            'RoleID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":1}]
        }
        
        response = self.client.post("/addskillrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Error Occured. Skill already tied to Role." })

    def test_add_skill_role_no_skill_in_list(self):
        request_body = {
            'RoleID': 1,
            "Skills":[]
        }
        
        response = self.client.post("/addskillrole",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "RoleID": 1,
                                        "message":"No Skills to add to role.", 
                                        "code": 500 })

class TestDeleteSkillRole(TestApp):
    def test_delete_skill_role(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.commit()

        request_body = {
            'RoleID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":1}]
        }
        
        response = self.client.post("/deletebyskillrole/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{ "RoleID": 1,"Success":True, "code": 201 })

    def test_delete_skill_role_no_skill_in_list(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.commit()

        request_body = {
            'RoleID': 1,
            "Skills":[]
        }
        
        response = self.client.post("/deletebyskillrole/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        {"RoleID": 1,
                        "message":"No Skills to add to role.", 
                        "code": 500 })

    def test_delete_skill_role_invalid_role_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.commit()

        request_body = {
            'RoleID': 2,
            "Skills":[{"SkillName":"Python","SkillsID":1}]
        }
        
        response = self.client.post("/deletebyskillrole/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        { "message": "SRBR is not valid." })

    def test_delete_skill_role_invalid_skill_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.commit()

        request_body = {
            'RoleID': 1,
            "Skills":[{"SkillName":"Python","SkillsID":3}]
        }
        
        response = self.client.post("/deletebyskillrole/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,
                        { "message": "SRBR is not valid." })

    def test_delete_skill_role_no_role_id(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.commit()

        request_body = {
            "Skills":[{"SkillName":"Python","SkillsID":1}]
        }
        
        response = self.client.post("/deletebyskillrole/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })

    def test_delete_skill_role_no_skill_list(self):
        srbr1 = SRBR(SRBR=1,RoleID=1,SkillsID=1)
        srbr2 = SRBR(SRBR=2,RoleID=1,SkillsID=2)
        db.session.add(srbr1)
        db.session.add(srbr2)
        db.session.commit()

        request_body = {
            "CourseID":1
        }
        
        response = self.client.post("/deletebyskillrole/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json,{ "message": "Incorrect JSON object provided." })