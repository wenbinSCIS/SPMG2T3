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
            "SABC": self.SRBR, 
            "CourseID": self.CourseID, 
            "SkillsID": self.SkillsID,

     }

@app.route("/getSABCbySkillID")
def get_all_by_skillid():
    args = request.args
    sid = args.get('sid')
    select = SABC.query.filter_by(SkillsID=sid)
    return jsonify(
        {
            "data": [item.to_dict()
                     for item in select]
        }
    ), 200






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)