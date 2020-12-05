import configparser
import pathlib
from file_sorter import Logger


class Config:
    def __init__(self, file_path):
        self.path = file_path
        self.parser = configparser.ConfigParser()
        try:
            self.parser.read(self.path)
        except Exception as e:
            Logger.error("Config load error", "Failed to load config file!")
            raise e

        self.parse_dir_value()

    def get_folders(self):
        result = {}
        for option in self.parser.options("Folders"):
            result[option] = self.parser.get("Folders", option).split(",")
        return result

    def parse_dir_value(self):
        dir_path = self.parser.get("General", "dir")
        if dir_path == "Downloads":
            dir_path = pathlib.Path.home() / "Downloads"
            self.parser.set("General", "dir", dir_path.as_posix())
