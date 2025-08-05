import logging

class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG

class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR
