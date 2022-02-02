from mylib.User import User

class LoginDataBase:
    def __init__(self):
        self.userdata = {}

    def __contains__(self, item):
        if type(item) is User:
            return item["username"] in self.userdata
        return item in self.userdata

    def __getitem__(self, item):
        return self.get(item)

    def get(self, user):
        if type(user) is User:
            user = user.username

        if user in self.userdata:
            return self.userdata[user]

    def add(self, user):
        if type(user) is not User:
            raise TypeError

        if user.info.get("username") in self.userdata:
            raise OverflowError

        self.userdata[user.info.get("username")] = user
        return True

    def rem(self, user):
        if type(user) is User:
            user = user.username
        del self.userdata[user]

    def saves(self):
        raise NotImplementedError

    def loads(self):
        raise NotImplementedError
    