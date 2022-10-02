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


class LearningJourney(db.Model):
  __tablename__ = 'LearningJourney'
  LJID = db.Column(db.Integer, primary_key=True)
  UserID = db.Column(db.Integer, nullable=True)

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
      "UserID": self.UserID
    }


@app.route("/LJ/getAll")
def get_all():
  '''
  How to: url - localhost:5011/LJ/getAll?UserID=2
  '''
  UserID = int(request.args.get('UserID'))
  data = LearningJourney.query.filter_by(UserID=UserID)
  if len(data):
    return jsonify({ "data": [lj.to_dict() for lj in data] }), 200
  else:
    return jsonify({ "code": 404, "message": "There are no learning journeys." }), 404


@app.route("/LJ/getById")
def get_by_id():
  LJID = request.args.get('LJID')
  data = LearningJourney.query.filter_by(LJID=LJID)
  if len(data):
    return jsonify({ "data": [lj.to_dict() for lj in data] }), 200
  else:
    return jsonify({ "code": 404, "message": "There are no learning journeys." }), 404


@app.route("/LJ/create",methods=["POST"])
def create():
  '''
  How to: url - localhost:5010/LJ/create
  json - {
    "UserID": 2
  }
  '''
  data = request.get_json()
  if not all(key in data.keys() for key in ('UserID')):
    return jsonify({ "message": "Incorrect JSON object provided." }), 500
  else:
    newLJ = LearningJourney(UserID=data["UserID"])
    try:
      db.session.add(newLJ)
      db.session.commit()
    except:
      return jsonify({ "message": "An error occurred when adding the learning journey to the database.", "code":500 })
    return { "New LJ": newLJ.json(), "code": 201 }


@app.route("/LJ/deleteById",methods=["DELETE"])
def delete_by_ID():
  '''
  How to - URL - localhost:5010/LJ/deleteById
  json - {
    "LJID": 1
  }
  '''
  LJID = request.args.get('LJID')
  lj_toDelete = LearningJourney.query.filter_by(LJID=LJID).first();
  if not lj_toDelete:
    return jsonify({ "message": "LJID is not valid." }), 500
  else:
    try:
      db.session.delete(lj_toDelete)
      db.session.commit()
    except:
      return jsonify({ "message": "An error occurred when deleting the learning journey from the database.", "code":500 })
    return { "Deleted LJ": lj_toDelete,"Success":True, "code": 201 }



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5010, debug=True)