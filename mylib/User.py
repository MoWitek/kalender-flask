from json import dumps, loads

class User:
    def __init__(self, username, password, email, name, user_permissions, appointments=[]):
        self.info = {
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "user_permissions": user_permissions,
            # 1 normal
            # 2 elevated
            # 3 full access

        }


    def __getitem__(self, item):
        return self.info[item]

    def __repr__(self):
        return f"User \"{self.info['username']}\""

    def __str__(self):
        return self.dumps()

    def get(self, item, default=None):
        return self.info.get(item, default)

    @staticmethod
    def loads(string):
        return User(**loads(string))

    # duno not used
    @staticmethod
    def dejsonify(dictionary):
        return User(**dictionary)

    def dumps(self):
        return dumps(self.info)

    def jsonify(self):
        return self.info



from json import dumps, loads

"""class User_PROTO:
    def __init__(self, username, password, email, name, user_permissions, *args, **kwargs):
        self.info = {
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "user_permissions": user_permissions,
            # 1 normal
            # 2 elevated
            # 3 full access

            "args": [],
            "kwargs": {}
        }

        types = [str, int, dict, list]

        for arg in args:
            if type(arg) in types:
                self.info["args"].append(arg)

        for kwarg in kwargs:
            if type(kwarg) in types:
                self.info["kwargs"][kwarg] = kwargs[kwarg]

    def __getitem__(self, item):
        return self.info[item]

    def __repr__(self):
        return f"User \"{self.info['username']}\""

    def __str__(self):
        return self.dumps()

    def get(self, item, default=None):
        return self.info.get(item, default)

    @staticmethod
    def loads(string):
        return User(**loads(string))

    def dumps(self):
        return dumps(self.info)
"""

