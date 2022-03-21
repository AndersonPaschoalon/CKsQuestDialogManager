import os
import subprocess

class FileUtils:

    @staticmethod
    def is_non_zero_file(fpath: str):
        """
        Tells if a given file is empty or not
        :return:the size of the file.
        """
        return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

    @staticmethod
    def open_file_on_file_explorer(file_path: str):
        """
        Open a directory with a given file already selected.
        :param path: file.
        :return: True on success, false otherwise.
        """
        try:
            subprocess.Popen(r'explorer /select,"{0}"'.format(file_path))
            return True
        except:
            return False

if __name__ == "__main__":
    TEST_PATH = "C:\\Users\\Usuario\\Desktop\\TEST.txt"
    FileUtils.open_file_explorer(TEST_PATH)
