class StreamStatsError(Exception):
    """Main exception class"""

class StreamStatsParseError(StreamStatsError):
    """Exception class for parsing errors"""

class StreamStatsTimestampError(StreamStatsError):
    """Exception class for timestamp errors"""

class UnsupportedTypeOfFileError(StreamStatsError):
    """Exception class for unsupported file type"""
