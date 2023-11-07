import logging

class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # Create handlers
        stream_hanlder = logging.StreamHandler()
        stream_hanlder.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(asctime)s [%(module)s:%(funcName)s] %(levelname)s - %(message)s')
        stream_hanlder.setFormatter(c_format)

        # Add handlers to the logger
        self.logger.addHandler(stream_hanlder)
