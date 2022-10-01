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
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:password@database-spm99.cdwudzthowm4.ap-southeast-1.rds.amazonaws.com:3306/LearningApp'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)

CORS(app)


class Roles(db.Model):
    __tablename__ = 'roles'

    RoleID = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(255), nullable=False)
    CreatedBy = db.Column(db.String(255), nullable=False)
    Fulfilled = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(255), nullable=False)

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
            "RoleID": self.RoleID, 
            "RoleName": self.RoleName, 
            "CreatedBy": self.CreatedBy,
            "Fulfilled": self.Fulfilled, 
            'Description': self.Description
    }

@app.route("/roles")
def get_all():
    role_list = Roles.query.all()
    print(role_list, flush=True)
    return jsonify({ "data": [role.to_dict() for role in role_list] }), 200
    
@app.route("/roles/create",methods=["POST"])
def create_role():
    '''
    How to: url - localhost:5000/roles/create
    json - {
        "Role Name":"Product Manager 2",
        "Created By": "Mr Dumb 2",
        "Description": "Testing 123 to see if adding roles work 2"
    }
'''
    data = request.get_json()
    if not all(key in data.keys() for key in ( 'Role Name','Created By', 'Description')):
        return jsonify({ "message": "Incorrect JSON object provided." }), 500
    
    Add_Role = Roles(
        # RoleID = 3,
        RoleName = data["Role Name"],
        CreatedBy = data["Created By"],
        Fulfilled = " ",
        Description = data["Description"]
    )
    try:
        db.session.add(Add_Role)
        db.session.commit()
    except:
        return jsonify({ "message": "An error occurred when adding the role to the database.", "code":500 })
    return { "role data": Add_Role.json(), "code": 201 }

@app.route("/roles/deletebyID/",methods=["GET"])
def delete_role_by_ID():
    '''
        How to - URL - localhost:5000/roles/deletebyID/?roleID=3
    '''
    args = request.args
    rid = args.get('roleID')
    #Check if role is created in DB
    role = Roles.query.filter_by(RoleID=rid).first()
    if not role:
        return jsonify({
            "message": "RoleID is not valid."
        }), 500
    else:
        try:
            Roles.query.filter_by(RoleID = rid).delete()
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when deleting the role from the database.", "code":500})
        return {"RoleID": rid,"Success":True, "code": 201}

@app.route("/roles/updateDescriptionbyID",methods=["POST"])
def update_description_by_ID():
    '''
        How to - URL - localhost:5000/roles/updateDescriptionbyID
        json = {
        "Role ID":0,
        "Description": "Testing 123 to see if updating roles work 2"
    }
    '''
    data = request.get_json()
    if not all(key in data.keys() for key in ( 'Role ID','Description')):
        return jsonify({
            "message": "Incorrect JSON object provided."}), 500
    #Check if role is created in DB
    role = Roles.query.filter_by(RoleID=data["Role ID"]).first()
    if not role:
        return jsonify({
            "message": "RoleID is not valid."
        }), 500
    else:
        try:
            db.session.query(Roles).filter(Roles.RoleID == data["Role ID"]).update({'Description': data["Description"]})
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when updating the description.", "code":500})
        return {"RoleID": data["Role ID"],"Success":True, "code": 201}

@app.route("/getAllRole")
def get_all_role():
    role_list = Roles.query.all()
    if len(role_list):
        return jsonify({
            "code": 200,
            "data":  [role.to_dict() for role in role_list]
        })
    return jsonify({
        "code": 404,
        "message": "There are no role."
    }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)