import app
import state
import unittest
import json

redis_collective_data = {
    'user:test-1': {
        'status': state.RedisClient.USER_AVAILABLE,
        'ip_addr': 'test.1.ip.addr',
        'username': 'test-1'
    },
    'user:test-2': {
        'status': state.RedisClient.USER_AVAILABLE,
        'ip_addr': 'test.2.ip.addr',
        'username': 'test-2'
    },
    'user:test-3': {
        'status': state.RedisClient.USER_LOCKED,
        'ip_addr': 'test.3.ip.addr',
        'username': 'test-3'
    },
    'user:test-4': {
        'status': state.RedisClient.USER_AVAILABLE,
        'ip_addr': 'test.4.ip.addr',
        'username': 'test-4'
    },
    'user:test-5': {
        'status': state.RedisClient.USER_AVAILABLE,
        'ip_addr': 'test.5.ip.addr',
        'username': 'test-5'
    },
    'user:test-6': {
        'status': state.RedisClient.USER_AVAILABLE,
        'ip_addr': 'test.6.ip.addr',
        'username': 'test-6'
    },
    'user:test-7': {
        'status': state.RedisClient.USER_AVAILABLE,
        'ip_addr': 'test.7.ip.addr',
        'username': 'test-7'
    },
}


class TestSetBase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def setup_redis(self, data):
        for key, value in data.items():
            state.RedisClient.redis_client.hmset(key, value)

    def tearDown(self):
        test_keys = state.RedisClient.redis_client.keys(pattern='user:test*')
        for key in test_keys:
            state.RedisClient.redis_client.delete(key)

    def post_payload_response(self, payload, redis_data={}, url=None):
        self.setup_redis(redis_data)
        response = self.app.post(
            url or self.URL,
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )
        return response

    def get_redis_data(self, *ids):
        redis_data = {}
        for id in ids:
            key = 'user:test-{}'.format(id)
            redis_data[key] = redis_collective_data[key]
        return redis_data


class TestSetBasic(TestSetBase):

    def test_default_404(self):
        "'/' returns 404"
        response = self.app.get('/')
        self.assertEqual(response.status_code, 404)


class TestSetUsersList(TestSetBase):

    def test_get_list(self):
        "/users :: GET should return list of users."
        redis_data = self.get_redis_data(1, 2)
        self.setup_redis(redis_data)

        response = self.app.get('/users?test=true')
        self.assertEqual(response.status_code, 200)
        data = response.get_data().decode('utf8')
        data = json.loads(data)
        self.assertEqual(len(redis_data), len(data))
        for dct in data:
            usr = dct.get('username')
            rd = redis_data.get('user:{}'.format(usr))
            self.assertTrue(rd)
            self.assertEqual(rd.get('status'), dct['status'])

    def test_post_list(self):
        "/users :: POST should return 405"
        response = self.app.post('/users')
        self.assertEqual(response.status_code, 405)

    def test_resource_list(self):
        "/users/x :: GET should return 404"
        response = self.app.post('/users/test-1')
        self.assertEqual(response.status_code, 404)


class TestSetUserConnect(TestSetBase):
    URL = '/connect'

    def test_get(self):
        "/connect :: GET should return 405"
        response = self.app.get('/connect')
        self.assertEqual(response.status_code, 405)

    @unittest.skip("X-Forwarded-For to be tested with nginx?")
    def test_post_xfwd_ip_addr(self):
        "Check server handles 'X-Forwarded-For'"
        self.assertTrue(False)

    def test_post_invalid_payload(self):
        "Server should handle invalid payload"
        response = self.post_payload_response({'asdf': 1})
        self.assertEqual(response.status_code, 400)

    def test_post_user_does_not_exist(self):
        "If a user does not exist, 409 should be thrown."
        payload = {'username': 1, 'opponent': 2}
        response = self.post_payload_response(payload)
        self.assertEqual(response.status_code, 400)

    def test_post_user_is_unavailable(self):
        "If a user is unavailable, 409 should be thrown."
        redis_data = self.get_redis_data(3, 4)
        payload = {'username': "test-3", 'opponent': "test-4"}
        response = self.post_payload_response(payload, redis_data)
        self.assertEqual(response.status_code, 409)

    def test_post_create_match(self):
        "If both users are available, 201 should be returned."
        redis_data = self.get_redis_data(5, 6)
        payload = {'username': "test-5", 'opponent': "test-6"}
        response = self.post_payload_response(payload, redis_data)
        self.assertEqual(response.status_code, 201)

    def test_post_match_fail_common_player(self):
        ("If two requests are received with a common user,"
         " ensure that only one match is created.")
        redis_data = self.get_redis_data(5, 6, 7)

        payload = {'username': "test-5", 'opponent': "test-6"}
        response = self.post_payload_response(payload, redis_data)
        self.assertEqual(response.status_code, 201)

        payload = {'username': "test-5", 'opponent': "test-7"}
        response = self.post_payload_response(payload)
        self.assertEqual(response.status_code, 409)


class TestSetState(TestSetBase):
    URL = '/connect'

    def test_match_user_pairing(self):
        "If a match is created, ensure it is between correct users"
        redis_data = self.get_redis_data(5, 6)
        payload = {'username': "test-5", 'opponent': "test-6"}
        response = self.post_payload_response(payload, redis_data)
        self.assertEqual(response.status_code, 201)

        match_id = json.loads(response.get_data().decode('utf8'))['game_id']
        r1 = state.RedisClient.redis_client

        match_data = r1.hgetall('match:{}'.format(match_id))
        self.assertEqual(
            bytes(payload['username'], 'utf8'),
            match_data[b'user1']
        )
        self.assertEqual(
            bytes(payload['opponent'], 'utf8'),
            match_data[b'user2']
        )
        self.assertEqual(b'created', match_data[b'status'])

    def test_match_users_status(self):
        "If a match is created, ensure their statuses are set to 'Playing'"
        redis_data = self.get_redis_data(5, 6)
        payload = {'username': "test-5", 'opponent': "test-6"}
        response = self.post_payload_response(payload, redis_data)
        self.assertEqual(response.status_code, 201)

        response = self.app.get('/users?test=true')
        data = json.loads(response.get_data().decode('utf8'))
        user1, user2 = None, None
        for dct in data:
            if dct['username'] == payload['username']:
                user1 = dct
            elif dct['username'] == payload['opponent']:
                user2 = dct

        self.assertTrue(user1 and user2)
        self.assertEqual(user1['status'], state.RedisClient.USER_PLAYING)
        self.assertEqual(user2['status'], state.RedisClient.USER_PLAYING)


class TestSetUserLogin(TestSetBase):
    URL = '/login'

    def test_login_new(self):
        "A new username should be able to log in"
        response = self.post_payload_response({'username': 'test-new'})
        data = response.get_data().decode('utf8').strip()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, '"User succesfully logged in."')

    def test_login_duplicate(self):
        "Duplicated username should fail."
        response = self.post_payload_response({'username': 'test-new'})
        self.assertEqual(response.status_code, 201)

        response = self.post_payload_response({'username': 'test-new'})
        self.assertEqual(response.status_code, 409)


if __name__ == '__main__':
    unittest.main()
