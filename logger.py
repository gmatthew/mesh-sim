import logging

class Logger:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

        # Create handlers
        stream_hanlder = logging.StreamHandler()
        stream_hanlder.setLevel(logging.INFO)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(asctime)s [%(module)s:%(funcName)s:%(lineno)d] %(levelname)s | %(message)s')
        stream_hanlder.setFormatter(c_format)

        # Add handlers to the logger
        self.log.addHandler(stream_hanlder)
