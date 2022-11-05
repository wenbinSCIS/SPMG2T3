import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flight_admin:6kKVm7C2PHtVtgGT@esd-g7t6-rds.cs2kfkrucphj.ap-southeast-1.rds.amazonaws.com:3306/flight_booking'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:spmfinalpassword6956@spmdb2.cte5x3a9ynus.ap-southeast-1.rds.amazonaws.com:3306/LearningApp'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)

CORS(app)


class learningjourneycourses(db.Model):
    __tablename__ = 'LearningJourneyCourses'

    LJCID = db.Column(db.Integer, primary_key=True)
    LJID = db.Column(db.Integer, nullable=False)
    CourseID = db.Column(db.Integer, nullable=False)


    def to_dict(self):
        """
        'to_dict' converts the object into a dictionary,
        in which the keys correspond to database columns
        """
        columns = self.__mapper__.column_attrs.keys()
        result = {}
        for column in columns:
            result[column] = getattr(self, column)
        return result

    def json(self):
        return {
            "LJCID": self.LJCID, 
            "LJID": self.LJID, 
            "CourseID": self.CourseID,

        }


@app.route("/LJC/getLJCoursesById")
def get_LJCoursesById():
    args = request.args
    ljids = args.get('ljid')
    lj_list = learningjourneycourses.query.filter(learningjourneycourses.LJID==ljids).all()

    # print(role_list, flush=True)
    if len(lj_list):
        return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
    else:
        return jsonify({ "code": 404, "message": 0 })

@app.route("/LJC/deleteLJCbyLJIDCID/")
def delete_LJC_by_ID():
    '''

    '''
    args = request.args
    cid = args.get('cid')
    ljid = args.get('ljid')
    ljc = learningjourneycourses.query.filter(learningjourneycourses.LJID == ljid, learningjourneycourses.CourseID == cid).first()
    if not ljc:
        return jsonify({"message": "LJID or/and CourseID is not valid."}), 404


    learningjourneycourses.query.filter_by(CourseID=cid,LJID=ljid).delete()
    db.session.commit()
    return { "Success":True, "code": 201 }


@app.route("/LJC/deleteAllLJCbyLJID/")
def delete_ALLLJC_by_LJID():
    '''

    '''
    args = request.args

    ljid = args.get('ljid')
    ljc = learningjourneycourses.query.filter(learningjourneycourses.LJID == ljid).all()
    if not ljc:
        return jsonify({"message": "No Such LJID in LJC."}), 404

    try:
        learningjourneycourses.query.filter_by(LJID=ljid).delete()
        db.session.commit()
    except:
        return jsonify({ "message": "An error occurred when deleting the role from the database.", "code":500 })
    return { "Success":True, "code": 201 }

@app.route("/LJC/addCourseIntoBasket")
def addCourseIntoBaskets():
    args = request.args
    ljid = args.get('ljid')
    courseid = args.get('cid')

    if not ljid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    if not courseid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    createLJC = learningjourneycourses(
    LJID = ljid,
    CourseID = courseid,
    )

    try:
        db.session.add(createLJC)
        db.session.flush()
        db.session.refresh(createLJC)
        db.session.commit()

    except:
        return jsonify({"message": "An error occurred when updating the description.", "code":500})
    return {"LJID": createLJC.LJCID, "Success":True, "code": 201 }



@app.route("/LJC/checkIfCourseInLJ")
def checkIfCourseInLJs():
    args = request.args
    ljids = args.get('ljid')
    cid = args.get('cid')

    if not ljids:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    if not cid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    lj_list = learningjourneycourses.query.filter(learningjourneycourses.LJID==ljids, learningjourneycourses.CourseID==cid).all()

    # print(role_list, flush=True)
    if len(lj_list):
        return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
    else:
        return jsonify({ "code": 404, "message": 0 }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5011, debug=True)


