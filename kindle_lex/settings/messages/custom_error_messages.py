class CustomErrorMessages:
    """
    Custom error messages
    """

    class Template(Exception):
        """
        Template for exceptions
        """

        def __init__(self, message):
            super().__init__(message)


if __name__ == "__main__":

    a = 0

    if a == 0:
        raise CustomErrorMessages.Template(message="Error message")
