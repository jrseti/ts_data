import sys
import os
import time
from datetime import datetime
import logging, logging.handlers
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from config import LOG_MESSAGE_FORMAT, LOG_DIRECTORY

class Logger():

    def __init__(self, name):
        self.name = name
        timed_handler = MyTimedRotatingFileHandler(name + ".log", whenTo="MIDNIGHT", intervals=1)
        messageFormatter = logging.Formatter(LOG_MESSAGE_FORMAT)
        timed_handler.setFormatter(messageFormatter)
        self.get_logger().addHandler(timed_handler)

    def get_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(DEBUG)
        return logger

    def info(self, message):
        self.get_logger().log(INFO, message)

    def warn(self, message):
        self.get_logger().log(WARNING, message)

    def error(self, message):
        self.get_logger().log(ERROR, message)

    def debug(self, message):
        self.get_logger().log(DEBUG, message)

    def critical(self, message):      
        self.get_logger().log(CRITICAL, message)

class MyTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """Class to handle log rotation. Based on TimedRotatingFileHandler and 
    modified to create a new directory for each rollover period"""

    def __init__(self, log_title, whenTo="midnight", intervals=1):
        """Constructor
        Arguments:
            log_title {str} -- log file name
            Keyword Arguments:
                whenTo {str} -- when to rotate the log file (default: {"midnight"})
                intervals {int} -- intervals to rotate the log file (default: {1})
        """

        self.when = whenTo.upper()
        self.inter = intervals
        self.log_file_path = os.path.abspath(LOG_DIRECTORY)
        if not os.path.isdir(self.log_file_path):
            os.mkdir(self.log_file_path)
        if self.when == "S":
            self.extStyle = "%Y%m%d%H%M%S"
        if self.when == "M":
            self.extStyle = "%Y%m%d%H%M"
        if self.when == "H":
            self.extStyle = "%Y%m%d%H"
        if self.when == "MIDNIGHT" or self.when == "D":
            self.extStyle = "%Y%m%d"

        self.dir_log = os.path.abspath(os.path.join(self.log_file_path, datetime.now().strftime(self.extStyle)))
        if not os.path.isdir(self.dir_log):
            os.mkdir(self.dir_log)
        self.title = log_title
        filename = os.path.join(self.dir_log, self.title)
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when=whenTo, interval=self.inter, backupCount=0)
        self._header = ""
        self._log = None
        self._counter = 0 
        self._last_rollover_time_item = -1


    def shouldRollover(self, record):
        """Determine if rollover should occur.
            Basically, see if the time of the record shoulf cause a rollover to occur.
            If it does, then call doRollover()
        Arguments:
            record {LogRecord} -- The record to be logged
        Returns:
            1 -- if rollover should occur
            0 -- if rollover should not occur
        """
        global log_server_config

        datetime_of_record = datetime.fromtimestamp(record.created)

        if self.when == "S":
            second_now = datetime_of_record.second
            if second_now != self._last_rollover_time_item:
                self._last_rollover_time_item = second_now
                #print("Forcing rollover")
                return 1
        if self.when == "M":
            minute_now = datetime_of_record.minute
            if minute_now != self._last_rollover_time_item:
                self._last_rollover_time_item = minute_now
                #print("Forcing rollover")
                return 1
        if self.when == "H":
            hour_now = datetime_of_record.hour
            if hour_now != self._last_rollover_time_item:
                self._last_rollover_time_item = hour_now
                #print("Forcing rollover")
                return 1
        if self.when == "MIDNIGHT" or self.when == "D":
            day_now = datetime_of_record.day
            if day_now != self._last_rollover_time_item:
                self._last_rollover_time_item = day_now
                #print("Forcing rollover")
                return 1

        return 0

    def doRollover(self):
        """Roll over the current log file to a new file."""
        print("LOG ROLLOVER")
        self.stream.close()
        # get the time that this sequence started at and make it a TimeTuple
        t = self.rolloverAt - self.interval
        timeTuple = time.localtime(t)

        self.new_dir = os.path.abspath(os.path.join(self.log_file_path, datetime.now().strftime(self.extStyle)))

        if not os.path.isdir(self.new_dir):
            os.mkdir(self.new_dir)
        self.baseFilename = os.path.abspath(os.path.join(self.new_dir, self.title))
        """if self.encoding:
            self.stream = codecs.open(self.baseFilename, "a", self.encoding)
        else:
            self.stream = open(self.baseFilename, "a")"""
        self.stream = open(self.baseFilename, "a")

        self.rolloverAt = self.rolloverAt + self.interval


if __name__ == "__main__":

    logger = Logger("test_logger")
    logger.warn('This is a test message 1')
    logger.error('This is a test message 2')
