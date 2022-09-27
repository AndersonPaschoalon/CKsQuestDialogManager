import os


class DirUtils:

    @staticmethod
    def mkdir(dir_name: str):
        if (not os.path.exists(dir_name)) and (dir_name != ""):
            os.makedirs(dir_name)
