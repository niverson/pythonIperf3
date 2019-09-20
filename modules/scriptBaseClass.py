import argparse
import logging
import datetime

class ScriptBase( ):
    """This is a class to contain all the common script setup and define common script arguments"""

    def __init__(self, log_file_prefix):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-slvl', type=int, default=2, choices=range(0, 6))
        self.parser.add_argument('-flvl', type=int, default=2, choices=range(0, 6))

        self.formatter = logging.Formatter('%(asctime)s - %(name)25s - %(levelname)8s - %(message)s')
        self.ch = logging.StreamHandler()

        self.utcNow = datetime.datetime.utcnow()
        self.log_file_directory = '/tmp'
        self.log_file_name = ('%s/%s_' % (self.log_file_directory,log_file_prefix) +
                            self.utcNow.strftime('%Y_%m_%d__%H_%M_%S' + '.log') )
        self.fh = logging.FileHandler(self.log_file_name)
        self.script_base_logger = None

    def __str__(self):
        return f"{self.utcNow} {self.log_file_name}"

    def __repr__(self):
        return f"{self.utcNow} {self.log_file_name}"

    def command_line_to_logging_level_options(self, cmd_line_level):
        """convert command line logging level declarations to logging class definitions. Valid inputs are 0 through 5
        All other inputs are invalid and should return the defaulted logging level of INFO."""
        level = None

        if type(cmd_line_level) not in [int]:
            raise TypeError( 'cmd_line_level must be a non-negative real number from 0 to 5' )

        if cmd_line_level == 0:
            level = logging.NOTSET      # value is 0
        elif cmd_line_level == 1:
            level = logging.DEBUG       # value is 10
        elif cmd_line_level == 2:
            level = logging.INFO        # value is 20
        elif cmd_line_level == 3:
            level = logging.WARNING     # value is 30
        elif cmd_line_level == 4:
            level = logging.ERROR       # value is 40
        elif cmd_line_level == 5:
            level = logging.CRITICAL    # value is 50
        else:
            level = logging.INFO        # set INFO as default

        return level

    def set_logging(self, slvl, flvl):
        """set up logging for the script. use the user defined logging level from command
        line to set the level in the stream and file handlers"""
        screen_logging_level = self.command_line_to_logging_level_options(slvl)
        self.ch.setLevel(screen_logging_level)

        file_logging_level = self.command_line_to_logging_level_options(flvl)
        self.ch.setLevel(file_logging_level)

        # add script instance formatter to handlers
        self.ch.setFormatter(self.formatter)
        self.fh.setFormatter(self.formatter)

        self.script_base_logger = logging.getLogger()
        self.script_base_logger.setLevel(logging.DEBUG)
        self.script_base_logger.addHandler(self.ch)
        self.script_base_logger.addHandler(self.fh)
        self.script_base_logger.critical("logs saved at: %s" % self.log_file_name)




