import csv
import os
import operator


class CsvDicTuple:
    """
    todo
    """

    def __init__(self, dic_file, delimiter=",", quotechar='"'):
        """
        CsvDicTuple constructor.
        :param dic_file: csv tuple dic file.
        :param delimiter: CSV delimiter.
        :param quotechar: CSV quote character.
        """
        try:
            self._csv_file = os.path.abspath(dic_file)
        except:
            self._csv_file = dic_file
        self._delimiter = delimiter
        self._quotechar = quotechar

    def has_tuple(self, key: str, value: str):
        """
        Tells if the tuple exists on the csv dic.
        :param key: tuple key.
        :param value: tuple value.
        :return: True if it exists, False otherwise.
        """
        ret_val = False
        try:
            with open(self._csv_file) as file:
                csvreader = csv.reader(file, delimiter=self._delimiter, quotechar=self._quotechar)
                for row in csvreader:
                    if row[0] == key:
                        if row[1] == value:
                            ret_val = True
                            break
        finally:
            return ret_val

    def add_tuple(self, key: str, value: str):
        """
        Add a new tuple to the csv file.
        :param key: tuple key.
        :param value: tuple value.
        :return: True if it was added, False if some error occurred.
        """
        try:
            if not self.has_tuple(key, value):
                with open(self._csv_file, "a") as f:
                    line = self._csv_build_line(key, value)
                    f.write(line)
            self._sort_csv_file()
            return True
        except:
            return False

    def tuple_position(self, key: str, value: str):
        """
        Tells the position of a (key, value) tuple in the csv file.
        If the tuple does not exits, returns -1, and if some error happened processing the csv file,
        returns -2.
        :param key: tuple key.
        :param value: tuple value.
        :return: the tuple position.
        """
        position = -1
        try:
            has_tuple = self.has_tuple(key, value)
            if not has_tuple:
                return -1
            with open(self._csv_file) as file:
                csvreader = csv.reader(file, delimiter=self._delimiter)
                for row in csvreader:
                    if row[0] == key:
                        position += 1
                        if row[1] == value:
                            break
            return position
        except:
            return -2

    def move_up(selfkey: str, value: str):
        print("todo")
        # todo

    def move_down(selfkey: str, value: str):
        print("todo")
        # todo

    def _sort_csv_file(self):
        """
        Sort the CSV file.
        :return: True if the file was sorted, false if some exception occurred.
        """
        try:
            # load csv file
            data = csv.reader(open(self._csv_file), delimiter=self._delimiter, quotechar=self._quotechar)
            # sort data on the first col
            data = sorted(data, key=operator.itemgetter(0))
            # create file content
            file_content = ""
            for line in data:
                file_content += self._csv_build_line(line[0], line[1])
            # write
            with open(self._csv_file, 'w') as f:
                f.write(file_content)
            return True
        except:
            return False

    def _csv_build_line(self, key, value):
        """
        Creates a string of a new csv line, to be added to a csv file.
        :param key: tuple key.
        :param value: tuple value.
        :return: a new line to be added to the csv file.
        """
        value_str = ("" if value.startswith(self._quotechar) else self._quotechar) + \
                    value + \
                    ("" if value.endswith(self._quotechar) else self._quotechar)
        line = key + self._delimiter + value_str + "\n"
        return line


def _print_position(csv_dic_tuple: CsvDicTuple, key: str, value: str, expected_position: int):
    """
    Print test.
    :param csv_dic_tuple:  class object.
    :param key: the key.
    :param value: the value.
    :param expected_position: expected value.
    :return: void
    """
    actual_position = csv_dic_tuple.tuple_position(key, value)
    print("(" + key + ", " + value + ") position: expected/actual = " + str(expected_position) + "/" + str(
        actual_position))


if __name__ == '__main__':
    dic = CsvDicTuple("../Sandbox/DicTuple01.csv")
    dic.add_tuple("key1", "AA")
    dic.add_tuple("key1", "A")
    dic.add_tuple("key1", "AA")
    dic.add_tuple("key2", "AAA")
    dic.add_tuple("key3", "AAAA")
    dic.add_tuple("key3", "AAAA")
    dic.add_tuple("key3", "AAAAA")
    dic.add_tuple("key3", "BB")
    dic.add_tuple("key3", "CC")
    dic.add_tuple("key3", "CC2")
    dic.add_tuple("key6", "EE")
    dic.add_tuple("key5", "DD")
    _print_position(dic, "key1", "A", 1)
    _print_position(dic, "key1", "AA", 0)
    _print_position(dic, "key6", "EE", 0)
    _print_position(dic, "key3", "BB", 2)
    _print_position(dic, "key3", "BB", 2)
    _print_position(dic, "key3", "xsddd", -1)
