from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('name')


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

class HelloFriend(Resource):
    def get(self):
        return {'hello': 'friend'}


class PostTest(Resource):
    def post(self):
        args = parser.parse_args()
        name = {'hello ': args['name']}
        return(name, 201)

api.add_resource(HelloWorld, '/')
api.add_resource(HelloFriend, '/api/get')
api.add_resource(PostTest, '/api/post')

if __name__ == '__main__':
    app.run(debug=True)