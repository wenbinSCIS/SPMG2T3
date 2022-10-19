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


class SRBR(db.Model):
    __tablename__ = 'Skills_Required_By_Role'

    SRBR = db.Column(db.Integer, primary_key=True)
    RoleID = db.Column(db.Integer, nullable=False)
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
            "SRBR": self.SRBR, 
            "RoleID": self.RoleID, 
            "SkillsID": self.SkillsID,

    }

@app.route("/getSRBRbyRoleID")
def get_all_by_roleid():
    args = request.args
    rid = args.get('RoleID')
    select = SRBR.query.filter_by(RoleID=rid)
    return jsonify(
        {
            "data": [role.to_dict()
                    for role in select]
        }
    ), 200


@app.route("/getByRIDSID")
def get_byRIDSID():
  
    args = request.args
    roleid = args.get('roleid')
    skillid = args.get('sid')

    res = SRBR.query.filter(SRBR.RoleID==roleid,SRBR.SkillsID== skillid).all()
    # print(role_list, flush=True)
    if len(res):
        return jsonify({ "code": 201,"message": "Required." })
    else:
        return jsonify({ "code": 404, "message": "Not required." })

@app.route("/addskillrole",methods=["POST"])
def add_skill_role():
    data = request.get_json()
    if not all(key in data.keys() for key in ('Skills', 'RoleID')):
        return jsonify({ "message": "Incorrect JSON object provided." }), 500
    
    srbr_list = SRBR.query.all()
    # print(role_list, flush=True)
    skill_list=data["Skills"]

    if skill_list==[]:
        return { "RoleID": data["RoleID"],"Success":True, "code": 201 }

    for cur_skill in skill_list:
        add_skill_role = SRBR(
            RoleID = data["RoleID"],
            SkillsID = cur_skill["SkillsID"]
        )
        try:
            db.session.add(add_skill_role)
            db.session.commit()
        except:
            return jsonify({ "message": "An error occurred when adding the role to the database.", "code":500 })
    return { "role data": add_skill_role.json(), "code": 201 }

@app.route("/deletebyskillrole/",methods=["POST"])
def delete_by_skill_role():
    data = request.get_json()
    rid = data["RoleID"]
    skill_list = data["Skills"]

    if skill_list==[]:
        return { "RoleID": rid,"Success":True, "code": 201 }
    #Check if role is created in DB
    for cur_skill in skill_list:
        cur_skill_id = cur_skill["SkillsID"]
        skill_role = SRBR.query.filter_by(RoleID=rid,SkillsID=cur_skill_id).first()
        if not skill_role:
            return jsonify({ "message": "SRBR is not valid." }), 500
        else:
            try:
                skill_role.query.filter_by(RoleID = rid,SkillsID=cur_skill_id).delete()
                db.session.commit()
            except:
                return jsonify({ "message": "An error occurred when deleting the role from the database.", "code":500 })
        return { "RoleID": rid,"Success":True, "code": 201 }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)