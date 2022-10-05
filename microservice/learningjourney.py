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
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:password@spmdb.cte5x3a9ynus.ap-southeast-1.rds.amazonaws.com:3306/LearningApp'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)

CORS(app)


class learningjourney(db.Model):
    __tablename__ = 'LearningJourney'

    LJID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, nullable=False)
    Saved = db.Column(db.Integer, nullable=False)


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
            "LJID": self.LJID, 
            "UserID": self.UserID, 
            "Saved": self.Saved,

        }


@app.route("/LJ/getUnsavedLJById")
def get_Unfilled():
    args = request.args
    userid = args.get('userid')
    lj_list = learningjourney.query.filter(learningjourney.Saved=="0", learningjourney.UserID==userid).all()

    # print(role_list, flush=True)
    if len(lj_list):
        return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
    else:
        return jsonify({ "code": 404, "message": 0 }), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)