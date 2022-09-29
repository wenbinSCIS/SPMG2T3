import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flight_admin:6kKVm7C2PHtVtgGT@esd-g7t6-rds.cs2kfkrucphj.ap-southeast-1.rds.amazonaws.com:3306/flight_booking'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:password@database-spm99.cdwudzthowm4.ap-southeast-1.rds.amazonaws.com:3306/LearningApp'


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






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)