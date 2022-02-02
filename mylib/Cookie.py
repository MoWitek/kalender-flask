from mylib.User import User
from base64 import b64encode, b64decode

class Cookie:
    def __init__(self, user: User):
        self.user = user

    def __bool__(self):
        return bool(self.user.info)

    def __repr__(self):
        return "Cookie: " + self.user.__repr__()

    @staticmethod
    def loads(string):

        return Cookie(User.loads(string))
        # return b64decode(User.loads(string)).decode()

    def saves(self):
        return self.user.dumps()
        # return b64encode(str(self.user).encode()).decode()

