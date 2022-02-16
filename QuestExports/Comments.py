import csv

class Comments:

    def __init__(self, comment_files):
        self._csv_file = comment_files
        self._last_get = ""

    def has_comment(self, key: str):
        try:
            file = open(self._csv_file)
            csvreader = csv.reader(file)
            for row in csvreader:
                if row[0] == key:
                    self._last_get = str(row[1])
                    return True
        except:
            return False

    def get(self, key: str, default_comment=""):
        try:
            file = open(self._csv_file)
            csvreader = csv.reader(file)
            for row in csvreader:
                if row[0] == key:
                    return str(row[1])
        except:
            return default_comment

    def get_last(self, default_comment=""):
        if self._last_get == "":
            return default_comment
        else:
            return  self._last_get

