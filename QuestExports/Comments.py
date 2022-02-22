import csv

class Comments:
    """This class handles the comments file. This file is responsible for storing commentaries for elements of the
    exported dialogues."""

    COMMENTS_FILE_NAME = "Comments.csv"
    COMMENTS_CSV_SEPARATOR = ";"
    def __init__(self, comment_files, delimiter=";"):
        self._csv_file = comment_files
        self._last_get = ""
        self._delimiter = delimiter

    def has_comment(self, key: str):
        """Tells if the given key has a  comment in the Comment file."""
        ret_val = False
        try:
            with open(self._csv_file) as file:
                csvreader = csv.reader(file, delimiter=self._delimiter)
                for row in csvreader:
                    if row[0] == key:
                        self._last_get = str(row[1])
                        ret_val = True
                        break
                if not ret_val:
                    self._last_get = ""
        except:
            self._last_get = ""
        finally:
            return ret_val
        #try:
        #    file = open(self._csv_file)
        #    csvreader = csv.reader(file, delimiter=self._delimiter)
        #    for row in csvreader:
        #        if row[0] == key:
        #            self._last_get = str(row[1])
        #            return True
        #    self._last_get = ""
        #    return False
        #except:
        #    self._last_get = ""
        #    return False

    def get(self, key: str, default_comment=""):
        """Returns a given comment for the key, stored in the comments file. If the comment does not exist, returns
        the default_comment value instead."""
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
        """Get the last comment readed by the method has_comment()"""
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

