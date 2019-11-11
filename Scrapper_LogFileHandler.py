import logging
import random
import os


class LogFileHandler( logging.FileHandler ):
    """
    Add process id to file name.

    ex: wikipedia.log -> wikipedia-12345.log
    """
    def __init__( self, fileName, mode="w" ):
        filename, file_extension = os.path.splitext( fileName )
        pid = os.getpid()
        process_file_name = f"{filename}-{pid}{file_extension}"
        super().__init__( process_file_name, mode )

