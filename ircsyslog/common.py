from enum   import IntEnum
from typing import Dict

class LogFacility(IntEnum):
    KERNEL   = 0
    USER     = 1
    MAIL     = 2
    SYSTEM   = 3
    SECURITY = 4
    INTERAL  = 5
    LINE     = 6
    NETWORK  = 7
    UUCP     = 8
    CLOCK    = 9
    SECAUTH  = 10
    FTP      = 11
    NTP      = 12
    AUDIT    = 13
    ALERT    = 14

class LogSeverity(IntEnum):
    EMERGENCY = 0
    ALERT     = 1
    CRITICAL  = 2
    ERROR     = 3
    WARNING   = 4
    NOTICE    = 5
    INFO      = 6
    DEBUG     = 7


def severity_str(s: LogSeverity):
    if s == LogSeverity.EMERGENCY:
        out = "04EMERGENCY"
    elif s == LogSeverity.ALERT:
        out = "04ALERT"
    elif s == LogSeverity.CRITICAL:
        out = "04CRITICAL"
    elif s == LogSeverity.ERROR:
        out = "04ERROR"
    elif s == LogSeverity.WARNING:
        out = "08WARNING"
    elif s == LogSeverity.NOTICE:
        out = "11NOTICE"
    elif s == LogSeverity.INFO:
        out = "11INFO"
    elif s == LogSeverity.DEBUG:
        out = "03INFO"
    else:
        out = "08UNKNOWN"
    return f"\x02\x03{out}\x03\x02"

def format_string(string: str, formats: Dict[str, str]):

    # sort keys by length backwards
    fkeys   = sorted(formats.keys(), key=len, reverse=True)

    # expand formats
    for i in range(10):
        changed = False
        for key in fkeys:
            fkey = f"${key}"
            if fkey in string:
                changed = True
                string = string.replace(fkey, formats[key])
        if not changed:
            # don't keep going if nothing changes
            break
    return string.rstrip()
