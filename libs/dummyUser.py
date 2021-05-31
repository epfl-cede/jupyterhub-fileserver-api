class notoUser:
    """
    Mockup class to fake the EPFL notouser library. For a given ID, just returns this ID.
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
        user = {"normalised": id, "uid": id}
        return user
