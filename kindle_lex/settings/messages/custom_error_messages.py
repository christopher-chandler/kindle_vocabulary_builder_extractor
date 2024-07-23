class CustomErrorMessages:
    """
    Custom error messages
    """

    class MultiLingualSpacyError(Exception):
        """
        Exception raised for unsupported languages in Spacy.
        """

        def __init__(self, message):
            self.language = message

            super().__init__(message)
