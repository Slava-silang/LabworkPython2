class StreamStatsError(Exception):
    """Main exception class"""
    pass

class StreamStatsParseError(StreamStatsError):
    """Exception class for parsing errors"""
    pass

class StreamStatsTimestampError(StreamStatsError):
    """Exception class for timestamp errors"""
    pass

class UnsupportedTypeOfFileError(StreamStatsError):
    """Exception class for unsupported file type"""
    pass
