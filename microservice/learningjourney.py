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
    LJName = db.Column(db.Integer, nullable=False)
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
            "LJName": self.LJName,
            "RoleID" : self.RoleID,

        }



@app.route("/LJ/getLJByUserId")
def get_savedLJByID():
    args = request.args
    userid = args.get('userid')
    lj_list = learningjourney.query.filter(learningjourney.UserID==userid).all()

    # print(role_list, flush=True)
    if len(lj_list):
        return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
    else:
        return jsonify({ "code": 404, "message": 0 }), 404


@app.route("/LJ/updateRoleIDByLJID")
def UpdateRoleIDByLJId():
    args = request.args
    roleid = args.get('role')
    ljid = args.get('ljid')

    if not roleid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    if not ljid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    lj = learningjourney.query.filter(learningjourney.LJID == ljid).first()
    if not lj:
        return jsonify({ "message": "LJID is not valid." }), 500
    else:

        db.session.query(learningjourney).filter(learningjourney.LJID == ljid).update({ 'RoleID': roleid })
        db.session.commit()
        return {"Success":True, "code": 201 }  
    

@app.route("/LJ/updateLJNameByLJID")
def UpdateLJNameByLjId():
    args = request.args
    ljname = args.get('ljname')
    ljid = args.get('ljid')

    if not ljname:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    if not ljid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404

    lj = learningjourney.query.filter(learningjourney.LJID == ljid).first()
    if not lj:
        return jsonify({ "message": "LJID is not valid." }), 500
    else:
        db.session.query(learningjourney).filter(learningjourney.LJID == ljid).update({ 'LJName': ljname })
        db.session.commit()

  
        return {"Success":True, "code": 201 }


@app.route("/LJ/insertgetLJID")
def insertgetLJID():
    args = request.args
    userid = args.get('userid')
    roleid = args.get('roleid')
    ljname = args.get('ljname')

    if not userid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    if not roleid:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404
    if not ljname:
        return jsonify({ "message": "Incorrect JSON object provided."}), 404

    createLJ = learningjourney(
    # RoleID = 3,
    UserID = userid,
    LJName = ljname,
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




@app.route("/LJ/getLJByLJID")
def get_getLJByLJID():
    args = request.args
    ljid = args.get('ljid')
    lj_list = learningjourney.query.filter( learningjourney.LJID==ljid).all()

    # print(role_list, flush=True)
    if len(lj_list):
        return jsonify({ "data": [lj.to_dict() for lj in lj_list] }), 200
    else:
        return jsonify({ "code": 404, "message": 0 }), 404


@app.route("/LJ/deleteLJbyLJID/")
def delete_LJ_by_LJID():
    '''

    '''
    args = request.args

    ljid = args.get('ljid')




    lj = learningjourney.query.filter(learningjourney.LJID == ljid).first()

    if not lj:
        return jsonify({"message": "LJID is not valid."}), 404
    learningjourney.query.filter_by(LJID=ljid).delete()
    db.session.commit()

    return { "Success":True, "code": 201 }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5010, debug=True)