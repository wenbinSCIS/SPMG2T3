import unittest
import flask_testing
import json
from freezegun import freeze_time
from roles import app, db, Roles

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

class TestGetAllRoles(TestApp):
    def test_get_all(self):
        r1 = Roles(RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/roles/getAll")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'RoleID': 1,
            'RoleName': r1.RoleName,
            'CreatedBy': r1.CreatedBy,
            "Fulfilled": r1.Fulfilled,
            "Description":r1.Description,
            "TimeAdded": r1.TimeAdded
        }])

    def test_get_all_no_role(self):
        response = self.client.get("/roles/getAll")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, { "code": 404, "message": "There are no role." })


class TestGetUnfilled(TestApp):
    def test_get_Unfilled(self):
        r1 = Roles(RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        r2 = Roles(RoleName='Coder', CreatedBy=2, Fulfilled="Filled",
                    Description="For coding",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        
        response = self.client.get("/roles/getUnfilled")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            'RoleID': 1,
            'RoleName': r1.RoleName,
            'CreatedBy': r1.CreatedBy,
            "Fulfilled": r1.Fulfilled,
            "Description":r1.Description,
            "TimeAdded": r1.TimeAdded
        }])

    def test_get_Unfilled_no_unfilled(self):
        r1 = Roles(RoleName='Coder', CreatedBy=2, Fulfilled="Filled",
                    Description="For coding",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/roles/getUnfilled")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, { "code": 404, "message": "There are no role." })

@freeze_time("2022-10-05 09:19:17")
class TestAddRole(TestApp):
    def test_add_role(self):
        request_body = {
            'Role Name': 'Programmer',
            'Created By': 1,
            "Description":"To programme the newest project"
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], {
            'RoleID': 1,
            'RoleName': 'Programmer',
            'CreatedBy': 1,
            "Fulfilled": " ",
            "Description":"To programme the newest project",
            "CreatedTime": "2022-10-05 09:19:17"
        })

    def test_add_role_no_name(self):
        request_body = {
            'Created By': 1,
            "Description":"To programme the newest project"
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

    def test_add_role_no_creator(self):
        request_body = {
            'RoleName': 'Programmer',
            "Description":"To programme the newest project"
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

    def test_add_role_no_description(self):
        request_body = {
            'RoleName': 'Programmer',
            'CreatedBy': 1
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

    def test_add_role_role_name_no_alphabet(self):
        request_body = {
            'Role Name': '12345',
            'Created By': 1,
            "Description":"To programme the newest project"
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Role name has no alphabet" })

    def test_add_role_description_similar_to_role_name(self):
        request_body = {
            'Role Name': 'Programmer',
            'Created By': 1,
            "Description":'Programmer'
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { 'message': 'Description cannot be similar to rolename' })

    def test_add_role_role_name_start_with_number_or_symbol(self):
        request_body = {
            'Role Name': '1Programmer',
            'Created By': 1,
            "Description":'To programme the new project'
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { 'message': 'Role name cannot start with number or symbol' })

    def test_add_role_role_name_is_empty_string(self):
        request_body = {
            'Role Name': '',
            'Created By': 1,
            "Description":'To programme the new project'
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Role name cannot be blank or contain only whitespace" })

    def test_add_role_role_name_contain_only_white_space(self):
        request_body = {
            'Role Name': '   ',
            'Created By': 1,
            "Description":'To programme the new project'
        }

        response = self.client.post("/roles/create",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "Role name cannot be blank or contain only whitespace" })

class TestDeleteRoleById(TestApp):
    def test_delete_role_by_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "RoleID": r1.RoleID,
        }

        response = self.client.post("/roles/deletebyID/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"RoleID": 1,"Success":True, "code": 201})

    def test_delete_role_by_id_invalid_role_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "RoleID": 2,
        }

        response = self.client.post("/roles/deletebyID/",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, { "message": "RoleID is not valid." })

class TestUpdateDescriptionById(TestApp):
    def test_update_description_by_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "Description":"To code"
        }

        response = self.client.post("/roles/updateDescriptionbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "RoleID": r1.RoleID,"Success":True, "code": 201 })

    def test_update_description_by_id_invalid_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": 2,
            "Description":"To code"
        }

        response = self.client.post("/roles/updateDescriptionbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "RoleID is not valid." })

    def test_update_description_by_id_no_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Description":"To code"
        }

        response = self.client.post("/roles/updateDescriptionbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

    def test_update_description_by_id_no_description(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": 2
        }

        response = self.client.post("/roles/updateDescriptionbyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

class TestUpdateRoleStatus(TestApp):
    def test_update_status(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "Status":"Filled"
        }

        response = self.client.post("/roles/updateRoleStatus",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "RoleID": r1.RoleID,"Success":True,"Status": "Filled", "code": 201 })

    def test_update_status_sameStatus(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled="Filled",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "Status":"Filled"
        }

        response = self.client.post("/roles/updateRoleStatus",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 501)
        self.assertEqual(response.json, 
                    { "message": "Role is already the thing you are changing to" })
        
    def test_update_status_status_FilledtoAvailable(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled="Filled",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "Status":""
        }

        response = self.client.post("/roles/updateRoleStatus",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "RoleID": r1.RoleID,"Success":True,"Status": "", "code": 201 })

    def test_update_status_invalid_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID":2,
            "Status":"Filled"
        }

        response = self.client.post("/roles/updateRoleStatus",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "RoleID is not valid." })

    def test_update_status_no_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Status":"Filled"
        }

        response = self.client.post("/roles/updateRoleStatus",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

    def test_update_status_no_status(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID
        }

        response = self.client.post("/roles/updateRoleStatus",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

class TestUpdateRoleNameById(TestApp):
    def test_update_role_name_by_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "RoleName":"Coder"
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "RoleID": r1.RoleID,"Success":True, "code": 201 })

    def test_update_role_name_by_id_invalid_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": 2,
            "RoleName":"Coder"
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "RoleID is not valid." })

    def test_update_role_name_by_id_no_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "RoleName":"Coder"
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

    def test_update_role_name_by_id_invalid_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": 2,
            "RoleName":"Coder"
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "RoleID is not valid." })

    def test_update_role_name_by_id_no_name(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})

    def test_update_role_name_by_id_only_white_space(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "RoleName":"   "
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Role name cannot be blank or contain only whitespace" })

    def test_update_role_name_by_id_no_alphabet(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "RoleName":"123456"
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Role name has no alphabet" })

    def test_update_role_name_by_id_start_with_number_or_symbol(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        request_body = {
            "Role ID": r1.RoleID,
            "RoleName":"1Programmer"
        }

        response = self.client.post("/roles/updateNamebyID",
                                    data=json.dumps(request_body),
                                    content_type='application/json')

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Role name cannot start with number or symbol" })

class TestGetRoleById(TestApp):
    def test_get_role_by_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        

        response = self.client.get("/roles/getById?roleid="+str(r1.RoleID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, 
                    { "code": 200,"data": 
                    [{
                    'RoleID': r1.RoleID,
                    'RoleName': r1.RoleName,
                    'CreatedBy': r1.CreatedBy,
                    "Fulfilled": r1.Fulfilled,
                    "Description":r1.Description,
                    "TimeAdded": r1.TimeAdded
                    }]})


    def test_get_role_by_id_invalid_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        

        response = self.client.get("/roles/getById?roleid="+str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, 
                    {"code": 404, "message": "There are no role."})

    def test_get_role_by_id_no_id(self):
        r1 = Roles(RoleID=1,RoleName='Programmer', CreatedBy=1, Fulfilled=" ",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()

        response = self.client.get("/roles/getById?roleid=")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, 
                    { "message": "Incorrect JSON object provided."})