import logging

FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'
BASE_PATH = 'logs/'
RECORD = '{function} | {arguments}'
ERROR = '{function} | {arguments} | {reason}'

class APILogger():
    """Logger for API
        
    Logs which endpoints are called by which user and the arguments provided
    Logs additional high-level information of whether the database action is successful
    """

    def __init__(self, name, record_type):
        formatter = logging.Formatter(FORMAT)
        file_handler = logging.FileHandler(filename=BASE_PATH + 'api.log')
        file_handler.setFormatter(formatter)
        
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        logger.propagate = False # Turn off logging to console

        self.logger = logger
        self.record_type = record_type

    def record(self, function, arguments):

        self.logger.info(RECORD.format(function=function, arguments=arguments))

    def error(self, function, arguments,reason):

        self.logger.error(ERROR.format(function=function, arguments=arguments,reason=reason))
  
    def warning(self, function, arguments):
        self.logger.warning(RECORD.format(function=function, arguments=arguments))