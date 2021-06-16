import pathlib
import shutil
from PySide2 import QtCore
from file_sorter import Logger


class DirManager(QtCore.QObject):
    def __repr__(self) -> str:
        return "Managing dir: {0}; Files: {1}".format(self.path, self.EXTENSIONS)

    def __init__(self, path: pathlib.Path, sort_existing=True, folders_dict: dict = {}, parent=None):
        super().__init__(parent)
        self.FOLDERS = folders_dict
        self.EXTENSIONS = [item for ext_list in list(self.FOLDERS.values()) for item in ext_list]
        self.IGNORED_NAMES = ['desktop.ini']

        self.path = pathlib.Path(path)
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.addPath(self.path.as_posix())
        self.previous = []
        Logger.info(self)

        if not sort_existing:
            self.previous = [f for f in self.path.iterdir() if f.is_file()]

        self.check_files()
        self.watcher.directoryChanged.connect(self.check_files)

    def check_files(self):
        current = self.get_current_files()
        new_files = [f for f in current if f not in self.previous]
        for each in new_files:
            self.handle_new_file(each)
        self.previous = self.get_current_files()

    def get_current_files(self) -> list:
        return [f for f in self.path.iterdir() if f.is_file() and f.name not in self.IGNORED_NAMES]

    def handle_new_file(self, file_path: pathlib.Path):
        Logger.info("New file: {0}".format(file_path.as_posix()))
        if file_path.suffix not in self.EXTENSIONS:
            Logger.info(f"{file_path.suffix} files are not managed, skipping...")
            return

        for folder_name, extensions in self.FOLDERS.items():
            if file_path.suffix in extensions:
                sub_dir = self.path / folder_name
                if not sub_dir.is_dir():
                    pathlib.Path.mkdir(sub_dir)
                shutil.move(file_path, sub_dir / file_path.name)
                Logger.info(f"Moved {file_path.name} --> {sub_dir.name}")
