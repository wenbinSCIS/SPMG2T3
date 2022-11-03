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

@freeze_time("2022-10-05 09:19:17")
class TestGetAll(TestApp):
    def test_get_all(self):
        r1 = Roles(RoleName='Programmer', CreatedBy='Ryan Tan', Fulfilled="",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/roles/getAll")

        self.assertEqual(response.json["data"], [{
            'RoleID': 1,
            'RoleName': r1.RoleName,
            'CreatedBy': r1.CreatedBy,
            "Fulfilled": r1.Fulfilled,
            "Description":r1.Description,
            "TimeAdded": r1.TimeAdded
        }])
        db.drop_all()

@freeze_time("2022-10-05 09:19:17")
class TestGetUnfilled(TestApp):
    def test_get_Unfilled(self):
        r1 = Roles(RoleName='Programmer', CreatedBy='Ryan Tan', Fulfilled="",
                    Description="To programme the newest project",TimeAdded="2022-10-05 09:19:17")
        r2 = Roles(RoleName='Coder', CreatedBy='Brian Lee', Fulfilled="Filled",
                    Description="For coding",TimeAdded="2022-10-05 09:19:17")
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()
        
        response = self.client.get("/roles/getUnfilled")

        self.assertEqual(response.json["data"], [{
            'RoleID': 1,
            'RoleName': r1.RoleName,
            'CreatedBy': r1.CreatedBy,
            "Fulfilled": r1.Fulfilled,
            "Description":r1.Description,
            "TimeAdded": r1.TimeAdded
        }])

