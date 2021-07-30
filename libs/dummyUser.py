class notoUser:
    """
    Mockup class to fake the EPFL notouser library. For a given ID, just returns this ID, after doing some
    sanitizing (hex encoding of special characters in mail address).
    """

    def __init__(self):
        # used for path building
        self.normalised = ""
        # used for logging only
        self.uid = ""

    def userFromAPI(self, id, email):
        """
        :param id: THE id, user identification from IAM
        :param email: 2nd argument for validation?
        """
        id = id.replace(".", "-2e")
        id = id.replace("@", "-40")
        user = {"normalised": id, "uid": id}
        return user
