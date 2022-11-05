import unittest
import flask_testing
import json
from freezegun import freeze_time
from learningjourney import app, db, learningjourney

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

class getLJByUserID(TestApp):
    def test_get_savedLJByID(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJ/getLJByUserId?userid="+str(r1.UserID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            "LJID": r1.LJID, 
            "UserID": r1.UserID, 
            "LJName": r1.LJName,
            "RoleID" : r1.RoleID,
        }])

    def test_get_savedLJByID_noUser(self):
        response = self.client.get("/LJ/getLJByUserId?userid="+str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": 0 })



class TestUpdateRoleIDByLJId(TestApp):
    def test_update_role_id_by_ljid(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)

        db.session.add(r1)
        db.session.commit()
        


        response = self.client.get("/LJ/updateRoleIDByLJID?ljid="+str(r1.LJID)+"&role=" + str(2))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "Success":True, "code": 201 })

    def test_update_role_id_by_ljid_by_id_invalid_id(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        response = self.client.get("/LJ/updateRoleIDByLJID?ljid="+str(2)+"&role=" + str(2))

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "LJID is not valid."})

    def test_update_role_id_by_ljid_by_id_no_roleid(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJ/updateRoleIDByLJID?ljid="+str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

    def test_update_role_id_by_ljid_by_id_no_ljid(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJ/updateRoleIDByLJID?role=" + str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})


class TestUpdateLJNameByLjId(TestApp):
    def test_update_lj_name_by_ljid(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)

        db.session.add(r1)
        db.session.commit()
        


        response = self.client.get("/LJ/updateLJNameByLJID?ljid="+str(r1.LJID)+"&ljname=" + "Not Important")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "Success":True, "code": 201 })

    def test_update_role_id_by_ljid_by_id_invalid_id(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        response = self.client.get("/LJ/updateLJNameByLJID?ljid="+str(2)+"&ljname=" + "Not Important")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "LJID is not valid."})

    def test_update_role_id_by_ljid_by_id_no_ljname(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJ/updateLJNameByLJID?ljid="+str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

    def test_update_role_id_by_ljid_by_id_no_ljid(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJ/updateLJNameByLJID?role=" + str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})



class TestinsertgetLJID(TestApp):
    def test_insert_get_ljid(self):

        response = self.client.get("/LJ/insertgetLJID?userid="+str(1)+"&ljname=" + "Not Important"+"&roleid=" + str(1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'LJID': 1,
            "Success":True, "code": 201

        })

    def test_insert_get_ljid_no_userid(self):

        response = self.client.get("/LJ/insertgetLJID?ljname=" + "Not Important"+"&roleid=" + str(1))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

    def test_insert_get_ljid_no_ljname(self):

        response = self.client.get("/LJ/insertgetLJID?userid="+str(1)+ "&roleid=" + str(1))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

    def test_insert_get_ljid_no_roleid(self):

        response = self.client.get("/LJ/insertgetLJID?userid="+str(1)+"&ljname=" + "Not Important")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })



class TestgetLJByLJID(TestApp):
    def test_get_savedLJByLJID(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJ/getLJByLJID?ljid="+str(r1.LJID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            "LJID": r1.LJID, 
            "UserID": r1.UserID, 
            "LJName": r1.LJName,
            "RoleID" : r1.RoleID,
        }])

    def test_get_savedLJByID_noUser(self):
        response = self.client.get("/LJ/getLJByLJID?ljid="+str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": 0 })


class Testdelete_LJ_by_LJID(TestApp):
    def test_delete_LJ_by_LJID(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "RoleID": r1.RoleID,
        }
        response = self.client.get("/LJ/deleteLJbyLJID/?ljid="+str(1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Success":True, "code": 201})

    def test_delete_LJ_by_LJID_invalid_ljid(self):
        r1 = learningjourney(LJID = 1, UserID=8, LJName='Important', RoleID=2)
        db.session.add(r1)
        db.session.commit()
        response = self.client.get("/LJ/deleteLJbyLJID/?ljid="+str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "message": "LJID is not valid." })
