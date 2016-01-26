from flask_restful import Resource
from flask import request


def get_payload(req):
    try:
        payload = request.get_json()
    except Exception as e:
        return False, {"error": "Payload expected", "status": 400}, 400

    return True, payload, 200


class UsersList(Resource):

    def get(self):
        return [{'username': i, 'status': 'available'} for i in range(10)]


class UserConnect(Resource):

    def post(self):
        is_payload, payload, status = get_payload(request)
        return payload, status


class UserLogin(Resource):

    def post(self):
        is_payload, payload, status = get_payload(request)

        return payload

resources = (
    (UsersList, '/users'),
    (UserConnect, '/connect'),
    (UserLogin, '/login')

)
