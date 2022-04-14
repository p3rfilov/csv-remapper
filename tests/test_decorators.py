
import sys
import unittest

from csv_remapper.components import decorators


class TestDecorators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = 'Something bad happened...'

    def test_exception_decorator(self):
        @decorators.exception
        def raising_func():
            raise Exception(self.text)

        self.assertRaisesRegex(Exception, self.text, raising_func)

    def _test_gui_exception_decorator(self):
        from PySide2 import QtWidgets
        QtWidgets.QApplication(sys.argv)

        @decorators.exception
        def raising_func():
            raise Exception('Something bad happened...')

        self.assertRaisesRegex(Exception, self.text, raising_func)


if __name__ == '__main__':
    unittest.main()

