import unittest
import flask_testing
import json
from freezegun import freeze_time
from learningjourneycourses import app, db, learningjourneycourses

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

class GetLJCoursesById(TestApp):
    def test_get_LJCoursesById(self):
        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJC/getLJCoursesById?ljid="+str(r1.LJID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            "LJCID": r1.LJCID, 
            "LJID": r1.LJID, 
            "CourseID": r1.CourseID, 

        }])

    def test_get_LJCoursesById_no_ljid_item(self):
        response = self.client.get("/LJC/getLJCoursesById?ljid="+str(2))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, { "code": 404, "message": 0 })


class Testdelete_LJC_by_CID_LJID(TestApp):
    def test_delete_LJC_by_id(self):
        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJC/deleteLJCbyLJIDCID/?ljid="+str(1) +"&cid=" + str(2))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Success":True, "code": 201})

    def test_delete_LJ_by_LJID_invalid_ljid(self):
        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)
        db.session.add(r1)
        db.session.commit()

        response = self.client.get("/LJC/deleteLJCbyLJIDCID/?ljid="+str(1) +"&cid=" + str(1))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "LJID or/and CourseID is not valid."})


class Test_Delete_ALLLJC_by_LJID(TestApp):
    def test_delete_ALLLJC_by_LJID(self):
        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)
        r2 = learningjourneycourses(LJCID=2, LJID = 1, CourseID= 3)
        db.session.add(r1)
        db.session.commit()

        db.session.add(r2)
        db.session.commit()
        
        response = self.client.get("/LJC/deleteAllLJCbyLJID/?ljid="+str(1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"Success":True, "code": 201})


    def test_delete_LJ_by_LJID_invalid_ljid(self):
        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)
        db.session.add(r1)
        db.session.commit()

        response = self.client.get("/LJC/deleteAllLJCbyLJID/?ljid="+str(2))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {"message": "No Such LJID in LJC."})



class TestaddCourseIntoBaskets(TestApp):
    def test_add_course_into_baskets(self):

        response = self.client.get("/LJC/addCourseIntoBasket?ljid="+str(1)+ "&cid=" + str(1))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'LJID': 1,
            "Success":True, "code": 201

        })

    def test_add_course_into_baskets_no_ljid(self):

        response = self.client.get("/LJC/addCourseIntoBasket?cid=" + str(1))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })

    def test_add_course_into_baskets_no_cid(self):

        response = self.client.get("/LJC/addCourseIntoBasket?ljid=" + str(1))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "message": "Incorrect JSON object provided." })





class TestcheckIfCourseInLJs(TestApp):
    def test_check_if_course_in_ljs(self):
        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)
        db.session.add(r1)
        db.session.commit()
        
        response = self.client.get("/LJC/checkIfCourseInLJ?ljid="+str(r1.LJID) +"&cid=" + str(r1.CourseID))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["data"], [{
            "LJCID": r1.LJCID, 
            "LJID": r1.LJID, 
            "CourseID": r1.CourseID,

        }])

    def test_check_if_course_in_ljs_no_lj(self):

        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)

        response = self.client.get("/LJC/checkIfCourseInLJ?ljid="+str(r1.LJID) +"&cid=" + str(3))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, { "code": 404, "message": 0 })

    def test_check_if_course_in_ljs_no_ljid(self):

        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)

        response = self.client.get("/LJC/checkIfCourseInLJ?cid=" + str(r1.CourseID))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {  "message": "Incorrect JSON object provided."})

    def test_check_if_course_in_ljs_no_cid(self):

        r1 = learningjourneycourses(LJCID=1, LJID = 1, CourseID= 2)

        response = self.client.get("/LJC/checkIfCourseInLJ?ljid="+str(r1.LJID))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {  "message": "Incorrect JSON object provided."})


