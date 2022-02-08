import json

class Obj2Json:

    KEY_VAL = '"{key}": "{val}"'
    KEY_VAL2 = '"{key}": {val}'

    def __init__(self):
        self._jsonstr = ""

    def add(self, key: str, val: str):
        payload = Obj2Json.KEY_VAL.format(key=key, val=val)
        if self._jsonstr != "":
            self._jsonstr += ",\n"
        self._jsonstr += "\t" + payload

    def addi(self, key: str, val):
        payload = Obj2Json.KEY_VAL2.format(key=key, val=val)
        if self._jsonstr != "":
            self._jsonstr += ",\n\t"
        self._jsonstr += payload

    def addl(self, key, obj_str: list):
        val = ""
        i = 0
        for obj in obj_str:
            if i != 0:
                val += ",\n"
            val += "\t\t" + str(obj)
            i += 1
        val = "[\n" + val + "\n\t]"
        payload = Obj2Json.KEY_VAL2.format(key=key, val=val)
        if self._jsonstr != "":
            self._jsonstr += ",\n\t"
        self._jsonstr += payload

    def obj(self):
        val = "{\n" + self._jsonstr + "\n}"
        # return val
        json_formatted_str = ""
        dataform = ""
        try:
            dataform = str(val).strip("'<>() ").replace('\'', '\"')
            parsed = json.loads(dataform)
            json_formatted_str = json.dumps(parsed, indent=2)
        except ValueError as e:
            print("dataform:" + dataform)
            print("json_formatted_str:" + json_formatted_str)
            raise e

        return json_formatted_str


if __name__ == '__main__':
    obj = Obj2Json()
    obj.add("name", "John")
    obj.addi("age", 30)
    obj.add("married", True)
    obj.add("divorced", False)
    list_cars = []
    list_cars.append('{"model": "BMW 230", "mpg": 27.5}')
    list_cars.append('{"model": "Ford Edge", "mpg": 24.1}')
    #list_tp = []
    #list_tp.append({"1111", "22222"})
    #list_tp.append({"aaaaa", "bbb"})
    obj.addl("cars", list_cars)
    #obj.addl("tp", list_tp)
    print(obj.obj())