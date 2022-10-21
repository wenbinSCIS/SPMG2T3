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


class skills(db.Model):
    __tablename__ = 'skills'

    SkillsID = db.Column(db.Integer, primary_key=True)
    Skillname = db.Column(db.String(255), nullable=False)
   


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
            "SkillsID": self.SkillsID, 
            "Skillname": self.Skillname, 
     

     }

@app.route("/getSkillbyId")
def get_skill_by_skillid():
    args = request.args
    sid = args.get('skillid')
    select = skills.query.filter_by(SkillsID=sid)
    return jsonify(
        {
            "data": [skill.to_dict()
                     for skill in select]
        }
    ), 200

@app.route("/getAllSkill")
def get_all_skill():
    skill_list = skills.query.all()
    if len(skill_list):
        return jsonify(
            {
                "code": 200,
                "data":  [skill.to_dict() for skill in skill_list] # edited to same format as /getSkillbyId
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no skill creation."
        }
    ), 404
@app.route("/updateskillnamebyID",methods=["POST"])
def update_skillname_by_ID():
    '''
        How to - URL - localhost:5000/roles/updateAllbyID
        json = {
            "Skill ID":0,
            "Skillname": "newskillnamehere"
        }
    '''
    data = request.get_json()
    if not all(key in data.keys() for key in ('Skill ID', 'Skillname')):
        return jsonify({ "message": "Incorrect JSON object provided."}), 500
    #Check if role is created in DB
    skill = skills.query.filter_by(SkillsID=data["Skill ID"]).first()
    if not skill:
        return jsonify({ "message": "Skill ID is not valid." }), 500
    else:
        try:
            db.session.query(skills).filter(skills.SkillsID == data["Skill ID"]).update({ 'Skillname': data["Skillname"] })
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when updating the skillname.", "code":500})
        return { "Skill ID": data["Skill ID"],"Success":True, "code": 201 }


@app.route("/skills/create",methods=["POST"])
def create_skill():
    '''
    How to: url - localhost:5000/roles/create
    json - {
        "Role Name":"Product Manager 2",
        "Created By": "Mr Dumb 2",
        "Description": "Testing 123 to see if adding roles work 2"
    }
    '''
    data = request.get_json()

    if not (key in data.keys() for key in ( 'Skillname')):
        return jsonify({ "message": "Incorrect JSON object provided." }), 500
    
    Add_skills = skills(
        
        Skillname = data["Skillname"]

    )
    try:
        db.session.add(Add_skills)
        db.session.commit()

    except:
        return jsonify({ "message": "An error occurred when adding the role to the database.", "code":500 })

    return { "data": Add_skills.json(), "code": 201}

@app.route("/deleteskillsbyID",methods=["POST"])
def delete_skillname_by_ID():
    '''Skillid is in a list'''
    data = request.get_json()
    all_pass = True
    if not (key in data.keys() for key in ('Skill IDs')):
        return jsonify({ "message": "Incorrect JSON object provided."}), 500
    #Check if skills is created in DB
    for each_skill in data["Skill IDs"]:
        skill = skills.query.filter_by(SkillsID=each_skill).first()
        if not skill:
            all_pass = False
            return jsonify({ "message": "Skill ID is not valid." }), 500
    if all_pass:
        try:
            for each_skillID in data["Skill IDs"]:
                skills.query.filter_by(SkillsID = each_skillID).delete()
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when deleting the skills", "code":500})
        return { "Skill IDs": data["Skill IDs"],"Success":True, "code": 201 }



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)