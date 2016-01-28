from flask_restful import Resource
from flask import request

from ..state import RedisClient

redis_api = RedisClient()


# def get_payload(req):
# try:
#     payload = request.get_json()
# except Exception as e:
#     return False, {"error": "Payload expected", "status": 400}, 400

# payload = request.get_json()
# return payload, 200


class UsersList(Resource):

    def get(self):
        return redis_api.get_all_users()


class UserConnect(Resource):

    """
    Start a match between self and opponent.

    Expected Payload: 
        {
            'username': ___,
            'opponent': ___
        }
    """

    def post(self):
        """
            * Check if `username` matches the ip_addr in system.
            * Check if `opponent` is available for match.
            * Create a match with game id & two users.
            * Send status and game id in Response.
        """
        payload = request.get_json()

        ip_addr = request.environ.get('X-Forwarded-For', request.remote_addr)

        if not redis_api.is_valid_user_request(payload['username'], ip_addr):
            return 'User does not validate.', 403

        user1 = payload['username']
        user2 = payload['opponent']
        is_user1_available = redis_api.is_user_available(user1, lock_user=True)
        is_user2_available = redis_api.is_user_available(user2, lock_user=True)
        if is_user1_available and is_user2_available:
            game = redis_api.create_game(user1, user2)
            game_id = game[1]
            status = 201
        else:
            redis_api.release_lock(users=[user1, user2])
            game_id = 'Unable to create the match'
            status = 409

        return game_id, status


class UserLogin(Resource):

    def post(self):
        payload = request.get_json()
        user = payload['username']

        if not all(redis_api.get_user(user)):
            return 'User already logged in.', 409

        ip_addr = request.environ.get('X-Forwarded-For', request.remote_addr)
        redis_api.set_user(user, {'ip_addr': ip_addr})

        return "User logged in.", 201

resources = (
    (UsersList, '/users'),
    (UserConnect, '/connect'),
    (UserLogin, '/login')

)
