import os
import time
import json

class SchoolObject():

    def __init__(self,schoolID):
        self.id = schoolID

        self.name = ""
        self.head = ""

    def setName(self,name):
        self.name = name

    def setAttr(self,attrObject):

        for key, value in attrObject.items():
            self.__setattr__(key,value)

    def setOfsted(self,date,grade,report):
        """
        """

        self.date = date
        self.grade = grade
        self.report = report

    def save(self):

        filename = "{}.json".format(self.name)
        filename = os.path.join("schools",filename)

        with open(filename,"w") as openFile:
            openFile.write(json.dumps(self.__dict__))

    def __str__(self):

        date = time.strftime("%d/%m/%y",self.date)

        string = "{} ({}) - Ofsted Grade {} on {}".format(self.name,
            self.head,
            self.grade,
            date
            )

        # more = "\n" + str(self.__dict__)

        return string
