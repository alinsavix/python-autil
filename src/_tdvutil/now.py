import time


def now() -> int:
    """
    Return the current time (as unix epoch time) as an integer

    :return: An integer seconds-past-the-epoch count
    :rtype: int
    """
    return int(time.time())

def nowf() -> float:
    """
    Return the current time (as unix epoch time) as a float

    :return: A floating point seconds-past-the-epoch count
    :rtype: float
    """
    return float(time.time())
