class notoUser:
    """
    Mockup class to fake the EPFL notouser library
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
        user = {"normalised": "130", "uid": "130"}
        return user
