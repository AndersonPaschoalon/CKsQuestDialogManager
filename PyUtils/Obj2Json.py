import json


class Obj2Json:
    """This class is a helper for convertion of Python objects into a JSON string."""

    KEY_VAL_STR = '"{key}": "{val}"'
    KEY_VAL_OBJ = '"{key}": {val}'

    def __init__(self):
        """Default constructor, initializes the object with an empty string for the Json object"""
        self._jsonstr = ""

    def add(self, key: str, val):
        """Adds a key value to the json object"""
        if type(val) == tuple or type(val) == list or type(val) == list or type(val) == dict:
            return self.addl(key, val)
        vald = json.dumps(val)
        val = str(val)
        payload = Obj2Json.KEY_VAL_OBJ.format(key=key, val=vald)
        if self._jsonstr != "":
            self._jsonstr += ",\n"
        self._jsonstr += "\t" + payload

    def addl(self, key, obj_str: list):
        """This method will add a list to the json. Use add() instead."""
        val = ""
        i = 0
        str_vec = ""
        for oo in obj_str:
            # print(" * strapp:" + strapp)
            if i != 0:
                str_vec += ",\n"
            str_vec += "\t\t"
            str_vec += self.safe_json_dump_obj(oo)
            i += 1
        val = "[\n" + str_vec + "\n\t]"
        payload = Obj2Json.KEY_VAL_OBJ.format(key=key, val=val)
        if self._jsonstr != "":
            self._jsonstr += ",\n\t"
        self._jsonstr += payload

    def json(self):
        """This Method will return the stored values into a fromatted json string."""
        val = "{\n" + self._jsonstr + "\n}"
        # return val
        json_formatted_str = ""
        data_form = ""
        try:
            # data_form = val
            # data_form = str(val).strip("'<>() ").replace('\'', '\"')
            data_form = str(val)
            parsed = json.loads(data_form)
            json_formatted_str = json.dumps(parsed, indent=2)
        except ValueError as e:
            print("data_form:" + data_form)
            print("json_formatted_str:" + json_formatted_str)
            raise e
        return json_formatted_str

    @staticmethod
    def safe_json_dump_obj(obj):
        """
        Safey tries to convert the object into a valid json object. If it is None, returns an empty string.
        Then, it will try to convert from the more flexible format to the lesser one.
        """
        if obj is None:
            return ""
        json_val = ""
        # if it is a dictionary jsonify it
        try:
            obj = json.loads(obj)
        except:
            obj = obj
        try:
            json_val = json.dumps(obj)
        except:
            try:
                json_val = json.dumps(str(obj))
            except:
                json_val = str(obj)
        return json_val


if __name__ == '__main__':
    obj = Obj2Json()
    obj.add("name", "John")
    obj.add("age", 30)
    # obj.addi("age", 30)
    # obj.add("age-str", 30)
    obj.add("married", True)
    obj.add("divorced", False)

    list_cars = []
    list_cars.append('{"model": "BMW \\"230", "mpg": 27.5}')
    list_cars.append('{"model": "Ford Edge", "mpg": 24.1}')

    list_tp = []
    list_tp.append({"1111", "22222"})
    list_tp.append({"aaaaa", "bbb"})
    list_tp.append({"aaaaa\"", "bbb"})

    list_bool = []
    list_bool.append(True)
    list_bool.append(True)
    list_bool.append(True)
    list_bool.append(False)

    list_int = []
    list_int.append(1)
    list_int.append(2)
    list_int.append(3)
    list_int.append(4)

    obj.add("cars", list_cars)
    obj.add("tp", list_tp)
    obj.add("bools", list_bool)
    obj.add("intss", list_int)

    print(obj.json())
