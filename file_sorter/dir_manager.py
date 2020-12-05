import pathlib
import shutil
from PySide2 import QtCore
from file_sorter import Logger


class DirManager(QtCore.QObject):
    def __repr__(self) -> str:
        return "Managing dir: {0}; Files: {1}".format(self.path, self.EXTENSIONS)

    def __init__(self, path: pathlib.Path, update_interval=10, sort_existing=True, folders_dict: dict = {}, parent=None):
        super().__init__(parent)
        self.FOLDERS = folders_dict
        self.EXTENSIONS = [item for ext_list in list(self.FOLDERS.values()) for item in ext_list]

        self.path = pathlib.Path(path)
        self.update_interval = update_interval * 1000
        self.previous = []
        Logger.info(self)

        if sort_existing:
            self.previous = [f for f in self.path.iterdir() if f.is_file()]

        # Setup timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.check_files)
        self.timer.start(self.update_interval)

    def check_files(self):
        current = [f for f in self.path.iterdir() if f.is_file()]
        new_files = [f for f in current if f not in self.previous]
        for each in new_files:
            self.handle_new_file(each)
        self.previous = current

    def handle_new_file(self, file_path: pathlib.Path):
        Logger.info("New file: {0}".format(file_path.as_posix()))
        if file_path.suffix not in self.EXTENSIONS:
            Logger.info("{} files are not managed, skipping...".format(file_path.suffix))
            return

        for folder_name, extensions in self.FOLDERS.items():
            if file_path.suffix in extensions:
                sub_dir = self.path / folder_name
                if not sub_dir.is_dir():
                    pathlib.Path.mkdir(sub_dir)
                shutil.move(file_path, sub_dir / file_path.name)
                Logger.info("Moved {0} --> {1}".format(file_path.name, sub_dir.name))
