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
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:password123@database-spm.cuafqmupljkl.us-east-2.rds.amazonaws.com:3306/LearningApp'


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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)