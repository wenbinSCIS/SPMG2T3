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


class SABC(db.Model):
    __tablename__ = 'Skills_Acquired_By_Course'

    SABC = db.Column(db.Integer, primary_key=True)
    CourseID = db.Column(db.Integer, nullable=False)
    SkillsID = db.Column(db.Integer, nullable=False)


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
            "SABC": self.SABC, 
            "CourseID": self.CourseID, 
            "SkillsID": self.SkillsID,
        }

@app.route("/getSABCbySkillID")
def get_all_by_skillid():
    args = request.args
    sid = args.get('sid')
    if sid==None or sid=="":
        return jsonify({ "message": "Incorrect JSON object provided." }), 500

    select = SABC.query.filter_by(SkillsID=sid).all()
    if len(select):
        return jsonify({ "data": [item.to_dict() for item in select] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no SABC." }), 404

@app.route("/getSABCbyCourseID")
def get_all_by_courseid():
    args = request.args
    cid = args.get('CourseID')

    if cid==None or cid=="":
        return jsonify({ "message": "Incorrect JSON object provided." }), 500

    select = SABC.query.filter_by(CourseID=cid).all()

    if len(select):
        return jsonify({ "data": [item.to_dict() for item in select] }), 200

    else:
        return jsonify({ "code": 404, "message": "There are no SABC." }), 404


@app.route("/addskillcourse",methods=["POST"])
def add_skill_course():
    data = request.get_json()
    if not all(key in data.keys() for key in ('Skills', 'CourseID')):
        return jsonify({ "message": "Incorrect JSON object provided." }), 500
    
    sabc_list = SABC.query.all()
    skill_list=data["Skills"]

    if skill_list==[]:
        return { "CourseID": data["CourseID"],"message":"No Skills to add to course.", "code": 500 },500

    all_skill_sabc=[]

    for sabc in sabc_list:
        all_skill_sabc.append(sabc.SkillsID)
    
    for skill in data["Skills"]:
        if skill["SkillsID"] in all_skill_sabc:
            return jsonify({ "message": "Error Occured. Skill already tied to Course." }), 500

    for cur_skill in skill_list:
        add_skill_course = SABC(
            CourseID = data["CourseID"],
            SkillsID = cur_skill["SkillsID"]
        )
        try:
            db.session.add(add_skill_course)
            db.session.commit()
        except:
            return jsonify({ "message": "An error occurred when adding the SABC to the database.", "code":500 })
    return { "course data": add_skill_course.json(), "code": 201 }

@app.route("/deletebyskillcourse",methods=["POST"])
def delete_by_skill_course():
    data = request.get_json()
    if not all(key in data.keys() for key in ('Skills', 'CourseID')):
        return jsonify({ "message": "Incorrect JSON object provided." }), 500
    cid = data["CourseID"]
    skill_list = data["Skills"]
    error_sabc_list=[]
    have_error=False
    addition_happen=False

    if skill_list==[]:
        return { "CourseID": data["CourseID"],"message":"No Skills to add to role.", "code": 500 },500
    #Check if role is created in DB
    for cur_skill in skill_list:
        cur_skill_id = cur_skill["SkillsID"]
        skill_course = SABC.query.filter_by(CourseID=cid,SkillsID=cur_skill_id).first()
        if not skill_course:
            error_sabc_list.append(cur_skill_id)
            have_error=True
        else:
            try:
                skill_course.query.filter_by(CourseID = cid,SkillsID=cur_skill_id).delete()
                db.session.commit()
                addition_happen=True
            except:
                return jsonify({ "message": "An error occurred when deleting the SABC from the database.", "code":500 })

    if have_error:
        message="Course did not exist or Course does not has skill with id "
        for i in range(len(error_sabc_list)):
            cur_skill_id=error_sabc_list[i]
            message+=str(cur_skill_id)

            if i!=len(error_sabc_list)-1:
                message+=", "

        if addition_happen:
            message+=". The rest of the skills are deleted"

        return jsonify({ "message": message }), 500
    return { "CourseID": cid,"Success":True, "code": 201 }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)