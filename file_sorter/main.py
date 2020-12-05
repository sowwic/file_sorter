import sys
from PySide2 import QtWidgets
from PySide2 import QtGui


from file_sorter import Logger
from file_sorter import Config
from file_sorter.dialog import LoggerWindow
from file_sorter import palette
from file_sorter import tray


if __name__ == "__main__":
    # Load config
    config = Config("config.ini")
    Logger.set_level(config.parser.getint("DEFAULT", "logging_lvl", fallback=20))
    if config.parser.getboolean("General", "file_log", fallback=True):
        Logger.write_to_rotating_file("file_sorter.log")

    # Create Qt application
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))
    app.setPalette(palette.dark_fusion())

    # Create logger dialog
    LoggerWindow.display(show=0)

    # Create tray
    tray_widget = QtWidgets.QWidget()
    tray_icon = tray.TrayIcon(QtGui.QIcon("./res/images/icon.ico"), tray_widget)
    tray_icon.open_logger_action.triggered.connect(LoggerWindow.display)
    tray_icon.show()

    sys.exit(app.exec_())
