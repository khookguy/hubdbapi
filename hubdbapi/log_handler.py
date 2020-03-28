import logging
from logging.handlers import TimedRotatingFileHandler

handler = TimedRotatingFileHandler("hubdbapi.log", when="W0", backupCount=52)
handler.setLevel(logging.DEBUG)
handler.suffix = "%Y%m%d"
formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s",
                              datefmt='%d-%b-%y %H:%M:%S')
handler.setFormatter(formatter)
