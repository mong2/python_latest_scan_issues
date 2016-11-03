import json
import os


class FilesController():
    def check_filepath(self, file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

    def as_json(self, path, content):
        self.check_filepath(path)
        with open(path, "w") as f:
            json.dump(content, f)
