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

class LearningJourneyCourses(db.Model):
  __tablename__ = 'LearningJourneyCourses'
  LJCID = db.Column(db.Integer, primary_key=True)
  LJID = db.Column(db.Integer, nullable=True)
  CourseID = db.Column(db.String(45), nullable=True)

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
      "CourseID": self.CourseID
    }


@app.route("/LJ/getAll")
def get_all():
  data = LearningJourneyCourses.query.all()
  if len(data):
    return jsonify({ "data": [ljc.to_dict() for ljc in data] }), 200
  else:
    return jsonify({ "code": 404, "message": "There are no learning journey courses." }), 404


@app.route("/LJC/getById")
def get_by_id():
  LJCID = request.args.get('LJCID')
  data = LearningJourneyCourses.query.filter_by(LJCID=LJCID)
  if len(data):
    return jsonify({ "data": [ljc.to_dict() for ljc in data] }), 200
  else:
    return jsonify({ "code": 404, "message": "There are no learning journey courses." }), 404


@app.route("/LJC/create",methods=["POST"])
def create():
  '''
  How to: url - localhost:5011/LJC/create
  json - {
    "LJID": 1,
    "CourseID": 2
  }
  '''
  data = request.get_json()
  if not all(key in data.keys() for key in ('LJID', 'CourseID')):
    return jsonify({ "message": "Incorrect JSON object provided." }), 500
  else:
    newLJ = LearningJourneyCourses(LJID=data["LJID"], CourseID=data["CourseID"])
    try:
      db.session.add(newLJ)
      db.session.commit()
    except:
      return jsonify({ "message": "An error occurred when adding the learning journey course to the database.", "code":500 })
    return { "New LJC": newLJ.json(), "code": 201 }


@app.route("/LJC/deleteById",methods=["DELETE"])
def delete_by_ID():
  '''
  How to - URL - localhost:5011/LJC/deleteById
  json - {
    "LJID": 1
  }
  '''
  LJCID = request.args.get('LJCID')
  ljc_toDelete = LearningJourneyCourses.query.filter_by(LJCID=LJCID).first();
  if not ljc_toDelete:
    return jsonify({ "message": "LJCID is not valid." }), 500
  else:
    try:
      db.session.delete(ljc_toDelete)
      db.session.commit()
    except:
      return jsonify({ "message": "An error occurred when deleting the learning journey course from the database.", "code":500 })
    return { "Deleted LJC": ljc_toDelete,"Success":True, "code": 201 }



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5011, debug=True)