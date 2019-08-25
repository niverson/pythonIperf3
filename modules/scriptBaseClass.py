import argparse
import logging
import datetime


class threadPoolListObj():
    pass

class scriptBase( ):
    def __init__(self, logFilePrefix):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-slvl', type=int, choices=range(0, 6))
        self.parser.add_argument('-flvl', type=int, choices=range(0, 6))

        self.formatter = logging.Formatter('%(asctime)s - %(name)25s - %(levelname)8s - %(message)s')
        self.ch = logging.StreamHandler()

        self.utcNow = datetime.datetime.utcnow()
        self.logfileDirectory = '/tmp'
        self.logfileName = ('%s/%s_' % (self.logfileDirectory,logFilePrefix) +
                            self.utcNow.strftime('%Y_%m_%d__%H_%M_%S' + '.log') )
        self.fh = logging.FileHandler(self.logfileName)
        self.scriptBaseLogger = None



    def setLogging(self,slvl,flvl):
        if slvl:
            self.ch.setLevel(slvl * 10)
        else:
            self.ch.setLevel(logging.INFO)

        if flvl:
            self.fh.setLevel(flvl * 10)
        else:
            self.fh.setLevel(logging.INFO)

        # add formatter to handlers
        self.ch.setFormatter(self.formatter)
        self.fh.setFormatter(self.formatter)

        self.scriptBaseLogger = logging.getLogger()
        self.scriptBaseLogger.setLevel(logging.DEBUG)
        self.scriptBaseLogger.addHandler(self.ch)
        self.scriptBaseLogger.addHandler(self.fh)
        self.scriptBaseLogger.critical("logs saved at: %s" % self.logfileName)




