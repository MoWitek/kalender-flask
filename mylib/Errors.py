class Error:
    @staticmethod
    def __str(err):
        if err == 403:
            return "You are not Permited to see this page."

        if err == 404:
            return "This Page does not Exist."

        return None

    def __call__(self, err_id):
        return self.__str(err_id)

