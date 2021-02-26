from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy

# For new flask app
app = Flask(__name__)

# Wraps app in API; initializes a RESTful API
api = Api(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Wraps app in API; initializes a RESTful API
db = SQLAlchemy(app)


# Models in database to store names
class NameModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Nullable - has to have information
    gender = db.Column(db.String(100), nullable=False)

    # Prints for validity - Happens when you print object.
    def __repr__(self):
        return f"Person(name = {name}, gender = {gender})"


# Creates and initializes the database - Do this once!
db.create_all()

"""Request parser makes sure that when a request is sent, 
that we pass the information we need with the request. 
This makes sure it fits guidelines and has correct information.
This is for validation"""
name_put_args = reqparse.RequestParser()

# Information needs to be sent with it
name_put_args.add_argument("name", type=str, help="Person name", required=True)
name_put_args.add_argument("gender", type=str, help="Person gender")

# Dictionary object - returns to user the information about the name the user requests
names = {"daryl": {"age": 36, "gender": "male"},
         "bill": {"age": 70, "gender": "male"}}


def abort_name_none(name):
    if name not in names:
        # Error message if name is not found/invalid
        abort(404, message="Invalid name.")


def abort_name_exists(name):
    if name in names:
        abort(409, message="Name exists.")


# Resource - Handles CRUD
class HelloWorld(Resource):

    # GET request to access name typed after string - can use specifically
    def get(self, name):

        # Aborts if name invalid
        abort_name_none(name)

        return names[name]

        """{"name": name, "test": test} 
        Key value pair - python dictionary (serializable) 
        Returns JSON serializable objects"""

    def post(self):
        return {"data": "Posted"}

    def put(self, name):

        # Prevents creation of video that already exists
        abort_name_exists(name)

        """print(request.form) # gets data from put request with JSON data"""

        # Gets all arguments - send error message if it cannot
        args = name_put_args.parse_args()

        # Adding names
        names[name] = args

        """return {name: args}"""

        # Code to requester - status code - default is 200
        return names[name], 201

    def delete(self, name):
        abort_name_none(name)
        del names[name]
        return '', 204


# Register as a resource - add to API to make accesible by URL
api.add_resource(HelloWorld, "/helloworld/<string:name>")

"""Angle brackets to define the parameter to be passed in;
This defines the type of parameter - we want the user to type 
a 'string' after url"""

# Starts server, flask app - in debug mode for output and logs - use only in development mode
if __name__ == "__main__":
    app.run(debug=True)


