import datetime
import time

import redis

redis_client = redis.StrictRedis(host="localhost", port=6379)


class RedisClient(object):
    USER_SET_KEYS = ['username', 'ip_addr', 'status']
    USER_GET_KEYS = ['username', 'status']
    USER_AVAILABLE = 'Available'
    USER_PLAYING = 'Playing'
    USER_LOCKED = 'Locked'
    MAX_GAMETIME = datetime.timedelta(seconds=45)

    def __to_dict(self, data):
        translated = {}
        for key, value in data.items():
            translated[self.translate(key)] = self.translate(value)
        return translated

    def __to_list(self, data):
        translated = [self.translate(value) for value in data]
        return translated

    def __to_value(self, data):
        translated = data.decode('utf8')
        if translated.isdigit():
            try:
                translated = int(translated)
            except ValueError:
                translated = float(translated)
        return translated

    def translate(self, data):
        if isinstance(data, dict):
            translated = self.__to_dict(data)
        elif isinstance(data, list):
            translated = self.__to_list(data)
        elif isinstance(data, bytes):
            try:
                translated = self.__to_value(data)
            except Exception as e:
                translated = (data, e)
        else:
            translated = data

        return translated

    def __set_hmfield(self, hm, key, data):
        hm[key] = data.get(key) or hm.get(key)

    def get_user(self, user):
        """
        Retrieve user info from Users collection.

        Return Data:
            * Username
            * IP Address
            * Status
        """
        redis_user = "user:{}".format(user)
        data = redis_client.hmget(redis_user, self.USER_GET_KEYS)
        return self.translate(data)

    def set_user(self, user, data):
        """
        Set or update `user` with `data`.

        Expected Fields:
            * ip_addr
            * status
        """
        redis_user = "user:{}".format(user)
        user_data = self.get_user(user)
        data['username'] = user
        data_status = data['status']
        data['status'] = data_status if data_status else self.USER_AVAILABLE

        for key in self.USER_SET_KEYS:
            self.__set_hmfield(user_data, key, data)

        redis_client.hmset(redis_user, user_data)

    def get_all_users(self):
        users_keys = redis_client.keys(pattern="user:*")
        users = []
        for user in users_keys:
            users.append(
                dict(zip(
                    self.USER_GET_KEYS,
                    self.translate(
                        redis_client.hmget(redis_user, self.USER_GET_KEYS))
                ))
            )
        return users

    def is_user_available(self, username, lock_user=False):
        user = redis_client.hmget('user:{}'.format(username))
        is_available = user and user['status'] == self.USER_AVAILABLE
        if is_available and lock_user:
            user['status'] = self.USER_LOCKED
        return is_available

    def release_lock(self, users):
        for user in users:
            user_status = self.get_user(user)['status']
            if user_status == self.USER_LOCKED:
                self.set_user(user, {'status': self.USER_AVAILABLE})

    def is_valid_user_request(self, username, ip_addr):
        user = redis_client.hmget('user:{}'.format(username))
        return user['ip_addr'] == ip_addr

    def create_match(self, user1, user2):
        now = time.mktime(datetime.datetime.utcnow().timetuple()) * 1000
        match_id = 'match:{}'.format(now)
        expire_at = time.mktime(now + self.MAX_GAMETIME)

        self.set_user(user1, {'status': self.USER_PLAYING})
        self.set_user(user2, {'status': self.USER_PLAYING})

        redis_client.hmset(match_id, {
            'user1': user1, 'user2': user2,
            'created': now, 'expire': expire_at,
            'status': 'created'
        })
        return match_id, now, expire_at
