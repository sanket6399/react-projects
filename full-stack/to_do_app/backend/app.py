from flask import Flask, request
from flask_cors import CORS

app = Flask("app")

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
todolist = {}

class APIBuilder():
    
    @app.route("/addTask", methods=['POST'])
    def add_task():
        try:
            data = request.get_json()
            print(data)
            if data['task_id'] not in todolist:
                todolist[data['task_id']] = data['task_name']
                print(todolist)
                response = {
                    "status_code" : 200,
                    "Message" : "Data Added Successfully" 
                }
                return response
            else:
                response = {
                    "status_code" : 400,
                    "Message" : "Data already exists" 
                }
                return response
        except Exception as e:
            print("Error Occured while adding the task")
    
    @app.route("/DeleteTask", methods=['DELETE'])
    def delete_task():
        try:
            data = request.get_json()
            print(todolist)
            if data['task_id'] in todolist:
                del(todolist[data['task_id']])
                response = {
                    "status_code" : 200,
                    "Message" : "Data Deleted Successfully" 
                }
                return response
            else:
                response = {
                    "status_code" : 400,
                    "Message" : "Data does not exists" 
                }
                return response
        except Exception as e:
            print("Error Occured while deleting the task")
    
    @app.route("/updateTask", methods=['PUT'])
    def update_task():
        try:
            data = request.get_json()
            if data['task_id'] in todolist:
                todolist[data['task_id']] = data['task_name']
                response = {
                    "status_code" : 200,
                    "Message" : "Data Updated Successfully" 
                }
                return response
            else:
                response = {
                    "status_code" : 400,
                    "Message" : "Data does not exists" 
                }
                return response
        except Exception as e:
            print("Error Occured while deleting the task")
    
    @app.route("/getTask", methods=['POST'])
    def get_task():
        try:
            data = request.get_json()
            print(data)
            if data['task_id'] in todolist:
                print("Here")
                response = {
                    "status_code" : 200,
                    "Message" : todolist[data['task_id']]
                }
                return response
            else:
                response = {
                    "status_code" : 400,
                    "Message" : "Data does not exists" 
                }
                return response
        except Exception as e:
            print("Error Occured while updating the task")
    
    @app.route("/getAllTask", methods=['GET'])
    def get_all_task():
        try:
            response = {
                "status_code" : 200,
                "Message" : todolist
            }
            return response
            
        except Exception as e:
            print("Error Occured while getting the task")
    
    @app.route("/deleteAll", methods=['GET'])
    def delete_all_task():
        try:
            todolist.clear()
            if len(todolist) == 0:
                response = {
                    "status_code" : 200,
                    "Message" : "Deleted all tasks"
                }
                return response
            return {
                    "status_code" : 200,
                    "Message" : "Could not Delete all tasks"
                }
            
        except Exception as e:
            print("Error Occured while deleting the task", e)


if __name__ == "__main__":
    app.run(debug=True)
        
