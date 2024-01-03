import orjson
import numpy as np
from datetime import datetime

"""
A custom class for making data objects that are easily exported/imported as json. Uses orjson for fast export and 
import of numpy arrays. 

The export and import methods can handle DataObj objects inside other DataObj objects. 

Why not just use the pickle library? 
--> Answer: Json is a more universal format than python pickle. The exports from this library could be parsed by Matlab, 
Javascript, etc. The use of orjson here should also make this much faster than python pickle for large datasets. 
"""


class DataObj:
    def __init__(self, name=None, dic=None):
        if name is not None:
            self.load_file(name)
        if dic is not None:
            self.load_dic(dic)

    def export(
        self, name, include_time=False, print_info=False, include_time_inside=False
    ):
        dic = self.export_dic()
        if include_time:
            now = datetime.now()
            dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
            name = name + dt_string
        if include_time_inside:
            now = datetime.now()
            dt_string = now.strftime("%d.%m.%Y_%H.%M.%S")
            dic["date_time"] = dt_string
        strb = orjson.dumps(dic, option=orjson.OPT_SERIALIZE_NUMPY)

        if name[-5:] != ".json":
            json_name = name + ".json"
        else:
            json_name = name
        with open(json_name, "wb") as file:
            file.write(strb)
        if print_info:
            print("Saving data as: ", name)
        return name  # if I want to save other file types with same name

    @classmethod
    def from_file(cls, name):
        obj = cls()
        obj.load_file(name)
        return obj


    def load_file(self, name):
        with open(name, "rb") as file:
            strb = file.read()
        self.load_dic(orjson.loads(strb))
        print(self.__dict__.keys())


    # recursive
    def check_list(self, item):
        if type(item) is list:
            return self.check_list(item[0])
        if (type(item) is float) or (type(item) is int):
            return True
        else:
            return False

    def load_dic(self, dic):

        dic_2 = dic.copy()
        for key in dic.keys():
            # handle numpy arrays
            # does not working with multi-dimensional numpy arrays yet. 
            # need recursive check function so that lists of lists of numpy becomes np.array(np.array(np.array))
            if self.check_list(dic[key]):
                dic_2[key] = np.array(dic[key])

            # handle lists of objects of type JsonTool
            if (type(dic[key]) is list) and (key[-3:] == "_do"):
                ls = dic_2[key]
                del dic_2[key]
                for i in range(len(ls)):
                    ls[i] = DataObj(dic=ls[i])
                dic_2[key[:-3]] = ls
                continue

            # handle keys with value of type JsonTool
            if key[-3:] == "_do":
                sub_dic = dic[key]
                del dic_2[key]
                dic_2[key[:-3]] = DataObj(dic=sub_dic)
        self.__dict__.update(dic_2)

    def export_dic(self):
        dic = self.__dict__
        dic_2 = dic.copy()
        for key in dic.keys():

            # handle non-continuous numpy arrays
            if isinstance(dic[key], np.ndarray):
                is_continuous = dic[key].flags.contiguous
                # print(is_continuous)
                if not is_continuous:
                    dic_2[key] = dic[key].copy(order="C")


            if (type(dic[key]) is type(self)) or issubclass(type(dic[key]), type(self)):
                # dic[key] = dic[key].export_dic()
                json_tool_dic = dic[key].export_dic()
                del dic_2[key]
                new_key = str(key) + "_do"
                dic_2[new_key] = json_tool_dic

            if (type(dic[key]) is list) and (
                (type(dic[key][0]) is type(self))
                or issubclass(type(dic[key][0]), type(self))
            ):
                ls = []
                for i, item in enumerate(dic[key]):
                    ls.append(dic[key][i].export_dic())

                del dic_2[key]
                new_key = str(key) + "_do"
                dic_2[new_key] = ls
        return dic_2


# would be cool if this could overload the list functionality if I only wanted to use this object as a list.
# right now it does not encode lists of numpy arrays correctly.


if __name__ == "__main__":
    # create a DataObj with various things inside, including a list of DataObj, a single DataObj,
    # and an extra numpy array.
    parent = DataObj()
    parent.items = []
    # for i in range(20):
    #     struct = DataObj()
    #     struct.item = "this is an item"
    #     struct.dB = f"{i} dB"
    #     struct.ls = [
    #         np.array([3, 34, 2, 43]),
    #         np.array([3, 34, 2, 43]),
    #         np.array([3, 34, 2, 43]),
    #     ]
    #     struct.arr = np.array([23, 2, 34, 2, 43, 3, 4.433])
    #     parent.items.append(struct)
    # parent.extraObj = DataObj()
    # parent.extraObj.item = "this is an item inside an nested DataObj"
    # parent.numpy = np.array([3, 54, 3, 45, 2, 5, 7, 3])
    # # export
    # parent.export("try_this.json")

    # # import
    # parent_2 = DataObj("try_this.json")
    # print(type(parent_2))
    # for item in parent_2.__dict__.keys():
    #     print(item)
    # print(parent_2.extraObj.item)
    # print()
    # print(parent_2.numpy)
    # print(type(parent_2.numpy))
    # print()
    # print([parent_2.items[i].dB for i in range(10)])
    # print([parent_2.items[i].arr for i in range(10)])
    parent.items.append([np.array([4,5,23,45,3,4]),np.array([4,5,23,45,3,4]),np.array([55,5,23,45,3,4])])
    parent.export("try_this.json")
    print()
    parent_2 = DataObj("try_this.json")
    print(parent_2.items)
    print(type(parent_2.items))
    # print(parent.check_numpy(parent.items))



