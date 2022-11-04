import requests
from flask_cors import CORS
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
import os
from dotenv import load_dotenv
from datetime import datetime
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://flight_admin:6kKVm7C2PHtVtgGT@esd-g7t6-rds.cs2kfkrucphj.ap-southeast-1.rds.amazonaws.com:3306/flight_booking'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or 'mysql+mysqlconnector://admin:spmfinalpassword6956@spmdb2.cte5x3a9ynus.ap-southeast-1.rds.amazonaws.com:3306/LearningApp'


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 1800}

db = SQLAlchemy(app)




class Roles(db.Model):
    __tablename__ = 'roles'

    RoleID = db.Column(db.Integer, primary_key=True)
    RoleName = db.Column(db.String(255), nullable=False)
    CreatedBy = db.Column(db.String(255), nullable=False)
    Fulfilled = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    TimeAdded = db.Column(db.String(255),nullable=True)

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
            'Description': self.Description,
            'CreatedTime' : self.TimeAdded
        }

@app.route("/roles/getAll")
def get_all():
    role_list = Roles.query.all()
    # print(role_list, flush=True)
    if len(role_list):
        return jsonify({ "code": 200,"data": [role.to_dict() for role in role_list] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no role." })
    
    
@app.route("/roles/getUnfilled")
def get_Unfilled():
    role_list = Roles.query.filter(Roles.Fulfilled==" ").all()
    role_list+= Roles.query.filter(Roles.Fulfilled=="").all()
    # print(role_list, flush=True)
    if len(role_list):
        return jsonify({ "data": [role.to_dict() for role in role_list] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no role." })
    
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
    cur_time = datetime.now()

    if not all(key in data.keys() for key in ('Role Name', 'Created By', 'Description')):
        return jsonify({ "message": "Incorrect JSON object provided." }), 500
    
    Add_Role = Roles(
        RoleName = data["Role Name"],
        CreatedBy = data["Created By"],
        Fulfilled = " ",
        Description = data["Description"],
        TimeAdded = cur_time
    )
    try:
        db.session.add(Add_Role)
        db.session.commit()

    except:
        return jsonify({ "message": "An error occurred when adding the role to the database.", "code":500 })

    return { "data": Add_Role.json(), "code": 201}

@app.route("/roles/deletebyID/",methods=["POST"])
def delete_role_by_ID():
    '''
        How to - URL - localhost:5000/roles/deletebyID/?roleID=3
    '''
    data = request.get_json()
    rid = data["RoleID"]
    #Check if role is created in DB
    role = Roles.query.filter_by(RoleID=rid).first()
    if not role:
        return jsonify({ "message": "RoleID is not valid." }), 500
    else:
        try:
            Roles.query.filter_by(RoleID = rid).delete()
            db.session.commit()
        except:
            return jsonify({ "message": "An error occurred when deleting the role from the database.", "code":500 })
        return { "RoleID": rid,"Success":True, "code": 201 }

@app.route("/roles/getById")
def get_roleById():
  
    args = request.args
    roleid = args.get('roleid')

    role_list = Roles.query.filter(Roles.RoleID==roleid).all()
    # print(role_list, flush=True)
    if len(role_list):
        return jsonify({ "code": 200,"data": [role.to_dict() for role in role_list] }), 200
    else:
        return jsonify({ "code": 404, "message": "There are no role." }), 404

@app.route("/roles/updateNamebyID",methods=["POST"])
def update_name_by_ID():
    '''
        How to - URL - localhost:5000/roles/updateAllbyID
        json = {
            "Role ID":0,
            "Description": "Testing 123 to see if updating roles work 2"
        }
    '''
    data = request.get_json()
    if not all(key in data.keys() for key in ('Role ID', 'RoleName')):
        return jsonify({ "message": "Incorrect JSON object provided."}), 500
    #Check if role is created in DB
    role = Roles.query.filter_by(RoleID=data["Role ID"]).first()
    if not role:
        return jsonify({ "message": "RoleID is not valid." }), 500
    else:
        try:
            cur_role=db.session.query(Roles).get(data["Role ID"])
            cur_role.RoleName = data["RoleName"]
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred when updating role name.", "code":500})
        return { "RoleID": data["Role ID"],"Success":True, "code": 201 }

@app.route("/roles/updateDescriptionbyID",methods=["POST"])
def update_description_by_ID():
    '''
        How to - URL - localhost:5000/roles/updateAllbyID
        json = {
            "Role ID":0,
            "Description": "Testing 123 to see if updating roles work 2"
        }
    '''
    data = request.get_json()
    if not all(key in data.keys() for key in ('Role ID', 'Description')):
        return jsonify({ "message": "Incorrect JSON object provided."}), 500
    #Check if role is created in DB
    role = Roles.query.filter_by(RoleID=data["Role ID"]).first()
    if not role:
        return jsonify({ "message": "RoleID is not valid." }), 500
    else:
        try:
            cur_role=db.session.query(Roles).get(data["Role ID"])
            cur_role.Description = data["Description"]
            db.session.commit()

        except:
            return jsonify({"message": "An error occurred when updating the description.", "code":500})
        return { "RoleID": data["Role ID"],"Success":True, "code": 201 }


@app.route("/roles/updateRoleStatus",methods=["POST"])
def update_role_status():
    data = request.get_json()
    if not all(key in data.keys() for key in ('Role ID', 'Status')):
        return jsonify({ "message": "Incorrect JSON object provided."}), 500
    #Check if role is created in DB
    role = Roles.query.filter_by(RoleID=data["Role ID"]).first()
    if not role:
        return jsonify({ "message": "RoleID is not valid." }), 500
    else:
        if role.Fulfilled == data["Status"]:
            return jsonify({ "message": "Role is already the thing you are changing to" }), 501
        else:
            try:
                db.session.query(Roles).filter(Roles.RoleID == data["Role ID"]).update({'Fulfilled': data["Status"] })
                db.session.commit()
            except:
                return jsonify({"message": "An error occurred when updating the Fulfilled status.", "code":500})
        return { "RoleID": data["Role ID"],"Success":True,"Status": data["Status"], "code": 201 }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)