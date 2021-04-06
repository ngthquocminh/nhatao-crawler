import pymongo
import re
import json


class PostAnno:
    def __init__(self):
        self.content = ""
        self.annotation = list()
        self.extras = None
        self.meta_data = dict()

    def addLabel(self, label_anno):
        if isinstance(label_anno, LabelAnno):
            self.annotation.append(label_anno)


class LabelAnno:
    def __init__(self, label, point):
        self.lable = label
        self.point = point


class PointAnno:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.text = ""


_re = lambda r, v, l: re.compile(r).match(str(v)) and len(str(v)) >= l


def check_validate(key, value):
    if value is None or ("<eof>" in str(value)) or len(str(value)) < 1:
        return False

    if key == "price":
        return _re(r'[0-9]+', value, 3)

    if key == "front":
        return _re(r'[0-9]+', value, 2)

    if key == "surface":
        return _re(r'[0-9]+', value, 2)

    if key == "room":
        return _re(r'[0-9]+', value, 1)

    if key == "floor":
        return _re(r'[0-9]+', value, 1)

    if key == "title":
        return len(str(value)) >= 20

    if key == "date":
        return len(str(value)) >= 5

    if key == "phone":
        return _re(r"0|\+84[0-9]+", value.replace(" ", ""), 9)

    if key == "email":
        return _re(r"[a-zA-Z0-9.]+@[a-zA-Z0-9.]+.[a-z]+", value.replace(" ", ""), 9)

    if key == "address":
        return len(str(value)) >= 10

    if key == "category":
        return len(str(value)) >= 3

    if key == "description":
        return len(str(value)) >= 50

    if key == "user":
        return len(str(value)) >= 2

    return False


def changekey(key):
    if key == "surface":
        return "area"
    if key == "user":
        return "saller"
    if key == "room":
        return "rooms"
    if key == "floor":
        return "floors"
    if key == "category":
        return "type"

    return key


def new_attr():
    ""


def main():
    myclient = pymongo.MongoClient(
        "mongodb://synapselynk:SaHj2L86s2pC0YvvAdV26u25M74RDhaWhUglTyRsuKa0xrcFdfh9y1RZkTZQX55F12bpd6Dc3WqlBWWcvCI32Q"
        "==@synapselynk.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS"
        "=120000&appName=@synapselynk@")
    mydb = myclient["bds_database"]
    mycol = mydb["parse_data_02"]

    query = None
    mydoc = mycol.find(query)
    index = 0
    for post in mydoc:
        # print(post)
        print("\n", "-" * 100, "\n", post["url"])

        post_anno = PointAnno()

        detail = post["detail"]
        # print(detail)
        i = 0
        for key in detail:
            value = detail[key]
            if check_validate(key, value):
                i += 1
                key = changekey(key)
                print(i, ". ", key, ": ", value)
                label_str = key
                point_anno = PointAnno()

                label_anno = LabelAnno(label_str, point_anno)
                post_anno.addLabel(label_anno)

        index += 1
        if index > 100:
            break


if __name__ == "__main__":
    main()