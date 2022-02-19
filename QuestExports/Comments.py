import csv

class Comments:

    def __init__(self, comment_files, delimiter=";"):
        self._csv_file = comment_files
        self._last_get = ""
        self._delimiter = delimiter

    def has_comment(self, key: str):
        try:
            file = open(self._csv_file)
            csvreader = csv.reader(file, delimiter=self._delimiter)
            for row in csvreader:
                if row[0] == key:
                    self._last_get = str(row[1])
                    return True
            self._last_get = ""
            return False
        except:
            self._last_get = ""
            return False

    def get(self, key: str, default_comment=""):
        try:
            file = open(self._csv_file)
            csvreader = csv.reader(file, delimiter=self._delimiter)
            for row in csvreader:
                if row[0] == key:
                    return str(row[1])
            return default_comment
        except:
            return default_comment

    def get_last(self, default_comment=""):
        if self._last_get == "":
            return default_comment
        else:
            return self._last_get

if __name__ == '__main__':
    comments = Comments("../Comments.csv")
    print("has comment? " + str(comments.has_comment("DSilHand_M10SilverHunt")))
    print("comment:" + str(comments.get_last("")))
    print("comment:" + str(comments.get("DSilHand_M10SilverHunt")))
    print("-----------------")
    print("has comment? " + str(comments.has_comment("DSilHand_M10SilverHunt2222")))
    print("comment:" + str(comments.get_last("def1")))
    print("comment:" + str(comments.get("DSilHand_M10SilverHun22t", "def1")))
    print("comment:" + str(comments.get("DSilHand_M10DH_Topic02", "def1")))

