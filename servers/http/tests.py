import app

import unittest


class TestSetBase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_default_404(self):
        "'/' returns 404"
        assert False

class TestSetUsersList(TestSetBase):
    def test_get_list(self):
        "/users :: GET should return list of users."
        assert False

    def test_post_list(self):
        "/users :: POST should return 405"
        assert False

    def test_resource_list(self):
        "/users/x :: GET should...?"
        assert False

class TestSetUserConnect(TestSetBase):
    def test_get(self):
        "/connect :: GET should return 405"
        assert False

    def test_post_no_xfwd_ip_addr(self):
        "Check server doesn't crash when 'X-Forwarded-For' is not set in request"
        assert False

    def test_post_invalid_payload(self):
        "Server should handle invalid payload"
        assert False

    def test_post_user_does_not_exist(self):
        "If a user does not exist, 409 should be thrown."
        assert False

    def test_post_user_is_unavailable(self):
        "If a user is unavailable, 409 should be thrown."
        assert False

    def test_post_create_match(self):
        "If both users are available, 201 should be returned."
        assert False


class TestSetState(TestSetBase):
    def test_match_user_pairing(self):
        "If a match is created, ensure it is between correct users"
        assert False

    def test_match_users_status(self):
        "If a match is created, ensure their statuses are set to 'Playing'"
        assert False



if __name__ == '__main__':
    unittest.main()
