# Standard
from enum import Enum

# Pip
# None

# Standard
# None


class MessageKeys:
    """
    Here the names and messages, which are output by the program,
    are stored centrally.
    """

    class General(Enum):
        INCORRECT_DIRECTORY = "The home directory was not correctly specified."
