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


class learningjourney(db.Model):
    __tablename__ = 'LearningJourney'

    LJID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, nullable=False)
    Saved = db.Column(db.Integer, nullable=False)
    RoleID = db.Column(db.Integer, nullable=False)


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
            "RoleID" : self.RoleID,

        }


@app.route("/LJ/getUnsavedLJById")
def get_UnsavedLJByID():
    args = request.args
    userid = args.get('userid')
    lj_list = learningjourney.query.filter(learningjourney.Saved=="0", learningjourney.UserID==userid).all()

    # print(role_list, flush=True)
    try:
        if(len(lj_list)):
            return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
        else:
            return jsonify({ "code": 404, "message": 0 })
    except:
        return jsonify({ "code": 404, "message": 0 })

@app.route("/LJ/saveLJById")
def saveLJById():
    args = request.args
    ljid = args.get('ljid')
    try:
        db.session.query(learningjourney).filter(learningjourney.LJID == ljid).update({ 'Saved': 1 })
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred when updating the description.", "code":500})
    return {"Success":True, "code": 201 }


@app.route("/LJ/unsaveLJById")
def unsaveLJById():
    args = request.args
    ljid = args.get('ljid')
    try:
        db.session.query(learningjourney).filter(learningjourney.LJID == ljid).update({ 'Saved': 0 })
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred when updating the description.", "code":500})
    return {"Success":True, "code": 201 }

@app.route("/LJ/updateRoleIDByLJID")
def UpdateRoleIDByLJId():
    args = request.args
    roleid = args.get('role')
    ljid = args.get('ljid')
    try:
        db.session.query(learningjourney).filter(learningjourney.LJID == ljid).update({ 'RoleID': roleid })
        db.session.commit()
    except:
        return jsonify({"message": "An error occurred when updating the description.", "code":500})
    return {"Success":True, "code": 201 }


@app.route("/LJ/insertgetLJID")
def insertgetLJID():
    args = request.args
    userid = args.get('userid')
    roleid = args.get('roleid')
    createLJ = learningjourney(
    # RoleID = 3,
    UserID = userid,
    Saved = 0,
    RoleID = roleid,

    )



    try:
        db.session.add(createLJ)
        db.session.flush()
        db.session.refresh(createLJ)
        db.session.commit()

    except:
        return jsonify({"message": "An error occurred when updating the description.", "code":500})
    return {"LJID": createLJ.LJID, "Success":True, "code": 201 }

@app.route("/LJ/getsavedLJById")
def get_savedLJByID():
    args = request.args
    userid = args.get('userid')
    lj_list = learningjourney.query.filter(learningjourney.Saved=="1", learningjourney.UserID==userid).all()

    # print(role_list, flush=True)
    try:
    
        return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
    except:
        return jsonify({ "code": 404, "message": 0 })


@app.route("/LJ/getLJByLJID")
def get_getLJByLJID():
    args = request.args
    ljid = args.get('ljid')
    lj_list = learningjourney.query.filter( learningjourney.LJID==ljid).all()

    # print(role_list, flush=True)
    try:
    
        return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
    except:
        return jsonify({ "code": 404, "message": 0 })


@app.route("/LJ/deleteLJbyLJID/")
def delete_LJ_by_LJID():
    '''

    '''
    args = request.args

    ljid = args.get('ljid')



    try:
        learningjourney.query.filter_by(LJID=ljid).delete()
        db.session.commit()
    except:
        return jsonify({ "message": "An error occurred when deleting the role from the database.", "code":500 })
    return { "Success":True, "code": 201 }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)