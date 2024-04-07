from flask import Flask, request
from flask_restx import Api, Resource
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Example API', description='A simple example API with Flask-RestX')

# Connect to MongoDB
client = MongoClient('mongodb+srv://asif2403:asif@cluster0.lqdqbg2.mongodb.net/')
db = client['Login_page']
collection = db['users']  # Specify the collection name (e.g., 'users')

@api.route('/signup')
class SignUp(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Check if the username already exists
        if collection.find_one({'username': username}):
            return {'message': 'Username already exists'}, 400
        
        # Insert new user into MongoDB collection
        collection.insert_one({'username': username, 'password': password})
        
        return {'message': 'User registered successfully'}, 201
    
# ... (rest of the code remains the same)



@api.route('/signin')
class SignIn(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        # Verify username and password from MongoDB collection
        user = collection.find_one({'username': username, 'password': password})
        
        if user:
            return {'message': 'Sign in successful'}
        else:
            return {'message': 'Invalid username or password'}, 401

if __name__ == '__main__':
    app.run(debug=True)
