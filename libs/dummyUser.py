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
        :param id: User identification from IAM, user@ethz.ch. Empty for external users
        :param email: full mail address, i.e. hans.muster@org.ethz.ch, or hmuster@ethz.ch for students
        """
        email = email.replace(".", "-2e")
        email = email.replace("_", "-5f")
        email = email.replace("@", "-40")
        user = {"normalised": email, "uemail": email}
        return user
