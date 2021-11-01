class Auth:
    def __init__(self, ConfigAuth):
        self.ConfigAuth = ConfigAuth

    def CheckUser(self, user):
        """
        Return true if user exist and the key
        :param user: userid
        :return: T/F True if user exist, and the key if user exist
        """
        userexist = False
        for userlist in self.ConfigAuth:
            if userlist["user"] == user:
                userexist = True
                break
        return userexist

    def UserKey(self, user):
        """
        return the key for a given user
        :param user: userid
        :return: userkey
        """
        key = self._FindKey(user)
        return key

    def _FindKey(self, user):
        """
        Return true if user exist and the key
        :param user: userid
        :return: T/F True if user exist, and the key if user exist
        """
        key = None
        for userlist in self.ConfigAuth:
            if userlist["user"] == user:
                key = userlist["key"]
                break
        return key
