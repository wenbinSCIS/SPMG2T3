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


class courses(db.Model):
    __tablename__ = 'course'

    CourseID = db.Column(db.Integer, primary_key=True)
    CourseName = db.Column(db.String(255), nullable=False)
    CourseDescription = db.Column(db.String(255), nullable=False)


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
            "CourseID": self.CourseID,
            "CourseName": self.CourseName, 
            "CourseDescription": self.CourseDescription, 
        }

@app.route("/getCoursebyId")
def get_course_by_courseid():
    args = request.args
    cid = args.get('cid')
    if cid:
        select = courses.query.filter_by(CourseID=cid).all()
        if len(select)<1:
            return jsonify({ "message": "CourseID is not valid." }), 500
        else:
            return jsonify({ "data": [course.to_dict() for course in select] }), 200
    else:
        return jsonify({ "message": "No Course ID provided" }), 500
        

@app.route("/courses/getAll")
def get_all_courses():
    course_list = courses.query.all()
    if len(course_list)>0:
        return jsonify({ "data": [course.to_dict() for course in course_list] }, 200)
    else:
        return jsonify({ "code": 404, "message": "No Courses Found." }), 404



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)