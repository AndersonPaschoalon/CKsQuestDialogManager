import csv
import os

class CsvDic:
    """
    This class handles a simple CSV file with two columns: a key column and a value column.
    You may check if a key exist, get its value or add a new one.
    """

    def __init__(self, dic_file, delimiter=";"):
        try:
            self._csv_file = os.path.abspath(dic_file)
        except:
            self._csv_file = dic_file
        self._last_get = ""
        self._delimiter = delimiter

    def has_key_(self, key: str):
        """Tells if the given key exist in the CSV file."""
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

    def get(self, key: str, default_value=""):
        """
        Returns the value of a given key, stored in the CSV file.
        If the comment key not exist, returns the default_value value instead."""
        try:
            file = open(self._csv_file)
            csvreader = csv.reader(file, delimiter=self._delimiter)
            for row in csvreader:
                if row[0] == key:
                    return str(row[1])
            return default_value
        except:
            return default_value

    def get_last(self, default_comment=""):
        """Get the last value read by the method has_key_()"""
        if self._last_get == "":
            return default_comment
        else:
            return self._last_get

    def add(self, key: str, value=""):
        """
        Add a new pair of key/value if it already does not exist in the CSV dictionary.
        If it exit, it does nothing.
        """
        if not self.has_key_(key) and key != "" and key is not None:
            try:
                value_str = ("" if value.startswith('"') else '"') + value + ("" if value.endswith('"') else '"')
                with open(self._csv_file, "a") as f:
                    line = key + self._delimiter + value_str + "\n"
                    f.write(line)
                return True
            except:
                return False
        else:
            return True


if __name__ == '__main__':

    comments = CsvDic("../Sandbox/DicT01.csv")
    print("has comment? " + str(comments.has_key_("DSilHand_M10SilverHunt")))
    print("comment:" + str(comments.get_last("")))
    print("comment:" + str(comments.get("DSilHand_M10SilverHunt")))
    print("-----------------")
    print("has comment? " + str(comments.has_key_("DSilHand_M10SilverHunt2222")))
    print("comment:" + str(comments.get_last("def1")))
    print("comment:" + str(comments.get("DSilHand_M10SilverHun22t", "def1")))
    print("comment:" + str(comments.get("DSilHand_M10DH_Topic02", "def1")))
    print("-----------------")
    new_dic = CsvDic("../Sandbox/NewDic.csv")
    print("has key ola ?" + str(new_dic.has_key_("ola")))
    new_dic.add("boitata", "amarelo e rosa")
    new_dic.add("curupira", "preto e branco")
    print("has key boitata ?" + str(new_dic.has_key_("boitata")))
    comments = CsvDic("../Sandbox/DicT01.csv")
    print("has comment? " + str(comments.has_key_("DSilHand_M10SilverHunt")))
    print("comment:" + str(comments.get_last("")))
    print("comment:" + str(comments.get("DSilHand_M10SilverHunt")))
    print("-----------------")
    print("has comment? " + str(comments.has_key_("DSilHand_M10SilverHunt2222")))
    print("comment:" + str(comments.get_last("def1")))
    print("comment:" + str(comments.get("DSilHand_M10SilverHun22t", "def1")))
    print("comment:" + str(comments.get("DSilHand_M10DH_Topic02", "def1")))
    """
    print("-----------------")
    new_dic = CsvDic2("../Sandbox/NewDic_2.csv", ",")
    print("has key ola ?" + str(new_dic.has_key_("ola")))
    new_dic.add("boitata", "amarelo e rosa")
    new_dic.add("curupira", "preto e branco")
    new_dic.add("curupira", "preto e branco")
    new_dic.add("unhudu", "AAAAAAAAAAAAAAA")
    new_dic.add("saci", "BBBBBBBBBB,,,,,,,,,,,,,,,,,,,,,,")
    print("has key boitata ?" + str(new_dic.has_key_("boitata")))
    print("new_dic.get():" + new_dic.get("boitata", "bb"))
    print("new_dic.get():" + new_dic.get("curupira", "cc"))
    print("new_dic.get():" + new_dic.get("saci", "cc"))
    print("new_dic.get():" + new_dic.get("unhudu", "cc"))
    """

