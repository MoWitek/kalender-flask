from mylib import User

class Date:
    def __init__(self, year=None, month=None, day=None, json=None, raw=None):
        self.y, self.m, self.d = None, None, None

        if json:
            self.y = json["year"]
            self.m = json["month"]
            self.d = json["day"]

        if year is not None:
            self.y = year

        if month is not None:
            self.m = month

        if day is not None:
            self.d = day

    def raw(self):
        return self.d, self.m, self.y

    def convert_to_day(self):
        return self.d + self.m * 31 + self.y * 365

    def __str__(self):
        return "{0}-{1}-{2}".format(self.y, self.m, self.d)

    def dumps(self):
        return self.__str__()

    @staticmethod
    def loads(string):
        return Date(*[int(x) for x in string.split("-")])

    def __eq__(self, other):
        if other.convert_to_day() == self.convert_to_day():
            return True
        return False

    def __lt__(self, other):
        if other.convert_to_day() > self.convert_to_day():
            return True
        return False


class Kalender:
    def __init__(self):
        self.data = {}
        self.user_map = {}

    def __exist(self, date: Date, time):
        day, month, year = date.raw()

        if None in [date.y, date.m, date.d, time]:
            return False

        if not self.data.get(year):
            self.data[year] = {}

        if not self.data[year].get(month):
            self.data[year][month] = {}

        if not self.data[year][month].get(day):
            self.data[year][month][day] = {}

        if not self.data[year][month][day].get(time):
            self.data[year][month][day][time] = None

    def set(self, date: Date, time, user: User) -> bool:
        day, month, year = date.raw()

        self.__exist(date, time)

        if not self.data[year][month][day][time]:
            if not self.user_map.get(user["username"]):
                self.user_map[user["username"]] = []

            self.data[year][month][day][time] = user
            self.user_map[user["username"]].append(("{0}-{1}-{2}+{3}".format(year, month, day, time)))

            return True
        else:
            return False

    def rem(self, date: Date, time) -> bool:
        day, month, year = date.raw()
        try:
            u = self.data[year][month][day][time]
            del self.data[year][month][day][time]
            del self.user_map[u["username"]][self.user_map[u["username"]].index(("{0}-{1}-{2}+{3}".format(year, month, day, time)))]

            return True
        except:
            return False

    def get(self, date: Date, time) -> User:
        try:
            return self.data.get(date.y).get(date.m).get(date.d).get(time)
        except:
            return None

    def get_user_appointments(self, user):
        if type(user) is User:
            user = user["username"]
        return self.user_map.get(user, [])

    def dump(self, date: Date):
        _, month, year = date.raw()

        if None in [date.y, date.m]:
            return False

        if not self.data.get(year):
            self.data[year] = {}

        if not self.data[year].get(month):
            self.data[year][month] = {}

        return self.data[year][month]
