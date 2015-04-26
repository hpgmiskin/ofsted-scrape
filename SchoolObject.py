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

    def filename(self,folderPath="schools"):

        filename = "{}_{}.json".format(self.date[0],self.name.lower().replace(" ","_"))
        filename = os.path.join(folderPath,filename)

        return filename

    def save(self):

        with open(self.filename(),"w") as openFile:
            openFile.write(json.dumps(self.__dict__))

    def load(self,filename=None):

        if not filename: self.filename()

        with open(filename,"r") as openFile:
            content = openFile.read()
            attrObject = json.loads(content)

        self.setAttr(attrObject)

    def __str__(self):

        try:
            date = time.strftime("%d/%m/%y",self.date)
        except TypeError:
            date = self.date

        string = "{} ({}) - Ofsted Grade {} on {}".format(self.name,
            self.head,
            self.grade,
            date
            )

        # more = "\n" + str(self.__dict__)

        return string
