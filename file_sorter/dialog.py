from PySide2 import QtWidgets
from PySide2 import QtGui
from file_sorter import Logger
from file_sorter import Config
from file_sorter.dir_manager import DirManager


class LoggerWindow(QtWidgets.QDialog):

    UI_INSTANCE = None

    @classmethod
    def display(cls, show=True):
        if not cls.UI_INSTANCE:
            cls.UI_INSTANCE = LoggerWindow()
            if show:
                cls.UI_INSTANCE.show()
        elif cls.UI_INSTANCE.isHidden():
            cls.UI_INSTANCE.show()
        else:
            cls.UI_INSTANCE.raise_()
            cls.UI_INSTANCE.activateWindow()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.config = Config("config.ini")
        # Dialog properties
        self.setModal(1)
        self.setMinimumSize(500, 200)
        self.setWindowTitle("File sorter log")
        self.setWindowIcon(QtGui.QIcon("./res/images/log.png"))

        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # Init manager
        self.manager = DirManager(path=self.config.parser.get("General", "dir"),
                                  folders_dict=self.config.get_folders(),
                                  sort_existing=self.config.parser.getboolean("General", "sort_existing", fallback=True),
                                  update_interval=self.config.parser.getint("General", "update_interval", fallback=10))

    def create_actions(self):
        pass

    def create_widgets(self):
        self.text_wgt = QtWidgets.QTextEdit()
        font = QtGui.QFont("Helvetica")
        font.setBold(True)
        self.text_wgt.setFont(font)
        self.text_wgt.setReadOnly(True)

    def create_layouts(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.text_wgt)
        self.setLayout(self.main_layout)

    def create_connections(self):
        Logger._signal_handler.emitter.message_logged.connect(self.text_wgt.append)

    def set_manager(self, manager):
        self.manager = manager

    def closeEvent(self, event):
        event.ignore()
        self.hide()
