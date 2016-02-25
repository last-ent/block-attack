from flask_restful import Resource
from flask import request

from state import RedisClient

redis_api = RedisClient()


class UsersList(Resource):

    def get(self):
        return redis_api.get_all_users(request.args.get('test') == 'true')


class UserConnect(Resource):

    """
    Start a match between self and opponent.

    Expected Payload: 
        {
            'username': ___,
            'opponent': ___
        }
    """

    def validate_payload(self, payload):
        username = payload.get('username')
        opponent = payload.get('opponent')
        return username, opponent

    def post(self):
        """
            * Check if `username` matches the ip_addr in system.
            * Check if `opponent` is available for match.
            * Create a match with game id & two users.
            * Send status and game id in Response.
        """
        payload = request.get_json()
        user1, user2 = self.validate_payload(payload)

        if not (user1 and user2):
            return "Error with payload", 400
        elif not (
            redis_api.redis_client.exists("user:{}".format(user1)) and
            redis_api.redis_client.exists("user:{}".format(user2))
        ):
            return "Both users are not valid.", 400

        ip_addr = request.environ.get('X-Forwarded-For', request.remote_addr)

        # FIXME: Might need to remove this one.
        # Do we really want to handle ip_addr stuff?
        if not redis_api.is_valid_user_request(user1, ip_addr):
            return 'User does not validate.', 400

        is_user1_available = redis_api.is_user_available(user1, lock_user=True)
        is_user2_available = redis_api.is_user_available(user2, lock_user=True)
        if is_user1_available and is_user2_available:
            game = redis_api.create_match(user1, user2)
            response = {'game_id': game[1]}
            status = 201
        else:
            redis_api.release_lock(users=[user1, user2])
            response = {'error': 'Unable to create the match'}
            status = 409

        return response, status


class UserLogin(Resource):

    def post(self):
        payload = request.get_json()
        user = payload['username']

        if redis_api.does_user_exist(user):
            return 'User already logged in.', 409

        ip_addr = request.environ.get('X-Forwarded-For', request.remote_addr)
        redis_api.set_user(user, {'ip_addr': ip_addr})

        return "User succesfully logged in.", 201

resources = (
    (UsersList, '/users'),
    (UserConnect, '/connect'),
    (UserLogin, '/login')

)
