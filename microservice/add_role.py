from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests

import json

app = Flask(__name__)
CORS(app)

@app.route("/add_role", methods=['POST'])
def create_booking():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            role_skill_data = request.get_json()
            print("\nReceived a booking in JSON:", role_skill_data)

            # do the actual work
            # 1. Send order info {cart items}
            result_add_role = processAddRole(role_skill_data)
            print('\n------------------------')
            print('\nresult: ', result_add_role)

            role_id = result_add_role["data"]["add_role_result"]["data"]["RoleID"]

            result_add_skill_role = processAddSRBR(role_skill_data,role_id)
            print('\n------------------------')
            print('\nresult: ', result_add_skill_role)

            return jsonify(result_add_skill_role), result_add_role["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "manage_booking.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

@app.route("/add_role/add_role", methods=['POST'])
def processAddRole(role_skill_data):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print('\n-----Invoking order microservice-----')
    add_role_result = requests.post('http://127.0.0.1:5000/roles/create', json=role_skill_data).json()
    print('add_role_result:', add_role_result)

    # Check the order result; if a failure, send it to the error microservice.
    code = add_role_result["code"]
    message = json.dumps(add_role_result)

    if code not in range(200, 300): 
        # 7. Return error
        return {
            "code": 500,
            "data": {"booking_result": add_role_result},
            "message": "Role creation failed."
        }

    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    else:
        return {
        "code": 201,
        "data": {
            "add_role_result": add_role_result,
            }
        }

@app.route("/add_role/add_skill_role", methods=['POST'])
def processAddSRBR(role_skill_data,role_id):
    # 2. Send the order info {cart items}
    # Invoke the order microservice
    print('\n-----Invoking order microservice-----')
    skill_role_data = {"Skills":role_skill_data["skill_list"],"RoleID":role_id}
    add_skill_role_result = requests.post('http://127.0.0.1:5001/addskillrole', json=skill_role_data).json()
    print('add_role_result:', add_skill_role_result)

    # Check the order result; if a failure, send it to the error microservice.
    code = add_skill_role_result["code"]
    message = json.dumps(add_skill_role_result)

    if code not in range(200, 300): 
        # 7. Return error
        return {
            "code": 500,
            "data": {"booking_result": add_skill_role_result},
            "message": "Role creation failed."
        }

    # Notice that we are publishing to "Activity Log" only when there is no error in order creation.
    # In http version, we first invoked "Activity Log" and then checked for error.
    # Since the "Activity Log" binds to the queue using '#' => any routing_key would be matched 
    # and a message sent to “Error” queue can be received by “Activity Log” too.

    else:
        return {
        "code": 201,
        "data": {
            "booking_result": add_skill_role_result,
            }
        }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for placing an order...")
    app.run(host="0.0.0.0", port=5020, debug=True)