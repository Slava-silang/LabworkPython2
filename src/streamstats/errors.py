class StreamStatsError(Exception):
    pass

class StreamStatsParseError(StreamStatsError):
    pass

class StreamStatsTimestampError(StreamStatsError):
    pass

class UnsupportedTypeOfFileError(StreamStatsError):
    pass
