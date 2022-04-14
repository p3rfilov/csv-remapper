
import sys
import traceback
import functools
from typing import Callable, Any


def exception(func):  # type: (Callable) -> Any
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            from PySide2 import QtCore, QtWidgets
            if QtWidgets.QApplication.instance():  # display dialog if Qt app is running
                exc_type, exc_obj, exc_tb = sys.exc_info()
                msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical, 'Error', f'{exc_type}\n{exc_obj}')
                ok = QtWidgets.QPushButton('Ok')
                msg.addButton(ok, QtWidgets.QMessageBox.YesRole)
                msg.setDetailedText(traceback.format_exc())
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
                msg.setStyleSheet('QLabel{min-width: 250px;}')
                msg.raise_()
                msg.exec_()
            raise e
    return wrapper


if __name__ == '__main__':
    from PySide2 import QtWidgets

    @exception
    def some_func():
        raise Exception('Something bad happened...')


    print(QtWidgets.QApplication.instance())
    app = QtWidgets.QApplication(sys.argv)
    print(QtWidgets.QApplication.instance())
    some_func()
