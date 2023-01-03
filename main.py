#-*- coding:utf-8 -*-

import sys
import time
import Collector as Collector
from Logger import set_logger, handle_exception


if __name__ == "__main__":
    logger = set_logger()
    sys.excepthook = handle_exception
    # DEBUG = 9999
    data = sys.argv[1]
    # DEBUG = 29
    zCode = sys.argv[2]
    # DEBUG = root:0706@localhost/test01
    db = sys.argv[3]
    # DEBUG = 15
    timeSec = int(sys.argv[4])

    # main
    while True:
        Collector.Colec(data, zCode, db)
        time.sleep(timeSec)


