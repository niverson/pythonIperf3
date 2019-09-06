import unittest
import logging
from scriptBaseClass import ScriptBase


class TestScriptBase(unittest.TestCase):
    """unit test class for scriptBaseClass"""
    def test_command_line_to_logging_level_options(self):
        """test the conversion from command line definition to logging definition."""
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, 0), logging.NOTSET)
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, 1), logging.DEBUG)
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, 2), logging.INFO)
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, 3), logging.WARNING)
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, 4), logging.ERROR)
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, 5), logging.CRITICAL)

        # should return the defaulted value.
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, -1), logging.INFO)
        self.assertEqual(ScriptBase.command_line_to_logging_level_options(ScriptBase, 6), logging.INFO)

        self.assertRaises(TypeError, ScriptBase.command_line_to_logging_level_options, (ScriptBase,'string'))

if __name__ == '__main__':
    unittest.main()
