import time


# Convert seconds to HH:MM:SS.SSS format. Sure, this could use strftime
# or datetime.timedelta, but both of those have their own issues when
# you want a consistent format involving milliseconds.
def sec_to_hms(secs: float) -> str:
    """
    Simple conversion from a time in seconds, to hh:mm:ss.sss format

    :param secs: A length of time to convert, in seconds
    :type secs: float

    :return: A string in the format of hh:mm:ss.sss
    :rtype: str
    """
    hours = int(secs // (60 * 60))
    secs %= (60 * 60)

    minutes = int(secs // 60)
    secs %= 60

    ms = int((secs % 1) * 1000)
    secs = int(secs)

    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


# Convert seconds to a compressed string, e.g. 1h15m6s
def sec_to_shortstr(secs: float) -> str:
    """
    Simple conversion from a time in seconds, to a compressd string format

    :param secs: A length of time to convert, in seconds
    :type secs: float

    :return: A string in the format of e.g. 1h15m6s
    :rtype: str
    """
    hours = int(secs // (60 * 60))
    secs %= (60 * 60)

    minutes = int(secs // 60)
    secs %= 60

    secs = int(secs)

    if hours:
        return f"{hours:d}h{minutes:d}m{secs:d}s"
    elif minutes:
        return f"{minutes:d}m{secs:d}s"
    else:
        return f"{secs:d}s"


# A very basic HH:MM:SS.SSS format to seconds conversion. We could
# use strptime here, but really, who in their right mind wants to use
# strptime? This is simple enough and straightforward. Also handles the
# case of just specifying some number of seconds without the HH or MM parts.
def hms_to_sec(hms: str) -> float:
    """
    Simple conversion from a time string (hh:mm:ss.sss) to a float time

    :param hms: A string in the format of hh:mm:ss.sss
    :type hms: str

    :return: A time in seconds
    :rtype: float
    """

    timesplit = hms.split(":")

    if len(timesplit) == 3:
        h, m, s = timesplit
    elif len(timesplit) == 2:
        h = "0"
        m, s = timesplit
    elif len(timesplit) == 1:
        h = "0"
        m = "0"
        s = timesplit[0]
    else:
        raise ValueError(f"too many fields ({len(timesplit)}) in hh:mm:ss string 'hms'")
        sys.exit(1)

    return (int(h) * 60 * 60) + (int(m) * 60) + float(s)


if __name__ == '__main__':
    sec = 18231
    hms = sec_to_hms(sec)
    hms_short = sec_to_shortstr(sec)
    sec = hms_to_sec(hms)

    print(f"{sec}s -> {hms}")
    print(f"{sec}s -> {hms_short}")
    print(f"{hms} -> {sec}s")
