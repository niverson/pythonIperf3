import argparse
import logging
import datetime

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

    def __str__(self):
        return f"{self.utcNow} {self.logfileName}"

    def __repr__(self):
        return f"{self.utcNow} {self.logfileName}"

    def commandLineToLoggingLevelOptions(self, cmdLineLevel):
        """convert command line logging level declarations to logging class definitions"""
        level = None
        if cmdLineLevel == 0:
            level = logging.NOTSET      # value is 0
        elif cmdLineLevel == 1:
            level = logging.DEBUG       # value is 10
        elif cmdLineLevel == 2:
            level = logging.INFO        # value is 20
        elif cmdLineLevel == 3:
            level = logging.WARNING     # value is 30
        elif cmdLineLevel == 4:
            level = logging.ERROR       # value is 40
        elif cmdLineLevel == 5:
            level = logging.CRITICAL    # value is 50
        else:
            level = logging.INFO        # set INFO as default

        return level

    def setLogging(self,slvl,flvl):
        """set up logging for the script. use the user defined logging level from command
        line to set the level in the stream and file handlers"""
        screenLoggingLevel = self.commandLineToLoggingLevelOptions(slvl)
        self.ch.setLevel(screenLoggingLevel)

        fileLoggingLevel = self.commandLineToLoggingLevelOptions(flvl)
        self.ch.setLevel(fileLoggingLevel)

        # add script instance formatter to handlers
        self.ch.setFormatter(self.formatter)
        self.fh.setFormatter(self.formatter)

        self.scriptBaseLogger = logging.getLogger()
        self.scriptBaseLogger.setLevel(logging.DEBUG)
        self.scriptBaseLogger.addHandler(self.ch)
        self.scriptBaseLogger.addHandler(self.fh)
        self.scriptBaseLogger.critical("logs saved at: %s" % self.logfileName)




