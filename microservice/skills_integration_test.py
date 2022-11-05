import unittest
import flask_testing
import json
from freezegun import freeze_time
from skills import app, db, skills

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

class TestGetAll(TestApp):
    def test_get_all_skills(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        response = self.client.get("/getAllSkill")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'SkillsID': sk1.SkillsID,
            "Skillname":sk1.Skillname
        },{
            'SkillsID': sk2.SkillsID,
            "Skillname":sk2.Skillname
        }])

    def test_get_all_skills_no_skills(self):
        response = self.client.get("/getAllSkill")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": "There are no skills created." })


@freeze_time("2022-10-05 09:19:17")
class TestAddSkill(TestApp):
    def test_add_skill(self):
        request_body = {
        "Skillname":"javascript",
    }

        response = self.client.post("/addSkill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], {
        "Skillname":"javascript",
        "SkillsID" : 1
    })

    def test_add_skill_no_skillname(self):
        request_body = {
            
        }

        response = self.client.post("/addSkill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

    def test_add_skill_blankskillname(self):
        request_body = {
            "Skillname":" ",
        }

        response = self.client.post("/addSkill",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Skillname should not be blank" })

    

class TestDeleteSkillById(TestApp):
    def test_delete_skill_by_id_singular(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        request_body ={
            "Skill IDs":[1]
        }

        response = self.client.post("/deleteskillsbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "Skill IDs": [1],"Success":True, "code": 201 })

    def test_delete_skill_by_id_singular(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        request_body ={
            "Skill IDs":[1,2]
        }

        response = self.client.post("/deleteskillsbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "Skill IDs": [1,2],"Success":True, "code": 201 })


    def test_delete_role_by_id_invalid_skill_id(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        request_body = {
            "Skill IDs":[1,3]
        }

        response = self.client.post("/deleteskillsbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Skill ID is not valid." })
    def test_delete_role_by_id_emptyskillIDlist(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        request_body = {
            "Skill IDs":[]
        }

        response = self.client.post("/deleteskillsbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Skill ID list is empty"})

    def test_delete_role_by_id_nolistprovided(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        request_body = {
        }

        response = self.client.post("/deleteskillsbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided." })

class TestUpdateSkillname(TestApp):
    def test_update_skillname(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        db.session.add(sk1)
        db.session.commit()
        
        request_body ={
            "Skill ID":1,
            "Skillname": "newskillnamehere"
        }

        response = self.client.post("/updateskillnamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "Skill ID": sk1.SkillsID,"Success":True, "code": 201 })

    def test_update_skillname_invalid_id(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        db.session.add(sk1)
        db.session.commit()
        
        request_body ={
            "Skill ID":10,
            "Skillname": "newskillnamehere"
        }

        response = self.client.post("/updateskillnamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Skill ID is not valid." })

    def test_update_skillname_no_id(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        db.session.add(sk1)
        db.session.commit()
        
        request_body ={
            "Skillname": "newskillnamehere"
        }

        response = self.client.post("/updateskillnamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided." })

    def test_update_skillname_no_skillname(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        db.session.add(sk1)
        db.session.commit()
        
        request_body ={
            "Skill ID":10,
        }

        response = self.client.post("/updateskillnamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided." })

    def test_update_skillname_blankskillname(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        db.session.add(sk1)
        db.session.commit()
        
        request_body ={
            "Skill ID":10,
            "Skillname": ""
        }
        response = self.client.post("/updateskillnamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Skill name cannot be empty." })

class TestGetSkillById(TestApp):
    def test_get_skill_by_id(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        response = self.client.get("/getSkillbyId?skillid="+str(sk1.SkillsID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'SkillsID': sk1.SkillsID,
            "Skillname":sk1.Skillname
        }])


    def test_get_role_by_id_invalid_id(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        
        response = self.client.get("/getSkillbyId?skillid="+str(3))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 
                    {"code": 404, "message": "No skill with this skill ID present in DB."})

    def test_get_role_by_id_no_id(self):
        sk1 = skills(SkillsID=1,Skillname='Being on Time')
        sk2 = skills(SkillsID=2,Skillname='Alwways Late')
        db.session.add(sk1)
        db.session.add(sk2)
        db.session.commit()
        

        response = self.client.get("/getSkillbyId?skillid=")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 
                    { "code": 404, "message": "No Skill ID provided" })