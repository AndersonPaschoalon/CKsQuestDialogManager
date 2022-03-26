import os
import subprocess

###############################################################################
# Constants
###############################################################################
class Exts:
    EXT_JSON = "json"
    EXT_XML = "xml"
    EXT_CSV = "csv"
    EXT_TXT = "txt"
    EXT_LOG = "log"
    EXT_EXE = "exe"
    EXT_MP3 = "mp3"
    EXT_WAV = "wav"
    EXT_XWM = "xwm"
    EXT_FUZ = "fuz"


###############################################################################
# Methods
###############################################################################

class FileUtils:
    """
    Helper methods for handling files and file information.
    """
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

    @staticmethod
    def change_ext(filename, new_ext):
        """
        Change the extension of a file for a new one, or add in case the files does not have extension.
        :param filename: the filename (with or without its path).
        :param new_ext: The new extension, without the dot.
        :return:
        """
        try:
            return FileUtils.remove_ext(filename) + "." + new_ext
        except:
            return filename + new_ext

    @staticmethod
    def remove_ext(filename):
        """
        Removes the extension from the filename (with or without  the path).
        :param filename:
        :return:
        """
        try:
            return os.path.splitext(filename)[0]
        except:
            return filename


if __name__ == "__main__":
    TEST_PATH = "C:\\Users\\Usuario\\Desktop\\TEST.txt"
    FileUtils.open_file_explorer(TEST_PATH)
